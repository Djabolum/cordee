"""
Moteur émotionnel pour la sélection et l'application des archétypes
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from .archetypes_internal import get_archetype, ARCHETYPES


@dataclass
class EmotionalState:
    """État émotionnel de l'utilisateur pour le priming archétypal."""

    user_signal: Optional[str] = None
    conflict_level: float = 0.0  # 0.0 à 1.0
    voice_shakiness: float = 0.0  # 0.0 à 1.0
    current_color: Optional[str] = None
    current_tone: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)


def get_archetype_by_emotional_context(
    conflict: float = 0.0, shakiness: float = 0.0, signal: Optional[str] = None
) -> str:
    """
    Sélectionne un archétype basé sur le contexte émotionnel.

    Args:
        conflict: Niveau de conflit (0.0 à 1.0)
        shakiness: Niveau de tremblement dans la voix (0.0 à 1.0)
        signal: Signal utilisateur ("start", etc.)

    Returns:
        Clé de l'archétype sélectionné
    """
    # Signal de démarrage prioritaire
    if signal == "start":
        return "fil_daube"

    # Conflit élevé -> archétype de passage/apaisement
    if conflict > 0.7:
        return "pont_silencieux"

    # Voix tremblante -> archétype de présence vocale
    if shakiness > 0.5:
        return "voix_nue"

    # Par défaut -> ancrage/stabilité
    return "racine_calme"


def archetype_priming(state: EmotionalState) -> EmotionalState:
    """
    Applique le priming archétypal à l'état émotionnel.

    Args:
        state: État émotionnel actuel

    Returns:
        État émotionnel mis à jour avec les paramètres de l'archétype
    """
    # Déterminer l'archétype approprié
    archetype_key = get_archetype_by_emotional_context(
        conflict=state.conflict_level,
        shakiness=state.voice_shakiness,
        signal=state.user_signal,
    )

    # Récupérer l'archétype
    archetype = get_archetype(archetype_key)
    if not archetype:
        # Fallback sur le premier archétype si erreur
        archetype = ARCHETYPES[0]

    # Appliquer les paramètres de l'archétype à l'état
    state.current_color = archetype.color_hex
    state.current_tone = archetype.note_hz
    state.tags["arch"] = archetype.archetype
    state.tags["totem"] = archetype.totem
    state.tags["archetype_key"] = archetype.key

    return state
