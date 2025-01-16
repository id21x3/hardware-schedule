# app_states/idle_state.py

import logging


class IdleState:
    def __init__(self):
        self.state_name = "IdleState"

    def handle(self):
        """Ничего не делаем, просто ждём."""
        logging.debug(f"[{self.state_name}] Ожидание новых сообщений...")
