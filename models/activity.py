from dataclasses import dataclass
from typing import Optional

@dataclass
class Activity:
    id: Optional[int]
    module_type: str # from ModuleType enum
    name: str
    description: str
    base_difficulty: int # 1-5
