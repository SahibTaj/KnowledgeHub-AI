from typing import List, Dict, Any
from openai import OpenAI
from app.llm.base import BaseLLMClient
from app.config import OPENAI_API_KEY

class OpenAILLMClient(BaseLLMClient):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def completion(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Any:
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )