# display_manager.py

from flask import Flask, render_template
import threading
import logging

app = Flask(__name__)

# Глобальные переменные для хранения данных
schedule_data = {}
notes_data = {}

@app.route("/")
def index():
    """Основной маршрут для отображения расписания и заметок."""
    return render_template("index.html", schedule=schedule_data, notes=notes_data)

class DisplayManager:
    def __init__(self):
        pass

    def run_server(self):
        """Запускает Flask-сервер в отдельном потоке."""
        def flask_thread():
            logging.info("Запуск Flask-сервера для отображения на 0.0.0.0:5000")
            app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

        thread = threading.Thread(target=flask_thread, daemon=True)
        thread.start()

    def update_schedule(self, new_schedule):
        """Обновляет данные о расписании для Flask."""
        global schedule_data
        schedule_data = new_schedule
        logging.info(f"Данные расписания обновлены: {schedule_data}")

    def update_notes(self, new_notes):
        """Обновляет данные о заметках для Flask."""
        global notes_data
        notes_data = new_notes
        logging.info(f"Данные заметок обновлены: {notes_data}")
