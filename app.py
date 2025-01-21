# Flask Application (app.py)
from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_folder="static")

# Endpoint to serve the main HTML page
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# API to return schedule data
@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        with open('data/schedule.json', 'r', encoding='utf-8') as file:
            schedule = json.load(file)
        return jsonify(schedule)
    except FileNotFoundError:
        return jsonify([]), 404
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400

# Serve static files (CSS, JS, etc.)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Ensure default schedule exists for testing
    if not os.path.exists('schedule.json'):
        with open('schedule.json', 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    app.run(host='0.0.0.0', port=5000)