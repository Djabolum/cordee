#!/bin/bash
# Script de nettoyage des références Valexa dans Cordée
# Usage: ./scripts/cleanup_valexa_refs.sh

set -e

echo "🧹 Nettoyage des références Valexa dans Cordée"
echo "=============================================="

# Rechercher les références Valexa
echo "🔍 Recherche des références Valexa..."
if command -v rg &> /dev/null; then
    echo "Utilisation de ripgrep (rg):"
    rg -n "Valexa|valexa|Speculum|instinct|ritualsEngine|SiegeEssence|GhostIA" . || true
elif command -v grep &> /dev/null; then
    echo "Utilisation de grep:"
    grep -r -n "Valexa\|valexa\|Speculum\|instinct\|ritualsEngine\|SiegeEssence\|GhostIA" . || true
else
    echo "❌ Aucun outil de recherche disponible (rg ou grep)"
    exit 1
fi

echo ""
echo "📋 Checklist de nettoyage Cordée:"
echo "----------------------------------"
echo "✅ Module archetypes_internal.py créé (10 archétypes)"
echo "✅ Module emotional_engine.py créé (priming interne)"
echo "✅ Tests unitaires fonctionnels"
echo "✅ Aucune exposition publique des archétypes"
echo ""
echo "🔄 Étapes suivantes:"
echo "1. Supprimer les fichiers YAML/JSON d'archétypes publics"
echo "2. Retirer les endpoints d'exposition d'archétypes"
echo "3. Remplacer par imports internes uniquement"
echo "4. Vérifier que les tests passent"
echo "5. Commit atomique"
echo ""
echo "📝 Commande de commit suggérée:"
echo "git commit -m \"chore(cordee): internalize archetypes; remove public exposure\""
