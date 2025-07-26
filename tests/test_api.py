from src.setup_db import init_db
import http.client
import json
from datetime import datetime
from email.utils import parsedate_to_datetime

def make_connection():
    return http.client.HTTPConnection("127.0.0.1", 5000)

def send_request(method, path, body=None, headers=None):
    conn = make_connection()
    try:
        conn.request(method, path, body, headers or {}) #headers cant be none, it will try to iterate it
        return conn.getresponse()
    finally:
        conn.close()

def parse_date(raw_date):
    return parsedate_to_datetime(raw_date).replace(tzinfo=None)

def assert_event_match(event, expected_title, expected_date_iso):
    expected_date = datetime.fromisoformat(expected_date_iso)
    actual_date = parse_date(event["date"])
    if event["title"] != expected_title or actual_date != expected_date:
        print("Mismatch:")
        print("Title: expected =", expected_title, "actual =", event["title"])
        print("Date: expected =", expected_date, "actual =", actual_date)
        return False
    return True

def test_post_get():
    init_db()
    print("Start post followed by get test")

    title = "Testing event"
    date = "2025-07-26T11:58:00"
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"title": title, "date": date})

    response = send_request("POST", "/events", body=body, headers=headers)
    print("POST /events status:", response.status)
    if response.status != 201:
        print("POST failed")
        return False
    print("Test post is success")

    response = send_request("GET", "/events")
    if response.status != 200:
        print("GET /events failed:", response.status)
        return False
    event_list = json.loads(response.read().decode("utf-8"))
    if not event_list:
        print("No events returned")
        return False
    event = event_list[0]
    if not assert_event_match(event, title, date):
        return False
    print("GET /events is success")

    # GET /events/{id}
    event_id_path = f"/events/{event['id']}"
    response = send_request("GET", event_id_path)
    if response.status != 200:
        print(f"GET {event_id_path} failed:", response.status)
        return False
    event = json.loads(response.read().decode("utf-8"))
    if not assert_event_match(event, title, date):
        return False
    print(f"GET {event_id_path} is success")

    print("Successfully finished post followed by get test")
    return True

if __name__ == "__main__":
    test_post_get()