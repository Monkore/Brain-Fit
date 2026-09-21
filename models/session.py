from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Session:
    id: Optional[int]
    user_id: int
    date: str
    status: str # "planned", "completed"

@dataclass
class SessionActivity:
    id: Optional[int]
    session_id: int
    activity_id: int
    order: int
    status: str # "pending", "completed", "skipped"
