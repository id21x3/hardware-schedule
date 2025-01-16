# mqtt_client.py

import paho.mqtt.client as mqtt
import json
import logging

class MqttClient:
    def __init__(self, broker, port, room_id):
        self.broker = broker
        self.port = port
        self.room_id = room_id
        self.client = mqtt.Client()
        self.last_message = None
        self.schedule_data = None
        self.notes_data = None

        # Темы для подписки (можно изменить по вкусу)
        self.schedule_topic = f"{self.room_id}/schedule"
        self.notes_topic = f"{self.room_id}/notes"

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Подключение к MQTT-брокеру {self.broker}:{self.port} успешно.")
            # Подписываемся на топики
            client.subscribe(self.schedule_topic)
            client.subscribe(self.notes_topic)
        else:
            raise ConnectionError("Ошибка подключения к MQTT-брокеру.")

    def on_message(self, client, userdata, msg):
        """Обработчик входящих сообщений."""
        payload_str = msg.payload.decode('utf-8')
        logging.debug(f"Получено сообщение из топика {msg.topic}: {payload_str}")
        self.last_message = json.loads(payload_str)

        # В зависимости от топика обновляем локальные данные
        if msg.topic == self.schedule_topic:
            self.schedule_data = self.last_message
        elif msg.topic == self.notes_topic:
            self.notes_data = self.last_message

    def connect(self):
        """Подключается к брокеру и запускает цикл обработки сообщений в фоновом режиме."""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def get_message(self):
        """Возвращает последнее полученное сообщение (и очищает)."""
        if self.last_message:
            msg = self.last_message
            self.last_message = None
            return msg
        return None

    def get_schedule_data(self):
        """Возвращает текущие данные о расписании."""
        return self.schedule_data

    def get_notes_data(self):
        """Возвращает текущие данные о заметках."""
        return self.notes_data
