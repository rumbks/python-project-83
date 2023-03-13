from dataclasses import dataclass, asdict
from typing import Optional

from bs4 import BeautifulSoup


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content, features='html.parser')


@dataclass
class AnalysisResult:
    h1: Optional[str]
    title: Optional[str]
    description: Optional[str]

    to_dict = asdict


def analyze(parsed_page: BeautifulSoup) -> AnalysisResult:
    h1 = getattr(parsed_page.find('h1'), 'text', None)
    title = getattr(parsed_page.find('title'), 'text', None)
    description = parsed_page.find('meta', {'name': 'description'})
    description = description['content'] if description else None
    return AnalysisResult(h1, title, description)
