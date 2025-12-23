from sqlite3 import Connection
from dataclasses import dataclass


@dataclass
class AnimalType:
    """Models rows from animal_type table"""
    animal_type_id: int
    name: str


def get_by_id(conn: Connection, animal_type_id: int) -> AnimalType | None:
    """
    Retrieves a row from the animal_type table corresponding to the given id.

    :param conn: Database connection to use
    :param animal_type_id: animal_type id
    :return: AnimalType object or None
    """
    result = (conn.execute(
        'SELECT * FROM animal_type WHERE animal_type_id = ?',
        (animal_type_id,)).
              fetchone())
    if result is None:
        return None
    else:
        return AnimalType(**result)


def get_by_name(conn: Connection, name: str) -> AnimalType | None:
    """
    Retrieves a row from the animal_type table corresponding to the given name.

    :param conn: Database connection to use
    :param name: Name of the animal_type
    :return: AnimalType object or None
    """
    result = conn.execute(
        'SELECT * FROM animal_type WHERE name=?', name).fetchone()
    if result is None:
        return None
    else:
        return AnimalType(**result)


def insert_new(conn: Connection, name: str) -> bool:
    """
    Inserts a new row into the animal_type table with the given name if one does not already exist.

    :param conn: Database connection to use
    :param name: Name of the animal_type to insert
    :return: True if a new row was successfully created, False otherwise
    """
    if get_by_name(conn, name) is not None:
        return False
    else:
        conn.execute('INSERT INTO animal_type VALUES (?)', (name,))
        return True
