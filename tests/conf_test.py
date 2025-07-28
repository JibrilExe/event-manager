import pytest
import http.client
from src.setup_db import init_db

@pytest.fixture(scope="function", autouse=True)
def reset_database():
    init_db()

def make_connection():
    return http.client.HTTPConnection("127.0.0.1", 5000)

def send_request(method, path, body=None, headers=None):
    conn = make_connection()
    try:
        conn.request(method, path, body, headers or {})
        return conn.getresponse()
    finally:
        conn.close()
