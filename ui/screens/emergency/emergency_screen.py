from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "emergency.kv"))

class EmergencyScreen(MDScreen):
    def call_contact(self):
        # In a real Android app, this would dispatch an intent to dial the number
        print("Calling emergency contact...")
        
    def go_back(self):
        self.manager.current = "dashboard"
