from src.setup_db import init_db
import http.client
import json
from datetime import datetime
from email.utils import parsedate_to_datetime

def test_post_get():
    init_db() #gives us a fresh db
    print("Start post followed by get test")

    title = "Testing event"
    date = "2025-07-26T11:58:00"

    connection = http.client.HTTPConnection("127.0.0.1", 5000)
    headers = {"Content-Type": "application/json"}
    body = json.dumps({
        "title": title,
        "date": date
    })
    try: # test the post endpoint
        connection.request("POST", "/events", body, headers)
        response = connection.getresponse()
        print("Status:", response.status)
        if response.status == 201:
            print("Test post is succes")
        else:
            print("Test post failed, unexpected status:", response.status)
            return False
    except Exception as e:
        print("Post request failed: ", e)
        return False
    
    try:
        connection.request("GET", "/events")
        response = connection.getresponse()
        if response.status != 200:
            print("Get /events return wrong status: ", response.status)
        event = json.loads(response.read().decode("utf-8"))[0]
        server_date = parsedate_to_datetime(event["date"]).replace(tzinfo=None)
        test_date = datetime.fromisoformat(date)
        if event["title"] != title or server_date != test_date:
            print("Get returned wrong event: ", event)
            print(event["title"], title)
            print(server_date, test_date)
            return False
        print("Get /events is succes")
    except Exception as e:
        print("Get request failed: ", e)
        return False
    
    id = event["id"]
    try:
        event_id_path = f"/events/{id}"
        connection.request("GET", event_id_path)
        response = connection.getresponse()
        if response.status != 200:
            print(f"Get {event_id_path} failed, wrong status code: ", response.status)
        event = json.loads(response.read().decode("utf-8"))
        server_date = parsedate_to_datetime(event["date"]).replace(tzinfo=None)
        test_date = datetime.fromisoformat(date)
        if event["title"] != title or server_date != test_date:
            print("Get returned wrong event: ", event)
            print(event["title"], title)
            print(server_date, test_date)
            return False
        print(f"Get {event_id_path} is succes")
    except Exception as e:
        print("Get request failed: ", e)
        return False

    print("Succesfully finished post followed by get test")

if __name__ == "__main__":
    test_post_get()