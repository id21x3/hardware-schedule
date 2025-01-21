import json
import threading

from app_state import AbstractState
from mqtt_service import MQTTService


class MQTTState(AbstractState):
    def __init__(self, app):
        super().__init__(app)
        self.mqtt_service = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def execute(self):
        print("Executing MQTT state.")
        config = self.app.config

        self.mqtt_service = MQTTService(
            broker=config["mqtt_broker"],
            port=config["mqtt_port"],
            username=config["mqtt_username"],
            password=config["mqtt_password"]
        )

        self.mqtt_service.connect()
        self.mqtt_service.subscribe("gw/monitor/id21x3rasbery-monitor", self.on_message)

        print("MQTT client started in background.")
        self.mqtt_service.start()

        try:
            while not self.stop_event.is_set():
                self.stop_event.wait(timeout=1)
        except Exception as e:
            print(f"Error in MQTTState: {e}")
        finally:
            print("Stopping MQTTState...")
            self.mqtt_service.stop()

    def on_message(self, client, userdata, message):
        print(f"Message received on topic {message.topic}: {message.payload.decode()}")
        try:
            data = json.loads(message.payload.decode())
            with self.lock:
                with open('data/schedule.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            print("Schedule updated and saved to data/schedule.json")
        except Exception as e:
            print(f"Error processing message: {e}")