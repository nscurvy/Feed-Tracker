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


def check_or_insert(conn: Connection, name: str) -> Source:
    row = conn.execute('SELECT * FROM source WHERE name = ?', (name,)).fetchone()
    if row is not None:
        return Source(**row)
    else:
        id = conn.execute('INSERT INTO source (name) VALUES (?)', (name,)).lastrowid
        return Source(source_id=id, name=name)