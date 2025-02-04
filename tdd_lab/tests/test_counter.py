"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src.counter import app
from http import HTTPStatus

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == HTTPStatus.CREATED

    #Writing failed test case for student 2
    def test_duplicate_counter(self, client):
        """It should return a conflict error if the counter already exists"""
        # Create a counter
        client.post('/counters/bar')
        # Try to create the same counter again
        result = client.post('/counters/bar')
        assert result.status_code == HTTPStatus.CONFLICT
        assert result.get_json() == {"error": "Counter bar already exists"}