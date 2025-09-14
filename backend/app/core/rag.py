import os
from typing import Tuple, List

from dotenv import load_dotenv
from langchain_openai import OpenAI

from .retriever import similar_docs

load_dotenv()

_llm = OpenAI(model="gpt-4o-mini", temperature=0)

_PROMPT = (
    "Use the following documentation snippets to answer the user question. "
    "Cite sources with markdown footnotes (e.g., [1], [2]). If the answer is not "
    "Provide link to sources also "
    "in the snippets, say you don't know.\n\n"
    "Snippets:\n{chunks}\n\nQuestion: {query}\nAnswer:" 
)


def answer_with_rag(query: str, topic: str) -> Tuple[str, List[str]]:
    collection = "docs" if topic in {"Product", "How-to", "Best practices", "SSO"} else "dev"
    print(collection)
    docs = similar_docs(query, collection=collection, k=3)
    if not docs:
        return "I don't have enough information at the moment.", []

    def _snippet(d):
        text = d.page_content.strip()[:800]
        url = d.metadata.get("url", "")
        return f"[{url}]\n{text}"
    chunks = "\n\n".join(_snippet(d) for d in docs)
    prompt = _PROMPT.format(chunks=chunks, query=query)
    resp = _llm(prompt)
    source_urls = [d.metadata.get("url") for d in docs if d.metadata.get("url")]
    return resp, source_urls
