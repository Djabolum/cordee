# Cordée

[![CI](https://github.com/Djabolum/cordee/actions/workflows/ci.yml/badge.svg)](https://github.com/Djabolum/cordee/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Djabolum/cordee?logo=github)](https://github.com/Djabolum/cordee/releases)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**Dépôt public d'une implémentation historique et expérimentale de Cordée.** Il contient principalement un petit serveur RAG (FastAPI, ChromaDB et fastembed), des tests et des exemples de services systemd. Il ne représente **ni l'ensemble de l'écosystème AI-ZI-ME, ni l'état actuel des services Cordée en production**.

Ce dépôt documente ce qui est effectivement présent dans son code. Les modules de recherche, d'observation, de mémoire et d'interaction développés ailleurs ne doivent pas être déduits de ce squelette.

## Fonctionnalités présentes

- **API RAG** dans `src/rag_http.py` : ajout de documents, recherche par embeddings et contrôle de santé.
- **Persistance locale** avec ChromaDB ; modèle d'embedding fastembed téléchargé au premier usage réel.
- **Mode de tests hors ligne** (`CORDEE_CI=1`), avec embeddings factices et déterministes. Il valide des chemins techniques, **pas la pertinence sémantique**.
- **Tests, scripts de vérification et CI** pour ce périmètre limité.
- **Exemples systemd** conservés pour référence ; chemins et utilisateurs historiques à adapter avant tout déploiement.

### Modules d'archétypes (expérimentaux et séparés)

Deux modules Python sont effectivement inclus :

- `cordee/core/archetypes_internal.py` définit **10 archétypes** et une fonction de recherche.
- `cordee/core/emotional_engine.py` sélectionne un archétype à partir d'un état d'entrée et applique des paramètres symboliques (couleur, tonalité et étiquettes).

Ces modules **ne constituent pas un moteur de rituels complet** et ne sont **pas intégrés à l'API RAG** de `src/rag_http.py`. Aucun endpoint `/ritual/*`, `/archetype/*` ou `/emotional/*` n'est défini par le serveur de ce dépôt.

Le mot « internal » désigne ici l'usage dans le code, **pas la confidentialité** : les définitions des archétypes sont publiques dans ce dépôt. Ce prototype ne démontre ni détection fiable des émotions, ni authenticité émotionnelle mesurable.

## Installation locale

Prérequis : Python 3.11 ou compatible, `pip` et un environnement Unix pour les commandes ci-dessous. Aucun service systemd n'est nécessaire pour tester localement.

```bash
git clone https://github.com/Djabolum/cordee.git
cd cordee
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Démarrer en mode hors ligne (test)

```bash
CORDEE_CI=1 CHROMA_PATH=.chroma python src/rag_http.py
```

Le serveur écoute par défaut sur `127.0.0.1:8008`. Dans ce mode, les vecteurs factices ne permettent **pas** de vérifier la qualité d'une recherche sémantique.

Dans un autre terminal :

```bash
curl -fsS http://127.0.0.1:8008/health
```

### Démarrer avec un véritable modèle d'embedding

```bash
CHROMA_PATH=.chroma python src/rag_http.py
```

Cette commande peut télécharger un modèle au premier lancement ; elle nécessite alors un accès réseau et suffisamment de ressources. Elle n'est pas un déploiement prêt pour la production.

## API RAG disponible

| Méthode | Route | Usage |
| --- | --- | --- |
| GET | `/health` | Renvoie l'état minimal, le nom de la collection et le modèle |
| POST | `/upsert` | Ajoute des documents avec identifiants et métadonnées facultatives |
| POST | `/query` | Recherche les documents les plus proches d'une requête |

Exemple local (avec le serveur démarré) :

```bash
curl -X POST http://127.0.0.1:8008/upsert \
  -H 'Content-Type: application/json' \
  -d '{"ids":["demo-1"],"documents":["Bonjour Cordée"],"metadatas":[{"source":"demo"}]}'

curl -X POST http://127.0.0.1:8008/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"Bonjour","n_results":1}'
```

`/upsert` renvoie notamment `{"ok": true, "n": 1}` ; `/query` renvoie un objet `result` contenant les résultats ChromaDB.

## Tests et contributions

```bash
# Installer les outils de développement et lancer les contrôles locaux
make ci-local

# Tests unitaires hors ligne (après installation des outils de test)
CORDEE_CI=1 CHROMA_PATH=.chroma pytest -q

# Démonstration isolée des archétypes
python test_simple.py
```

La cible `make ci-local` applique un seuil de couverture de **70 %**. Le workflow GitHub Actions principal produit un rapport de couverture, mais **ne fait pas respecter ce seuil** dans sa configuration actuelle. Les résultats d'exécution doivent être vérifiés dans les runs CI ; la présence de scripts ne vaut pas validation.

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour participer et [CHANGELOG.md](CHANGELOG.md) pour les évolutions historiques.

## Configuration et précautions de sécurité

Variables principales :

| Variable | Rôle |
| --- | --- |
| `CORDEE_CI` | Active le mode de tests et les embeddings factices |
| `CHROMA_PATH` | Chemin du stockage ChromaDB |
| `CHROMA_COLLECTION` | Nom de la collection |
| `FASTEMBED_MODEL` | Modèle d'embedding utilisé hors mode CI |
| `RAG_HOST` / `RAG_PORT` | Adresse et port du serveur (par défaut `127.0.0.1:8008`) |

**Attention :** les routes `/upsert` et `/query` ne comportent **aucune authentification dans ce code**. Ne pas exposer directement ce serveur sur Internet ou sur un réseau non fiable. Un usage au-delà du laboratoire exige des contrôles d'accès, une limitation de débit, une gestion des données et une revue de sécurité adaptés.

Les unités du dossier `systemd/` sont des exemples historiques, **pas une procédure de mise en production validée**. Les adapter aux chemins, comptes et permissions de l'environnement cible.

Pour signaler une vulnérabilité, voir [SECURITY.md](SECURITY.md).

## Périmètre non inclus

Ce dépôt ne fournit pas d'interface React, d'analyse vocale ou vidéo en temps réel, de système de facturation, d'abonnements, de moteur de rituels complet ni de pipeline d'ingestion documentaire décrit comme un produit utilisable. Il ne constitue pas à lui seul une preuve de conformité réglementaire ou de sûreté pour des usages sensibles.

## Licence

Code publié sous [Apache License 2.0](LICENSE). Consulter aussi [NOTICE](NOTICE).

---

## English overview

**Cordée (this repository)** is a historical, experimental FastAPI + ChromaDB + fastembed RAG server, **not** the current AI-ZI-ME / Cordée production platform.

- Implemented endpoints: `GET /health`, `POST /upsert`, `POST /query`.
- Local test mode: `CORDEE_CI=1` uses deterministic dummy embeddings (not meaningful semantic retrieval).
- Ten experimental archetype definitions and a small selection module are present under `cordee/core/`. Their source code is public; they are **not connected** to the RAG API.
- No ritual endpoints, speech/video analysis, React interface, Stripe integration or subscription service are implemented in this repository.
- The RAG endpoints have no built-in authentication. Run locally only unless adequate access controls are independently implemented and verified.

For local setup, API examples, tests and security limitations, see the French sections above. License: Apache-2.0.
