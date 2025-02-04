"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

# Code from class website (needed to make sure counter exists)
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if name in COUNTERS:
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

# New code 
# Get counter function
@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Finds counter"""
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED