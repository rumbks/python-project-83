from dataclasses import dataclass
from datetime import datetime


@dataclass
class Url:
    id: int
    name: str
    created_at: datetime


@dataclass
class UrlCheck:
    id: int
    url_id: int
    status_code: int
    h1: str
    title: str
    description: str
    created_at: datetime