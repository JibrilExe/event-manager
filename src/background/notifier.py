from time import sleep
from ..controllers.event import EventService
from datetime import datetime, timedelta

# This background worker will query the active events table every 10 seconds
# and send notifications for the events that are within 5 minutes, if this
# is the case, they are also moved to the past database

if __name__ == "__main__":
    subscribers = ["Jef", "Katy", "Borogrove"] # idea is that we can have multiple instances of notifiers workers
    # with each their list of subscribers

    event_service = EventService()
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
