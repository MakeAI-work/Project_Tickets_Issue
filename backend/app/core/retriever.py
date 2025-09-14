import os
from functools import lru_cache
from typing import List

from langchain_deeplake import DeeplakeVectorStore
from langchain_openai import OpenAIEmbeddings

# Environment vars
ACTIVELOOP_ORG = os.getenv("ACTIVELOOP_ORG") or os.getenv("USER")
DEEPLAKE_TOKEN = os.getenv("DEEPLAKE_TOKEN")
if DEEPLAKE_TOKEN:
    os.environ["ACTIVELOOP_TOKEN"] = DEEPLAKE_TOKEN

EMBED = OpenAIEmbeddings(model="text-embedding-ada-002")

COL_PATHS = {
    "docs": f"hub://{ACTIVELOOP_ORG}/atlan_docs_support",
    "dev": f"hub://{ACTIVELOOP_ORG}/developer_hub_support",
}


@lru_cache(maxsize=2)
def _get_store(key: str) -> DeeplakeVectorStore:
    """Load Deep Lake vector store lazily and cache."""
    path = COL_PATHS[key]
    return DeeplakeVectorStore(dataset_path=path, embedding_function=EMBED, read_only=True)


def similar_docs(query: str, collection: str = "docs", k: int = 4):
    
    store = _get_store(collection)
    return store.similarity_search(query, k=k)
