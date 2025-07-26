from flask import Flask, jsonify, request
from ..models.event import Event
import psycopg2
from ..services.eventdb import EventService
from ..get_db_connection import get_connection
from datetime import datetime

connection = get_connection()
event_service = EventService(connection)

app = Flask(__name__)

@app.route("/events/<int:id>", methods=["GET"])
def get_event(id):
    event = event_service.get_event(id)
    return jsonify({
            "id": event.id,
            "title": event.title,
            "date": event.date
        })

@app.route("/events", methods=["GET"])
def get_events():
    events = event_service.get_all_events()
    return jsonify([
        {
            "id": event.id,
            "title": event.title,
            "date": event.date
        }
        for event in events
    ])

@app.route("/events", methods=["POST"])
def post_event():
    data = request.get_json()
    event = Event(title=data["title"], date=datetime.fromisoformat(data["date"]))
    event_service.post_event(event)
    return jsonify({"message": "Event added"}), 201

if __name__ == "__main__":
    app.run(debug=True)
    