from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from httpx import HTTPStatusError, RequestError

from app.core.config import Settings, get_settings
from app.llm.base import ChatMessage, LLMProvider
from app.llm.factory import create_llm_provider
from app.schemas.chat import ChatRequest, ChatResponse

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="RAG Evaluation Platform")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


def get_llm_provider(settings: Settings = Depends(get_settings)) -> LLMProvider:
    return create_llm_provider(settings)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm_provider: LLMProvider = Depends(get_llm_provider),
) -> ChatResponse:
    messages = [
        ChatMessage(
            role="system",
            content=(
                "You are a concise assistant for studying department center documents, "
                "regulations, instructions, service descriptions, and internal knowledge base materials. "
                "Answer clearly, distinguish facts from assumptions, and say when a document source is needed. "
                "Use plain text without markdown formatting."
            ),
        ),
        ChatMessage(role="user", content=request.message),
    ]

    try:
        result = await llm_provider.chat(messages)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM provider returned HTTP {exc.response.status_code}",
        ) from exc
    except RequestError as exc:
        raise HTTPException(status_code=502, detail="LLM provider request failed") from exc

    return ChatResponse(answer=result.content, provider=result.provider, model=result.model)
