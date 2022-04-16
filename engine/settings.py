import json
import os.path


class Settings:
    def __init__(self, settings_dir):
        self.settings_path = os.path.join(settings_dir, 'settings.json')
        self.defaults_path = os.path.join(settings_dir, 'defaults.json')
        self.settings = {}
        self.defaults = {}
        self.load()

    def save(self):
        """Saves the settings to settings.json inside the file path"""
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f)

    def get(self, keys):
        """Get a value from the settings dictionary. If the key is not found, use the default value"""
        if isinstance(keys, str):
            keys = keys.split('.')

        value = self.settings
        for i in range(len(keys)):
            if keys[i] in value:
                value = value[keys[i]]
            else:
                value[keys[i]] = self.get_default(keys[:i + 1])
                self.save()
                value = value[keys[i]]
        return value

    def set(self, keys, val):
        """Set a value in the settings dictionary"""
        if isinstance(keys, str):
            keys = keys.split('.')

        # Set the value
        value = self.settings
        for key in keys[:-1]:
            if key in value:
                value = value[key]
            else:
                value[key] = {}
                value = value[key]
        value[keys[-1]] = val
        self.save()

    def get_default(self, keys):
        """Get a value from the defaults dictionary. If the key is not found, return None"""
        if isinstance(keys, str):
            keys = [keys]

        value = self.defaults
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None
        return value



    def load(self):
        """Loads the settings and defaults from json files"""
        # Load the defaults
        with open(self.defaults_path, 'r') as f:
            self.defaults = json.load(f)

        # Check to make sure the file exists
        try:
            with open(self.settings_path, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            print("Settings file not found. Creating new settings file.")
            self.settings = self.defaults
            self.save()

settings = Settings(os.path.join("resources", "misc", "settings"))