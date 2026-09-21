from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: Optional[int]
    name: str
    age: int
    gender: str
    language: str
    activity_level: str
    sleep_duration: str
    meditation_exp: str
    exercise_freq: str
    created_at: datetime = datetime.now()
