# Contributing

Merci ! Quelques règles simples :

- Discutez une feature via issue avant une grosse PR.
- Ouvrez des PR petites, testées, décrites.
- Lint: `ruff check .` – Format: `black .`

## Dev rapide
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff==0.6.9 black==24.8.0 pytest==8.3.2 pytest-cov==5.0.0
make dev   # lance l'API en local (uvicorn ou script)
```

## Tests & CI locale
Tests unitaires offline (sans téléchargement de modèles) avec couverture:
```bash
CORDEE_CI=1 pytest -q \
  --cov=src --cov=tests --cov-report=term-missing \
  --cov-report=xml:coverage.xml --cov-fail-under=70
```

CI locale tout-en-un (lint + format check + tests + e2e smoke):
```bash
make ci-local
```

Astuce: pour rejouer l’e2e seulement:
```bash
bash scripts/run_smoke_e2e.sh
```

## Pre-commit
Activez les hooks pour aligner local et CI:
```bash
pip install pre-commit && pre-commit install
# ou via Makefile
make hooks
```

## Branches, PRs et release
- Branche principale: `main` (protégée; exiger CI + 1 review recommandé).
- Convention: petites PRs, description claire, tests inclus.
- Releases: tags `v*` (ajoutez une règle de protection des tags `v*` côté GitHub).
