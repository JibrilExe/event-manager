from time import sleep
from ..services.eventdb import get_active, active_to_past
from datetime import datetime, timedelta, timezone

# This background worker will query the active events table every 10 seconds
# and send notifications for the events that are within 5 minutes, if this
# is the case, they are also moved to the past database

if __name__ == "__main__":
    subscribers = ["Jef", "Katy", "Borogrove"] # idea is that we can have multiple instances of notifiers workers
    # with each their list of subscribers
    delta_fivemin = timedelta(minutes=5)
    while True:
        sleep(5)
        now = datetime.now(timezone.utc)  # always UTC for internal system
        five_minutes_further = now + delta_fivemin
        active_events = get_active()[0]
        for event in active_events:
            if event.date <= five_minutes_further:
                print(f"notify subscribers {event.title} {event.date} {event.id}")
                active_to_past(event)
