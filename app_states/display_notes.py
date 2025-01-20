
import logging

class DisplayNotes:
    def __init__(self, display_manager, mqtt_client):
        self.display_manager = display_manager
        self.mqtt_client = mqtt_client

    def run(self):
        if self.mqtt_client.notes_data:
            logging.info("DisplayNotes: Displaying notes data.")
            self.display_manager.show_notes(self.mqtt_client.notes_data)
        else:
            logging.warning("DisplayNotes: No notes data available.")
