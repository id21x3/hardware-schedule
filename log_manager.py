import logging

class LogManager:
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            filename='app.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def log(message, level=logging.INFO):
        logging.log(level, message)