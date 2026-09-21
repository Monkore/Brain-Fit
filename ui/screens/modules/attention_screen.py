from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import os
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "attention.kv"))

class AttentionScreen(MDScreen):
    current_letter = StringProperty("")
    score = NumericProperty(0)
    trials_left = NumericProperty(20)
    
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "O", "P", "Q", "Y", "Z"]
    
    def on_enter(self, *args):
        self.score = 0
        self.trials_left = 20
        self.start_task()
        
    def start_task(self):
        self.timer_event = Clock.schedule_interval(self.show_next_letter, 1.5)
        
    def show_next_letter(self, dt):
        if self.trials_left <= 0:
            self.timer_event.cancel()
            self.finish_game()
            return
            
        # 30% chance of 'X'
        if random.random() < 0.3:
            self.current_letter = "X"
        else:
            self.current_letter = random.choice(self.letters)
            
        self.trials_left -= 1
        
        # Reset color
        self.ids.btn_tap.md_bg_color = self.theme_cls.primary_color
        
    def on_tap(self):
        if self.current_letter == "X":
            self.score += 10
            self.ids.btn_tap.md_bg_color = (0.2, 0.8, 0.2, 1) # Green
        else:
            self.score = max(0, self.score - 5)
            self.ids.btn_tap.md_bg_color = (0.8, 0.2, 0.2, 1) # Red

    def finish_game(self):
        print(f"Attention Complete! Score: {self.score}")
        self.manager.current = "dashboard"
        
    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
