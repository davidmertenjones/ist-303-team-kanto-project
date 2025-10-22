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
    q = request.args.get('q', '').lower()
    facilities = load_facilities()
    if not q:
        return jsonify(facilities)
    results = []
    for f in facilities:
        # Search by city, name, or zip (case-insensitive)
        if (q in f['city'].lower() or
            q in f['fac_name'].lower() or
            q in f.get('zip', '').lower()):
            results.append(f)
    return jsonify(results)