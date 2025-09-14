import os
import pathlib
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# from langchain.document_loaders import SeleniumURLLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import DeepLake
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_openai import OpenAIEmbeddings
from langchain_deeplake import DeeplakeVectorStore as DeepLake

"""
DeepLake ingestion script for Atlan help-desk demo.

• Recursively collects up to `MAX_PAGES` HTML pages from the root docs and developer sites.
• Uses SeleniumURLLoader to render & extract page text (handles JS-rendered docs).
• Splits text into 1k-character chunks.
• Generates OpenAI embeddings (text-embedding-ada-002).
• Stores embeddings & metadata in two separate DeepLake datasets:
    hub://<ACTIVELOOP_ORG>/atlan_docs_support
    hub://<ACTIVELOOP_ORG>/developer_hub_support

Environment variables required:
  OPENAI_API_KEY   – your OpenAI key
  ACTIVELOOP_ORG   – activeloop username/org id (defaults to env USER if unset)
  DEEPLAKE_TOKEN   – (optional) if your DeepLake datasets are private

Run once:
    python deeplake_ingest.py
"""

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY env var missing.")

ACTIVELOOP_ORG = os.getenv("ACTIVELOOP_ORG") or os.getenv("USER")
if not ACTIVELOOP_ORG:
    raise RuntimeError("ACTIVELOOP_ORG env var missing and USER not set.")

DEEPLAKE_TOKEN = os.getenv("DEEPLAKE_TOKEN")
if DEEPLAKE_TOKEN:
    os.environ["ACTIVELOOP_TOKEN"] = DEEPLAKE_TOKEN 

# ---------------------------------------------------------------------------
# Crawl helpers – lightweight HTML link extraction (no JS)
# ---------------------------------------------------------------------------

MAX_PAGES = 40  # per site – tune for demo speed
HEADERS = {"User-Agent": "Atlan-Helpdesk-Ingest/0.1"}

def collect_links(seed: str, max_pages: int = MAX_PAGES) -> list[str]:
    """Breadth-first crawl limited to same host; returns list of absolute URLs."""
    seen: set[str] = set()
    queue: list[str] = [seed]
    collected: list[str] = []

    while queue and len(collected) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except Exception:
            continue

        collected.append(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue
            abs_url = urljoin(url, href)
            # same domain only
            if urlparse(abs_url).netloc != urlparse(seed).netloc:
                continue
            # drop fragments, media, mailto, etc.
            if any(abs_url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".svg", ".pdf", ".zip"]):
                continue
            abs_url = abs_url.split("#")[0]
            if abs_url not in seen and abs_url not in queue and len(collected) + len(queue) < max_pages:
                queue.append(abs_url)
    return collected

# ---------------------------------------------------------------------------
# Ingestion routine using LangChain + DeepLake
# ---------------------------------------------------------------------------

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def ingest_site(root_url: str, dataset_suffix: str):
    urls = collect_links(root_url)
    print(f"Collected {len(urls)} URLs for {root_url}")

    # Selenium loader sometimes hits rate-limits; load in small batches
    docs_raw = []
    for i in range(0, len(urls), 5):
        batch = urls[i:i+5]
        print(f"  Loading batch {i//5+1} / {(len(urls)+4)//5}")
        loader = SeleniumURLLoader(urls=batch)
        docs_raw.extend(loader.load())
        time.sleep(1)  # polite delay

    docs = text_splitter.split_documents(docs_raw)
    print(f"  {len(docs)} total chunks → embedding")

    path = f"hub://{ACTIVELOOP_ORG}/{dataset_suffix}"
    db = DeepLake(dataset_path=path, embedding_function=embeddings)
    db.add_documents(docs)
    print("Finished & persisted to", path)


def main():
    ingest_site("https://docs.atlan.com/", "atlan_docs_support")
    ingest_site("https://developer.atlan.com/", "developer_hub_support")

if __name__ == "__main__":
    main()
