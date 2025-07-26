DROP TABLE IF EXISTS events_active CASCADE;
DROP TABLE IF EXISTS events_past CASCADE;
DROP SEQUENCE IF EXISTS events_id;

CREATE SEQUENCE events_id; --active and past table should have unique ids so that union view doesnt have duplicates

CREATE TABLE events_active (
    id INT PRIMARY KEY DEFAULT nextval('events_id'),
    title TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL
);

CREATE TABLE events_past (
    id INT PRIMARY KEY DEFAULT nextval('events_id'),
    title TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL
);

DROP VIEW IF EXISTS events_all;
CREATE VIEW events_all AS
SELECT id, title, event_time FROM events_active
UNION ALL
SELECT id, title, event_time FROM events_past;