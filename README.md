# Cordée

[![CI](https://github.com/Djabolum/cordee/actions/workflows/ci.yml/badge.svg)](https://github.com/Djabolum/cordee/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Djabolum/cordee?logo=github)](https://github.com/Djabolum/cordee/releases)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Petit serveur RAG minimal (ChromaDB + FastAPI + fastembed) pensé pour tourner sur un Pi, avec unités systemd et tests de fumée.

---

## 🌿 Cordée → Cordée-Authentic

### 📖 Contexte

- **Cordée** est le squelette open-source initial : un petit serveur RAG minimal, basé sur FastAPI + ChromaDB.  
- **Cordée-Authentic** est son évolution commerciale : un moteur d'analyse émotionnelle (texte, audio, bientôt vidéo) conçu pour détecter la sincérité dans les échanges humains.

---

### 🚀 Évolution du projet

#### ✅ Déjà réalisé

- Archétypes internes (propre à Cordée)
- API FastAPI (text/audio)
- Intégration Stripe (abonnements B2C/B2B)
- Frontend React minimal (recording, scoring, feedback)
- Respect RGPD (pas de stockage brut)

#### 🛠️ En cours

- Tests API (texte + audio)
- Dashboard simple pour coachs / RH
- Première mise en ligne (démo cloud)

#### 📅 À venir

- Phase 2 : analyse vidéo (micro-expressions, posture)
- Phase 3 : API publique (apps tierces)
- Phase 4 : extensions (Zoom/Teams, batch médias)
- Phase 5 : internationalisation (EN/ES)

---

### 💳 Tarifs (Cordée-Authentic Phase 1)

- Grand public (auto-coaching) : 14,99€/mois
- B2C (coaching individuel / coachs) : 39€/mois
- B2B (RH / bien-être) : 179€/mois (50 utilisateurs inclus)
- Politique / Médias : 9,99€/analyse unitaire
- Entreprise : devis personnalisé

---

### 🤝 Soutenir le projet

Cordée-Authentic est en partie sponsorisé par la communauté.  
En devenant sponsor GitHub, vous soutenez le développement d'une IA éthique qui replace la **sincérité** au cœur de nos échanges.  

👉 [💜 Devenir sponsor](https://github.com/sponsors/Djabolum)

---

## Pourquoi "Cordée" ?
Clin d'œil aux Cordée en Haute‑Savoie 😉

## Licence
Par défaut **Apache‑2.0**. Tu peux basculer vers **MIT** tant qu'il n'y a pas encore de contributions externes.

---

## Prérequis
- Python 3.11
- `systemd`
- Accès Internet au premier lancement (téléchargement du modèle d'embedding)

## Installation locale (dev)

```bash
git clone https://github.com/Djabolum/cordee.git cordee
cd cordee
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Option Makefile (installe aussi ruff/black/pytest/pytest-cov)
make dev

# Lancer le serveur en dev
python src/rag_http.py

# Vérifier la santé
curl -fsS http://127.0.0.1:8008/health
```

Alternative avec uvicorn (reload en dev) :
```bash
uvicorn src.rag_http:app --host 127.0.0.1 --port 8008 --reload
```

## Installation production

Installation sous /opt/valexa :
```bash
sudo mkdir -p /opt/valexa && sudo chown -R $USER:$USER /opt/valexa
rsync -a --delete ./ /opt/valexa/
cd /opt/valexa
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Secrets / variables d'environnement :
```bash
# RAG
sudo cp systemd/valexa-rag.env.example /etc/default/valexa-rag
sudo nano /etc/default/valexa-rag
```

Unités systemd :
```bash
sudo cp systemd/valexa-rag.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now valexa-rag.service
```

Test rapide ("smoke test") :
```bash
chmod +x scripts/smoke_rag.sh
./scripts/smoke_rag.sh
```

## API

- GET `/health`
  - Réponse: `{ "ok": true, "collection": "...", "model": "..." }`

- POST `/upsert`
  - Corps: `{ "ids": [...], "documents": [...], "metadatas": [...] }`
  - Réponse: `{ "ok": true, "n": <int> }`

- POST `/query`
  - Corps: `{ "query": "salut monde", "n_results": 2 }`
  - Réponse: `{ "ok": true, "result": { "ids": [[...]], "documents": [[...]], ... } }`

### Endpoints Priming Émotionnel (Extension)

Si le moteur émotionnel est installé (`emotional_engine.py`), les endpoints suivants sont disponibles :

**Configuration requise :**
```bash
# Activer le moteur émotionnel
export EMOTIONAL_ENGINE_ENABLED=true
```

**Endpoints principaux :**

- **GET** `/ritual/library` - Bibliothèque des archétypes
- **POST** `/ritual/execute` - Exécuter un priming
- **POST** `/ritual/complete` - Compléter session priming
- **GET** `/emotional/profile/{user_id}` - Profil émotionnel utilisateur
- **POST** `/emotional/state` - Mise à jour état émotionnel
- **GET** `/ritual/active` - Sessions de priming en cours
- **GET** `/health/full` - Health check étendu

**Usage interne du moteur émotionnel :**

```python
# cordee/core/emotional_engine.py (extrait d'implémentation)
from .rituals_internal import RITUALS, get_ritual

def archetype_priming(state):
    """
    Sélection interne d'un archétype de priming selon l'état courant.
    Aucune donnée archétypale n'est renvoyée au client.
    """
    # Exemple simple (à raffiner plus tard) :
    if state.user_signal == "start": 
        r = get_ritual("fil_daube")
    elif state.conflict_level > 0.7:
        r = get_ritual("pont_silencieux")
    elif state.voice_shakiness > 0.5:
        r = get_ritual("voix_nue")
    else:
        r = get_ritual("racine_calme")

    state.apply_color(r.color_hex)       # interne: modulation UI/intensity
    state.apply_tone(r.note_hz)          # interne: régulateur audio/feedback
    state.tag("arch", r.archetype)       # interne: features d'alignement
    # On n'expose ni `inner_note` ni `edge` ni `call` au client
    return state
```

**Exemples d'utilisation d'API :**

```bash
# Lister tous les rituels
curl http://127.0.0.1:8008/ritual/library

# Exécuter priming de base
curl -X POST http://127.0.0.1:8008/ritual/execute \
  -H "Content-Type: application/json" \
  -d '{"ritual_name": "ce_qui_est_la", "user_id": "test_user"}'

# Mettre à jour état émotionnel
curl -X POST http://127.0.0.1:8008/emotional/state \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "current_emotions": ["anxieux", "stressé"]}'
```

## Ingestion locale

Créer une mémoire locale (notes, exports) et l'indexer en chunks traçables :

```bash
# Installation dépendances ingestion
pip install -r requirements-ingest.txt

# Exemple minimal
python ingest.py --root rituels --api http://127.0.0.1:8008

# Avec tags et cas (recommandé)
python ingest.py --root archetyps --api http://127.0.0.1:8008 --tag archetype --case famille-2025

# Dry-run (aperçu sans envoi)
python ingest.py --root rituels --api http://127.0.0.1:8008 --dry-run

# Aide avec exemples détaillés
python ingest.py --examples
```

**Script d'aide interactif :**
```bash
chmod +x scripts/ingest_examples.sh
./scripts/ingest_examples.sh interactive
```

**Formats supportés :**
- Notes: `.txt`, `.md` (avec extraction titre/participants/tags)
- Documents: `.pdf`, `.docx`, `.html`
- Chats: `.json` (Telegram), `.csv` (SMS), `.zip` (WhatsApp)
- Emails: `.eml`, `.mbox`

## Génération de documentation

Convertir la documentation Markdown en formats bureautiques :

```bash
# Installation dépendances
pip install python-docx odfpy

# Génération DOCX/ODT
python build_docs.py README.md

# Génération avec répertoire personnalisé
python build_docs.py --out docs/exports README.md

# Via Makefile
make docs          # README seulement
make docs-all      # Documentation complète
```

## Variables utiles
- `FASTEMBED_MODEL` : modèle d'embedding (par défaut : `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`).
- `CHROMA_PATH` : chemin du store Chroma (défaut `/opt/cordee/index`).
- `RAG_HOST` / `RAG_PORT` : interface/port HTTP (défaut `127.0.0.1:8008`).
- `HF_HOME` / `HUGGINGFACE_HUB_CACHE` : caches modèles HF.
- `EMOTIONAL_ENGINE_ENABLED` : active les endpoints de priming (défaut `false`).

### Arborescence
```
cordee/
├─ src/                # code applicatif (FastAPI + Chroma + fastembed)
│  ├─ rag_http.py      # serveur principal RAG
│  └─ emotional_engine.py  # moteur de priming (extension publique)
├─ cordee/             # modules core internes
│  └─ core/           # archétypes internes
│     ├─ __init__.py
│     ├─ archetypes_internal.py  # 10 archétypes core (privés)
│     └─ emotional_engine.py  # moteur de priming interne
├─ systemd/            # unités & exemples d'env
├─ scripts/            # smoke tests + outils
├─ tests/              # tests unitaires
├─ requirements.txt    # dépendances Python de base
├─ requirements-ingest.txt  # dépendances ingestion
├─ ingest.py          # script d'ingestion locale
├─ build_docs.py      # générateur de documentation
└─ README.md          # cette documentation
```

## Contrib (pre-commit)

```bash
# via Makefile
make hooks

# ou manuellement
pip install pre-commit && pre-commit install
pre-commit run -a
```

Hooks actifs : Ruff (avec `--fix`) et Black (versions alignées avec la CI).

## Sécurité
- Aucun secret en dépôt. Les fichiers `*.env.example` documentent quoi mettre dans `/etc/default/*`.
- **Le dépôt GitHub contient uniquement le squelette Cordée** (core RAG), pas les applications privées.
- **Les installations locales** restent sur votre système et sont protégées par `.gitignore`.

---

Notes CI:
- Les tests CI tournent en mode offline avec `CORDEE_CI=1` et `CHROMA_PATH=.chroma`.
- La configuration `pytest.ini` ajoute `src` au chemin Python et limite les tests au dossier `tests`.

Changelog: voir CHANGELOG.md

Bon vol ✌️

## Tests

Tests locaux (offline, sans téléchargement de modèles) :
```bash
# Tests de base du serveur RAG
CORDEE_CI=1 pytest -q

# Avec rapport de couverture (aligné CI, seuil 70%)
CORDEE_CI=1 pytest -q \
  --cov=src --cov=tests --cov-report=term-missing \
  --cov-report=xml:coverage.xml --cov-fail-under=70

# Test rapide des archétypes internes
python test_simple.py

# Tests des rituels internes complets
python tests/test_archetypes_internal.py

# Tests complets avec moteur émotionnel
EMOTIONAL_ENGINE_ENABLED=true pytest tests/
```

**Tests du système de priming :**
- Validation des 10 archétypes core
- Immutabilité des structures de données
- Moteur de priming émotionnel interne (aucune exposition client)
- Sélection contextuelle par état émotionnel
- Intégration ChromaDB pour persistence
- **Aucune exposition publique des archétypes** (logique interne uniquement)
- **Priming UI/audio** : couleur, tonalité, tags d'alignement

**Test rapide :**
```bash
# Vérification basique du module archétypes
python test_simple.py
```