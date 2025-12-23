from sqlite3 import Connection
from dataclasses import dataclass
from typing import Optional


@dataclass
class Source:
    source_id: int
    name: str


def get_by_id(conn: Connection, source_id: int) -> Optional[Source]:
    result = conn.execute('SELECT * FROM source WHERE source_id = ?', (source_id,)).fetchone()
    if result is not None:
        return Source(**result)
    else:
        return None


def get_all(conn: Connection) -> list[Source]:
    result = []
    rows = conn.execute('SELECT * FROM source').fetchall()
    for row in rows:
        result.append(Source(**row))
    return result


def get_by_name(conn: Connection, name: str) -> Optional[Source]:
    result = conn.execute('SELECT * FROM source WHERE name = ?', (name,)).fetchone()
    if result is not None:
        return Source(**result)
    else:
        return None
