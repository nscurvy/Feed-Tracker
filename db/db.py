import sqlite3 as sql
from pathlib import Path
from typing import Optional


DB_PATH = Path(__file__).parent.parent / 'data' / 'FeedTracker.db'
SCHEMA_PATH = Path(__file__).parent / 'schema.sql'
DEFAULTS_PATH = Path(__file__).parent / 'defaults.sql'


def get_connection(db_path: Path | str = DB_PATH) -> sql.Connection:
    """Create a connection to a SQLite3 database with foreign keys enabled."""
    if str(db_path) == ':memory:':
        conn = sql.connect(db_path)
    else:
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sql.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sql.Row
    return conn


def get_schema_version(conn: sql.Connection) -> Optional[int]:
    version = conn.execute('SELECT value FROM schema_meta WHERE key = ?', ('schema_version',)).fetchone()
    return int(version[0]) if version else None


def initialize_db(conn: sql.Connection,
                  schema_path: Path | str = SCHEMA_PATH,
                  defaults_path: Path | str = DEFAULTS_PATH):
    """Initialize the given database connection with the path specified by schema_path."""
    schema_path = Path(schema_path)
    defaults_path = Path(defaults_path)
    if not get_schema_version(conn):
        with conn:
            if schema_path.exists():
                conn.executescript(schema_path.read_text())
            else:
                raise FileNotFoundError(f'Schema path {str(schema_path)} does not exist.')
            if defaults_path.exists():
                conn.executescript(defaults_path.read_text())
            else:
                raise FileNotFoundError(f'Defaults Path {str(defaults_path)} does not exist.')
