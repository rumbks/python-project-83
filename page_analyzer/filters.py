from datetime import datetime
from flask import Flask


def format_datetime(date: datetime, format=None) -> str:
    if format is None:
        return date.strftime("%Y-%m-%d")
    return date.strftime(format)


def setup(app: Flask) -> None:
    app.template_filter('dt')(format_datetime)
