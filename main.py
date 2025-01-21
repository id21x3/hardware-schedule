import threading
import signal
import sys
from flask_state import FlaskState
from mqtt_state import MQTTState
from config_loader import ConfigLoader

DEVICE_CONFIG_PATH = "config/device_config.json"

class Application:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = ConfigLoader.load_config(self.config_path)
        self.stop_event = threading.Event()

    def run_flask(self):
        flask_state = FlaskState()
        flask_state.execute()

    def run_mqtt(self):
        mqtt_state = MQTTState(self)
        mqtt_state.stop_event = self.stop_event  # Передаём общий stop_event
        mqtt_state.execute()

    def stop(self):
        print("\nStopping application...")
        self.stop_event.set()  # Устанавливаем флаг остановки
        sys.exit(0)  # Завершаем программу

    def run(self):
        flask_thread = threading.Thread(target=self.run_flask, daemon=True)
        mqtt_thread = threading.Thread(target=self.run_mqtt, daemon=True)

        flask_thread.start()
        mqtt_thread.start()

        signal.signal(signal.SIGINT, lambda sig, frame: self.stop())  # Обрабатываем Ctrl+C

        flask_thread.join()
        mqtt_thread.join()

if __name__ == "__main__":
    app = Application(DEVICE_CONFIG_PATH)
    app.run()
