.PHONY: help install dev lint fmt test run smoke pack

help:
	@echo "Targets: install dev lint fmt test run smoke pack"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt || true

dev: install
	pip install ruff==0.6.9 black==24.8.0 pytest==8.3.2

lint:
	ruff check .

fmt:
	black .

test:
	@if [ -d tests ]; then pytest -q; else echo "no tests/ directory"; fi

run:
	python -m uvicorn rag_http:app --host 127.0.0.1 --port 8008

smoke:
	bash scripts/smoke_rag.sh

pack:
	tar -czf cordee-$(shell date +%F).tgz .
