from collections import defaultdict
from typing import List

from page_analyzer import entities

from page_analyzer.db import connection


def get_all_for_url(url_id: int) -> List[entities.Url]:
    cursor = connection.get_cursor()
    cursor.execute(
        "SELECT id, url_id, status_code, h1, title, description, DATE(created_at) "
        "FROM url_checks WHERE url_id=(%s) ORDER BY id DESC",
        (url_id,),
    )
    return [entities.UrlCheck(*columns) for columns in cursor.fetchall()]


def create_for_url(url_id: int, **fields) -> entities.UrlCheck:
    cursor = connection.get_cursor()
    fields = defaultdict(lambda: None, fields)
    fields['url_id'] = url_id
    cursor.execute(
        "INSERT INTO url_checks(url_id, status_code, h1, title, description) "
        "VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s) "
        "RETURNING id, url_id, status_code, h1, title, description, DATE(created_at)",
        fields,
    )
    connection.commit()
    url_check = entities.UrlCheck(*cursor.fetchone())
    return url_check
