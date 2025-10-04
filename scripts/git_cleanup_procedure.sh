#!/bin/bash
# Procédure de nettoyage
# 6. Tests rapides
echo "6️⃣ Vérification des tests..."
python test_simple.py
python tests/test_archetypes.py

# 7. Commit atomique
echo "7️⃣ Commit des changements..."
git commit -m "chore(cordee): internalize archetypes; remove public exposure

- Add archetypes_internal.py with 10 emotional archetypes (internal use only)
- Add emotional_engine.py for internal priming logic
- Add comprehensive test suite
- Update README with internal usage examples
- No public API exposure of archetype content
- Ready for engine integration"pre (Cordée)
# Usage: ./scripts/git_cleanup_procedure.sh

set -e

echo "🔧 Procédure de nettoyage Git pour Cordée"
echo "=========================================="

# 1. Créer la branche de correction
echo "1️⃣ Création de la branche de correction..."
git checkout -b chore/rituals-internalize-cordee || echo "Branche déjà existante"

# 2. Ajouter les modules internes
echo "2️⃣ Ajout des modules internes..."
mkdir -p cordee/core
git add cordee/core/archetypes_internal.py
git add cordee/core/emotional_engine.py
git add cordee/core/__init__.py

# 3. Ajouter les tests
echo "3️⃣ Ajout des tests..."
git add tests/test_archetypes.py
git add tests/__init__.py

# 4. Ajouter les scripts de test
echo "4️⃣ Ajout des scripts de démonstration..."
git add test_simple.py
git add test_avance.py

# 5. Mise à jour de la documentation
echo "5️⃣ Mise à jour de la documentation..."
git add README.md

# 6. Tests rapides
echo "6️⃣ Vérification des tests..."
python test_simple.py
python tests/test_rituals.py

# 7. Commit atomique
echo "7️⃣ Commit des changements..."
git commit -m "chore(cordee): internalize archetypal rituals; remove public exposure

- Add rituals_internal.py with 10 archetypal rituals (internal use only)
- Add emotional_engine.py for internal priming logic
- Add comprehensive test suite
- Update README with internal usage examples
- No public API exposure of ritual content
- Ready for engine integration"

echo ""
echo "✅ Procédure terminée !"
echo "📤 Pour pousser: git push origin chore/rituals-internalize-cordee"
echo "�� Pour créer une PR: ouvrir GitHub et créer la pull request"
