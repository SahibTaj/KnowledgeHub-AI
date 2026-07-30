import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models import Document, Chunk
from app.utils.chunk_config import CHUNK_SIZE, CHUNK_OVERLAP

def clean_text(text):

    if not text:
        return ""
    
    text = re.sub(r'[\r\n]+', '\n', text)

    text = re.sub(r'\t+', ' ', text)

    text = '\n'.join(line.strip() for line in text.split('\n'))

    text = re.sub(r'\n{3,}', '\n\n', text)

    text = re.sub(r' +', ' ', text)

    return text.strip()


def split_text(clean_text_str: str) -> list[str]:
    if not clean_text_str:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    chunks = text_splitter.split_text(clean_text_str)
    return chunks

class ProcessingService:
    def __init__(self):
          pass
    
    def process_document(self, document: Document) -> list[Chunk]:
        processed_chunks: list[Chunk] = []
        chunk_counter = 0

        for page in document.pages:
            cleaned_page_text = clean_text(page.text)
            
            text_segments = split_text(cleaned_page_text)
            
            for segment in text_segments:
                chunk_counter += 1
                
                chunk_metadata = {
                    **page.metadata,
                    "global_document_title": document.title,
                    "sequence_index": chunk_counter
                }
                
                chunk_obj = Chunk(
                    chunk_id=f"{document.document_id}_p{page.page_number}_c{chunk_counter}",
                    document_id=document.document_id,
                    page_number=page.page_number,
                    text=segment,
                    metadata=chunk_metadata
                )
                processed_chunks.append(chunk_obj)
                
        return processed_chunks