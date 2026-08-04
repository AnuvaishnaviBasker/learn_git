import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Backend.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    VECTOR_DB_DIR,
)
from Backend.data_loader import load_all_documents


def build_vector_database() -> None:
    """Load, split, embed and store all scheme documents."""

    print("Loading documents...")
    documents = load_all_documents()

    if not documents:
        raise RuntimeError(
            "No documents were found. Add PDFs to data/pdfs "
            "or scraped JSON files to data/scraped."
        )

    print(f"Loaded {len(documents)} document pages/items.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # Rebuild the local vector database.
    if VECTOR_DB_DIR.exists():
        shutil.rmtree(VECTOR_DB_DIR)

    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DB_DIR),
    )

    print("Vector database created successfully.")
    print(f"Location: {VECTOR_DB_DIR}")


if __name__ == "__main__":
    try:
        build_vector_database()
    except Exception as error:
        print(f"Ingestion failed: {error}")
