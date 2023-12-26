import json
from paths import ROOT_DIR

settings_file_path = ROOT_DIR / "settings.json"
defualt = {
    "volume":100,
    "guess_time": 60,
    "guesses": 3,
    'difficulty': 1
}

class Settings:
    @staticmethod
    def create_settings_file_if_not_exist():
        if settings_file_path.exists():
            return
        Settings.update_settings_file(defualt)
        
    @staticmethod
    def update_settings_file(data):
        with open(settings_file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file)
            
    @staticmethod
    def load_settings_file():
        with open(settings_file_path, mode="r", encoding="utf-8-sig") as file:
            return json.loads(file.read())
        
    @staticmethod
    def get_guess_time():
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        return data.get("guess_time")

    @staticmethod
    def get_guesses():
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        return data.get("guesses")

    @staticmethod
    def get_difficulty():
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        return data.get("difficulty")

    @staticmethod
    def get_volume():
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        return data.get("volume")
    
    @staticmethod
    def update_volume(new_vol):
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        data["volume"] = new_vol
        Settings.update_settings_file(data)

    @staticmethod
    def update_guess_time(new_time):
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        data["guess_time"] = new_time
        Settings.update_settings_file(data)
    
    @staticmethod
    def update_guesses(new):
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        data["guesses"] = new
        Settings.update_settings_file(data)
        
    @staticmethod
    def update_difficulty(new):
        Settings.create_settings_file_if_not_exist()
        data = Settings.load_settings_file()
        data["difficulty"] = new
        Settings.update_settings_file(data)