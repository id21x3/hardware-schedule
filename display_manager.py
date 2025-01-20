
from flask import Flask, render_template, jsonify
import threading
import logging

class DisplayManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.current_data = {"schedule": None, "notes": None}
        self._setup_routes()
        self._start_server()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/data")
        def data():
            return jsonify(self.current_data)

    def _start_server(self):
        def run():
            logging.info("Starting Flask server for display.")
            self.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
        
        threading.Thread(target=run, daemon=True).start()

    def show_message(self, message):
        self.current_data = {"schedule": None, "notes": {"note": message}}
        logging.info(f"DisplayManager: Showing message: {message}")

    def show_schedule(self, schedule_data):
        self.current_data["schedule"] = schedule_data
        logging.info(f"DisplayManager: Updated schedule: {schedule_data}")

    def show_notes(self, notes_data):
        self.current_data["notes"] = notes_data
        logging.info(f"DisplayManager: Updated notes: {notes_data}")
