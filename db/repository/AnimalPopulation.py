from sqlite3 import Connection
from dataclasses import dataclass
from datetime import date


@dataclass
class AnimalPopulation:
    animal_type_id: int
    quantity: int
    date_updated: date


def get_by_id(conn: Connection, animal_id: int) -> AnimalPopulation | None:
    result = conn.execute('SELECT * FROM animal_population WHERE animal_type_id=?', animal_id).fetchone()
    if result is not None:
        return AnimalPopulation(**result)
    else:
        return None


def get_all(conn: Connection) -> list[AnimalPopulation]:
    result = []
    rows = conn.execute('SELECT * FROM animal_population').fetchall()
    for row in rows:
        result.append(AnimalPopulation(**row))
    return result
