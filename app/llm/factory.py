from app.llm.base import BaseLLMClient
from app.llm.groq_client import GroqLLMClient
from app.llm.openai_client import OpenAILLMClient
from app.llm.ollama_client import OllamaLLMClient
from app.config import LLM_MODEL, LLM_PROVIDER

class LLMFactory:
    @staticmethod
    def get_client(provider: str = LLM_PROVIDER, model: str = LLM_MODEL) -> BaseLLMClient:
        provider_lower = provider.lower()
        if provider_lower == "groq":
            return GroqLLMClient(model_name=model)
        elif provider_lower == "openai":
            return OpenAILLMClient(model_name=model)
        elif provider_lower == "ollama":
            return OllamaLLMClient(model_name=model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")