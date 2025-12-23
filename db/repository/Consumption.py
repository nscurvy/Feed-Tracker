from sqlite3 import Connection, Row
from typing import Optional
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, date


@dataclass
class Consumption:
    consumption_id: int
    feed_id: int
    quantity: Decimal
    unit_id: int
    animal_type_id: int
    consumption_date: date
    note: Optional[str]


def _row_to_consumption(row: Row) -> Consumption:
    return Consumption(
        consumption_id=row['consumption_id'],
        feed_id=row['feed_id'],
        quantity=Decimal(row['quantity']),
        unit_id=row['unit_id'],
        animal_type_id=row['animal_type_id'],
        consumption_date=datetime.strptime(row['consumption_date'], '%Y-%m-%d').date(),
        note=row['note']
    )


def get_all(conn: Connection) -> list[Consumption]:
    result = []
    rows = conn.execute('SELECT * FROM consumption')
    for row in rows:
        result.append(_row_to_consumption(row))
    return result
