from __future__ import annotations

from typing import Any

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from .config import COLLECTION_NAME, EMBEDDING_MODEL, VECTOR_DB_DIR


class FarmerSchemeRAG:
    def __init__(self) -> None:
        self.embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=self.embedding,
        )

        if not self.vector_store:
            raise RuntimeError(
                "Could not initialize the vector store. "
                "Make sure the vector database exists and is populated."
            )

    def ask(self, question: str, chat_history: list[dict[str, Any]]) -> dict[str, Any]:
        documents = self._retrieve(question)
        answer = self._generate_answer(question, documents)

        return {
            "answer": answer,
            "details": {
                "question": question,
                "history": chat_history,
                "retrieved_documents": [
                    {
                        "source": doc.metadata.get("source", "unknown"),
                        "file_name": doc.metadata.get("file_name", "unknown"),
                        "snippet": doc.page_content[:300].strip(),
                    }
                    for doc in documents
                ],
            },
        }

    def _retrieve(self, question: str, k: int = 4) -> list[Document]:
        try:
            return self.vector_store.similarity_search(question, k=k)
        except Exception as error:
            raise RuntimeError(
                f"Failed to retrieve documents for question: {error}"
            ) from error

    def _generate_answer(self, question: str, documents: list[Document]) -> str:
        if not documents:
            return (
                "I could not find any relevant documents for your question. "
                "Try rephrasing or checking the data ingestion pipeline."
            )

        content_blocks = []
        for index, document in enumerate(documents, start=1):
            source = document.metadata.get("source", "unknown")
            title = document.metadata.get("title") or document.metadata.get("file_name", "document")
            snippet = document.page_content.strip().replace("\n", " ")
            if len(snippet) > 800:
                snippet = snippet[:800].rsplit(" ", 1)[0] + "..."

            content_blocks.append(
                f"[{index}] Source: {title} ({source})\n{snippet}"
            )

        combined = "\n\n".join(content_blocks)
        return (
            "I found relevant information from the indexed documents. "
            "Here are the top retrieved passages:\n\n"
            f"{combined}"
        )
