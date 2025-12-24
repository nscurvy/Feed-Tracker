from sqlite3 import Connection,Row
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class AnimalPopulationUpdate:
    id: int
    animal_type_id: int
    delta: int
    date_updated: date
    reason: Optional[str]


def _row_to_animal_population_update(row: Row) -> AnimalPopulationUpdate:
    return AnimalPopulationUpdate(
        id=row['id'],
        animal_type_id=row['animal_type_id'],
        delta=row['delta'],
        date_updated=datetime.strptime(row['date_updated'], '%Y-%m-%d').date(),
        reason=row['reason']
    )


def get_by_id(conn: Connection, id: int) -> Optional[AnimalPopulationUpdate]:
    result = conn.execute('SELECT * FROM animal_population WHERE id = ?', (id,)).fetchone()
    if result:
        return _row_to_animal_population_update(result)
    else:
        return None


def get_all(conn: Connection) -> list[AnimalPopulationUpdate]:
    result = []
    rows = conn.execute('SELECT * FROM animal_population ORDER BY id').fetchall()
    for row in rows:
        result.append(_row_to_animal_population_update(row))
    return result


def get_by_name(conn: Connection, name: str) -> list[AnimalPopulationUpdate]:
    sql = '''
        SELECT apu.* 
        FROM animal_population_update apu
        JOIN animal_type at
            ON apu.animal_type_id = at.animal_type_id
        WHERE at.name = ?
    '''
    rows = conn.execute(sql, (name,)).fetchall()
    result = []
    for row in rows:
        result.append(_row_to_animal_population_update(row))
    return result


def insert_update(conn: Connection, animal_type_id: int, delta: int, date_updated: date, reason: Optional[str] = None) -> AnimalPopulationUpdate:
    print(date_updated.isoformat())
    new_id = conn.execute('INSERT INTO animal_population_update(animal_type_id, delta, date_updated, reason) VALUES(?,?,?,?)',
                          (animal_type_id, delta, date_updated.isoformat(), reason)).lastrowid
    return AnimalPopulationUpdate(new_id, animal_type_id, delta, date_updated, reason)
