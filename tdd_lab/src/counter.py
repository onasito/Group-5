"""
Counter API Implementation
"""

from flask import Flask, jsonify
from src import status  # Importing HTTP status codes

app = Flask(__name__)

# Dictionary to store counter values
COUNTERS = {}

def counter_exists(name):
    """Check if a counter already exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):  # Use helper function
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

# Harrison Atherton
@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters to zero"""
    global COUNTERS
    for key in COUNTERS.keys():
        COUNTERS[key] = 0
    return jsonify({"message": "All counters have been reset"}), status.HTTP_200_OK

# Harrison Atherton
@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve the current value of a counter"""
    if name not in COUNTERS:
        return jsonify({"error": "Counter not found"}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK
