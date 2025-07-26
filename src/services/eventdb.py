# service for db queries
import psycopg2
from ..models.event import Event
from datetime import datetime, timedelta

class EventService:
    def __init__(self, db_conn):
        self.conn = db_conn

    def get_event(self, id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_all WHERE id = %s",(id,))
                row = cur.fetchall()[0]
                return Event(id=row[0], title=row[1], date=row[2])
        except psycopg2.Error as e:
            #logging.error("get for " + str(id) + "failed")
            return Event(id=id, tile="failed", date=datetime.now())

    def get_active(self): #TODO: code cleanup, merge duplicates
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_active")
                rows = cur.fetchall()
                return [Event(id=r[0], title=r[1], date=r[2]) for r in rows]
        except psycopg2.Error as e:
            #logging.error("getting actives failed")
            return []

    def active_to_past(self, event):
        try:
            with self.conn.cursor() as cur:
                # delete from events_active
                cur.execute("DELETE FROM events_active WHERE id = %s", (event.id,))
                # insert into events_past
                cur.execute(
                    "INSERT INTO events_past (title, event_time) VALUES (%s, %s)",
                    (event.title, event.date)
                )
                self.conn.commit()
        except psycopg2.Error as e:
            #logging.error(f"moving event to past failed: {e}")
            print(e)
            self.conn.rollback()

    def get_all_events(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, title, event_time FROM events_all")
                rows = cur.fetchall()
                return [Event(id=r[0], title=r[1], date=r[2]) for r in rows]
        except psycopg2.Error as e:
            #logging.error("getting failed")
            return []

    def post_event(self, event: Event):
        now = datetime.now()
        five_minutes_further = now + timedelta(minutes=5)

        try:
            with self.conn.cursor() as cur:
                if event.date <= five_minutes_further:
                    cur.execute("""
                        INSERT INTO events_past (title, event_time)
                        VALUES (%s, %s)
                    """, (event.title, event.date))
                else:
                    cur.execute("""
                        INSERT INTO events_active (title, event_time)
                        VALUES (%s, %s)
                    """, (event.title, event.date))

            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            #logging.error(f"error while inserting event: {e}")
            