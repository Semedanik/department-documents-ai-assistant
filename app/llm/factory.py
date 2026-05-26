from app.core.config import Settings
from app.llm.base import LLMProvider
from app.llm.gemini import GeminiProvider
from app.llm.openrouter import OpenRouterProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "openrouter":
        return OpenRouterProvider(settings)
    if settings.llm_provider == "gemini":
        return GeminiProvider(settings)

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
