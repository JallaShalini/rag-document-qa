# RAG Document QA

A Retrieval-Augmented Generation (RAG) document question-answering API powered by FastAPI, local embeddings, and a Chroma vector database.

## Project Overview

This project enables users to upload documents in `.txt`, `.md`, or `.pdf` format, ingest text into a local vector store, and query indexed documents using natural language.

## Features

- Upload and index documents
- Extract text from plain text, Markdown, and PDF files
- Chunk documents into smaller text pieces for embedding
- Generate embeddings using Sentence Transformers
- Store and search vectors in a local ChromaDB vector store
- Query indexed documents with an LLM-backed answer generation flow
- Health report endpoint for system status
- Dockerized deployment and CI/CD with GitHub Actions

## Architecture

The application is organized as a modular FastAPI service.

- `app/main.py`: application entrypoint and router registration
- `app/api/`: REST API endpoints for upload, query, and report
- `app/services/`: document processing, embeddings, retrieval, and LLM integration
- `app/database/`: ChromaDB client and collection management
- `app/parsers/`: reading text from `.txt`, `.md`, and `.pdf` files
- `app/prompts/`: prompt template used for RAG-style generation
- `app/schemas/`: request and response models
- `app/utils/`: logging, validation, and helper utilities

## Folder Structure

```text
.
├── app
│   ├── api
│   ├── config.py
│   ├── constants.py
│   ├── database
│   ├── models
│   ├── parsers
│   ├── prompts
│   ├── schemas
│   ├── services
│   ├── startup.py
│   └── utils
├── docs
│   ├── api_examples.md
│   ├── architecture.png
│   ├── workflow.png
│   └── screenshots
├── scripts
│   ├── cleanup_uploads.py
│   ├── download_embedding_model.py
│   └── initialize_vector_db.py
├── tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
└── .github
    └── workflows
```

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-org/rag-document-qa.git
cd rag-document-qa
pip install -r requirements.txt
```

## Virtual Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Docker Setup

Build and start the application with Docker Compose:

```bash
docker compose up --build
```

Then open `http://localhost:8000/`.

## Environment Variables

Copy `.env.example` to `.env` and configure values:

```text
LLM_API_KEY=your_secret_key_here
LLM_PROVIDER=openai
MODEL_NAME=all-MiniLM-L6-v2
UPLOAD_PATH=uploads
CHROMA_PATH=chroma_db
LOG_PATH=logs/app.log
TOP_K=3
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## API Documentation

Available endpoints:

- `GET /` - health check
- `POST /upload` - upload and index a document
- `POST /query` - ask a question against the indexed documents
- `GET /report` - retrieve system report data

For examples, see `docs/api_examples.md`.

## Example Requests

### Upload document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/document.pdf"
```

### Query document

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main idea of the document?"}'
```

## Example Responses

### Upload response

```json
{
  "message": "File uploaded and indexed successfully."
}
```

### Query response

```json
{
  "answer": "The main idea is to ...",
  "sources": [
    "first chunk text...",
    "second chunk text..."
  ]
}
```

## Testing

Run the test suite using pytest:

```bash
pytest -q
```

## Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- Sentence Transformers
- ChromaDB
- PyPDF2
- Requests
- Docker
- GitHub Actions

## Future Improvements

- Add authentication and authorization
- Support more file formats
- Improve RAG prompt and retrieval quality
- Add a web UI or dashboard
- Add monitoring and observability
- Add end-to-end integration tests

## License

This project is licensed under the MIT License.
