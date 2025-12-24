from gui.app import run
from db.db import get_connection, initialize_db


def main():
    connection = get_connection()
    initialize_db(connection)
    run(connection)


if __name__ == "__main__":
    main()
