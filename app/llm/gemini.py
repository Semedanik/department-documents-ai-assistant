import httpx

from app.core.config import Settings
from app.llm.base import ChatMessage, ChatResult, LLMProvider


class GeminiProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")

        self._api_key = settings.gemini_api_key
        self._model = settings.gemini_model
        self._base_url = settings.gemini_base_url.rstrip("/")
        self._temperature = settings.llm_temperature
        self._timeout = settings.llm_timeout_seconds

    async def chat(self, messages: list[ChatMessage]) -> ChatResult:
        system_instruction = self._build_system_instruction(messages)
        contents = self._build_contents(messages)
        payload: dict[str, object] = {
            "contents": contents,
            "generationConfig": {"temperature": self._temperature},
        }
        if system_instruction:
            payload["system_instruction"] = system_instruction

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/models/{self._model}:generateContent",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return ChatResult(content=content, model=self._model, provider="gemini")

    def _build_system_instruction(self, messages: list[ChatMessage]) -> dict[str, object] | None:
        system_messages = [message.content for message in messages if message.role == "system"]
        if not system_messages:
            return None

        return {"parts": [{"text": "\n\n".join(system_messages)}]}

    def _build_contents(self, messages: list[ChatMessage]) -> list[dict[str, object]]:
        contents: list[dict[str, object]] = []

        for message in messages:
            if message.role == "system":
                continue

            role = "model" if message.role == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": message.content}]})

        return contents
