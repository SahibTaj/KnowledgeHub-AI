# KnowledgeHub-AI

> Enterprise Knowledge Base Copilot powered by Retrieval-Augmented
> Generation (RAG)

KnowledgeHub-AI is an internal AI assistant designed to help employees
ask questions about company knowledge and receive grounded answers based
on trusted internal documents.

The long-term goal is to connect enterprise knowledge sources such as
Google Drive, Notion, Confluence, and other internal systems while
respecting user access permissions.

## Project Status

🚧 **Work in Progress --- MVP under development**

The current project is being built from the core RAG pipeline upward.
The initial MVP focuses on document ingestion, chunking, embeddings,
vector search, retrieval, and grounded answer generation through an API.

## Core Problem

Company information is often distributed across:

-   PDFs
-   Text documents
-   Internal policies
-   Google Drive
-   Notion
-   Confluence
-   Other knowledge repositories

Employees spend time searching through these sources manually.

KnowledgeHub-AI aims to provide a single interface where an employee can
ask:

> "What is our annual leave policy?"

and receive an answer based on the company's internal knowledge, along
with the relevant source information.

## Planned Architecture

``` text
                 Enterprise Knowledge Sources
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Google        Notion     Confluence
            Drive
              │            │            │
              └────────────┼────────────┘
                           ↓
                    Ingestion Pipeline
                           ↓
                    Document Processing
                           ↓
                    Text Chunking
                           ↓
                       Embeddings
                           ↓
                     Vector Database
                           │
                           │
User Question ─────────────┘
       ↓
   Retrieval
       ↓
 Relevant Chunks
       ↓
 Prompt Construction
       ↓
      LLM
       ↓
 Grounded Answer
       ↓
 Answer + Sources
```

## Current Project Structure

``` text
enterprise-copilot/
│
├── app/
│   ├── agents/
│   │
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── core/
│   │   ├── exception_handler.py
│   │   ├── middleware.py
│   │   ├── security.py
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── session.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── groq_client.py
│   │   ├── ollama_client.py
│   │   └── openai_client.py
│   │
│   ├── pipeline/
│   │   └── rag_pipeline.py
│   │
│   ├── storage/
│   │   ├── document_manager.py
│   │   └── vectordb.py
│   │
│   ├── utils/
│   │   ├── chunk_config.py
│   │   └── helpers.py
│   │
│   ├── generator.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── processing.py
│   └── retriever.py
│
├── data/
├── docs/
├── logs/
├── tests/
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Main Components

### Document Processing

Responsible for converting raw documents into clean, manageable chunks.

``` text
Document
   ↓
Text Extraction
   ↓
Cleaning
   ↓
Chunking
   ↓
Chunks
```

### Embedding Layer

Converts text chunks and user questions into numerical vector
representations.

``` text
Text
 ↓
Embedding Model
 ↓
Vector
```

### Vector Database

Stores document chunk embeddings and their metadata so relevant
information can be retrieved efficiently.

### Retriever

Takes a user's question, searches the vector database, and returns the
most relevant chunks.

### Generator

Provides the retrieved context to an LLM and generates a grounded
answer.

### RAG Pipeline

Coordinates the complete question-answering flow:

``` text
Question
   ↓
Embed
   ↓
Retrieve
   ↓
Build Context
   ↓
Generate
   ↓
Answer + Sources
```

## LLM Support

The project uses an LLM abstraction so that the application is not
tightly coupled to a single provider.

Currently planned/supported providers include:

-   Groq
-   OpenAI
-   Ollama

The provider can be selected through configuration.

## Planned Enterprise Features

The basic RAG MVP will be extended with enterprise-specific
capabilities.

### Authentication

Users will be able to:

-   Register
-   Login
-   Receive JWT access tokens
-   Access protected APIs

### Role-Based Access Control

Different users will have different permissions.

Example:

``` text
Admin
  ├── Upload documents
  ├── Delete documents
  └── Manage users

Employee
  └── Query permitted knowledge
