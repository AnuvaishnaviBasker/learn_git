from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "data" / "pdfs"
SCRAPED_DIR = BASE_DIR / "data" / "scraped"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

OLLAMA_MODEL = "qwen2.5:0.5b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

COLLECTION_NAME = "farmer_schemes"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
RETRIEVAL_COUNT = 4

PDF_DIR.mkdir(parents=True, exist_ok=True)
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)