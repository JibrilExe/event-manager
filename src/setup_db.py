import psycopg2

# first try read setup sql
try:
    with open("events.sql", "r") as file:
        sql = file.read()
except FileNotFoundError:
    print("Setup file not found")
    exit(1)
except IOError as e:
    print(e)
    exit(1)

# then try to connect with db and setup the tables
try:
    conn = psycopg2.connect( #assumes database name and user and password and address to psql server, need to make setting file or..
        dbname="eventmanager",
        user="postgres",
        password="Ce+Me2000",
        host="localhost",
        port="5432"
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