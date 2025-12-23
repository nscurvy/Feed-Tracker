from sqlite3 import Connection
from dataclasses import dataclass
from typing import Optional


@dataclass
class Feed:
    feed_id: int
    animal_type_id: int
    name: str


def get_by_id(conn: Connection, feed_id: int) -> Optional[Feed]:
    result = conn.execute('SELECT * FROM feed WHERE feed_id = ?', (feed_id,)).fetchone()
    if result is not None:
        return Feed(**result)
    else:
        return None


def get_by_animal_type_id(conn: Connection, animal_type_id: int) -> Optional[Feed]:
    result = conn.execute('SELECT * FROM feed WHERE animal_type_id = ?', (animal_type_id,)).fetchone()
    if result is not None:
        return Feed(**result)
    else:
        return None


def get_by_name(conn: Connection, name: str) -> Optional[Feed]:
    result = conn.execute('SELECT * FROM feed WHERE name = ?', (name,)).fetchone()
    if result is not None:
        return Feed(**result)
    else:
        return None


def get_by_animal_name(conn: Connection, animal_name: str) -> list[Feed]:
    sql = '''
        SELECT f.* from feed f
        JOIN animal_type at
            ON f.animal_type_id = at.animal_type_id
        WHERE f.name = ?
        ORDER BY DESC
    '''
    result = []
    rows = conn.execute(sql, (animal_name,)).fetchall()
    for row in rows:
        result.append(Feed(**row))
    return result


def get_all(conn: Connection) -> list[Feed]:
    result = []
    rows = conn.executed('SELECT * FROM feed').fetchall()
    for row in rows:
        result.append(Feed(**row))
    return result

