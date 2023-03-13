import psycopg2
from flask import Flask, g

from page_analyzer.environ import env


def teardown_db(exception):
    db_connection = g.pop('db', None)

    if db_connection is not None:
        db_connection.close()


def setup(app: Flask) -> None:
    app.teardown_appcontext(teardown_db)


def _get_connection():
    if 'db_connection' not in g:
        g.db_connection = psycopg2.connect(env("DATABASE_URL"))
    return g.db_connection


def get_cursor():
    connection = _get_connection()
    return connection.cursor()


def commit() -> None:
    connection = _get_connection()
    connection.commit()
