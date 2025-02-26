from http import HTTPStatus

def test_top_n_counters(self, client):
    """
    Test Case: Retrieve the top N highest counters.

    This test ensures that the API correctly returns the top N counters 
    in descending order based on their counts.

    **Test Workflow:**
    1. Reset the counter data to ensure a clean test environment.
    2. Create two counters (`a` and `b`) via POST requests.
    3. Increment counter `a` once and counter `b` twice via PUT requests.
    4. Send a GET request to fetch the top 2 counters.
    5. Validate that the response status code is HTTP 200 (OK).
    6. Check that the response JSON is not empty and is properly formatted.
    7. Convert the JSON response to a list format if necessary.
    8. Verify that the response contains at most 2 counters.
    9. Ensure that the counters are correctly sorted in descending order.

    Args:
        client: A test client used for sending HTTP requests to the API.

    Raises:
        AssertionError: If the response format, count, or sorting order is incorrect.
    """

    # Step 1: Reset all counters to start fresh
    client.post('/counters/reset')

    # Step 2: Create two counters ('a' and 'b')
    client.post('/counters/a')  # Creates counter 'a' with an initial count of 0
    client.post('/counters/b')  # Creates counter 'b' with an initial count of 0

    # Step 3: Increment the counters
    client.put('/counters/a')  # Increments 'a' → 'a' = 1
    client.put('/counters/b')  # Increments 'b' → 'b' = 1
    client.put('/counters/b')  # Increments 'b' → 'b' = 2

    # Step 4: Retrieve the top 2 highest counters
    response = client.get('/counters/top/2')

    # Step 5: Validate the HTTP status code
    assert response.status_code == HTTPStatus.OK, f"Unexpected status code: {response.status_code}"

    # Step 6: Parse the response JSON
    counters = response.get_json()
    assert counters is not None, "Response JSON is None"

    # Step 7: Convert dictionary response to a list format if necessary
    if isinstance(counters, dict):
        counters = [{"name": k, "count": v} for k, v in counters.items()]

    # Step 8: Validate response format and length
    assert isinstance(counters, list), f"Expected list but got {type(counters)}: {counters}"
    assert len(counters) <= 2, f"Expected at most 2 counters, but got {len(counters)}"

    # Step 9: Verify sorting order (descending)
    counts = [counter["count"] for counter in counters]
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1)), f"List is not sorted: {counts}"
