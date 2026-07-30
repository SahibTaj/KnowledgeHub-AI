from typing import List, Dict, Any
import datetime
import uuid

class Page:
    def __init__(self, page_number: int, text: str, metadata: Dict[str, Any] = None):
        self.page_number = page_number
        self.text = text
        self.metadata = metadata if metadata is not None else {}


class Document:
    def __init__(
        self, 
        document_id: str, 
        title: str, 
        source: str, 
        metadata: Dict[str, Any], 
        pages: List[Page],
        file_hash: str = "",
        version: str = "1.0",
        status: str = "pending"
    ):
        self.document_id = document_id
        self.title = title
        self.source = source
        self.metadata = metadata
        self.pages = pages
        self.file_hash = file_hash
        self.version = version
        self.status = status


class Chunk:
    def __init__(
        self, 
        chunk_id: str, 
        document_id: str, 
        page_number: int, 
        text: str, 
        metadata: Dict[str, Any]
        
    ):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.page_number = page_number
        self.text = text
        self.metadata = metadata

class EmbeddingRecord:
    def __init__(
        self, 
        chunk: Chunk, 
        embedding: List[float], 
        model_name: str,
        embedding_id: str = None
    ):
        self.embedding_id = embedding_id if embedding_id is not None else f"emb_{uuid.uuid4()}"
        self.chunk = chunk  
        self.embedding = embedding  
        self.model_name = model_name
        self.created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

class SearchResult:
    def __init__(self, id: str, text: str, metadata: Dict[str, Any], distance: float):
        self.id = id
        self.text = text
        self.metadata = metadata
        self.distance = distance