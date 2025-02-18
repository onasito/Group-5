"""
Counter API Implementation
"""

from flask import Flask, jsonify
from src import status 

app = Flask(__name__)

COUNTERS ={}
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    '''Create a counter'''
    if name in COUNTERS:
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name:COUNTERS[name]}), status.HTTP_201_CREATED

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS

#code for invalid http
@app.route('/test/route', methods=['POST','GET','DELETE'])
def tmp(route):
  '''checks http methods'''
  if route.request.methods == "POST":
      return
  #test checks PATCH the unsupported HTTP
  if route.request.method == 'PATCH':
    return