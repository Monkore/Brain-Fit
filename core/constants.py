from enum import Enum

class ModuleType(str, Enum):
    PROCESSING_SPEED = "Processing Speed"
    MEMORY = "Memory"
    ATTENTION = "Attention"
    EXECUTIVE_FUNCTION = "Executive Function"
    LANGUAGE = "Language"
    ORIENTATION = "Orientation"
    DUAL_TASK = "Dual Task"
    YOGA = "Yoga"
    MEDITATION = "Meditation"
    BREATHING = "Breathing"

class Difficulty(int, Enum):
    BEGINNER = 1
    EASY = 2
    MODERATE = 3
    CHALLENGING = 4
    ADVANCED = 5

class FeedbackDifficulty(str, Enum):
    TOO_EASY = "Too Easy"
    JUST_RIGHT = "Just Right"
    TOO_HARD = "Too Hard"

class FeedbackEnjoyment(str, Enum):
    ENJOYED = "Enjoyed"
    NEUTRAL = "Neutral"
    DISLIKED = "Disliked"

class FeedbackEnergy(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Language(str, Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    BILINGUAL = "Bilingual"
