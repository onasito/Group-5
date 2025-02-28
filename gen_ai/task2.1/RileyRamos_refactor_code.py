from http import HTTPStatus

def test_bottom_n_counters(self, client):
    """It should return the bottom N lowest counters"""
    
    # Reset and initialize counters in a structured way
    client.post('/counters/reset')
    for counter in ['a', 'b']:
        client.post(f'/counters/{counter}')

    # Test fetching the single lowest counter
    response = client.get('/counters/bottom/1')
    assert response.status_code == HTTPStatus.OK
    
    json_data = response.get_json()
    assert isinstance(json_data, dict), "Response should be a dictionary"
    
    # Ensure that there is only one result, and it has the expected value
    assert len(json_data) == 1, "Should return exactly one counter"
    assert min(json_data.values()) == 0, "Lowest counter value should be 0"
    
    # Test fetching the bottom 2 counters
    response = client.get('/counters/bottom/2')
    assert response.status_code == HTTPStatus.OK

    json_data = response.get_json()
    assert isinstance(json_data, dict), "Response should be a dictionary"
    
    # Ensure 'b' is in the bottom 2 counters
    assert 'b' in json_data, "'b' should be in the returned bottom 2 counters"

    # Verify that counters are sorted in ascending order
    sorted_values = list(json_data.values())
    assert sorted_values == sorted(sorted_values), "Counters should be sorted in ascending order"
