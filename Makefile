
.PHONY: help venv install dev lint fmt test smoke e2e ci-local pack hooks
.DEFAULT_GOAL := help

PY ?= python
RAG_HOST ?= 127.0.0.1
RAG_PORT ?= 8008

# Ensure venv binaries are preferred
export PATH := .venv/bin:$(PATH)
help:
	@echo "Targets:"
	@echo "  venv        Create venv and install deps"
	@echo "  install     Install dev tools (ruff, black, pytest)"
	@echo "  dev         Run dev server (RAG_HOST=$(RAG_HOST) RAG_PORT=$(RAG_PORT))"
	@echo "  lint        Ruff lint"
	@echo "  fmt         Black format"
	@echo "  test        Run pytest"
	@echo "  smoke       Run smoke test against a running server"
	@echo "  e2e         Start server then run smoke test"
	@echo "  ci-local    Lint + tests (offline) + e2e"
	@echo "  pack        Tarball the repo"
	@echo "  hooks       Install pre-commit hooks"

venv:
	@if [ ! -d .venv ]; then \
		$(PY) -m venv .venv; \
	fi
	@. .venv/bin/activate && pip install -r requirements.txt

install: venv
	@. .venv/bin/activate && pip install \
		ruff==0.6.9 black==24.8.0 pytest==8.3.2 pytest-cov==5.0.0

dev: install
	@echo "Starting dev server on $(RAG_HOST):$(RAG_PORT)"
	RAG_HOST=$(RAG_HOST) RAG_PORT=$(RAG_PORT) python src/rag_http.py

lint:
	ruff check .

fmt:
	black .

test:
	@if [ -d tests ]; then pytest -q; else echo "no tests/ directory"; fi

smoke:
	RAG_HOST=$(RAG_HOST) RAG_PORT=$(RAG_PORT) bash scripts/smoke_rag.sh

e2e: install
	RAG_HOST=$(RAG_HOST) RAG_PORT=$(RAG_PORT) bash scripts/run_smoke_e2e.sh

ci-local: install
	ruff check .
	black --check .
	CORDEE_CI=1 CHROMA_PATH=.chroma pytest -q --maxfail=1 --disable-warnings \
	  --cov=src --cov=tests --cov-report=term-missing \
	  --cov-report=xml:coverage.xml --cov-fail-under=70
	RAG_HOST=$(RAG_HOST) RAG_PORT=$(RAG_PORT) bash scripts/run_smoke_e2e.sh

pack:
	tar -czf cordee-$(shell date +%F).tgz .

# Install git hooks for lint/format (pre-commit)
hooks:
	@command -v pre-commit >/dev/null 2>&1 || pip install pre-commit
	pre-commit install
