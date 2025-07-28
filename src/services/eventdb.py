# service for db queries
from datetime import datetime, timedelta, timezone
import psycopg2
from ..models.event import Event
from ..get_db_connection import get_connection

def generic_query_executor(query, params, handler, insert=False):
    """
    Generic function to help us execute queries without code duplication
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            if insert:
                conn.commit()
                return 201
            return handler(cur)
    except psycopg2.Error as e:
        print(f"database query failed: {e}")
        if conn:
            conn.rollback()
        return None, 500
    finally:
        if conn:
            conn.close()

def handler_get(cur):
    """
    Handler for get by id result
    """
    row = cur.fetchone()
    if not row:
        return None, 404
    return Event(id=row[0], title=row[1], date=row[2]), 200

def handler_get_all(cur):
    """
    Handler for get all result
    """
    rows = cur.fetchall()
    return [Event(id=r[0], title=r[1], date=r[2]) for r in rows], 200

def get_event_by_id(id):
    """
    Get event with id
    """
    query = "SELECT id, title, event_time FROM events_all WHERE id = %s"
    params = (id,)
    print("getting by id")
    return generic_query_executor(query, params, handler_get)

def get_all_events():
    """
    Get all the events.
    """
    query = "SELECT id, title, event_time FROM events_all"
    return generic_query_executor(query, (), handler_get_all)

def insert_event(event: Event):
    """
    Create new events.
    If past 5 minute mark, moved into events_past otherwise events_active
    """
    now = datetime.now(timezone.utc)
    five_minutes_further = now + timedelta(minutes=5)
    params = (event.title, event.date)
    query = "INSERT INTO "
    if event.date <= five_minutes_further:
        query += "events_past"
    else:
        query += "events_active"
    query += " (title, event_time) VALUES (%s, %s)"

    return generic_query_executor(query, params, None, True)

def get_active():
    """
    Get all the active events
    """
    query = "SELECT id, title, event_time FROM events_active"
    return generic_query_executor(query, (), handler_get_all)

def active_to_past(event):
    """
    Move an active event to the past table
    """
    generic_query_executor("DELETE FROM events_active WHERE id = %s", (event.id,), None, True)
    generic_query_executor("INSERT INTO events_past (title, event_time) VALUES (%s, %s)", (event.title, event.date), None, True)