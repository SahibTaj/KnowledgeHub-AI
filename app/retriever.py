import logging
from typing import List, Optional, Dict, Any
from app.models import SearchResult
from app.storage.vectordb import VectorDB
from app.embeddings.embedder import Embedder

logger = logging.getLogger(__name__)

class Retriever:
    """
    Retrieves semantically relevant document chunks from the vector database for a user query.
    """
    def __init__(self, embedder: Embedder, vectordb: VectorDB):
        self.embedder = embedder
        self.vectordb = vectordb

    def _validate_query(self, query: str) -> str:
        if not isinstance(query, str):
            logger.warning("query validation failed: Input is not a string.")
            raise ValueError("Query must be a string")
        
        cleaned_query = query.strip()
        if not cleaned_query:
            logger.warning("Empty query received")
            raise ValueError("Query cannot be empty.")
            
        if len(cleaned_query) < 3:
            logger.warning(f"Query validation failed: Query '{cleaned_query}' is too short.")
            raise ValueError("Query is too short.")
        
        return cleaned_query
    
    def _embed_query(self, query: str) -> List[float]:
        logger.info("Embedding validated query...")
        return self.embedder.embed_query(query)
    
    def _search(self, query_vector: List[float], top_k: int, where_filter: Optional[Dict[str, Any]]) -> List[SearchResult]:
        logger.info("Executing semantic retrieval...")
        return self.vectordb.semantic_search(
            vector=query_vector,
            top_k=top_k,
            where_filter=where_filter
        )
    
    def retrieve(self, query: str, top_k: int = 5, where_filter: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        logger.info("Received retrieval request")

        try:
            cleaned_query = self._validate_query(query)
        except ValueError:
            return []
        
        try:
            query_vector = self._embed_query(cleaned_query)
        except Exception as e:
            logger.error(f"Embedding failed: {str(e)}")
            return []
        
        try:
            results = self._search(query_vector, top_k, where_filter)
        except TimeoutError as e:
            logger.error(f"Search timeout: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"VectorDB unavailable: {str(e)}")
            return []
        
        if not results:
            logger.warning("No documents found")
            return []

        logger.info(f"Retrieved {len(results)} chunks")
        logger.info("Returning results")
        return results
