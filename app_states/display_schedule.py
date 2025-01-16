# app_states/display_schedule.py

import logging

class DisplaySchedule:
    def __init__(self, mqtt_client, display_manager):
        self.state_name = "DisplaySchedule"
        self.mqtt_client = mqtt_client
        self.display_manager = display_manager

    def handle(self):
        """Отображаем расписание, получая данные из MQTT-клиента."""
        logging.info(f"[{self.state_name}] Получаем расписание из MQTT-клиента.")
        schedule_data = self.mqtt_client.get_schedule_data()
        if schedule_data:
            self.display_manager.update_schedule(schedule_data)
        else:
            logging.warning(f"[{self.state_name}] Нет данных о расписании.")
