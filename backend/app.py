# app.py
from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

def load_facilities():
    facilities = []
    with open('data/facilities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            facilities.append(row)
    return facilities

@app.route('/api/services')
def get_services():
    facilities = load_facilities()
    services = set()
    for f in facilities:
        services.update(f['services'].split(';'))
    return jsonify(sorted(list(services)))

@app.route('/api/facilities')
def get_facilities():