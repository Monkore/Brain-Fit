from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, DictProperty # type: ignore
from kivy.clock import Clock
import os
import random
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "cognitive_template.kv"))

class CognitiveTemplateScreen(MDScreen):
    activity_name = StringProperty("")
    activity_description = StringProperty("")
    target_prompt = StringProperty("")
    score = NumericProperty(0)
    time_left = NumericProperty(60)
    activity_data = DictProperty({})
    
    def on_enter(self, *args):
        self.score = 0
        self.time_left = 60
        
        if self.activity_data:
            self.activity_name = self.activity_data.get("name", "Cognitive Task")
            self.activity_description = self.activity_data.get("description", "")
            
            # Parse parameters
            params = json.loads(self.activity_data.get("parameters_json", "{}"))
            self.mode = params.get("mode", "text")
            self.options_count = params.get("options_count", 4)
            
            self.generate_challenge()
            self.timer_event = Clock.schedule_interval(self.tick, 1)
        
    def generate_challenge(self):
        # Dummy dynamic generation for 200+ activities. 
        # In a real app, this would use a content factory to load images/questions.
        if self.activity_data.get("domain") == "Reasoning":
            self.target_prompt = f"Solve the logical sequence for {self.activity_name}"
            options = ["Option A", "Option B", "Option C", "Option D"]
        elif self.activity_data.get("domain") == "Social":
            self.target_prompt = f"Identify the emotion in this scenario"
            options = ["Happy", "Sad", "Angry", "Surprised"]
        else:
            self.target_prompt = f"Complete the task: {self.activity_name}"
            options = ["1", "2", "3", "4"]
            
        random.shuffle(options)
        self.correct_answer = options[0] # Simplification
        
        # We assume 4 buttons in KV for simplicity, can dynamically add/remove widgets
        for i in range(1, 5):
            btn = self.ids.get(f"btn_{i}")
            if btn:
                if i <= len(options):
                    btn.text = options[i-1]
                    btn.opacity = 1
                    btn.disabled = False
                else:
                    btn.opacity = 0
                    btn.disabled = True

    def tick(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.timer_event.cancel()
            self.finish_game()
            
    def check_match(self, selected_text):
        if self.time_left > 0:
            if selected_text == self.correct_answer:
                self.score += 10
            else:
                self.score = max(0, self.score - 5)
            self.generate_challenge()
            
    def finish_game(self):
        print(f"[{self.activity_name}] Complete! Score: {self.score}")
        app = self.manager.parent.parent
        if hasattr(app, "play_next_activity"):
            app.play_next_activity()
        else:
            self.manager.current = "dashboard"
        
    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
