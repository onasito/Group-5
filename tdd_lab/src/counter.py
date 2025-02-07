"""
Counter API Implementation
"""
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

# Get counter function
@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Finds counter"""
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['GET'])
def check_if_counter_exists(name): 
    if not counter_exists(name): 
        return jsonify({"error": f"Counter {name} doesn't exist"}), status.HTTP_404_NOT_FOUND
    
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
   """Increment a counter"""
   COUNTERS[name] += 1
   return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

