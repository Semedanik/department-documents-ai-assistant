from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class ChatMessage:
    role: Role
    content: str


@dataclass(frozen=True)
class ChatResult:
    content: str
    model: str
    provider: str


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[ChatMessage]) -> ChatResult:
        """Generate an assistant response for a conversation."""
