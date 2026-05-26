from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, examples=["Explain RAG in one paragraph"])


class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str
