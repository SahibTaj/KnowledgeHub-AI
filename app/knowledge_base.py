import logging
from typing import List, Dict, Any, Optional
from app.storage.vectordb import VectorDB
from app.embeddings.embedder import Embedder

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    Manages the lifecycle, indexing, and state of documents within the storage layer.
    """
    def __init__(self, processing_service: Any, embedder: Embedder, vectordb: VectorDB):
        self.processing_service = processing_service
        self.embedder = embedder
        self.vectordb = vectordb

    def add_document(self, document_id: str, file_name: str, raw_text: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        logger.info(f"Adding document: {file_name} with ID: {document_id}")
        if not raw_text or not raw_text.strip():
            logger.warning(f"Skipped empty content submission for document: {document_id}")
            return False

        try:
            chunks = self.processing_service.process_document(
                document_id=document_id,
                file_name=file_name,
                raw_text=raw_text,
                metadata=metadata
            )
            
            embedding_records = self.embedder.embed_documents(chunks)
            self.vectordb.store(embedding_records)
            
            logger.info(f"Successfully indexed document: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add document {document_id}: {str(e)}")
            return False

    def remove_document(self, document_id: str) -> bool:
        logger.info(f"Removing document: {document_id}")
        try:
            self.vectordb.delete_by_document_id(document_id)
            logger.info(f"Successfully purged document state: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove document {document_id}: {str(e)}")
            return False

    def update_document(self, document_id: str, file_name: str, new_text: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        logger.info(f"Executing atomic update for document: {document_id}")
        try:
            self.remove_document(document_id)
            return self.add_document(document_id, file_name, new_text, metadata)
        except Exception as e:
            logger.error(f"Failed to atomically update document {document_id}: {str(e)}")
            return False

    def rebuild_index(self) -> bool:
        logger.info("Rebuilding vector storage collection indices")
        try:
            self.vectordb.delete_collection()
            self.vectordb.get_or_create_collection()
            logger.info("Successfully reset the knowledge base index structures")
            return True
        except Exception as e:
            logger.error(f"Failed to execute structural index rebuild: {str(e)}")
            return False
