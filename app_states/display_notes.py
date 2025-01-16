# app_states/display_notes.py

import logging

class DisplayNotes:
    def __init__(self, mqtt_client, display_manager):
        self.state_name = "DisplayNotes"
        self.mqtt_client = mqtt_client
        self.display_manager = display_manager

    def handle(self):
        """Отображаем заметки, получая данные из MQTT-клиента."""
        logging.info(f"[{self.state_name}] Получаем заметки из MQTT-клиента.")
        notes_data = self.mqtt_client.get_notes_data()
        if notes_data:
            self.display_manager.update_notes(notes_data)
        else:
            logging.warning(f"[{self.state_name}] Нет данных о заметках.")
