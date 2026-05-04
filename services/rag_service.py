import logging
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
RAG_DIR = PROJECT_ROOT / "rag"
CHROMA_PATH = RAG_DIR / "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"

_client = None
_collection = None

def _get_collection():
    """Initializes the ChromaDB client and collection once."""
    global _client, _collection
    if _collection is None:
        try:
            _client = chromadb.PersistentClient(path=str(CHROMA_PATH))
            embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=MODEL_NAME
            )
            _collection = _client.get_or_create_collection(
                name="edu_content", embedding_function=embed_fn
            )
        except Exception as e:
            logger.error(f"Could not initialize RAG service: {e}")
            _collection = False
    return _collection if _collection is not False else None

def search(query: str, top_k: int = 3) -> list[str]:
    """Retrieves the most relevant text chunks for a given query."""
    collection = _get_collection()
    if not collection:
        return []
    try:
        results = collection.query(query_texts=[query], n_results=top_k)
        if results and 'documents' in results and results['documents']:
            return results['documents'][0]
    except Exception as e:
        logger.warning(f"Error during RAG search: {e}")
    return []

def get_context_for_prompt(query: str, top_k: int = 2) -> str:
    """Searches and formats the results for injection into the final prompt."""
    docs = search(query, top_k)
    if not docs:
        return ""

    context = "\n\n---\n\n".join(docs)
    return f"=== CONTEXTO DE CONOCIMIENTO (RAG) ===\n{context}\n=== FIN DEL CONTEXTO ===\n\n"