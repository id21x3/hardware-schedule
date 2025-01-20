
import logging

class IdleState:
    def __init__(self, display_manager):
        self.display_manager = display_manager

    def run(self):
        logging.info("IdleState: Waiting for incoming data...")
        self.display_manager.show_message("Waiting for data...")
