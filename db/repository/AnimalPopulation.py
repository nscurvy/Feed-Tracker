from sqlite3 import Connection,Row
from dataclasses import dataclass
from datetime import date,datetime


@dataclass
class AnimalPopulation:
    """
    Models a row in the animal_population table.
    """
    animal_type_id: int
    quantity: int
    date_updated: date


def _row_to_animal_population(row: Row) -> AnimalPopulation:
    return AnimalPopulation(
        animal_type_id=int(row['animal_type_id']),
        quantity=int(row['quantity']),
        date_updated=datetime.strptime(row['date_updated'], '%Y-%m-%d').date()
    )


def get_by_id(conn: Connection, animal_type_id: int) -> AnimalPopulation | None:
    """
    Returns a row from the animal_population table by the given animal_type_id

    :param conn: The database connection to use.
    :param animal_type_id: The animal type id of the population row to return.
    :return: An AnimalPopulation object or None
    """
    result = conn.execute('SELECT * FROM animal_population WHERE animal_type_id = ?',
                          animal_type_id).fetchone()
    if result is not None:
        return _row_to_animal_population(result)
    else:
        return None


def get_all(conn: Connection) -> list[AnimalPopulation]:
    """
    Returns all rows from the animal_population table.

    :param conn: The database connection to use.
    :return: A list of AnimalPopulation objects.
    """
    result = []
    rows = conn.execute('SELECT * FROM animal_population').fetchall()
    for row in rows:
        result.append(_row_to_animal_population(row))
    return result


def get_by_name(conn: Connection, name: str) -> AnimalPopulation | None:
    """
    Returns a row from the animal_population table by the given name corresponding to a row in the animal_type table.
    :param conn: The database connection to use.
    :param name: The name of the corresponding animal_type to return a population for.
    :return: An AnimalPopulation object or None
    """
    sql = '''
        SELECT ap.*
        FROM animal_population ap
        JOIN animal_type at
            ON ap.animal_type_id = at.animal_type_id
        WHERE ap.name = ?
    '''
    result = conn.execute(sql, name).fetchone()
    if result is not None:
        return _row_to_animal_population(result)
    else:
        return None
