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
from src import app
from src import status

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
        assert result.status_code == status.HTTP_201_CREATED
    
    # Harrison Atherton
    def test_reset_all_counters(self, client):
        """Reset all counters to zero"""

        # Create two counters
        client.post('/counters/foo')
        client.post('/counters/bar')
        client.put('/counters/foo')  # Increment foo

        # Verify that the counters exist before resetting
        foo_response = client.get('/counters/foo')
        assert foo_response.status_code == status.HTTP_200_OK  # Ensure it exists

        # Reset all counters
        response = client.post('/counters/reset')
        assert response.status_code == status.HTTP_200_OK

        # Verify all counters are reset
        foo_response = client.get('/counters/foo')
        bar_response = client.get('/counters/bar')

        assert foo_response.status_code == status.HTTP_200_OK
        assert bar_response.status_code == status.HTTP_200_OK

        assert foo_response.get_json() == {"foo": 0}
        assert bar_response.get_json() == {"bar": 0}