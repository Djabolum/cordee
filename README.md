# Cordée

[![CI](https://github.com/Djabolum/cordee/actions/workflows/ci.yml/badge.svg)](https://github.com/Djabolum/cordee/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)


Petit serveur RAG minimal (ChromaDB + FastAPI + fastembed) pensé pour tourner sur un Pi, avec unités systemd et tests de fumée.

## Pourquoi “Cordée” ?
Clin d’œil aux Cordée en Haute‑Savoie 😉

## Licence
Par défaut **Apache‑2.0** (brevet + clause de contribution). Tu peux basculer vers **MIT** tant qu’il n’y a pas encore de contributions externes (voir section *Changer de licence* ci‑dessous).

---

## Prérequis
- Python 3.11
- `systemd`
- Accès Internet au premier lancement (téléchargement du modèle d’embedding)

## Installation locale (dev)
```bash
git clone <TON_URL_REPO> cordee && cd cordee
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Lancer en dev
python src/rag_http.py
# Santé
curl -fsS http://127.0.0.1:8008/health
```

Commande e2e locale (serveur + smoke):
```bash
chmod +x scripts/run_smoke_e2e.sh
RAG_HOST=127.0.0.1 RAG_PORT=8008 ./scripts/run_smoke_e2e.sh
```

## Déploiement système (prod légère sur Pi)
1) Copier le dépôt dans **/opt/valexa** (chemin utilisé par les unités) :
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

### Proxy Caddy (exemple)
Fichier d’exemple: `deploy/Caddyfile.example`
```caddy
your.domain.tld {
  encode zstd gzip
  reverse_proxy 127.0.0.1:8008
}
```

### Arborescence
```
cordee/
├─ .github/
│  └─ workflows/
│     └─ ci.yml       # workflow CI (smoke e2e)
├─ deploy/
│  └─ Caddyfile.example  # reverse proxy example
├─ src/                # code applicatif (FastAPI + Chroma + fastembed)
├─ systemd/            # unités & exemples d'env
├─ scripts/            # smoke tests + e2e
│  ├─ smoke_rag.sh
│  └─ run_smoke_e2e.sh
├─ data/               # (optionnel) dossier pour index local si tu ne veux pas /opt/valexa/index
├─ Makefile            # cibles: venv, dev, smoke, e2e
├─ requirements.txt
├─ LICENSE
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

## Dépannage

### Erreur « gh: command not found »
- Cause: la CLI GitHub (gh) n’est pas installée. Cordée n’en a pas besoin nativement, mais tes scripts/CI peuvent l’utiliser.
- Solutions:
  - Local (Debian/Ubuntu):
    ```bash
    sudo apt update
    sudo apt install -y curl ca-certificates gnupg
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update
    sudo apt install -y gh
    ```
  - Local (macOS avec Homebrew):
    ```bash
    brew install gh
    ```
  - CI GitHub Actions (job Ubuntu):
    ```yaml
    - name: Install GitHub CLI
      run: |
        sudo apt-get update
        sudo apt-get install -y gh
    ```
  - Alternative: remplace les appels à `gh` par des commandes `git` ou appels API si possible.

Bon vol ✌️
