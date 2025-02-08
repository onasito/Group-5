import pytest
from src import app
from src import status


@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCOunterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED
# ===========================
# Test: Handle invalid HTTP methods
# Author: William
# Date: 2025-07-1
# Description: test for unsupported Http methods
# ===========================
@pytest.mark.usefixtures("client")
def test_Invalid_HTTP(client):
    methodsNotAllowed = client.patch('/test/route')
    assert methodsNotAllowed.status_code == 405
