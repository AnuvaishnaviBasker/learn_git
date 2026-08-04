from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse
from .rag_service import FarmerSchemeRAG


app = FastAPI(
    title="Farmer Schemes RAG API",
    description="RAG chatbot API for Indian farmer schemes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_service: FarmerSchemeRAG | None = None


@app.on_event("startup")
def startup_event() -> None:
    global rag_service

    try:
        rag_service = FarmerSchemeRAG()
        print("RAG service initialized.")
    except Exception as error:
        print(f"RAG initialization failed: {error}")
        rag_service = None


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Farmer Schemes RAG API is running."
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy" if rag_service else "not_ready"
    }


@app.get("/status")
def status() -> dict[str, str]:
    if rag_service is None:
        return {
            "status": "not_ready",
            "message": (
                "RAG service is unavailable. Build the vector database "
                "and ensure the backend dependencies are installed."
            ),
        }

    return {
        "status": "ready",
        "message": "RAG service is initialized and ready to answer questions.",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "RAG service is unavailable. Build the vector database "
                "and confirm that Ollama is running."
            ),
        )

    try:
        history = [
            message.model_dump()
            for message in request.chat_history
        ]

        result = rag_service.ask(
            question=request.question,
            chat_history=history,
        )

        return ChatResponse(**result)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not generate an answer: {error}",
        ) from error