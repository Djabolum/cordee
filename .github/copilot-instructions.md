# GitHub Copilot Instructions for Cordée

## Project Overview

Cordée is a minimal RAG (Retrieval-Augmented Generation) server built with ChromaDB, FastAPI, and fastembed. It's designed to run efficiently on a Raspberry Pi, with systemd units and smoke tests.

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: ChromaDB (vector database)
- **Embeddings**: fastembed (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- **Testing**: pytest with pytest-cov
- **Linting**: Ruff 0.6.9
- **Formatting**: Black 24.8.0

## Development Setup

### Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff==0.6.9 black==24.8.0 pytest==8.3.2 pytest-cov==5.0.0
make dev  # or: python src/rag_http.py
```

### Pre-commit Hooks
Always install pre-commit hooks before making changes:
```bash
make hooks
# or: pip install pre-commit && pre-commit install
```

## Code Standards

### Style & Linting
- **Always run linting** before committing: `ruff check .`
- **Always format code** with Black: `black .`
- Ruff runs with `--fix` in pre-commit hooks
- Follow existing code style and patterns in the repository

### Testing Requirements
- **Minimum coverage**: 70% (enforced in CI)
- **CI mode**: Tests run in offline mode with `CORDEE_CI=1` to avoid downloading models
- Run tests locally: `CORDEE_CI=1 pytest -q`
- Run tests with coverage:
  ```bash
  CORDEE_CI=1 pytest -q \
    --cov=src --cov=tests --cov-report=term-missing \
    --cov-report=xml:coverage.xml --cov-fail-under=70
  ```

### CI Workflow
Run the full CI suite locally before pushing:
```bash
make ci-local  # Runs lint + format check + tests + e2e smoke tests
```

## Architecture Guidelines

### Code Organization
- `src/`: Application code (FastAPI endpoints, ChromaDB integration)
- `tests/`: Unit and integration tests
- `scripts/`: Smoke tests and utilities
- `systemd/`: Service units and environment file examples
- `data/`: Optional local index directory

### Key Components
- **rag_http.py**: Main FastAPI application with health, upsert, and query endpoints
- **CI Mode**: Uses `EphemeralClient` instead of `PersistentClient` for offline testing
- **Environment Variables**:
  - `CORDEE_CI=1`: Enable CI/offline mode
  - `CHROMA_PATH`: ChromaDB storage path (default: `/opt/cordee/index`)
  - `CHROMA_COLLECTION`: Collection name (default: `cordee`)
  - `FASTEMBED_MODEL`: Embedding model name
  - `RAG_HOST`/`RAG_PORT`: Server configuration (default: 127.0.0.1:8008)

### Design Patterns
- **Lazy initialization**: Singletons for client, collection, and embedder
- **CI-aware code**: `ci_mode()` function to detect test environment
- **Dummy embedder**: Deterministic embeddings for offline testing
- **Legacy env support**: Maintains backward compatibility with older env var names

## Best Practices

### Making Changes
1. **Small, focused PRs**: Discuss features via issues before large PRs
2. **Test coverage**: Include tests with all changes
3. **Clear descriptions**: Explain what and why in PR descriptions
4. **Pre-commit checks**: Ensure hooks pass before pushing

### Branch Strategy
- **Main branch**: `main` (protected, requires CI + review)
- **Feature branches**: Create from `main`
- **Release tags**: Use `v*` format (protected tags)

### Security
- **No secrets in repo**: Use environment files (`/etc/default/*`)
- **Local binding**: Default to `127.0.0.1` for security
- **Environment examples**: Provide `*.env.example` files for documentation

## Common Tasks

### Running the Server
```bash
# Development server
make dev
# or: python src/rag_http.py
# or: uvicorn src.rag_http:app --host 127.0.0.1 --port 8008 --reload

# Check health
curl -fsS http://127.0.0.1:8008/health
```

### Testing
```bash
# Quick test
CORDEE_CI=1 pytest -q

# With coverage
CORDEE_CI=1 pytest -q --cov=src --cov=tests --cov-report=term-missing

# E2E smoke test
make e2e
```

### Linting & Formatting
```bash
make lint  # ruff check .
make fmt   # black .
```

## Contributing Guidelines

See `CONTRIBUTING.md` for detailed contribution guidelines. Key points:
- Install pre-commit hooks (`make hooks`)
- Run CI locally before pushing (`make ci-local`)
- Keep PRs small and well-tested
- Follow existing code patterns and style

## License

Apache-2.0 (see LICENSE file)
