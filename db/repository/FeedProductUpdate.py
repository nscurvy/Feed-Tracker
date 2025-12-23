from sqlite3 import Connection, Row
from typing import Optional
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, date


@dataclass
class FeedProductUpdate:
    id: int
    feed_product_id: int
    new_cost: Decimal
    date_updated: date


def _row_to_feed_product_update(row: Row) -> FeedProductUpdate:
    return FeedProductUpdate(
        id=row['id'],
        feed_product_id=row['feed_product_id'],
        new_cost=Decimal(row['new_cost']) / Decimal(100),
        date_updated=datetime.strptime(row['date_updated'], '%Y-%m-%dT%H').date()
    )


def get_all(conn: Connection) -> list[FeedProductUpdate]:
    result = []
    rows = conn.execute('SELECT * FROM feed_product_update').fetchall()
    for row in rows:
        result.append(_row_to_feed_product_update(row))
    return result