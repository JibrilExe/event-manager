import json
from datetime import datetime, timedelta, timezone
from time import sleep
from src.services.eventdb import get_active
from tests.conf_test import send_request

def test_notifier_moves_event_to_past():
    utc_now = datetime.now(timezone.utc)
    event_time = utc_now + timedelta(minutes=5, seconds=5)

    event_data = {
        "title": "Test Event 5 min and 5 sec ahead",
        "date": event_time.isoformat()
    }

    body = json.dumps(event_data)
    headers = {"Content-Type": "application/json"}

    response = send_request("POST", "/events", body=body, headers=headers)
    assert response.status == 201, "Failed to POST event"

    active_events = get_active()[0]
    assert active_events, "No active events found after insert"

    event = active_events[0]
    assert event.title == event_data["title"], "Event title mismatch"

    sleep(10)

    active_events = get_active()[0]
    assert len(active_events) == 0, f"Event still active: {active_events}"

    print("Notifier succeeded")
