import pytest


import db.repository.AnimalType as at
from tests.repositories.common_test_fixture import test_connection


def test_query_animal_types(test_connection):
    duck = at.get_by_name(test_connection, 'duck')
    cat = at.get_by_name(test_connection, 'cat')

    assert duck is not None
    assert cat is not None