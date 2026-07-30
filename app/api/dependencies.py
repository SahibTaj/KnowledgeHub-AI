import logging
from typing import Optional
from app.config import settings
from app.embeddings.embedder import Embedder
from app.storage.vectordb import VectorDB
from app.retriever import Retriever
from app.llm.base import BaseLLMClient
from app.llm.factory import LLMFactory
from app.generator import Generator
from app.pipeline.rag_pipeline import RAGPipeline
from app.knowledge_base import KnowledgeBase
from app.processing import ProcessingService

logger = logging.getLogger(__name__)

class AppContainer:
    _embedder: Optional[Embedder] = None
    _vectordb: Optional[VectorDB] = None
    _llm_client: Optional[BaseLLMClient] = None
    _retriever: Optional[Retriever] = None
    _processing_service: Optional[ProcessingService] = None
    _generator: Optional[Generator] = None
    _pipeline: Optional[RAGPipeline] = None
    _knowledge_base: Optional[KnowledgeBase] = None

    def __new__(cls):
        raise TypeError("AppContainer is a static configuration container and cannot be instantiated.")

    @classmethod
    def initialize(cls) -> None:
        logger.info("[Container] Triggering eager startup initialization...")
        cls.get_pipeline()
        cls.get_knowledge_base()
        logger.info("[Container] Eager initialization complete. Core services warmed up.")

    @classmethod
    def shutdown(cls) -> None:
        logger.info("[Container] Shutting down services and clearing resources...")
        cls._embedder = None
        cls._vectordb = None
        cls._llm_client = None
        cls._retriever = None
        cls._processing_service = None
        cls._generator = None
        cls._pipeline = None
        cls._knowledge_base = None
        logger.info("[Container] Shutdown lifecycle tasks finished.")

    @classmethod
    def get_embedder(cls) -> Embedder:
        if cls._embedder is None:
            logger.info("[Container] Embedder initialized")
            cls._embedder = Embedder()
        return cls._embedder

    @classmethod
    def get_vectordb(cls) -> VectorDB:
        if cls._vectordb is None:
            logger.info("[Container] VectorDB initialized")
            cls._vectordb = VectorDB()
        return cls._vectordb

    @classmethod
    def get_llm_client(cls) -> BaseLLMClient:
        if cls._llm_client is None:
            logger.info(f"[Container] LLMClient initialized ({settings.LLM_PROVIDER})")
            cls._llm_client = LLMFactory.get_client(
                provider=settings.LLM_PROVIDER, 
                model=settings.LLM_MODEL
            )
        return cls._llm_client

    @classmethod
    def get_retriever(cls) -> Retriever:
        if cls._retriever is None:
            logger.info("[Container] Retriever initialized")
            cls._retriever = Retriever(
                embedder=cls.get_embedder(),
                vectordb=cls.get_vectordb()
            )
        return cls._retriever

    @classmethod
    def get_processing_service(cls) -> ProcessingService:
        if cls._processing_service is None:
            logger.info("[Container] ProcessingService initialized")
            cls._processing_service = ProcessingService()
        return cls._processing_service

    @classmethod
    def get_generator(cls) -> Generator:
        if cls._generator is None:
            logger.info("[Container] Generator initialized")
            cls._generator = Generator(
                llm_client=cls.get_llm_client(),
                model_name=settings.LLM_MODEL
            )
        return cls._generator

    @classmethod
    def get_pipeline(cls) -> RAGPipeline:
        if cls._pipeline is None:
            logger.info("[Container] Pipeline initialized")
            cls._pipeline = RAGPipeline(
                retriever=cls.get_retriever(),
                generator=cls.get_generator()
            )
        return cls._pipeline

    @classmethod
    def get_knowledge_base(cls) -> KnowledgeBase:
        if cls._knowledge_base is None:
            logger.info("[Container] KnowledgeBase initialized")
            cls._knowledge_base = KnowledgeBase(
                processing_service=cls.get_processing_service(),
                embedder=cls.get_embedder(),
                vectordb=cls.get_vectordb()
            )
        return cls._knowledge_base

def get_embedder() -> Embedder:
    return AppContainer.get_embedder()

def get_vectordb() -> VectorDB:
    return AppContainer.get_vectordb()

def get_llm_client() -> BaseLLMClient:
    return AppContainer.get_llm_client()

def get_retriever() -> Retriever:
    return AppContainer.get_retriever()

def get_processing_service() -> ProcessingService:
    return AppContainer.get_processing_service()

def get_generator() -> Generator:
    return AppContainer.get_generator()

def get_pipeline() -> RAGPipeline:
    return AppContainer.get_pipeline()

def get_knowledge_base() -> KnowledgeBase:
    return AppContainer.get_knowledge_base()
