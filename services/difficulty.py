import logging
from models.user import User
from models.performance import PerformanceLog
from core.constants import FeedbackDifficulty, Difficulty

logger = logging.getLogger(__name__)

class DifficultyEngine:
    """
    Adaptive Difficulty Engine.
    Adjusts base difficulty based on performance feedback and user age.
    """
    
    @staticmethod
    def adjust_difficulty(user: User, current_difficulty: int, log: PerformanceLog) -> int:
        new_difficulty = current_difficulty
        
        # 1. Performance-based adjustment
        if log.difficulty_feedback == FeedbackDifficulty.TOO_EASY and log.accuracy > 0.90:
            new_difficulty = min(new_difficulty + 1, Difficulty.ADVANCED)
            logger.info(f"User found it too easy with high accuracy. Increasing difficulty to {new_difficulty}")
        elif log.difficulty_feedback == FeedbackDifficulty.TOO_HARD:
            new_difficulty = max(new_difficulty - 1, Difficulty.BEGINNER)
            logger.info(f"User found it too hard. Decreasing difficulty to {new_difficulty}")
        elif log.accuracy < 0.60:
            # Objective failure rate
            new_difficulty = max(new_difficulty - 1, Difficulty.BEGINNER)
            logger.info(f"Low accuracy ({log.accuracy}). Decreasing difficulty to {new_difficulty}")
            
        # 2. Age-based modifier constraints (Start lower for older, but allow performance to override eventually)
        if user.age >= 76 and new_difficulty > Difficulty.MODERATE:
            # Only allow advanced for 76+ if they consistently score > 95%
            if log.accuracy < 0.95:
                new_difficulty = Difficulty.MODERATE
                logger.info(f"Age 76+ safety constraint applied. Max difficulty capped at Moderate unless accuracy > 95%")
                
        return new_difficulty
