# Contributing

Merci ! Quelques règles simples :

- Discutez une feature via issue avant une grosse PR.
- Ouvrez des PR petites, testées, décrites.
- Lint: `ruff check .` – Format: `black .`

## Dev rapide
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ruff black pytest
make run   # lance l'API en local
```

## Tests
```bash
pytest -q   # s'il y a un dossier tests/
```
