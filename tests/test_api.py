import pytest
import http.client
import json
from datetime import datetime
from email.utils import parsedate_to_datetime

from tests.conf_test import send_request

def parse_date(raw_date):
    return parsedate_to_datetime(raw_date).replace(tzinfo=None)

def assert_event_match(event, expected_title, expected_date_iso):
    expected_date = datetime.fromisoformat(expected_date_iso)
    actual_date = parse_date(event["date"])
    assert event["title"] == expected_title, f"Expected title '{expected_title}', got '{event['title']}'"
    assert actual_date == expected_date, f"Expected date '{expected_date}', got '{actual_date}'"

def test_post_and_get_event():
    title = "Testing event"
    date = "2025-07-26T11:58:00"
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"title": title, "date": date})

    # POST /events
    response = send_request("POST", "/events", body=body, headers=headers)
    assert response.status == 201, f"POST failed with status {response.status}"

    # GET /events
    response = send_request("GET", "/events")
    assert response.status == 200, f"GET /events failed with status {response.status}"

    event_list = json.loads(response.read().decode("utf-8"))
    assert len(event_list) > 0, "No events returned from GET /events"

    event = event_list[0]
    assert_event_match(event, title, date)

    # GET /events/{id}
    event_id_path = f"/events/{event['id']}"
    response = send_request("GET", event_id_path)
    assert response.status == 200, f"GET {event_id_path} failed with status {response.status}"

    single_event = json.loads(response.read().decode("utf-8"))
    assert_event_match(single_event, title, date)
