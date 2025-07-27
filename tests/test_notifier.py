from src.setup_db import init_db
from src.services.eventdb import EventService 
import http.client
import json
from datetime import datetime, timezone, timedelta
from time import sleep

def make_connection():
    return http.client.HTTPConnection("127.0.0.1", 5000)

def post_close_to_five_minutes_test():
    init_db()
    utc_now = datetime.now(timezone.utc)
    event_time = utc_now + timedelta(minutes=6)
    event_data = {
        "title": "Test Event 8 min ahead",
        "date": event_time.isoformat()
    }

    body = json.dumps(event_data)
    headers = {"Content-Type": "application/json"}
    conn = make_connection()
    try:
        conn.request("POST", "/events", body=body, headers=headers)
        response = conn.getresponse()
        if response.status != 201:
            return False
        print("Event successfully posted.")
    finally:
        conn.close()
    
    event_service = EventService()
    event = event_service.get_active()[0]

    if event.title != event_data["title"]:
        print("Title wrong")
        return False

    print("Sleeping 2 minutes")
    sleep(120)
    events = event_service.get_active()
    if len(events) > 0:
        print("Notifier failed, did not move event from active to past")
        return False

    print("Notifier succeeded")
    
if __name__ == "__main__":
    post_close_to_five_minutes_test()