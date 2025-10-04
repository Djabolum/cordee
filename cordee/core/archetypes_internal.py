from dataclasses import dataclass
from typing import List

__all__ = ['Archetype', 'ARCHETYPES', 'get_archetype']

@dataclass(frozen=True)
class Archetype:
    key: str
    archetype: str
    totem: str
    color_hex: str
    note_name: str
    note_hz: float
    waveform: str
    call: str
    inner_note: str
    edge: str

ARCHETYPES: List[Archetype] = [
    Archetype("fil_daube", "Soleil naissant", "Hirondelle", "#F2A65A", "C4", 261.63, "ramp_up",
           "Ce qui naît de toi cherche déjà la lumière.",
           "Tiédeur fragile du premier souffle.",
           "S'élève en tremblant, puis se fixe."),
    Archetype("goutte_claire", "Eau primordiale", "Source", "#73B7E3", "D4", 293.66, "ripple",
           "Chaque mot s'étend comme une onde sincère.",
           "Fraîcheur qui saisit la peau.",
           "La pureté érode goutte après goutte."),
    Archetype("pont_silencieux", "Arc / Passage", "Corde tendue", "#B3B7C0", "E3", 164.81, "line",
           "Entre deux rives, la vérité traverse.",
           "Tension muette au-dessus du vide.",
           "Ne vit qu'en étant traversé."),
    Archetype("flamme_douce", "Feu intérieur", "Luciole", "#F6D365", "F4", 349.23, "flicker",
           "Ta chaleur éclaire sans brûler.",
           "Chaleur intime qui dévoile.",
           "Révèle l'ombre avec la lumière."),
    Archetype("racine_calme", "Arbre du monde", "Pierre enfouie", "#1F6F50", "G2", 98.00, "pulse",
           "Reste ancré, même quand tout vacille.",
           "Odeur de terre humide.",
           "La stabilité peut aussi enfermer."),
    Archetype("vent_clair", "Souffle", "Roseau", "#9ED3AF", "A4", 440.00, "sway",
           "Laisse le souffle emporter ce qui ne sert plus.",
           "Nettoyage qui dépouille.",
           "La transparence rend vulnérable."),
    Archetype("onde_doree", "Spirale", "Coquille vide", "#C8A76B", "B3", 246.94, "spiral",
           "L'essence tourne et revient vers toi.",
           "Vertige d'attraction/répulsion.",
           "Ascension ou chute selon l'axe intérieur."),
    Archetype("voix_nue", "Onde sonore", "Tambour", "#E8E8E8", "C#3", 138.59, "sine",
           "Parle, et rien n'existe entre toi et l'instant.",
           "Vibration dans la poitrine avant le mot.",
           "Parler expose, se taire trahit."),
    Archetype("lune_claire", "Miroir nocturne", "Miroir d'eau", "#A7B8C9", "D#4", 311.13, "hush",
           "Ta lumière éclaire même dans le silence.",
           "On s'entend soi-même dans le calme.",
           "La nuit révèle ce que le jour cache."),
    Archetype("eclat_juste", "Étoile / Cristal", "Cristal brut", "#8C7BD6", "F#5", 739.99, "spark",
           "Le vrai scintille sans chercher à briller.",
           "Brûlure brève sur la rétine.",
           "Ce qui brille trop vite s'éteint vite."),
]

def get_archetype(key: str) -> Archetype | None:
    for a in ARCHETYPES:
        if a.key == key:
            return a
    return None
