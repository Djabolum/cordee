"""
Tests pour le module archetypes_internal
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cordee.core.archetypes_internal import ARCHETYPES, get_archetype, Archetype
from cordee.core.emotional_engine import (
    archetype_priming,
    EmotionalState,
    get_archetype_by_emotional_context,
)


def test_archetypes_count():
    """Teste que nous avons bien 10 archétypes."""
    assert len(ARCHETYPES) == 10


def test_get_archetype_existing():
    """Teste la récupération d'un archétype existant."""
    archetype = get_archetype("fil_daube")
    assert archetype is not None
    assert archetype.key == "fil_daube"
    assert archetype.archetype == "Soleil naissant"
    assert archetype.totem == "Hirondelle"


def test_get_archetype_nonexistent():
    """Teste la récupération d'un archétype inexistant."""
    archetype = get_archetype("inexistant")
    assert archetype is None


def test_archetype_immutability():
    """Teste que les archétypes sont bien immutables."""
    archetype = get_archetype("fil_daube")
    try:
        archetype.key = "nouveau_key"
        assert False, "L'archétype devrait être immutable"
    except AttributeError:
        # C'est ce qu'on attend avec @dataclass(frozen=True)
        pass


def test_emotional_engine_start_signal():
    """Teste le priming avec signal de démarrage."""
    state = EmotionalState(user_signal="start")
    state = archetype_priming(state)

    assert state.current_color == "#F2A65A"  # Couleur de l'archétype "fil_daube"
    assert state.current_tone == 261.63  # Note C4
    assert state.tags["arch"] == "Soleil naissant"


def test_emotional_engine_high_conflict():
    """Teste le priming avec conflit élevé."""
    state = EmotionalState(conflict_level=0.8)
    state = archetype_priming(state)

    assert state.current_color == "#B3B7C0"  # Couleur de l'archétype "pont_silencieux"
    assert state.current_tone == 164.81  # Note E3
    assert state.tags["arch"] == "Arc / Passage"


def test_emotional_engine_voice_shakiness():
    """Teste le priming avec voix tremblante."""
    state = EmotionalState(voice_shakiness=0.6)
    state = archetype_priming(state)

    assert state.current_color == "#E8E8E8"  # Couleur de l'archétype "voix_nue"
    assert state.current_tone == 138.59  # Note C#3
    assert state.tags["arch"] == "Onde sonore"


def test_emotional_engine_default():
    """Teste le priming par défaut."""
    state = EmotionalState()
    state = archetype_priming(state)

    assert state.current_color == "#1F6F50"  # Couleur de l'archétype "racine_calme"
    assert state.current_tone == 98.00  # Note G2
    assert state.tags["arch"] == "Arbre du monde"


def test_get_archetype_by_emotional_context():
    """Teste la fonction de sélection par contexte émotionnel."""
    # Test avec conflit élevé
    key = get_archetype_by_emotional_context(conflict=0.8, shakiness=0.2)
    assert key == "pont_silencieux"

    # Test avec voix tremblante
    key = get_archetype_by_emotional_context(conflict=0.3, shakiness=0.6)
    assert key == "voix_nue"

    # Test avec signal de démarrage
    key = get_archetype_by_emotional_context(
        conflict=0.2, shakiness=0.1, signal="start"
    )
    assert key == "fil_daube"


if __name__ == "__main__":
    test_archetypes_count()
    test_get_archetype_existing()
    test_get_archetype_nonexistent()
    test_archetype_immutability()
    test_emotional_engine_start_signal()
    test_emotional_engine_high_conflict()
    test_emotional_engine_voice_shakiness()
    test_emotional_engine_default()
    test_get_archetype_by_emotional_context()
    print("✅ Tous les tests passent !")
