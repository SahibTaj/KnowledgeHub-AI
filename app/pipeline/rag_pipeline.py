import logging
import time
from datetime import datetime, timezone
from typing import Optional
from app.models import GeneratedResponse
from app.retriever import Retriever
from app.generator import Generator

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, retriever: Retriever, generator: Generator):
        self.retriever = retriever
        self.generator = generator

    def ask(self, question: str, top_k: int = 5, where_filter: Optional[dict] = None) -> GeneratedResponse:
        logger.info("Pipeline started")
        start_time = time.time()

        if not question or not question.strip():
            logger.warning("Pipeline validation failed: Empty question received.")
            return GeneratedResponse(
                answer="Question cannot be empty.",
                sources=[],
                model_name=self.generator.model_name,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency=0.0,
                created_at=datetime.now(timezone.utc).isoformat()
            )

        try:
            search_results = self.retriever.retrieve(
                query=question,
                top_k=top_k,
                where_filter=where_filter
            )
            logger.info("Retrieval completed")
        except Exception as e:
            logger.error(f"Pipeline failure during retrieval stage: {str(e)}")
            return GeneratedResponse(
                answer="An internal error occurred during the document retrieval stage.",
                sources=[],
                model_name=self.generator.model_name,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency=round(time.time() - start_time, 3),
                created_at=datetime.now(timezone.utc).isoformat()
            )

        try:
            response = self.generator.generate(
                question=question,
                search_results=search_results
            )
            logger.info("Generation completed")
        except Exception as e:
            logger.error(f"Pipeline failure during generation stage: {str(e)}")
            return GeneratedResponse(
                answer="An internal error occurred during the answer generation stage.",
                sources=[res.id for res in search_results if res.id],
                model_name=self.generator.model_name,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency=round(time.time() - start_time, 3),
                created_at=datetime.now(timezone.utc).isoformat()
            )

        logger.info("Pipeline finished")
        return response
