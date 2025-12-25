from sqlite3 import Connection, Row
from typing import Optional
from datetime import datetime, date
from dataclasses import dataclass


@dataclass
class Purchase:
    purchase_id: int
    feed_product_id: int
    quantity: int
    purchase_date: date


def _row_to_purchase(row: Row) -> Purchase:
    return Purchase(
        purchase_id=row['purchase_id'],
        feed_product_id=row['feed_product_id'],
        quantity=row['quantity'],
        purchase_date=datetime.strptime(row['purchase_date'], '%Y-%m-%d').date()
    )


def get_all(conn: Connection) -> list[Purchase]:
    result = []
    rows = conn.execute('SELECT * FROM purchase')
    for row in rows:
        result.append(_row_to_purchase(row))
    return result
