from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "settings.kv"))

class SettingsScreen(MDScreen):
    def go_back(self):
        self.manager.current = "dashboard"
        
    def save_settings(self):
        print("Settings saved.")
        self.go_back()
