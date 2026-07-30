import os
from langchain_community.document_loaders import PyPDFLoader
import uuid
from app.models import Page, Document 


def validator(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file does not exists: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f'The file is not a pdf: {file_path}')


def load_pdf(file_path):

    loader = PyPDFLoader(file_path)
    docs = loader.load()


def extract_metadata(single_doc_node):
    if not single_doc_node or not hasattr(single_doc_node, "metadata"):
        return {}
    meta = single_doc_node.metadata
    return {
        "filename": meta.get("source"),
        "total_pages": meta.get("total_pages"),
        "file_size": meta.get("file_size"),
        "author": meta.get("author"),
        "creation_date": meta.get("creation_date")
    }

def doc_service(file_path)-> Document:
    validator(file_path)
    load_doc = load_pdf(file_path)
    global_meta = extract_metadata(load_doc[0]) if load_doc else {}

    pages = [
        Page(
            page_number=idx + 1, 
            text=doc.page_content,
            metadata={}
        ) 
        for idx, doc in enumerate(load_doc)
    ]

    return Document(
        document_id=str(uuid.uuid4()),
        title=os.path.basename(global_meta.get("filename", "Untitled")),
        source = file_path,
        metadata=global_meta,
        pages=pages,
        status="loaded"
    )