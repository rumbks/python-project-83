from typing import Optional, List

from page_analyzer import entities

from page_analyzer.db import connection


def _get(
    *, url_id: Optional[int] = None, name: Optional[str] = None
) -> Optional[entities.Url]:
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
    return entities.Url(*fields)


def get_by_id(url_id: int) -> entities.Url:
    return _get(url_id=url_id)


def get_by_name(name: str) -> entities.Url:
    return _get(name=name)


def get_all() -> List[entities.Url]:
    cursor = connection.get_cursor()
    cursor.execute(
        "WITH most_recent_checks AS "
        "(SELECT * FROM (SELECT DISTINCT ON (url_id) * FROM url_checks "
        "ORDER BY url_id, created_at DESC) t ORDER BY id)"
        "SELECT * FROM urls LEFT JOIN most_recent_checks ON "
        "urls.id=most_recent_checks.url_id ORDER BY urls.id DESC"
    )
    urls = []
    for row in cursor.fetchall():
        id_, name, created_at, *url_check_fields = row
        url_check = (
            None
            if all(field is None for field in url_check_fields)
            else entities.UrlCheck(*url_check_fields)
        )
        urls.append(entities.Url(id_, name, created_at, url_check))

    return urls


def create(name: str) -> entities.Url:
    url = _get(name=name)
    if url is None:
        cursor = connection.get_cursor()
        cursor.execute(
            "INSERT INTO urls(name) VALUES (%s) RETURNING *", (name,)
        )
        connection.commit()
        url = entities.Url(*cursor.fetchone())
    return url
