import psycopg2
import os
from dotenv import load_dotenv

# first try read setup sql
try:
    with open("events.sql", "r") as file:
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
    print(f"Database error: {e}")
    exit(1)

# close connections
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()