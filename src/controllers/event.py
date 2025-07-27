from flask import Flask, jsonify, request
from ..models.event import Event
from ..services.eventdb import EventService
from datetime import datetime, timezone

event_service = EventService()

app = Flask(__name__)

@app.route("/events/<int:id>", methods=["GET"])
def get_event(id):
    event, statuscode = event_service.get_event(id)
    json = {}
    if event is None:
        if statuscode == 404:
            json = {"error": "Event not found"}
        else:
            json = {"error": "Internal failure"}
    else:
        json = {
            "id": event.id,
            "title": event.title,
            "date": event.date
        }

    return jsonify(json), statuscode

@app.route("/events", methods=["GET"])
def get_events():
    events, statuscode = event_service.get_all_events()
    json = [
        {
            "id": event.id,
            "title": event.title,
            "date": event.date
        }
        for event in events
    ]
    return jsonify(json), statuscode

@app.route("/events", methods=["POST"])
def post_event():
    data = request.get_json()
    naive_dt = datetime.fromisoformat(data["date"]) #always convert to utc to be sure of internal timezone
    aware_dt = naive_dt.replace(tzinfo=timezone.utc) if naive_dt.tzinfo is None else naive_dt.astimezone(timezone.utc)

    event = Event(title=data["title"], date=aware_dt)
    statuscode = event_service.post_event(event)
    if statuscode == 201:
        return jsonify({"message": "Event added"}), statuscode
    else:
        return jsonify({"error": "Event creation failed"}), statuscode

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    