from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, DictProperty, ListProperty
from kivy.clock import Clock
import os
import json
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "visual_spatial_template.kv"))

class VisualSpatialTemplateScreen(MDScreen):
    activity_name = StringProperty("")
    activity_description = StringProperty("")
    feedback_text = StringProperty("Analyze the shapes below...")
    score = NumericProperty(0)
    time_left = NumericProperty(60)
    activity_data = DictProperty({})
    
    # Visual Puzzle Data
    target_shape = StringProperty("rectangle")
    target_rotation = NumericProperty(0)
    options = ListProperty([])
    
    def on_enter(self, *args):
        self.score = 0
        self.time_left = 60
        self.options = []
        self.feedback_text = "Select the matching rotated shape!"
        
        if self.activity_data:
            self.activity_name = self.activity_data.get("name", "Visual-Spatial Task")
            self.activity_description = self.activity_data.get("description", "")
            
            params = json.loads(self.activity_data.get("parameters_json", "{}"))
            difficulty = params.get("difficulty", 1)
            self.time_left = 30 + (difficulty * 15)
            
            self.generate_puzzle(difficulty)
            
            app = self.manager.parent.parent
            if hasattr(app, 'voice_assistant'):
                app.voice_assistant.speak(f"Starting {self.activity_name}. {self.activity_description}")
            
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def generate_puzzle(self, difficulty):
        # Generate a target rotation puzzle
        shapes = ["rectangle", "ellipse", "triangle"]
        self.target_shape = random.choice(shapes)
        self.target_rotation = random.choice([0, 45, 90, 135, 180, 225, 270])
        
        correct_opt = {"shape": self.target_shape, "rotation": self.target_rotation, "is_correct": True}
        
        # Generate distractors
        num_options = 3 if difficulty == 1 else (4 if difficulty == 2 else 6)
        opts = [correct_opt]
        
        while len(opts) < num_options:
            dist_rot = random.choice([0, 45, 90, 135, 180, 225, 270])
            if dist_rot != self.target_rotation:
                opts.append({"shape": self.target_shape, "rotation": dist_rot, "is_correct": False})
                
        random.shuffle(opts)
        
        # We need to map these to UI
        self.ids.options_grid.clear_widgets()
        from kivymd.uix.button import MDFillRoundFlatButton
        
        for i, opt in enumerate(opts):
            btn = MDFillRoundFlatButton(
                text=f"Option {i+1}",
                size_hint=(1, None),
                height="64dp"
            )
            btn.bind(on_release=lambda x, is_corr=opt["is_correct"]: self.check_answer(is_corr))
            self.ids.options_grid.add_widget(btn)

    def update_timer(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.end_activity()

    def check_answer(self, is_correct):
        if is_correct:
            self.score += 10
            self.feedback_text = "Correct! Great spatial awareness."
            app = self.manager.parent.parent
            if hasattr(app, 'voice_assistant'):
                app.voice_assistant.speak("Correct!")
            Clock.schedule_once(lambda dt: self.end_activity(), 1.5)
        else:
            self.score = max(0, self.score - 2)
            self.feedback_text = "Not quite. Look closer at the angles."
            app = self.manager.parent.parent
            if hasattr(app, 'voice_assistant'):
                app.voice_assistant.speak("Try again.")

    def end_activity(self):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
        
        # Record stats
        app = self.manager.parent.parent
        if hasattr(app, 'gamification'):
            app.gamification.award_xp(self.score)
            
        self.feedback_text = f"Activity Complete! Score: {self.score}"
        
        # Move to next activity
        if hasattr(app, 'play_next_activity'):
            Clock.schedule_once(lambda dt: app.play_next_activity(), 2)
        else:
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'dashboard'), 2)
