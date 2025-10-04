#!/usr/bin/env python3
"""
Test avancé des fonctionnalités du système d'archétypes.
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

from cordee.core.archetypes_internal import ARCHETYPES, get_archetype
from cordee.core.emotional_engine import (
    archetype_priming,
    EmotionalState,
    get_archetype_by_emotional_context,
)


def test_tous_les_archetypes():
    """Teste l'affichage de tous les archétypes."""
    print("🔮 Liste des archétypes disponibles :")
    print("=" * 50)
    for archetype in ARCHETYPES:
        print(f"🎯 {archetype.key:<15} | {archetype.archetype:<20} | {archetype.totem}")
    print()


def test_contextes_emotionnels():
    """Teste différents contextes émotionnels."""
    print("🎭 Tests des contextes émotionnels :")
    print("=" * 40)

    contexts = [
        {"desc": "Signal de démarrage", "signal": "start"},
        {"desc": "Conflit élevé", "conflict": 0.9},
        {"desc": "Voix tremblante", "shakiness": 0.7},
        {"desc": "État neutre", "conflict": 0.1, "shakiness": 0.1},
    ]

    for ctx in contexts:
        desc = ctx.pop("desc")
        archetype_key = get_archetype_by_emotional_context(**ctx)
        archetype = get_archetype(archetype_key)
        print(f"📊 {desc:<20} → {archetype.key:<15} ({archetype.archetype})")
    print()


def test_priming_complet():
    """Teste le priming complet avec différents états."""
    print("🌟 Test du priming émotionnel complet :")
    print("=" * 45)

    # Test avec conflit élevé
    state = EmotionalState(conflict_level=0.8, voice_shakiness=0.2)
    state = archetype_priming(state)

    print(f"🎨 Couleur sélectionnée : {state.current_color}")
    print(f"🎵 Fréquence (Hz) : {state.current_tone}")
    print(f"🏛️  Archétype : {state.tags['arch']}")
    print(f"🦅 Totem : {state.tags['totem']}")
    print(f"🔑 Archétype actif : {state.tags['archetype_key']}")

    # Afficher le message de l'archétype
    archetype = get_archetype(state.tags["archetype_key"])
    print(f'💬 Appel : "{archetype.call}"')
    print(f'�� Note intérieure : "{archetype.inner_note}"')
    print()


if __name__ == "__main__":
    print("🚀 Test avancé du système d'archétypes Cordée\n")

    test_tous_les_archetypes()
    test_contextes_emotionnels()
    test_priming_complet()

    print("✅ Tous les tests avancés réussis !")
