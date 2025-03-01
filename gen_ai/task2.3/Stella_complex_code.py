from flask import Flask, jsonify
from . import status
from threading import Lock 

app = Flask(__name__)
COUNTERS = {}
COUNTERS_LOCK = Lock()  # Ensure thread safety

@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Increment a counter"""
    # Inccrement counter with lock to prevent race conditions
    with COUNTERS_LOCK:  
        # Verify name before checking ounter
        if name not in COUNTERS:
            COUNTERS[name] = 0 # Initialize counter

        COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK