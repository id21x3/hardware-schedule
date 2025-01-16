# fake_mqtt.py

import json
import logging
import time

class FakeMqtt:
    def __init__(self, room_id):
        self.room_id = room_id
        self.last_message = None

        # Тестовые данные (можно расширить)
        self._test_schedule = {
            "type": "schedule",
            "lessons": [
                {"time": "08:00-08:45", "subject": "IOT", "teacher": "Ján Novák", "room": "101"},
                {"time": "09:00-09:45", "subject": "ISI", "teacher": "Mária Kováčová", "room": "102"}
            ]
        }
        self._test_notes = {
            "type": "notes",
            "note": "Dôležité: Cviko sa dnes presúva na 12:00."
        }

        self.schedule_data = None
        self.notes_data = None

        # Флаг для переключения между сообщениями
        self._switch = True

    def connect(self):
        """Фейковое подключение — всегда успешно."""
        logging.info("Фейковое подключение к MQTT (заглушка).")

    def get_message(self):
        """Поочерёдно «подбрасывает» сообщения расписания и заметок."""
        # Каждые 2 вызова функции выдаём разные сообщения
        time.sleep(1)  # Искусственная задержка для наглядности

        if self._switch:
            # Эмулируем получение расписания
            message = {
                "type": "schedule",
                **self._test_schedule
            }
            self.schedule_data = message
        else:
            # Эмулируем получение заметки
            message = {
                "type": "notes",
                **self._test_notes
            }
            self.notes_data = message

        self._switch = not self._switch
        self.last_message = message
        return message

    def get_schedule_data(self):
        return self.schedule_data

    def get_notes_data(self):
        return self.notes_data
