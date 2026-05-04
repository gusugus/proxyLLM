# scripts/index_rag.py
import os
import sys
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

# Obtener directorio raíz del proyecto (proxy/)
PROJECT_ROOT = Path(__file__).parent.parent  # scripts/ -> proxy/
RAG_DIR = PROJECT_ROOT / "rag"
CHROMA_PATH = RAG_DIR / "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"

def chunk_text(content, min_len=50):
    paragraphs = [p.strip() for p in content.split("\n\n")]
    return [p for p in paragraphs if len(p) >= min_len]

def main():
    # Crear directorios si no existen
    RAG_DIR.mkdir(exist_ok=True)
    CHROMA_PATH.mkdir(exist_ok=True)
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    collection_name = "edu_content"
    try:
        client.delete_collection(collection_name)
    except:
        pass
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )
    
    for md_file in RAG_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            doc_id = f"{md_file.name}_{i}"
            collection.add(
                ids=[doc_id],
                documents=[chunk],
                metadatas=[{"source": md_file.name}]
            )
        print(f"Indexados {len(chunks)} chunks de {md_file.name}")
    
    print(f"Total chunks indexados: {collection.count()}")

if __name__ == "__main__":
    main()