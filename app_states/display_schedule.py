
import logging

class DisplaySchedule:
    def __init__(self, display_manager, mqtt_client):
        self.display_manager = display_manager
        self.mqtt_client = mqtt_client

    def run(self):
        if self.mqtt_client.schedule_data:
            logging.info("DisplaySchedule: Displaying schedule data.")
            self.display_manager.show_schedule(self.mqtt_client.schedule_data)
        else:
            logging.warning("DisplaySchedule: No schedule data available.")
