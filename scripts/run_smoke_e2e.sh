#!/usr/bin/env bash
set -euo pipefail

# Local end-to-end: start API, wait for /health, run smoke test, cleanup

RAG_HOST=${RAG_HOST:-127.0.0.1}
RAG_PORT=${RAG_PORT:-8008}

# If port is busy, pick a free one
if python - "$RAG_PORT" >/dev/null 2>&1 <<'PY'
import socket, sys
s=socket.socket()
busy=0
try:
    s.bind(("127.0.0.1", int(sys.argv[1])))
except OSError:
    busy=1
finally:
    s.close()
sys.exit(busy)
PY
then
  : # ok (port free)
else
  RAG_PORT=$(python - <<'PY'
import socket
s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()
PY
  )
fi

# Default to offline mode for local smoke to avoid model downloads
export CORDEE_CI=${CORDEE_CI:-1}
export CHROMA_PATH=${CHROMA_PATH:-.chroma}

# Prefer venv binaries if available
export PATH=".venv/bin:$PATH"
export PYTHONPATH="src:${PYTHONPATH:-}"

# Ensure the port is free (best-effort)
if command -v fuser >/dev/null 2>&1; then
  fuser -k "${RAG_PORT}/tcp" >/dev/null 2>&1 || true
fi

FORCE_DUMMY_EMBED=1 CORDEE_CI=1 CHROMA_PATH="${CHROMA_PATH}" uvicorn rag_http:app --host "$RAG_HOST" --port "$RAG_PORT" &
PID=$!
trap 'kill $PID 2>/dev/null || true' EXIT

for i in {1..90}; do
  if curl -fsS "http://$RAG_HOST:$RAG_PORT/health" >/dev/null; then
    break
  fi
  sleep 1
done

bash scripts/smoke_rag.sh
