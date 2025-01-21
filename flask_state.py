from flask import Flask, jsonify, send_from_directory, render_template
import os
import json

class FlaskState:
    def __init__(self):
        self.app = Flask(__name__, static_folder="static")

    def execute(self):
        print("Starting Flask server state.")
        @self.app.route('/')
        def index():
            return send_from_directory(self.app.static_folder, 'index.html')

        @self.app.route('/api/schedule', methods=['GET'])
        def get_schedule():
            try:
                with open('data/schedule.json', 'r', encoding='utf-8') as file:
                    schedule = json.load(file)
                return jsonify(schedule)
            except FileNotFoundError:
                return jsonify([]), 404

        @self.app.route('/static/<path:path>')
        def serve_static(path):
            return send_from_directory(self.app.static_folder, path)

        if not os.path.exists('data/schedule.json'):
            with open('data/schedule.json', 'w', encoding='utf-8') as file:
                json.dump([[] for _ in range(7)], file, ensure_ascii=False, indent=4)

        print("Running Flask app on 0.0.0.0:5000.")
        self.app.run(host='0.0.0.0', port=5000)

