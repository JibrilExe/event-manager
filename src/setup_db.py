import psycopg2
import os
from .get_db_connection import get_connection

def init_db():
    """
    Tries to run events.sql on the database,
    which should setup the needed tables and view
    """
    try:
        # get the absolute path to avoid relative path issue when using init_db from test folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(base_dir, "events.sql")

        with open(sql_path, "r") as file:
            sql = file.read()
    except FileNotFoundError:
        print("Setup file not found, should be named events.sql")
        exit(1)
    except IOError as e:
        print(e)
        exit(1)

    # then try to connect with db and setup the tables
    try:
        connection = get_connection()
        cur = connection.cursor()

        # assumes one sql setup file with instruction seperated by ;
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt + ";")

        connection.commit()
        print("SQL setup done")

    except psycopg2.Error as e:
        print(f"Database setup error: {e}")
        exit(1)

    # close connections
    finally:
        cur.close()
        connection.close()

if __name__ == "__main__":
    init_db()