from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "checkin.kv"))

class CheckinScreen(MDScreen):
    question_text = StringProperty("How is your mood today?")
    current_step = NumericProperty(0)
    
    # Sliders for each dimension
    metrics = [
        {"key": "mood", "text": "How is your mood today?", "min": 1, "max": 10},
        {"key": "stress", "text": "How stressed do you feel?", "min": 1, "max": 10},
        {"key": "anxiety", "text": "How anxious do you feel?", "min": 1, "max": 10},
        {"key": "energy", "text": "What is your energy level?", "min": 1, "max": 10},
        {"key": "focus", "text": "How is your focus?", "min": 1, "max": 10},
        {"key": "motivation", "text": "How motivated are you?", "min": 1, "max": 10},
        {"key": "mental_fatigue", "text": "How mentally tired are you?", "min": 1, "max": 10},
        {"key": "sleep_hours", "text": "How many hours did you sleep?", "min": 0, "max": 16} # special case
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = {}

    def on_enter(self, *args):
        self.current_step = 0
        self.results = {}
        self.load_question()

    def load_question(self):
        if self.current_step < len(self.metrics):
            m = self.metrics[self.current_step]
            self.question_text = m["text"]
            self.ids.slider.min = m["min"]
            self.ids.slider.max = m["max"]
            self.ids.slider.value = (m["max"] + m["min"]) / 2 # Default to middle
        else:
            self.finish_checkin()

    def save_answer_and_next(self, value):
        m = self.metrics[self.current_step]
        self.results[m["key"]] = value
        print(f"Saved {m['key']}: {value}")
        self.current_step += 1
        self.load_question()
        
    def finish_checkin(self):
        print("Checkin Complete!")
        print("Results:", self.results)
        # In a real app, save to Checkin model via CheckinRepository
        self.manager.current = "dashboard"
