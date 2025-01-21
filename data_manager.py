import json

class DataManager:
    @staticmethod
    def save_data(file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(json.loads(data), file, indent=4)
            print(f"Data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")

    @staticmethod
    def load_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return None