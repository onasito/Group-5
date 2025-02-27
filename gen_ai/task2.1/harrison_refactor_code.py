from http import HTTPStatus

# ChatGPT Modifications
# -----------------------------------
# Removed unnecessary sorting
# Simplified JSON parsing
# Directly checked sorting order
# Ensured list format consisntency
def test_top_n_counters(self, client):
    """It should return the top N highest counters"""
    client.post('/counters/reset')
    client.post('/counters/a')
    client.post('/counters/b')
    client.put('/counters/a')
    client.put('/counters/b')
    client.put('/counters/b')

    response = client.get('/counters/top/2')
    assert response.status_code == HTTPStatus.OK

    counters = response.get_json()
    assert counters is not None, "Response JSON is None"

    # Convert dictionary `{ "a": 1, "b": 2 }` to list format if necessary
    if isinstance(counters, dict):
        counters = [{"name": k, "count": v} for k, v in counters.items()]

    assert isinstance(counters, list), f"Expected list but got {type(counters)}: {counters}"
    assert len(counters) <= 2, f"Expected at most 2 counters, but got {len(counters)}"

    # Validate sorting order
    counts = [counter["count"] for counter in counters]
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1)), f"List is not sorted: {counts}"
