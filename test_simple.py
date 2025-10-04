#!/usr/bin/env python3
"""
Test simple pour vérifier que le module fonctionne.
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from cordee.core.archetypes_internal import ARCHETYPES, get_archetype
    from cordee.core.emotional_engine import archetype_priming, EmotionalState

    print("✅ Import réussi !")
    print(f"📊 Nombre d'archétypes : {len(ARCHETYPES)}")

    # Test basique
    archetype = get_archetype("fil_daube")
    print(f"🌅 Archétype 'fil_daube' : {archetype.archetype}")

    # Test du moteur émotionnel
    state = EmotionalState(user_signal="start")
    state = archetype_priming(state)
    print(f"🎨 Couleur appliquée : {state.current_color}")
    print(f"🎵 Tonalité appliquée : {state.current_tone}")

    print("\n✅ Module des archétypes internes fonctionnel !")

except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
except Exception as e:
    print(f"❌ Erreur : {e}")
