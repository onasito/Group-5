# ChatGPT AI Task 2.1: Refactor Code
# ===========================
# Test: Retrieve counters with values less than a threshold
# Author: Student 10
# Modification: Ensure threshold is exclusive.
# ===========================

def test_counters_less_than_threshold(self, client):
    """Test that counters with values strictly less than the threshold are returned."""

    # Reset counters and set initial values
    client.post('/counters/reset')
    client.post('/counters/a')
    client.post('/counters/b')
    client.put('/counters/a/set/5')
    client.put("/counters/b/set/2")

    # Request counters with values less than 5
    response = client.get('/counters/less/5')

    # Ensure the response status is OK
    assert response.status_code == HTTPStatus.OK

    # Parse the response JSON
    counters = response.get_json()

    # Verify that 'b' is the only counter with value 2 (the only one below threshold 5)
    assert 'b' in counters
    assert counters['b'] == min(counters.values())  # Ensure 'b' has the lowest value
    assert counters['b'] < 5  # Ensure that 'b' is strictly less than the threshold
