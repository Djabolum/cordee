#!/usr/bin/env bash
set -euo pipefail
HOST=${RAG_HOST:-127.0.0.1}
PORT=${RAG_PORT:-8008}
BASE="http://$HOST:$PORT"

fail(){ echo "❌ $*"; exit 1; }
ok(){ echo "✅ $*"; }

# 1) health
HJSON=$(curl -sS --fail "$BASE/health") || fail "health KO (service down ?)"
echo "$HJSON" | grep -q '"ok": *true' || fail "health ne renvoie pas ok:true"
ok "health OK ($(echo "$HJSON" | tr -d '\n'))"

# 2) upsert
UJSON=$(curl -sS --fail -X POST "$BASE/upsert"   -H 'content-type: application/json'   -d '{"ids":["a1","a2"],"documents":["bonjour le monde","la montagne en savoie"],"metadatas":[{"lang":"fr"},{"lang":"fr"}]}')   || fail "upsert KO"
echo "$UJSON" | grep -q '"ok": *true' || fail "upsert KO"
ok "upsert OK ($(echo "$UJSON" | tr -d '\n'))"

# 3) query
QJSON=$(curl -sS --fail -X POST "$BASE/query" \
  -H 'content-type: application/json' \
  -d '{"query":"salut monde","n_results":2}') \
  || fail "query KO"
# The /query endpoint returns raw Chroma response (ids/documents/etc.), not {ok:true}
echo "$QJSON" | grep -q '"ids"' || fail "query ne contient pas 'ids'"
echo "$QJSON" | grep -q '"documents"' || fail "query ne contient pas 'documents'"
ok "query OK ($(echo "$QJSON" | tr -d '\n' | cut -c1-160)...)"

echo "🎉 Smoke test terminé."
