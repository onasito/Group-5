from flask import Flask, jsonify, request
from http import HTTPStatus
import heapq  # Import heapq for efficient retrieval of the smallest items

app = Flask(__name__)

# Dictionary to store counters
COUNTERS = {}

@app.route('/counters/bottom/<int:n>', methods=['GET'])
def get_bottom_n_counters(n):
    """
    Retrieve the bottom N lowest counters.
    
    Optimized to use heapq.nsmallest for efficiently finding the N smallest counters,
    which has O(n log k) complexity, compared to the O(n log n) complexity of sorting 
    the entire dictionary.
    
    Args:
        n (int): The number of bottom counters to retrieve.
        
    Returns:
        JSON response with the N lowest counters or an error if no counters are available.
    """
    if not COUNTERS:
        return jsonify({"error": "No counters available"}), HTTPStatus.NOT_FOUND

    # Use heapq.nsmallest to efficiently get the N lowest counters.
    # Explanation of this line:
    # - `COUNTERS.items()` returns an iterable of key-value pairs (name, value) from the COUNTERS dictionary.
    # - `key=lambda item: item[1]` tells heapq to sort the pairs based on the value (item[1]), i.e., the counter values.
    #   This is necessary to ensure that we are sorting based on the values (not the keys) to get the lowest counter values.
    # - `nsmallest(n, ...)` efficiently returns the N smallest items from the iterable (in this case, the N items with 
    #   the smallest counter values). The function uses a heap-based algorithm, which has a time complexity of O(n log k), 
    #   where n is the total number of items in COUNTERS and k is the number of smallest items requested (in this case, N).
    # - `dict(...)` is used to convert the result back into a dictionary format with keys as the counter names 
    #   and values as their respective counter values.
    bottom_n = dict(heapq.nsmallest(n, COUNTERS.items(), key=lambda item: item[1]))

    return jsonify(bottom_n), HTTPStatus.OK
