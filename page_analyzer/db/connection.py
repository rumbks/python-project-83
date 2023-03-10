import psycopg2
from flask import Flask, current_app

from page_analyzer.environ import env


def setup(app: Flask) -> None:
    connection = psycopg2.connect(env("DATABASE_URL"))
    app.db_connection = connection


def get_cursor():
    return current_app.db_connection.cursor()


def commit() -> None:
    current_app.db_connection.commit()
