# PDF Parse Service

Local PDF parsing microservice using Docling for My Health Log.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

```bash
# Install dependencies
uv sync

# Or via pnpm from repo root
pnpm install
```

## Development

```bash
# Run dev server
uv run fastapi dev app/main.py

# Or via pnpm from repo root
pnpm pdf:dev
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/extract` | Extract content from PDF |

## Usage

```bash
# Health check
curl http://localhost:8000/health

# Extract PDF
curl -X POST -F "file=@report.pdf" http://localhost:8000/extract
```
