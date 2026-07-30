from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMClient(ABC):
    @abstractmethod
    def completion(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> Any:
        pass