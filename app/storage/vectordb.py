import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from app.models import EmbeddingRecord, SearchResult
from app.config import COLLECTION_NAME

logger = logging.getLogger("app.vectordb")

class VectorDB:
    def __init__(self, db_path: str = "./data/my_chroma_db"):
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.client = chromadb.PersistentClient(path=db_path)
            logger.info(f"Successfully initialized PersistentClient at path: {db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize PersistentClient at path {db_path}: {str(e)}")
            raise

    def get_or_create_collection(self, collection_name: str = COLLECTION_NAME):
        try:
            return self.client.get_or_create_collection(name=collection_name)
        except Exception as e:
            logger.error(f"Failed to get or create collection '{collection_name}': {str(e)}")
            raise

    def store(self, embedding_records: List[EmbeddingRecord], collection_name: str = COLLECTION_NAME) -> None:
        if not embedding_records:
            logger.warning("No embedding records provided for storage execution pipeline.")
            return

        try:
            collection = self.get_or_create_collection(collection_name)

            ids = [record.embedding_id for record in embedding_records]
            embeddings = [record.embedding for record in embedding_records]
            documents = [record.chunk.text for record in embedding_records]

            metadatas: List[Dict[str, Any]] = []
            for record in embedding_records:
                meta_entry = {
                    **record.chunk.metadata,                  
                    "document_id": record.chunk.document_id,  
                    "chunk_id": record.chunk.chunk_id,        
                    "page_number": record.chunk.page_number,  
                    # 2. Extract explicit relative sequence index order position tracking
                    "chunk_index": record.chunk.metadata.get("sequence_index", 0),
                    "model_name": record.model_name,          
                    "created_at": record.created_at           
                }
                metadatas.append(meta_entry)

            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            logger.info(f"Successfully indexed {len(embedding_records)} records into collection '{collection_name}'.")
        except Exception as e:
            logger.error(f"Database write operation failed for collection '{collection_name}': {str(e)}")
            raise

    def semantic_search(
        self, 
        vector: List[float], 
        top_k: int = 3,                       
        where_filter: Optional[Dict[str, Any]] = None,
        collection_name: str = COLLECTION_NAME
    ) -> List[SearchResult]: 
        """
        Executes a semantic similarity search across the specified vector index collection.
        Accepts normalized parameter naming conventions for direct agent/retriever routing.
        """
        normalized_results: List[SearchResult] = []
        try:
            collection = self.get_or_create_collection(collection_name)
            
            # Map clean parameters to native Chroma API keywords
            raw_results = collection.query(
                query_embeddings=[vector],
                n_results=top_k,
                where=where_filter
            )

            # Chroma extracts multi-query arrays. Handle the first dimensional slice out safely.
            if not raw_results or not raw_results.get("ids") or not raw_results["ids"][0]:
                return normalized_results

            # Unpack Chroma dimensions safely
            query_ids = raw_results["ids"][0]
            query_docs = raw_results["documents"][0]
            query_metas = raw_results["metadatas"][0]
            query_dists = raw_results["distances"][0]

            for idx in range(len(query_ids)):
                result_obj = SearchResult(
                    id=query_ids[idx],
                    text=query_docs[idx],
                    metadata=query_metas[idx],
                    distance=query_dists[idx]
                )
                normalized_results.append(result_obj)

            logger.info(f"Semantic search returned {len(normalized_results)} hits from collection '{collection_name}'.")
            return normalized_results
        except Exception as e:
            logger.error(f"Semantic search operation failed on collection '{collection_name}': {str(e)}")
            return normalized_results

    def replace_document(self, document_id: str, new_records: List[EmbeddingRecord], collection_name: str = COLLECTION_NAME) -> None:
        try:
            logger.info(f"Executing atomic replace sequence for Document ID: {document_id}")
            self.delete_by_document_id(document_id, collection_name=collection_name)
            self.store(new_records, collection_name=collection_name)
            logger.info(f"Successfully replaced entire document state for Document ID: {document_id}")
        except Exception as e:
            logger.error(f"Failed to execute atomic replace sequence for Document ID {document_id}: {str(e)}")
            raise

    def delete_by_document_id(self, document_id: str, collection_name: str = COLLECTION_NAME) -> None:
        try:
            collection = self.get_or_create_collection(collection_name)
            collection.delete(where={"document_id": document_id})
            logger.info(f"Cleaned all chunk records matched with Document ID: {document_id}")
        except Exception as e:
            logger.error(f"Delete operation failed for Document ID {document_id}: {str(e)}")
            raise

    def delete_collection(self, collection_name: str = COLLECTION_NAME) -> None:
        try:
            self.client.delete_collection(name=collection_name)
            logger.info(f"Destroyed collection context index structure: '{collection_name}' successfully.")
        except Exception as e:
            logger.warning(f"Error during drop collection operation for '{collection_name}': {str(e)}")
