""" Counter API implmentation """
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Update a counter but check if it exists"""
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND

    return jsonify({"message": "Counter exists"}), status.HTTP_200_OK