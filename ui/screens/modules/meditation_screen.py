from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "meditation.kv"))

class MeditationScreen(MDScreen):
    time_left = NumericProperty(300) # 5 minutes
    is_active = BooleanProperty(False)
    instruction = StringProperty("Sit comfortably and focus on your breath.")
    
    def on_enter(self, *args):
        self.time_left = 300
        self.is_active = False
        self.instruction = "Sit comfortably and focus on your breath."
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, 'voice_assistant'):
            app.voice_assistant.speak("Let's begin a five minute meditation.")
            
    def toggle_meditation(self):
        if self.is_active:
            self.timer_event.cancel()
            self.is_active = False
            self.instruction = "Paused"
        else:
            self.timer_event = Clock.schedule_interval(self.tick, 1)
            self.is_active = True
            self.instruction = "Breathe in... Breathe out..."
            
    def tick(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.timer_event.cancel()
            self.finish_meditation()
            
    def finish_meditation(self):
        self.instruction = "Session Complete. Well done."
        self.is_active = False
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, 'voice_assistant'):
            app.voice_assistant.speak("Meditation complete. You did a great job.")
        
    def end_early(self):
        if self.is_active:
            self.timer_event.cancel()
        self.manager.current = "dashboard"
        
    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
