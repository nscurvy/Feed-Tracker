import pytest
from datetime import datetime

import db.repository.AnimalPopulation as ap
from tests.repositories.common_test_fixture import test_connection


def test_correct_duck_population(test_connection):
    duck_population = ap.get_by_name(test_connection, 'duck')

    assert duck_population.quantity == 5


def test_correct_date(test_connection):
    duck_population = ap.get_by_name(test_connection, 'duck')

    assert duck_population.date_updated == datetime.strptime('2025-02-15', '%Y-%m-%d').date()


def test_correct_query_name(test_connection):
    duck_population = ap.get_by_name(test_connection, 'duck')
    name = ap.get_name_by_id(test_connection, duck_population.animal_type_id)
    assert name == 'duck'


def test_get_all(test_connection):
    all_population = ap.get_all(test_connection)
    assert len(all_population) == 2
    names = [ap.get_name_by_id(test_connection, i.animal_type_id) for i in all_population]
    assert 'duck' in names
    assert 'cat' in names


def test_get_missing_name_returns_none(test_connection):
    dog_population = ap.get_by_name(test_connection, 'dog')
    assert dog_population is None


def test_get_by_id(test_connection):
    duck_population = ap.get_by_id(test_connection, 1)
    assert ap.get_name_by_id(test_connection, duck_population.animal_type_id) == 'duck'
    cat_population = ap.get_by_id(test_connection, 2)
    assert ap.get_name_by_id(test_connection, cat_population.animal_type_id) == 'cat'
    dog_population = ap.get_by_id(test_connection, 3)
    assert dog_population is None
