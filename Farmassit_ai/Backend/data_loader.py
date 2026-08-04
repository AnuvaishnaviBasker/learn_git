import json
from pathlib import Path
from typing import Any

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from .config import PDF_DIR, SCRAPED_DIR


def load_pdf_documents() -> list[Document]:
    documents: list[Document] = []

    for pdf_path in PDF_DIR.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(pdf_path))
            pdf_documents = loader.load()

            for document in pdf_documents:
                document.metadata.update(
                    {
                        "source": str(pdf_path),
                        "file_name": pdf_path.name,
                        "source_type": "pdf",
                    }
                )

            documents.extend(pdf_documents)
            print(f"Loaded PDF: {pdf_path.name}")

        except Exception as error:
            print(f"Could not load {pdf_path.name}: {error}")

    return documents


def load_scraped_documents() -> list[Document]:
    documents: list[Document] = []

    for json_path in SCRAPED_DIR.glob("*.json"):
        try:
            with json_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            content = data.get("content", "").strip()
            if not content:
                print(f"Skipped empty file: {json_path.name}")
                continue

            document = Document(
                page_content=content,
                metadata={
                    "source": data.get("source_url", str(json_path)),
                    "file_name": json_path.name,
                    "scheme_name": data.get("scheme_name", "Unknown"),
                    "title": data.get("title", ""),
                    "source_type": "webpage",
                },
            )

            documents.append(document)
            print(f"Loaded webpage: {json_path.name}")

        except Exception as error:
            print(f"Could not load {json_path.name}: {error}")

    return documents


def load_all_documents() -> list[Document]:
    documents = load_pdf_documents()
    documents.extend(load_scraped_documents())
    return documents
