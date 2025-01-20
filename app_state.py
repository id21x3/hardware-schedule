# app_state.py
class AbstractState:
    def __init__(self, app):
        self.app = app

    def execute(self):
        raise NotImplementedError("Execute method must be implemented in subclasses.")

class InitState(AbstractState):
    def execute(self):
        print("Initialization state executed.")
        from mqtt_state import MQTTState
        self.app.state = MQTTState(self.app)