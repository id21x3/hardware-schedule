import json

from app_state import AbstractState
from flask_state import FlaskState
from mqtt_service import MQTTService
from data_manager import DataManager

class MQTTState(AbstractState):
    def __init__(self, app):
        super().__init__(app)
        self.mqtt_service = None
        self.data_manager = DataManager()

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
        self.mqtt_service.subscribe("schedule/room1", self.on_message)
        self.mqtt_service.start()

        print("MQTT setup complete. Transitioning to FlaskState.")
        self.app.state = FlaskState(self.app)

    def on_message(self, client, userdata, message):
        print(f"Message received on topic {message.topic}: {message.payload.decode()}")
        try:
            schedule_data = self.data_manager.load_data("data/schedule.json") or [[] for _ in range(7)]
            updated_data = self.process_message(schedule_data, message.payload.decode())
            self.data_manager.save_data("data/schedule.json", updated_data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def process_message(self, current_schedule, new_data):
        try:
            new_schedule = json.loads(new_data)
            for day_index, lessons in enumerate(new_schedule):
                if day_index < len(current_schedule):
                    current_schedule[day_index] = lessons
            return current_schedule
        except json.JSONDecodeError as e:
            print(f"Invalid JSON format in message: {e}")
            return current_schedule

    def __del__(self):
        if self.mqtt_service:
            self.mqtt_service.stop()