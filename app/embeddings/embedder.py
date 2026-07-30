from typing import List
from app.config import EMBEDDING_MODEL
from app.models import Chunk, EmbeddingRecord

class Embedder:
    def __init__(self, embedding_model=EMBEDDING_MODEL):
        self.embedding_model = embedding_model
        self.model_name_str = getattr(self.embedding_model, "model_name", "BAAI/bge-small-en-v1.5")

    def encode_text(self, text_list: List[str]) -> List[List[float]]:
        embeddings = self.embedding_model.encode(text_list)
        return [list(vector) for vector in embeddings]

    def embed_query(self, query: str) -> List[float]:
        vectors = self.encode_text([query])
        return vectors[0]

    def embed_documents(self, chunks: List[Chunk]) -> List[EmbeddingRecord]:
        chunk_text_list = [chunk.text for chunk in chunks]
        vectors_list = self.encode_text(chunk_text_list)
        
        embedding_records: List[EmbeddingRecord] = []
        for chunk, vector in zip(chunks, vectors_list):
            record = EmbeddingRecord(
                chunk=chunk,
                embedding=vector,
                model_name=self.model_name_str
            )
            embedding_records.append(record)
            
        return embedding_records
