
import json
import time
import logging

from app_states.idle_state import IdleState
from app_states.display_schedule import DisplaySchedule
from app_states.display_notes import DisplayNotes

from mqtt_client import MqttClient
from fake_mqtt import FakeMqtt

from display_manager import DisplayManager

# Logger setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def load_configurations():
    """Load configurations from JSON files."""
    with open('configurations/device_config.json', 'r', encoding='utf-8') as f:
        device_config = json.load(f)
    with open('configurations/user_config.json', 'r', encoding='utf-8') as f:
        user_config = json.load(f)
    return device_config, user_config

def initialize_mqtt_client(device_config, use_fake=False):
    """Initialize the MQTT client, real or fake."""
    if use_fake:
        mqtt_client = FakeMqtt(device_config["room_id"])
        mqtt_client.connect()
        return mqtt_client
    else:
        mqtt_client = MqttClient(
            broker=device_config["mqtt_broker"],
            port=device_config["mqtt_port"],
            room_id=device_config["room_id"]
        )
        mqtt_client.connect()
        return mqtt_client

def main():
    # Load configurations
    device_config, user_config = load_configurations()
    logging.info("Configurations successfully loaded.")

    # Initialize MQTT client (real or fake based on config)
    try:
        mqtt_client = initialize_mqtt_client(device_config, use_fake=False)
    except Exception as e:
        logging.error(f"Failed to initialize real MQTT client: {e}. Switching to fake client.")
        mqtt_client = initialize_mqtt_client(device_config, use_fake=True)

    # Initialize DisplayManager
    display_manager = DisplayManager()

    # Initialize application states
    idle_state = IdleState(display_manager)
    display_schedule_state = DisplaySchedule(display_manager, mqtt_client)
    display_notes_state = DisplayNotes(display_manager, mqtt_client)

    # Application state loop
    current_state = idle_state
    try:
        while True:
            current_state.run()
            # Example of state switching based on messages
            if isinstance(mqtt_client, FakeMqtt):
                mqtt_client.get_message()
                if mqtt_client.schedule_data:
                    current_state = display_schedule_state
                elif mqtt_client.notes_data:
                    current_state = display_notes_state
            else:
                # Replace with real MQTT message handling
                pass
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Application stopped by user.")
    finally:
        mqtt_client.stop()

if __name__ == "__main__":
    main()
