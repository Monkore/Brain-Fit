from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, DictProperty # type: ignore
from kivy.clock import Clock
import os
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "audio_template.kv"))

class AudioTemplateScreen(MDScreen):
    activity_name = StringProperty("")
    activity_description = StringProperty("")
    time_left = NumericProperty(300)
    activity_data = DictProperty({})
    
    def on_enter(self, *args):
        if self.activity_data:
            self.activity_name = self.activity_data.get("name", "Meditation Task")
            self.activity_description = self.activity_data.get("description", "")
            
            params = json.loads(self.activity_data.get("parameters_json", "{}"))
            self.time_left = params.get("duration", 300)
            
            app = self.manager.parent.parent
            if hasattr(app, "voice_assistant"):
                app.voice_assistant.speak(f"Beginning {self.activity_name}. Please close your eyes.")
                
            self.timer_event = Clock.schedule_interval(self.tick, 1)
            
    def tick(self, dt):
        self.time_left -= 1
            
        if self.time_left <= 0:
            self.timer_event.cancel()
            self.finish_activity()
            
    def finish_activity(self):
        print(f"[{self.activity_name}] Complete!")
        app = self.manager.parent.parent
        if hasattr(app, "play_next_activity"):
            app.play_next_activity()
        else:
            self.manager.current = "dashboard"
        
    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
