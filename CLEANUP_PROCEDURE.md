# Procédure de nettoyage Cordée (archive historique)

> **Document historique, non validé comme procédure actuelle.** Il décrit une ancienne opération de nettoyage. Ne pas exécuter aveuglément les scripts Git mentionnés : `scripts/git_cleanup_procedure.sh` doit être relu et corrigé avant tout usage.
>
> Les « archétypes internes » désignent des modules **non exposés directement par des routes API**. Leurs dix définitions sont néanmoins **publiques dans le code source de ce dépôt**. Voir [README.md](README.md) pour le périmètre actuellement publié.


## Objectif

Purger toute référence Valexa-Nexus dans Cordée sans casser l'historique, et intégrer les nouveaux archétypes en logique interne uniquement.

## Structure créée

```
cordee/
├─ cordee/core/                    # Modules internes
│  ├─ archetypes_internal.py       # 10 archétypes (internes à l'application, mais source publique)
│  ├─ emotional_engine.py          # Moteur de priming interne
│  └─ __init__.py
├─ tests/                          # Tests unitaires
│  ├─ test_archetypes.py           # Suite complète de tests
│  └─ __init__.py
├─ scripts/                        # Outils de nettoyage
│  ├─ cleanup_valexa_refs.sh       # Recherche références Valexa
│  └─ git_cleanup_procedure.sh     # Procédure Git complète
├─ test_simple.py                  # Test rapide
├─ test_avance.py                  # Démonstration complète
└─ README.md                       # Documentation mise à jour
```

## Étapes de nettoyage

### 1. Recherche des références Valexa

```bash
./scripts/cleanup_valexa_refs.sh
```

### 2. Procédure Git complète

```bash
./scripts/git_cleanup_procedure.sh
```

### 3. Vérification manuelle

- ✅ Aucun endpoint n'expose le contenu des archétypes
- ✅ `archetypes_internal.py` en lecture seule (import interne uniquement)
- ✅ Tests/CI fonctionnels
- ⚠️ La recherche de références Valexa/Nexus est une tâche historique à revalider

## Usage interne du moteur

```python
# Dans l'engine Cordée-Authentic
from cordee.core.emotional_engine import archetype_priming, EmotionalState

# Priming interne sans exposition client
state = EmotionalState(conflict_level=0.8)
state = archetype_priming(state)
# → state.current_color, state.current_tone, state.tags mis à jour
```

## Points de validation

### ❌ À éviter (exposition publique)
- Endpoints retournant le contenu des archétypes
- Fichiers JSON/YAML avec données archétypales
- Routes `/archetype/content` ou similaires
- Variables d'environnement exposant des secrets archétypaux

### ✅ Acceptable (usage interne)
- Import `from cordee.core.archetypes_internal import get_archetype`
- Priming des couleurs/tonalités pour l'UI
- Tags d'alignement pour les features
- Tests unitaires du moteur

## Commit type

```bash
git commit -m "chore(cordee): internalize archetypes; remove public exposure"
```

## Notes importantes

- **Aucune exposition client** des données archétypales
- **Logique interne uniquement** pour le priming émotionnel
- **Tests complets** pour validation
- **Ready for engine integration** dans Cordée-Authentic
