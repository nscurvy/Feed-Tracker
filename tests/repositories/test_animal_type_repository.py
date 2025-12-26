from sqlite3 import IntegrityError

import pytest


import db.repository.AnimalType as at
from tests.repositories.common_test_fixture import test_connection


def test_query_animal_types_by_name(test_connection):
    duck = at.get_by_name(test_connection, 'duck')
    cat = at.get_by_name(test_connection, 'cat')

    assert duck is not None
    assert cat is not None


def test_query_get_all(test_connection):
    animal_types = at.get_all(test_connection)

    assert len(animal_types) == 2
    names = [animal_types[0].name, animal_types[1].name]

    assert 'duck' in names
    assert 'cat' in names


def test_query_animal_types_by_id(test_connection):
    animal_types = at.get_all(test_connection)
    id_map = { animal_types[i].animal_type_id: animal_types[i] for i in range(len(animal_types)) }

    for i in id_map.keys():
        assert id_map[i] == at.get_by_id(test_connection, i)


def test_query_nonexistent_animal(test_connection):
    dog = at.get_by_name(test_connection, 'dog')

    assert dog is None


def test_insertion(test_connection):
    new_animal_id = at.insert_new(test_connection, 'dog')

    assert new_animal_id is not None

    new_animal = at.get_by_id(test_connection, new_animal_id)

    assert new_animal is not None
    assert new_animal.name == 'dog'


def test_delete_by_name(test_connection):
    test_name = 'dog'
    assert at.insert_new(test_connection, test_name) is not None
    at.delete_by_name(test_connection, test_name)
    assert at.get_by_name(test_connection, test_name) is None


def test_delete_by_id(test_connection):
    test_id = at.insert_new(test_connection, 'dog')
    assert at.get_by_id(test_connection, test_id) is not None
    at.delete_by_id(test_connection, test_id)
    assert at.get_by_id(test_connection, test_id) is None


def test_delete_by_name_returns_false_for_fail(test_connection):
    test_name = 'dog'
    assert not at.delete_by_name(test_connection, test_name)


def test_delete_by_id_returns_false_for_fail(test_connection):
    test_name = 'dog'
    assert not at.delete_by_id(test_connection, test_name)


def test_database_protects_integrity_when_deleting(test_connection):
    with pytest.raises(IntegrityError):
        at.delete_by_name(test_connection, 'duck')
