import pytest
from pathlib import Path

from db import db


DEFAULTS_PATH = Path(__file__).parent / 'test_defaults.sql'


@pytest.fixture
def test_connection():
    test_conn = db.get_connection(':memory:')
    db.initialize_db(conn=test_conn,defaults_path=DEFAULTS_PATH)
    return test_conn
