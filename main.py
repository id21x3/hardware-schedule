from app_state import InitState
from config_loader import ConfigLoader

DEVICE_CONFIG_PATH = "config/device_config.json"

class Application:
    def __init__(self, config_path):
        self.config_path = config_path
        self.state = None
        self.config = None

    def initialize(self):
        try:
            self.config = ConfigLoader.load_config(self.config_path)
            print(f"Configuration loaded: {self.config}")
            self.state = InitState(self)
        except Exception as e:
            print(f"Error during initialization: {e}")

    def run(self):
        if not self.state:
            print("Application state is not initialized. Exiting.")
            return

        while True:
            try:
                self.state.execute()
            except Exception as e:
                print(f"Error during execution: {e}")

if __name__ == "__main__":
    app = Application(DEVICE_CONFIG_PATH)
    app.initialize()
    app.run()