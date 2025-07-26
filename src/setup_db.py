import psycopg2
import os
from dotenv import load_dotenv

def init_db():
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
        # assumes that we have required params in .env file
        load_dotenv()
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")

        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        cur = conn.cursor()

        # assumes one sql setup file with instruction seperated by ;
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt + ";")

        conn.commit()
        print("SQL setup done")

    except psycopg2.Error as e:
        print(f"Database setup error: {e}")
        exit(1)

    # close connections
    finally:
        cur.close()
        conn.close()