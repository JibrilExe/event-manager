DROP TABLE IF EXISTS events_active;
CREATE TABLE events_active (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS events_past;
CREATE TABLE events_past (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL,
);

DROP VIEW IF EXISTS events_all;
CREATE VIEW events_all AS
SELECT id, title, event_time FROM events_active
UNION ALL
SELECT id, title, event_time FROM events_past;