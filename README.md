# Event manager
Simple concept for an API that lets you register upcoming events, and will notify you when it is about to take place.  
[API docs](https://docs.google.com/document/d/1ohPlJFXRNphhnBTpZDh2oHMNYyy1fOdv8vmoBoaKx6w/edit?usp=sharing)

## How to run it

### Without docker
Have postgresql setup and create a .env file in the root of this project.  
Example .env:
```
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5430
```

Built with python 3.15 but also works on 3.12 and possibly even older.
```
pip install -r reqs.txt
```

Set up the database:
```
python -m src.setup_db
```

Run the backend app:
```
python -m src.controllers.event
```

Run the notifier (in another terminal):
```
python -m src.background.notifier
```

## With docker
Navigate to the docker folder.
docker-compose up

## Testing
Simple test setup didn't use a framework

```
python -m tests.test_all
```

## Example usage of API:
```
curl -Method POST http://127.0.0.1:5000/events -Headers @{"Content-Type"="application/json"} -Body '{"title":"My Event","date":"2025-07-27T11:18:00"}'
```
```
curl http://127.0.0.1:5000/events
```

## Weak points (if we have to support a lot of users):
Current system has no proper scaling, depending on server, one controller won't be enough, people would get longer waiting times and possibly timeouts.
Database and logs would take up too much memory and containers won't start.
Current notifier system would face massive delays having to iterate all the active events sequentially, resulting in notifications being sent too late.

## If I had more time:
Make better use of Docker or switch to Kubernetes but make it so the system never goes down. 
Changing notifier into a proper scalable broker system like Kafka for example.
Proper tests for all functionality integrated into github for automated testing on commits.
Extended API with more status codes and better error names.
Background workers to clean up docker logs and possibly database if they get too full.
Horizontal scaling setup to simulate a database per region or group of users.
