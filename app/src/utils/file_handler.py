import json
import os
from config import APP_LIST_FILE, WEBSITE_FILE

class FileHandler:
    @staticmethod
    def load_applications():
        if os.path.exists(APP_LIST_FILE):
            with open(APP_LIST_FILE, "r") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_applications(applications):
        with open(APP_LIST_FILE, "w") as file:
            json.dump(applications, file)

    @staticmethod
    def load_websites():
        if os.path.exists(WEBSITE_FILE):
            with open(WEBSITE_FILE, "r") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_websites(websites):
        with open(WEBSITE_FILE, "w") as file:
            json.dump(websites, file) 