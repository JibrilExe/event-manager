# service for db queries
import psycopg2
from ..models.event import Event
from datetime import datetime, timedelta
from ..get_db_connection import get_connection

class EventService:
    def __init__(self):
        pass

    def get_event(self, id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_all WHERE id = %s", (id,))
                row = cur.fetchone()
                if not row:
                    return None
                return Event(id=row[0], title=row[1], date=row[2])
        except psycopg2.Error as e:
            print(f"get_event failed: {e}")
            return None
        finally:
            conn.close()

    def get_active(self):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_active")
                rows = cur.fetchall()
                return [Event(id=r[0], title=r[1], date=r[2]) for r in rows]
        except psycopg2.Error as e:
            print(f"get_active failed: {e}")
            return []
        finally:
            conn.close()

    def active_to_past(self, event):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM events_active WHERE id = %s", (event.id,))
                cur.execute(
                    "INSERT INTO events_past (title, event_time) VALUES (%s, %s)",
                    (event.title, event.date)
                )
            conn.commit()
        except psycopg2.Error as e:
            print(f"active_to_past failed: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_all_events(self):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_all")
                rows = cur.fetchall()
                return [Event(id=r[0], title=r[1], date=r[2]) for r in rows]
        except psycopg2.Error as e:
            print(f"get_all_events failed: {e}")
            return []
        finally:
            conn.close()

    def post_event(self, event: Event):
        now = datetime.now()
        five_minutes_further = now + timedelta(minutes=5)
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                if event.date <= five_minutes_further:
                    cur.execute(
                        "INSERT INTO events_past (title, event_time) VALUES (%s, %s)",
                        (event.title, event.date),
                    )
                else:
                    cur.execute(
                        "INSERT INTO events_active (title, event_time) VALUES (%s, %s)",
                        (event.title, event.date),
                    )
            conn.commit()
        except psycopg2.Error as e:
            print(f"post_event failed: {e}")
            conn.rollback()
        finally:
            conn.close()
