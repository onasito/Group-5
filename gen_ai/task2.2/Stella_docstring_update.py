from http import HTTPStatus

"""Test case to verify the total number of counters.
This test ensures that after adding two counters, the endpoint correctly 
returns the expected count value.
"""

def test_get_total_number_of_counters(self, client):
    # Reset all counters to start from a clean state
    client.post('/counters/reset')
    
    # Add two test counters
    client.post('/counters/test1')
    client.post('/counters/test2')

    # Retrieve the total count of counters
    response = client.get('/counters/count')

    # Ensure the request was successful
    assert response.status_code == HTTPStatus.OK

    # Verify that the returned count is an integer
    assert isinstance(response.get_json()["count"], int)  

    # Add an assertion to check the exact count value dynamically
    assert response.get_json()["count"] == 2  # Expecting exactly 2 counters
