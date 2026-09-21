from dataclasses import dataclass
from typing import Optional

@dataclass
class PerformanceLog:
    id: Optional[int]
    session_activity_id: int
    score: int # 0-100
    accuracy: float # 0.0 - 1.0
    duration_seconds: int
    difficulty_feedback: str # from FeedbackDifficulty
    enjoyment_feedback: str # from FeedbackEnjoyment
    energy_after: str # from FeedbackEnergy
    timestamp: str # ISO format string
