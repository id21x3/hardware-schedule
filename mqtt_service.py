import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, broker, port, username, password):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client()

    def connect(self):
        try:
            self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker, self.port, 60)
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def subscribe(self, topic, callback):
        try:
            self.client.subscribe(topic)
            self.client.message_callback_add(topic, callback)
            print(f"Subscribed to topic: {topic}")
        except Exception as e:
            print(f"Error subscribing to topic {topic}: {e}")

    def start(self):
        try:
            self.client.loop_start()
            print("MQTT client loop started.")
        except Exception as e:
            print(f"Error starting MQTT loop: {e}")

    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
            print("MQTT client disconnected and loop stopped.")
        except Exception as e:
            print(f"Error stopping MQTT client: {e}")