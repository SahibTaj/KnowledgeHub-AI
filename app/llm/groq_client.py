from typing import List, Dict, Any
from groq import Groq
from app.llm.base import BaseLLMClient
from app.config import GROQ_API_KEY

class GroqLLMClient(BaseLLMClient):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = Groq(api_key=GROQ_API_KEY)

    def completion(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Any:
        return self.client.chat.completions.create(
            model = self.model_name,
            messages= messages,
            temperature=temperature,
            max_tokens= max_tokens
        )