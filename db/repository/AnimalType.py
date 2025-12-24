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
        'SELECT * FROM animal_type WHERE name=?', (name,)).fetchone()
    if result is None:
        return None
    else:
        return AnimalType(**result)


def insert_new(conn: Connection, name: str) -> int:
    """
    Inserts a new row into the animal_type table with the given name if one does not already exist.

    :param conn: Database connection to use
    :param name: Name of the animal_type to insert
    :return: The rowid of the inserted row
    :raise sqlite3.IntegrityError: If row already exists
    """
    result = conn.execute('INSERT INTO animal_type(name) VALUES (?)', (name,)).lastrowid
    return result


def get_all(conn: Connection) -> list[AnimalType]:
    """
    Retrieves all rows from the animal_type table.

    :param conn: Database connection to use
    :return: List of AnimalType objects
    """
    results = []
    rows = conn.execute('SELECT * FROM animal_type').fetchall()
    for row in rows:
        results.append(AnimalType(**row))
    return results


def delete_by_id(conn: Connection, animal_type_id: int) -> bool:
    """
    Deletes a row from the animal_type table corresponding to the given id.

    :param conn: Database connection to use
    :param animal_type_id: id of the animal_type to delete
    :return: True if row was successfully deleted, False otherwise
    """
    if get_by_id(conn, animal_type_id) is not None:
        conn.execute('DELETE FROM animal_type WHERE animal_type_id = ?',(animal_type_id,))
        return True
    else:
        return False


def delete_by_name(conn: Connection, name: str) -> bool:
    """
    Deletes a row from the animal_type table corresponding to the given name.

    :param conn: Database connection to use
    :param name: Name of the animal_type to delete
    :return: True if row was successfully deleted, False otherwise
    """
    candidate = get_by_name(conn, name)
    if candidate is not None:
        delete_by_id(conn, candidate.animal_type_id)
        return True
    else:
        return False
