import httpx

from app.core.config import Settings
from app.llm.base import ChatMessage, ChatResult, LLMProvider


class OpenRouterProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is required when LLM_PROVIDER=openrouter")

        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._base_url = settings.openrouter_base_url.rstrip("/")
        self._temperature = settings.llm_temperature
        self._timeout = settings.llm_timeout_seconds
        self._app_url = settings.openrouter_app_url
        self._app_name = settings.openrouter_app_name

    async def chat(self, messages: list[ChatMessage]) -> ChatResult:
        payload = {
            "model": self._model,
            "messages": [{"role": message.role, "content": message.content} for message in messages],
            "temperature": self._temperature,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self._app_url,
            "X-Title": self._app_name,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        model = data.get("model", self._model)
        return ChatResult(content=content, model=model, provider="openrouter")
