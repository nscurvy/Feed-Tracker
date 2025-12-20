import sqlite3 as sql
from pathlib import Path


DB_PATH = Path(__file__).parent.parent / "data" / "FeedTracker.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection(db_path: Path | str = DB_PATH) -> sql.Connection:
    if str(db_path) == ':memory:':
        conn = sql.connect(db_path)
    else:
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sql.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sql.Row
    return conn


def initialize_db(conn: sql.Connection,
                  schema_path: Path | str = SCHEMA_PATH):
    schema_path = Path(schema_path)
    with conn:
        if schema_path.exists():
            conn.executescript(schema_path.read_text())
        else:
            raise FileNotFoundError(f'Schema path {str(schema_path)} does '
                                    f'not exist.')
