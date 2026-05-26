# Department Documents AI Assistant

AI assistant for navigating department center documents, regulations, instructions, service descriptions, and internal knowledge base materials.

The project is built as a production-oriented FastAPI service with a provider-agnostic LLM layer and a lightweight web interface. The current version focuses on the conversational LLM layer; the architecture is prepared for document ingestion, retrieval, citations, and RAG quality evaluation.

## Use Case

Employees and operators often need to find precise information across internal documents: service rules, required documents, process steps, deadlines, responsibilities, and exceptions. This assistant is designed to reduce manual search time and provide a structured entry point into a document knowledge base.

Example questions:

- What documents are required for a specific service?
- Which regulation describes this process?
- What are the steps for handling a citizen request?
- Who is responsible for a specific workflow stage?
- Which source document should be checked before answering?

## Current Features

- FastAPI backend with typed request and response schemas.
- Web UI for interacting with the assistant.
- Provider-agnostic LLM interface.
- OpenRouter integration.
- Gemini integration.
- Environment-based configuration.
- Health endpoint.
- Swagger/OpenAPI documentation.
- Clear project structure for future RAG modules.

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic / pydantic-settings
- httpx
- OpenRouter API
- Gemini API
- HTML, CSS, JavaScript

## Architecture

```text
User
  |
  v
Web UI
  |
  v
FastAPI API
  |
  v
LLMProvider interface
  |
  +-- OpenRouterProvider
  |
  +-- GeminiProvider
```

The backend does not depend directly on a specific LLM provider. Application logic calls a shared `LLMProvider` interface, while provider adapters handle API-specific payloads, headers, models, and response parsing.

This design allows the project to add new providers or switch models without rewriting the application layer.

## Project Structure

```text
app/
  core/
    config.py          # environment-based settings
  llm/
    base.py            # provider interface and shared data models
    factory.py         # provider selection
    openrouter.py      # OpenRouter adapter
    gemini.py          # Gemini adapter
  schemas/
    chat.py            # API request/response schemas
  web/
    index.html         # web UI
    styles.css         # UI styles
    app.js             # browser-side chat logic
  main.py              # FastAPI application
```

## API

### `GET /health`

Returns service status.

```json
{
  "status": "ok"
}
```

### `POST /chat`

Sends a user question to the configured LLM provider.

Request:

```json
{
  "message": "Какие вопросы можно задавать по документам центра?"
}
```

Response:

```json
{
  "answer": "...",
  "provider": "openrouter",
  "model": "openai/gpt-4o-mini"
}
```

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

OpenRouter:

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Gemini:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```

Secrets are loaded from environment variables and must not be committed to the repository.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

Web UI:

```text
http://127.0.0.1:8000/
```

OpenAPI docs:

```text
http://127.0.0.1:8000/docs
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Какие документы нужны для получения услуги?"}'
```

## Security Notes

- API keys are stored only in environment variables.
- `.env` is excluded from git.
- The assistant is instructed to distinguish facts from assumptions and request source documents when needed.
- For production usage, add authentication, request limits, audit logs, and stricter source-grounding through retrieval and citations.

## Roadmap

- Document upload for PDF, DOCX, HTML, and TXT.
- Document parsing and normalization.
- Chunking strategy for regulations and instructions.
- Embeddings provider abstraction.
- Vector database integration.
- Retrieval endpoint.
- Reranking layer.
- Answers with source citations.
- RAG evaluation module for faithfulness, relevance, and context quality.
- Latency and cost logging.
- Docker Compose setup.
