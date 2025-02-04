"""
Counter API Implementation
"""
from flask import Flask, jsonify
from http import HTTPStatus

app = Flask(__name__)

COUNTERS = {}

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), HTTPStatus.CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), HTTPStatus.CREATED

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS