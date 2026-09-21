from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, ListProperty # type: ignore
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "onboarding.kv"))

class OnboardingScreen(MDScreen):
    question_text = StringProperty("What is your name?")
    current_step = NumericProperty(0)
    
    questions = [
        {"key": "name", "text": "What is your name?", "type": "text"},
        {"key": "age", "text": "What is your age?", "type": "number"},
        {"key": "gender", "text": "What is your gender?", "type": "choice", "options": ["Male", "Female", "Other"]},
        {"key": "language", "text": "Preferred Language?", "type": "choice", "options": ["English", "Hindi", "Bilingual"]},
        {"key": "activity", "text": "Activity Level?", "type": "choice", "options": ["Low", "Moderate", "High"]},
        {"key": "sleep", "text": "Average Sleep Duration?", "type": "choice", "options": ["< 5 hours", "5-7 hours", "7-9 hours", "> 9 hours"]},
        {"key": "meditation", "text": "Meditation Experience?", "type": "choice", "options": ["None", "Beginner", "Experienced"]},
        {"key": "exercise", "text": "Exercise Frequency?", "type": "choice", "options": ["Rarely", "1-2 times/week", "3+ times/week"]}
    ]

    def on_enter(self, *args):
        self.load_question()

    def load_question(self):
        if self.current_step < len(self.questions):
            q = self.questions[self.current_step]
            self.question_text = q["text"]
            self.ids.options_container.clear_widgets()
            
            from kivymd.uix.button import MDFillRoundFlatButton
            from kivymd.uix.textfield import MDTextField
            from kivy.metrics import dp

            if q["type"] in ["text", "number"]:
                input_field = MDTextField(
                    hint_text="Tap here to type",
                    font_size="24sp",
                    size_hint_x=0.8,
                    pos_hint={"center_x": 0.5}
                )
                if q["type"] == "number":
                    input_field.input_filter = "int"
                self.ids.options_container.add_widget(input_field)
                self.current_input = input_field
                
                btn = MDFillRoundFlatButton(
                    text="Next",
                    font_size="28sp",
                    size_hint_x=0.8,
                    pos_hint={"center_x": 0.5},
                    size_hint_y=None,
                    height=dp(64)
                )
                btn.bind(on_release=lambda x: self.save_answer_and_next(input_field.text))
                self.ids.options_container.add_widget(btn)

            elif q["type"] == "choice":
                for opt in q["options"]:
                    btn = MDFillRoundFlatButton(
                        text=opt,
                        font_size="28sp",
                        size_hint_x=0.8,
                        pos_hint={"center_x": 0.5},
                        size_hint_y=None,
                        height=dp(64)
                    )
                    btn.bind(on_release=lambda x, val=opt: self.save_answer_and_next(val))
                    self.ids.options_container.add_widget(btn)
        else:
            self.finish_onboarding()

    def save_answer_and_next(self, answer):
        q = self.questions[self.current_step]
        print(f"Saved {q['key']}: {answer}")
        
        # Store answer locally
        if not hasattr(self, 'answers'):
            self.answers = {}
        self.answers[q['key']] = answer
        
        self.current_step += 1
        self.load_question()
        
    def finish_onboarding(self):
        print("Onboarding Complete! Saving user...")
        from models.user import User
        from repositories.user_repo import UserRepository
        
        age = int(self.answers.get("age", 25)) if str(self.answers.get("age", "25")).isdigit() else 25
        
        new_user = User(
            id=None,
            name=self.answers.get("name", "User"),
            age=age,
            gender=self.answers.get("gender", "Other"),
            language=self.answers.get("language", "English"),
            activity_level=self.answers.get("activity", "Moderate"),
            sleep_duration=self.answers.get("sleep", "7-9 hours"),
            meditation_exp=self.answers.get("meditation", "None"),
            exercise_freq=self.answers.get("exercise", "Rarely")
        )
        
        repo = UserRepository()
        repo.create_user(new_user)
        
        # Set language and switch to dashboard
        app = self.manager.parent.parent
        if hasattr(app, 'voice_assistant'):
            app.voice_assistant.language = new_user.language
            
        self.manager.current = "dashboard"
