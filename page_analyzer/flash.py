from typing import Literal

from flask import flash


def info(message: str) -> None:
    flash(message, 'info')


def error(message: str) -> None:
    flash(message, 'danger')


def success(message: str) -> None:
    flash(message, 'success')
