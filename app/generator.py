import time
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.models import SearchResult, GeneratedResponse
from app.llm.base import BaseLLMClient

logger = logging.getLogger(__name__)

class Generator:
    def __init__(
        self, 
        llm_client: BaseLLMClient,
        model_name: str,
        temperature: float = 0.0, 
        max_tokens: int = 1024
    ):
        self.llm_client = llm_client
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _build_context(self, search_results: List[SearchResult]) -> str:
        extracted_texts = [result.text for result in search_results if result.text]
        return "\n\n".join(extracted_texts)

    def _build_prompt(self, question: str, context: str) -> List[Dict[str, str]]:
        system_prompt = (
            "You are a precise assistant. Answer the question using only the provided context. "
            "If the answer cannot be found in the context, state that you do not know."
        )
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def _generate(self, messages: List[Dict[str, str]]) -> Any:
        return self.llm_client.completion(
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    def generate(self, question: str, search_results: List[SearchResult]) -> GeneratedResponse:
        logger.info("Received generation request")
        start_time = time.time()
        sources = [res.id for res in search_results if res.id]

        if not question or not question.strip():
            logger.warning("Empty question received during generation block.")
            return GeneratedResponse(
                answer="Question cannot be empty.",
                sources=[],
                model_name=self.model_name,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency=0.0,
                created_at=datetime.now(timezone.utc).isoformat()
            )

        try:
            context = self._build_context(search_results)
            logger.info("Built context")

            messages = self._build_prompt(question, context)
            logger.info("Prompt created")

            logger.info("Calling LLM")
            response = self._generate(messages)

            if not response.choices or not response.choices[0].message.content:
                logger.warning("Empty response received from LLM")
                return GeneratedResponse(
                    answer="The model generated an empty response.",
                    sources=sources,
                    model_name=self.model_name,
                    prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                    completion_tokens=response.usage.completion_tokens if response.usage else 0,
                    total_tokens=response.usage.total_tokens if response.usage else 0,
                    latency=round(time.time() - start_time, 3),
                    created_at=datetime.now(timezone.utc).isoformat()
                )

            logger.info("Generation complete")
            return GeneratedResponse(
                answer=response.choices[0].message.content.strip(),
                sources=sources,
                model_name=self.model_name,
                prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                completion_tokens=response.usage.completion_tokens if response.usage else 0,
                total_tokens=response.usage.total_tokens if response.usage else 0,
                latency=round(time.time() - start_time, 3),
                created_at=datetime.now(timezone.utc).isoformat()
            )

        except Exception as e:
            logger.error(f"Generation failure: {str(e)}")
            return GeneratedResponse(
                answer="An error occurred while generating the answer.",
                sources=sources,
                model_name=self.model_name,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency=round(time.time() - start_time, 3),
                created_at=datetime.now(timezone.utc).isoformat()
            )