import pytest
from sqlite3 import OperationalError,Error

from viewmodel.AnimalViewModel import AnimalViewModel
import db.repository.AnimalType as AnimalType
import db.repository.AnimalPopulation as AnimalPopulation
import db.repository.AnimalPopulationUpdate as AnimalPopulationUpdate
import db.db as db


@pytest.fixture
def test_connection():
    test_conn = db.get_connection(':memory:')
    db.initialize_db(test_conn)
    return test_conn


@pytest.fixture
def test_viewmodel(test_connection):
    return AnimalViewModel(test_connection)


def test_avm_valid_insertion(test_connection, test_viewmodel):
    test_params = {
        'animal_name': 'dog',
        'delta': '5',
        'date_of_change': '2025-01-01',
        'reason': 'A reason given'
    }
    test_viewmodel.update_animal(**test_params)

    verification = AnimalType.get_by_name(test_connection, test_params['animal_name'])
    assert verification.name is not None


def test_avm_multiple_animal_updates(test_connection, test_viewmodel):
    test_params = {
        'animal_name': 'dog',
        'delta': '5',
        'date_of_change': '2025-01-01',
        'reason': 'A reason given'
    }
    test_viewmodel.update_animal(**test_params)
    test_viewmodel.update_animal(**test_params)

    verification = AnimalPopulationUpdate.get_all(test_connection)
    assert len(verification) == 2


def test_avm_delta_changes_population(test_connection, test_viewmodel):
    test_params = {
        'animal_name': 'dog',
        'delta': '5',
        'date_of_change': '2025-01-01',
        'reason': 'A reason given'
    }
    test_viewmodel.update_animal(**test_params)
    test_viewmodel.update_animal(**test_params)

    verification = AnimalPopulation.get_by_name(test_connection, test_params['animal_name'])
    assert verification.quantity == 10