```

### Access-Control-Aware Retrieval

A key goal of the project is preventing users from retrieving
information they are not authorized to access.

Document metadata will eventually contain access information such as:

``` text
department
role
visibility
owner
```

Retrieval will use this metadata when determining which chunks can be
returned.

### Multi-Source Connectors

Planned connectors include:

-   Google Drive
-   Notion
-   Confluence
-   SharePoint

### Knowledge Gap Detection

The system will eventually identify questions that cannot be answered
confidently from the existing knowledge base.

This can help organizations discover:

-   Missing documentation
-   Outdated policies
-   Frequently asked questions without clear answers

### Staleness Detection

Documents will be tracked for freshness so that outdated internal
knowledge can be identified.

## MVP Goal

The first working MVP should support this flow:

``` text
Upload Document
       ↓
Extract Text
       ↓
Clean + Chunk
       ↓
Generate Embeddings
       ↓
Store in Vector DB
       ↓

Ask Question
       ↓
Retrieve Relevant Chunks
       ↓
Generate Grounded Answer
       ↓
Return Answer + Sources
```

Example:

``` text
User:
"What is the company's annual leave policy?"

System:
1. Converts the question to an embedding
2. Searches the vector database
3. Retrieves relevant policy chunks
4. Sends the context to the LLM
5. Generates the answer
6. Returns the relevant source information
```

## Technology Stack

### Backend

-   Python
-   FastAPI

### RAG

-   Retrieval-Augmented Generation
-   Embedding models
-   ChromaDB / vector database
-   LLM provider abstraction

### Database

-   PostgreSQL for application/enterprise metadata
-   Vector database for semantic retrieval

### Authentication

-   JWT
-   Password hashing

### Development

-   Git
-   GitHub
-   Pytest

## Development Philosophy

This project is intentionally being built incrementally rather than
treating it as a collection of generated code.

Each major component follows:

``` text
Design
  ↓
Implement
  ↓
Test
  ↓
Review
  ↓
Integrate
```

The goal is not only to build a working RAG application, but also to
understand the engineering decisions behind each component.

## Roadmap

### Phase 1 --- RAG MVP

-   [x] Project structure
-   [ ] Document processing
-   [ ] Chunking
-   [ ] Embedding generation
-   [ ] Vector storage
-   [ ] Retrieval
-   [ ] LLM generation
-   [ ] End-to-end RAG pipeline
-   [ ] Source citations

### Phase 2 --- Backend MVP

-   [ ] Document upload API
-   [ ] Chat API
-   [ ] Document management
-   [ ] Error handling
-   [ ] API testing

### Phase 3 --- Enterprise Security

-   [ ] User registration
-   [ ] Login
-   [ ] JWT authentication
-   [ ] Role-based authorization
-   [ ] Access-control-aware retrieval

### Phase 4 --- Enterprise Integrations

-   [ ] Google Drive connector
-   [ ] Notion connector
-   [ ] Confluence connector
-   [ ] Document synchronization
-   [ ] Staleness detection

### Phase 5 --- Production Improvements

-   [ ] Evaluation framework
-   [ ] Retrieval quality evaluation
-   [ ] Observability
-   [ ] Audit logging
-   [ ] Knowledge gap detection
-   [ ] Deployment
-   [ ] Performance optimization

## Running Locally

Create a virtual environment:

``` bash
python -m venv .venv
```

Activate it on Windows:

``` powershell
.venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Create a `.env` file and provide the required configuration.

Start the FastAPI application:

``` bash
uvicorn app.main:app --reload
```

The API documentation will be available through FastAPI's Swagger UI.

## Environment Variables

Secrets and environment-specific configuration should be stored in
`.env` and never committed to Git.

Example categories:

``` text
DATABASE_URL
LLM_PROVIDER
LLM_MODEL
OPENAI_API_KEY
GROQ_API_KEY
```

Use the actual variables required by the current implementation.

## Git Workflow

Development is organized around small, meaningful commits.

Example:

``` bash
git add .
git commit -m "feat: implement document chunking"
git push
```

Avoid committing:

-   `.env`
-   virtual environments
-   generated logs
-   cache files
-   local databases
-   secrets

## Future Vision

KnowledgeHub-AI is intended to evolve from a basic RAG application into
an enterprise knowledge platform capable of:

``` text
Multiple Sources
      +
Access Control
      +
Reliable Retrieval
      +
Grounded Generation
      +
Freshness Detection
      +
Knowledge Gap Detection
      ↓
Enterprise Knowledge Copilot
```

------------------------------------------------------------------------

**Status:** 🚧 MVP in development

**Repository:** KnowledgeHub-AI
