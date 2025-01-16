# main.py

import json
import time
import logging

from app_states.idle_state import IdleState
from app_states.display_schedule import DisplaySchedule
from app_states.display_notes import DisplayNotes

from mqtt_client import MqttClient
from fake_mqtt import FakeMqtt

from display_manager import DisplayManager

# Логгер для наглядности
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


def load_configurations():
    """Загружает конфигурации из JSON-файлов."""
    with open('configurations/device_config.json', 'r', encoding='utf-8') as f:
        device_config = json.load(f)
    with open('configurations/user_config.json', 'r', encoding='utf-8') as f:
        user_config = json.load(f)
    return device_config, user_config


def main():
    # Загружаем конфиги
    device_config, user_config = load_configurations()
    logging.info("Конфигурации успешно загружены.")

    # Инициализируем MQTT-клиент
    try:
        mqtt_client = MqttClient(
            broker=device_config['mqtt_broker'],
            port=device_config['mqtt_port'],
            room_id=user_config['room_id']
        )
        mqtt_client.connect()
        logging.info("Успешно подключились к реальному MQTT-брокеру.")
    except Exception as e:
        logging.warning(f"Не удалось подключиться к MQTT-брокеру: {e}. Используем фейковый MQTT.")
        mqtt_client = FakeMqtt(room_id=user_config['room_id'])

    # Инициализируем менеджер отображения (Flask)
    display_manager = DisplayManager()

    # Создаём объекты состояний
    idle_state = IdleState()
    display_schedule_state = DisplaySchedule(mqtt_client, display_manager)
    display_notes_state = DisplayNotes(mqtt_client, display_manager)

    # Текущее состояние
    current_state = idle_state
    logging.info("Приложение запущено. Начинаем с IdleState.")

    try:
        # Запускаем Flask-сервер в отдельном потоке
        display_manager.run_server()

        # Основной цикл приложения
        while True:
            # Получаем новое сообщение (если оно есть)
            message = mqtt_client.get_message()

            if message is not None:
                # Допустим, смотрим на ключ "type" в сообщении
                msg_type = message.get('type')

                if msg_type == 'schedule':
                    current_state = display_schedule_state
                elif msg_type == 'notes':
                    current_state = display_notes_state
                else:
                    # Если тип сообщения не распознан, возвращаемся к IdleState
                    current_state = idle_state

            # Выполняем логику текущего состояния
            current_state.handle()

            # Небольшая задержка, чтобы не перегружать CPU
            time.sleep(2)

    except KeyboardInterrupt:
        logging.info("Остановка приложения пользователем (Ctrl+C).")
    except Exception as e:
        logging.error(f"Ошибка во время выполнения: {e}")


if __name__ == '__main__':
    main()
