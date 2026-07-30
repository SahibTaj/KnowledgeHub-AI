import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.config import settings
from app.api.schemas import (
    AskRequest, 
    AskResponse, 
    UploadRequest, 
    UploadResponse, 
    HealthResponse
)
from app.api.dependencies import get_pipeline, get_knowledge_base
from app.pipeline.rag_pipeline import RAGPipeline
from app.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["RAG Core Endpoints"])

@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    logger.info("Received health check request")
    return HealthResponse(
        status="healthy",
        llm_provider=settings.LLM_PROVIDER,
        embedding_model=settings.EMBEDDING_MODEL,
        vector_database="ChromaDB",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@router.post("/chat", response_model=AskResponse)
def chat(
    request: AskRequest, 
    pipeline: RAGPipeline = Depends(get_pipeline)
) -> AskResponse:
    logger.info("Received chat request")
    result = pipeline.ask(
        question=request.question,
        top_k=request.top_k,
        where_filter=request.where_filter
    )
    return AskResponse(
        answer=result.answer,
        sources=result.sources,
        model_name=result.model_name,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        total_tokens=result.total_tokens,
        latency=result.latency,
        created_at=result.created_at
    )

@router.post("/documents", response_model=UploadResponse)
def upload_document(
    request: UploadRequest, 
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> UploadResponse:
    logger.info("Received document upload request for ID: %s", request.document_id)
    success = kb.add_document(
        document_id=request.document_id,
        file_name=request.file_name,
        raw_text=request.raw_text,
        metadata=request.metadata
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document ingestion failed."
        )
    return UploadResponse(
        success=True,
        message="Document processed and stored successfully.",
        document_id=request.document_id
    )

@router.put("/documents/{document_id}", response_model=UploadResponse)
def update_document(
    document_id: str, 
    request: UploadRequest, 
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> UploadResponse:
    logger.info("Received document update request for ID: %s", document_id)
    if request.document_id != document_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Route identifier mismatch against body payload document ID."
        )
    success = kb.update_document(
        document_id=document_id,
        file_name=request.file_name,
        new_text=request.raw_text,
        metadata=request.metadata
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document update failed."
        )
    return UploadResponse(
        success=True,
        message="Document updated successfully.",
        document_id=document_id
    )

@router.delete("/documents/{document_id}", response_model=UploadResponse)
def delete_document(
    document_id: str, 
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> UploadResponse:
    logger.info("Received document deletion request for ID: %s", document_id)
    success = kb.remove_document(document_id=document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document removal failed."
        )
    return UploadResponse(
        success=True,
        message="Document and matching context chunks completely removed.",
        document_id=document_id
    )
