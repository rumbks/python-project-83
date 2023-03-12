from urllib.parse import urlparse
from validators.url import url as validate_url
from validators import ValidationFailure


def normalize(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_valid(url: str) -> bool:
    validation_result = validate_url(url)
    return False if isinstance(validation_result, ValidationFailure) else True
