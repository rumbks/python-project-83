from typing import Optional

from page_analyzer import models

from page_analyzer.db import connection

from psycopg2 import sql


def _get(*, url_id: Optional[int] = None, name: Optional[str] = None) -> models.Url:
    if url_id is not None:
        where_field = sql.Identifier('id')
        where_value = url_id
    elif name is not None:
        where_field = sql.Identifier('name')
        where_value = name
    else:
        raise ValueError("Neither url id nor url name was provided")
    query = (
        f"SELECT id, name, DATE(created_at) FROM urls WHERE {where_field}=(%s)"
    )
    cursor = connection.get_cursor()
    cursor.execute(query, (where_value,))
    return models.Url(*cursor.fetchone())


def get_by_id(url_id: int) -> models.Url:
    return _get(url_id=url_id)
    pass


def create(name: str) -> models.Url:
    url = _get(name=name)
    if url is None:
        cursor = connection.get_cursor()
        cursor.execute("INSERT INTO urls(name) VALUES (%s) RETURNING *", (name,))
        connection.commit()
        url_id, name, created_at = cursor.fetchone()
        url = models.Url(url_id, name, created_at)
    return url