from typing import Optional

from page_analyzer import models

from page_analyzer.db import connection

from psycopg2 import sql


def _get(
    *, url_id: Optional[int] = None, name: Optional[str] = None
) -> Optional[models.Url]:
    if url_id is not None:
        where_field = 'id'
        where_value = url_id
    elif name is not None:
        where_field = 'name'
        where_value = name
    else:
        raise ValueError("Neither url id nor url name was provided")
    query = (
        f"SELECT id, name, DATE(created_at) FROM urls WHERE {where_field}=(%s)"
    )
    cursor = connection.get_cursor()
    cursor.execute(query, (where_value,))
    if (fields := cursor.fetchone()) is None:
        return None
    return models.Url(*fields)


def get_by_id(url_id: int) -> models.Url:
    return _get(url_id=url_id)


def get_by_name(name: str) -> models.Url:
    return _get(name=name)


def create(name: str) -> models.Url:
    url = _get(name=name)
    if url is None:
        cursor = connection.get_cursor()
        cursor.execute("INSERT INTO urls(name) VALUES (%s) RETURNING *", (name,))
        connection.commit()
        url = models.Url(*cursor.fetchone())
    return url
