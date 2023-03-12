from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UrlCheck:
    id: int
    url_id: int
    status_code: int
    h1: Optional[str]
    title: Optional[str]
    description: Optional[str]
    created_at: datetime


@dataclass
class Url:
    id: int
    name: str
    created_at: datetime
    last_check: Optional[UrlCheck] = None
