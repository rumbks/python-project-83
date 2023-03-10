from dataclasses import dataclass
from datetime import datetime


@dataclass
class Url:
    id: int
    name: str
    created_at: datetime