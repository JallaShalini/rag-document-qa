# API Examples

## Upload Document

**Endpoint**: `POST /upload`

**Description**: Upload a supported document file (`.txt`, `.md`, `.pdf`) for processing and indexing.

**Request**:

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/document.pdf"
```

**Response**:

```json
{
  "message": "File uploaded and indexed successfully."
}
```

## Query Document

**Endpoint**: `POST /query`

**Description**: Query the indexed documents with a natural language question.

**Request**:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main idea of the document?"}'
```

**Response**:

```json
{
  "answer": "The main idea is to ...",
  "sources": [
    "first chunk text...",
    "second chunk text..."
  ]
}
```

## Health / Report

**Endpoint**: `GET /report`

**Description**: Retrieve a simple health and report status summary.

**Request**:

```bash
curl http://localhost:8000/report
```

**Response**:

```json
{
  "context_precision": 0.90,
  "faithfulness": 0.85,
  "system_status": "healthy"
}
```
