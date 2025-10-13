# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Ce fichier suit librement les principes de Keep a Changelog et le versionnage SemVer.

## [v0.2.0] - 2025-09-15

- Ajouts
  - Cible Makefile `ci-local` qui enchaîne lint (ruff), format check (black), tests offline avec couverture (≥70%), puis e2e (smoke).
  - Workflow GitHub Actions `ci-local` (workflow_dispatch + push sur branche `ci-local`), compatible `act`.

- Changements
  - Script `scripts/run_smoke_e2e.sh` plus robuste: lance `uvicorn` avec `PYTHONPATH=src`, sélectionne un port libre, force l’embedder dummy et le mode offline.
  - API `src/rag_http.py`: lecture dynamique du mode CI via l’environnement, désactivation de la télémétrie Chroma par défaut, support des variables `CHROMA_*` en plus des historiques `RAG_*`.
  - Exemple d’environnement systemd mis à jour pour préférer `CHROMA_*`.

- Qualité / DX
  - Résolution de conflits Makefile + harmonisation des cibles.
  - Lint/format appliqués; tests passent localement avec ~85% de couverture.

- Notes
  - Aucun changement de comportement en mode en ligne “classique”. Le mode offline + dummy n’est activé qu’en CI/e2e.
  - PR associée: #15.

[v0.2.0]: https://github.com/Djabolum/cordee/releases/tag/v0.2.0

