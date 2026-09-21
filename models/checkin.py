from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Checkin:
    id: Optional[int]
    user_id: int
    date: str # ISO format YYYY-MM-DD
    mood: int # 1-10
    stress: int
    anxiety: int
    energy: int
    focus: int
    motivation: int
    mental_fatigue: int
    sleep_hours: float
