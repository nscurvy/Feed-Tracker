from sqlite3 import Connection
from dataclasses import dataclass


@dataclass
class AnimalType:
    animal_type_id: int
    name: str


def get_by_id(conn: Connection, animal_type_id: int) -> AnimalType | None:
    result = (conn.execute(
        'SELECT * FROM animal_type WHERE animal_type_id = ?',
        (animal_type_id,)).
              fetchone())
    if result is None:
        return None
    else:
        return AnimalType(**result)


def get_by_name(conn: Connection, name: str) -> AnimalType | None:
    result = conn.execute(
        'SELECT * FROM animal_type WHERE name=?', name).fetchone()
    if result is None:
        return None
    else:
        return AnimalType(**result)


def insert_new(conn: Connection, name: str) -> bool:
    if get_by_name(conn, name) is not None:
        return False
    else:
        conn.execute('INSERT INTO animal_type VALUES (?)', (name,))
        return True
