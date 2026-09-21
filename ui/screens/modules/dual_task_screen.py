from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import os
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "dual_task.kv"))

class DualTaskScreen(MDScreen):
    instruction = StringProperty("Listen to the numbers. Tap the button when it turns RED.")
    score = NumericProperty(0)
    time_left = NumericProperty(30)
    phase = StringProperty("task") # 'task' or 'answer'
    
    def on_enter(self, *args):
        self.score = 0
        self.time_left = 30
        self.phase = "task"
        self.numbers = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
        self.current_number_idx = 0
        self.correct_sum = sum(self.numbers)
        
        self.ids.btn_tap.md_bg_color = self.theme_cls.primary_color
        self.ids.answer_grid.opacity = 0
        self.ids.btn_tap.opacity = 1
        
        # Start voice reading
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, 'voice_assistant'):
            app.voice_assistant.speak("Ready? Go.")
            
        self.timer_event = Clock.schedule_interval(self.tick, 1)
        self.color_event = Clock.schedule_interval(self.change_color, 2)
        
    def tick(self, dt):
        if self.phase == "task":
            self.time_left -= 1
            
            # Every 10 seconds, read a number
            if self.time_left == 25 and self.current_number_idx < 1:
                self.speak_num(0)
            elif self.time_left == 15 and self.current_number_idx < 2:
                self.speak_num(1)
            elif self.time_left == 5 and self.current_number_idx < 3:
                self.speak_num(2)
                
            if self.time_left <= 0:
                self.end_task_phase()
                
    def speak_num(self, idx):
        self.current_number_idx = idx + 1
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, 'voice_assistant'):
            app.voice_assistant.speak(str(self.numbers[idx]))
                
    def change_color(self, dt):
        if self.phase == "task":
            if random.random() < 0.4:
                self.ids.btn_tap.md_bg_color = (0.8, 0.2, 0.2, 1) # Red
                self.ids.btn_tap.is_target = True
            else:
                self.ids.btn_tap.md_bg_color = self.theme_cls.primary_color
                self.ids.btn_tap.is_target = False
                
    def on_tap(self):
        if self.phase == "task":
            if getattr(self.ids.btn_tap, 'is_target', False):
                self.score += 10
                self.ids.btn_tap.md_bg_color = self.theme_cls.primary_color
                self.ids.btn_tap.is_target = False
            else:
                self.score = max(0, self.score - 5)
                
    def end_task_phase(self):
        self.timer_event.cancel()
        self.color_event.cancel()
        self.phase = "answer"
        self.instruction = "What was the sum of the numbers you heard?"
        self.ids.btn_tap.opacity = 0
        self.ids.answer_grid.opacity = 1
        
        options = [self.correct_sum]
        while len(options) < 3:
            wrong = self.correct_sum + random.choice([-2, -1, 1, 2, 3])
            if wrong > 0 and wrong not in options:
                options.append(wrong)
                
        random.shuffle(options)
        
        self.ids.ans_btn_1.text = str(options[0])
        self.ids.ans_btn_2.text = str(options[1])
        self.ids.ans_btn_3.text = str(options[2])
        
    def check_answer(self, ans_str):
        if int(ans_str) == self.correct_sum:
            self.score += 50
        print(f"Dual Task Complete! Score: {self.score}")
        self.manager.current = "dashboard"

    def on_leave(self, *args):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
        if hasattr(self, 'color_event'):
            self.color_event.cancel()
