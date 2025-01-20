
import json
import logging
import time
import random

class FakeMqtt:
    def __init__(self, room_id, message_delay=5):
        self.room_id = room_id
        self.last_message = None
        self.message_delay = message_delay

        # Initial test data
        self._test_schedule = [
            {"time": "08:00-08:45", "subject": "Math", "teacher": "Dr. Smith", "room": "101"},
            {"time": "09:00-09:45", "subject": "Physics", "teacher": "Dr. Doe", "room": "102"}
        ]
        self._test_notes = [
            {"note": "Exam tomorrow at 10 AM."},
            {"note": "Classroom changed to Room 203."}
        ]

        self.schedule_data = None
        self.notes_data = None

    def connect(self):
        """Simulates a successful connection."""
        logging.info("Fake MQTT: Successfully connected (stub mode).")

    def generate_schedule_message(self):
        """Generates a random schedule message."""
        return {
            "type": "schedule",
            "lessons": random.sample(self._test_schedule, len(self._test_schedule))
        }

    def generate_notes_message(self):
        """Generates a random notes message."""
        return {
            "type": "notes",
            "notes": random.choice(self._test_notes)
        }

    def get_message(self):
        """Simulates receiving messages alternately for schedule and notes."""
        while True:
            if random.choice([True, False]):
                self.schedule_data = self.generate_schedule_message()
                logging.info(f"Fake MQTT: Generated schedule message: {self.schedule_data}")
            else:
                self.notes_data = self.generate_notes_message()
                logging.info(f"Fake MQTT: Generated notes message: {self.notes_data}")
            time.sleep(self.message_delay)
