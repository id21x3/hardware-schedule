
import paho.mqtt.client as mqtt
import json
import logging
import time

class MqttClient:
    def __init__(self, broker, port, room_id, reconnect_delay=5):
        self.broker = broker
        self.port = port
        self.room_id = room_id
        self.client = mqtt.Client()
        self.last_message = None
        self.schedule_data = None
        self.notes_data = None
        self.reconnect_delay = reconnect_delay

        # Topics for subscription
        self.schedule_topic = f"{self.room_id}/schedule"
        self.notes_topic = f"{self.room_id}/notes"

        # Set up MQTT callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT broker {self.broker}:{self.port}.")
            # Subscribe to topics
            client.subscribe(self.schedule_topic)
            client.subscribe(self.notes_topic)
        else:
            logging.error("Failed to connect to MQTT broker, return code %d", rc)

    def on_message(self, client, userdata, msg):
        """Handle incoming messages."""
        try:
            payload = json.loads(msg.payload.decode())
            if msg.topic == self.schedule_topic:
                self.schedule_data = payload
                logging.info(f"Schedule updated: {payload}")
            elif msg.topic == self.notes_topic:
                self.notes_data = payload
                logging.info(f"Notes updated: {payload}")
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON received on topic {msg.topic}: {msg.payload}")

    def on_disconnect(self, client, userdata, rc):
        """Handle disconnections."""
        logging.warning("Disconnected from MQTT broker. Attempting to reconnect...")
        self.reconnect()

    def reconnect(self):
        """Attempt to reconnect to the broker."""
        while True:
            try:
                self.client.connect(self.broker, self.port)
                self.client.loop_start()
                logging.info("Reconnected to MQTT broker.")
                break
            except Exception as e:
                logging.error(f"Reconnection failed: {e}. Retrying in {self.reconnect_delay} seconds...")
                time.sleep(self.reconnect_delay)

    def connect(self):
        """Connect to the broker."""
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}. Retrying...")
            self.reconnect()

    def stop(self):
        """Gracefully stop the client."""
        self.client.loop_stop()
        self.client.disconnect()
