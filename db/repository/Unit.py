from sqlite3 import Connection, Row
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional


@dataclass
class Unit:
    unit_id: int
    name: str
    type: str
    conversion_factor: Decimal


def _row_to_unit(row: Row) -> Unit:
    return Unit(
        unit_id=row['unit_id'],
        name=row['name'],
        type=row['type'],
        conversion_factor=Decimal(row['conversion_factor'])
    )


def get_by_id(conn: Connection, unit_id: int) -> Optional[Unit]:
    result = conn.execute('SELECT * FROM unit WHERE unit_id=?', (unit_id,)).fetchone()
    if result is not None:
        return _row_to_unit(result)
    else:
        return None


def get_by_name_and_type(conn: Connection, name: str, type: str) -> Optional[Unit]:
    result = conn.execute('SELECT * FROM unit WHERE name=? AND type=?', (name, type)).fetchone()
    if result is not None:
        return _row_to_unit(result)
    else:
        return None


def get_by_type(conn: Connection, type: str) -> list[Unit]:
    result = []
    rows = conn.execute('SELECT * FROM unit WHERE type=?', (type,)).fetchall()
    for row in rows:
        result.append(_row_to_unit(row))
    return result
