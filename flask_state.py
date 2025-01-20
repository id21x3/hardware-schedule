from app_state import AbstractState
from flask import Flask, jsonify, send_from_directory
import os
import json

class FlaskState(AbstractState):
    def execute(self):
        print("Starting Flask server state.")

        app = Flask(__name__, static_folder="static")

        @app.route('/')
        def index():
            return send_from_directory(app.static_folder, 'index.html')

        @app.route('/api/schedule', methods=['GET'])
        def get_schedule():
            try:
                with open('data/schedule.json', 'r', encoding='utf-8') as file:
                    schedule = json.load(file)
                return jsonify(schedule)
            except FileNotFoundError:
                return jsonify([[] for _ in range(7)]), 404
            except json.JSONDecodeError as e:
                return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400

        @app.route('/static/<path:path>')
        def serve_static(path):
            return send_from_directory(app.static_folder, path)

        if not os.path.exists('data/schedule.json'):
            with open('data/schedule.json', 'w', encoding='utf-8') as file:
                json.dump([[] for _ in range(7)], file, ensure_ascii=False, indent=4)

        app.run(host='0.0.0.0', port=5000)