from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
import os
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "processing_speed.kv"))

class ProcessingSpeedScreen(MDScreen):
    target_symbol = StringProperty("A")
    score = NumericProperty(0)
    time_left = NumericProperty(30)
    
    symbols = ["A", "B", "C", "X", "Y", "Z", "1", "2", "3", "9"]
    
    def on_enter(self, *args):
        self.score = 0
        self.time_left = 30
        self.generate_challenge()
        self.timer_event = Clock.schedule_interval(self.tick, 1)
        
    def generate_challenge(self):
        self.target_symbol = random.choice(self.symbols)
        options = [self.target_symbol]
        while len(options) < 4:
            sym = random.choice(self.symbols)
            if sym not in options:
                options.append(sym)
        random.shuffle(options)
        
        self.ids.btn_1.text = options[0]
        self.ids.btn_2.text = options[1]
        self.ids.btn_3.text = options[2]
        self.ids.btn_4.text = options[3]

    def tick(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.timer_event.cancel()
            self.finish_game()
            
    def check_match(self, selected_symbol):
        if self.time_left > 0:
            if selected_symbol == self.target_symbol:
                self.score += 10
            else:
                self.score = max(0, self.score - 5)
            self.generate_challenge()
            
    def finish_game(self):
        # Here we would normally prompt for feedback (Enjoyment/Difficulty/Energy)
        # and use the Adaptive Difficulty and Safety Engines.
        print(f"Processing Speed Complete! Score: {self.score}")
        self.manager.current = "dashboard"
        
    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
