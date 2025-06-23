from enum import Enum, IntEnum 

# Codificaciones de gestos
class Gest(Enum):
    """
    Enumeración para mapear todos los gestos de la mano a un string.
    """
    UNKNOWN = "unknown"
    PALM = "palm"
    CALL = "call"
    DISLIKE = "dislike"
    FIST = "fist"
    FOUR = "four"
    LIKE = "like"
    MUTE = "mute"
    OK = "ok"
    ONE = "one"          
    PEACE = "peace"     
    PEACE_INVERTED = "peace_inverted"
    ROCK = "rock"
    STOP = "stop"
    STOP_INVERTED = "stop_inverted"
    THREE = "three"      
    THREE2 = "three2"
    TWO_UP = "two_up"
    TWO_UP_INVERTED = "two_up_inverted"

# Etiquetas de multi-mano (no cambian)
class HLabel(IntEnum):
    """
    Etiquetas para la clasificación de las manos (izquierda, derecha).
    """
    MINOR = 0  # Mano secundaria (izquierda o menos dominante)
    MAJOR = 1  # Mano principal (derecha o más dominante)