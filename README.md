# Cordée

[![CI](https://github.com/Djabolum/cordee/actions/workflows/ci.yml/badge.svg)](https://github.com/Djabolum/cordee/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/Djabolum/cordee)](https://github.com/Djabolum/cordee/releases) [![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Petit serveur RAG minimal (ChromaDB + FastAPI + fastembed) pensé pour tourner sur un Pi, avec unités systemd et tests de fumée.

## Pourquoi “Cordée” ?
Clin d’œil aux Cordée en Haute‑Savoie 😉

## Licence
Par défaut **Apache‑2.0** (https://img.shields.io/badge/License-Apache_2.0-blue.svg). Tu peux basculer vers **MIT** tant qu’il n’y a pas encore de contributions externes (voir section *Changer de licence* ci‑dessous).

---

## Prérequis
- Python 3.11
- `systemd`
- Accès Internet au premier lancement (téléchargement du modèle d’embedding)

## Installation locale (dev)
Installation rapide (dev local) :
```bash
git clone https://github.com/Djabolum/cordee.git cordee
cd cordee
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Lancer le serveur en dev
python src/rag_http.py

# Vérifier la santé
curl -fsS http://127.0.0.1:8008/health
```

Alternative : installation sous /opt/valexa (voir le bloc juste en dessous).
```bash
sudo mkdir -p /opt/valexa && sudo chown -R $USER:$USER /opt/valexa
rsync -a --delete ./ /opt/valexa/
cd /opt/valexa
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Secrets / variables d’environnement :
```bash
# RAG
sudo cp systemd/valexa-rag.env.example /etc/default/valexa-rag
sudo nano /etc/default/valexa-rag

# Codex (si tu utilises aussi codex.service)
sudo cp systemd/codex.env.example /etc/default/codex
sudo nano /etc/default/codex
```

3) Unités systemd :
```bash
sudo cp systemd/valexa-rag.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now valexa-rag.service

# Optionnel : Codex
sudo cp systemd/codex.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now codex.service
```

4) Test rapide (“smoke test”)
```bash
chmod +x scripts/smoke_rag.sh
./scripts/smoke_rag.sh
```

### Arborescence
```
cordee/
├─ src/                # code applicatif (FastAPI + Chroma + fastembed)
├─ systemd/            # unités & exemples d'env
├─ scripts/            # smoke tests
├─ data/               # (optionnel) dossier pour index local si tu ne veux pas /opt/valexa/index
├─ requirements.txt
└─ README.md
```

## Variables utiles
- `FASTEMBED_MODEL` : modèle d’embedding (par défaut : `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`).
- `RAG_INDEX_PATH` : chemin du store Chroma (défaut `/opt/valexa/index`).
- `RAG_HOST` / `RAG_PORT` : interface/port HTTP (défaut `127.0.0.1:8008`).
- `HF_HOME` / `HUGGINGFACE_HUB_CACHE` : caches modèles HF.

## Changer de licence plus tard ?
- **Oui tant qu’il n’y a pas de contributions externes** (tu es le seul ayant‑droit). Après contributions, il faut leur accord ou un CLA.
- Pour simplifier, garde **Apache‑2.0** (solide juridiquement, inclut une *patent grant*). Si tu préfères le plus court possible, passe à **MIT**.

## Sécurité
- Aucun secret en dépôt. Les fichiers `*.env.example` documentent quoi mettre dans `/etc/default/*`.
- Pense à limiter l’écoute sur `127.0.0.1` si le service n’est pas exposé.

---

Bon vol ✌️
