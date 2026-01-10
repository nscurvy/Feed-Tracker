from sqlite3 import Connection, Row
from dataclasses import dataclass
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


@dataclass
class FeedProduct:
    feed_product_id: int
    feed_id: int
    quantity: Decimal
    unit_id: int
    source_id: int
    brand_name: str
    cost: Decimal
    date_updated: date


def _row_to_feed_product(row: Row) -> FeedProduct:
    return FeedProduct(
        feed_product_id=row['feed_product_id'],
        feed_id=row['feed_id'],
        quantity=Decimal(row['quantity']),
        unit_id=row['unit_id'],
        source_id=row['source_id'],
        brand_name=row['brand_name'],
        cost=Decimal(row['cost_cents']) / Decimal('100'),
        date_updated=datetime.strptime(row['date_updated'], '%Y-%m-%d').date()
    )


def get_all(conn: Connection) -> list[FeedProduct]:
    result = []
    rows = conn.execute('SELECT * FROM feed_product').fetchall()
    for row in rows:
        result.append(_row_to_feed_product(row))
    return result


def get_or_insert(conn: Connection, feed_id: int, quantity: Decimal, unit_id: int, source_id: int, brand_name: str, cost: int, date_updated: date) -> FeedProduct:
    get_sql = '''
        SELECT * FROM feed_product 
        WHERE feed_id = ?
            AND quantity = ?
            AND unit_id = ?
            AND source_id = ?
            AND brand_name = ?
    '''
    insert_sql = '''
        INSERT INTO feed_product (feed_id, quantity, unit_id, source_id, brand_name, cost_cents, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING *
    '''
    row = conn.execute(get_sql, (feed_id, float(quantity), unit_id, source_id, brand_name)).fetchone()
    if row is not None:
        return _row_to_feed_product(row)
    else:
        result = conn.execute(insert_sql, (feed_id, float(quantity), unit_id, source_id, brand_name, cost, date_updated.isoformat())).fetchone()
        return _row_to_feed_product(result)
