import os
from time import sleep
from dotenv import load_dotenv
import psycopg2
from ..controllers.event import EventService
from datetime import datetime, timedelta

# This background worker will query the active events table every 10 seconds
# and send notifications for the events that are within 5 minutes, if this
# is the case, they are also moved to the past database

if __name__ == "__main__":

    subscribers = ["Jef", "Katy", "Borogrove"] # idea is that we can have multiple instances of notifiers workers
    # with each their list of subscribers

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
    event_service = EventService(conn)

    delta_fivemin = timedelta(minutes=5)

    while True:
        sleep(10)
        now = datetime.now()
        five_minutes_further = now + delta_fivemin
        active_events = event_service.get_active()
        for event in active_events:
            if event.date <= five_minutes_further:
                print(f"notify subscribers {event.title} {event.date} {event.id}")
                event_service.active_to_past(event)
