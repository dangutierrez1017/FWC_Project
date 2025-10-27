"""
routes.py
---------
This module defines all Flask routes (endpoints) used in the FWRI Key Card
Tracking application. Bridges the web frontend(HTNML/CSS/JS) with the
backend services(keycard_tracker.py) that retrieve and filter keycard entry data.

Endpoints:
- GET /api/entries: Retrieves flattened keycard entries in JSON format based on 
  optional query parameters for employee name and/or date range.
- GET /: Hosts the main HTML page for user interaction in the FWRI Key Card
  Tracking application.


Author: Daniel Gutierrez
Date: 10/25/2025
"""


from flask import Flask, request, jsonify, render_template
from src.services.keycard_tracker import retrieve_information
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), 'src', 'views'), #Set path to the templates folder
    static_folder=os.path.join(os.getcwd(), 'src', 'static')   #Set path to the static folder
)

@app.route('/api/entries', methods=['GET'])
def get_entries():

    #API endpoint getting query parameters from Filter Form request
    name = request.args.get('name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    #Calls the service function from keycard_tracker.py to retrieve filtered data
    results = retrieve_information(name_query = name, start_date = start_date, end_date = end_date) 

    return jsonify(results) #Return the results as a JSON response to be used by frontend datatable.JS

@app.route('/')
def keyCard_entries_page():
    return render_template('index.html')
