import os
from pathlib import Path
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from core.database import init_db
from core.content_seeder import seed_activities
from ui.theme import apply_senior_theme
from engines.voice_assistant import VoiceAssistant
from engines.gamification_engine import GamificationEngine
from engines.recommendation_engine import RecommendationEngine

from ui.screens.onboarding.onboarding_screen import OnboardingScreen
from ui.screens.checkin.checkin_screen import CheckinScreen
from ui.screens.emergency.emergency_screen import EmergencyScreen
from ui.screens.settings.settings_screen import SettingsScreen
from ui.screens.modules.processing_speed_screen import ProcessingSpeedScreen
from ui.screens.modules.memory_screen import MemoryScreen
from ui.screens.modules.attention_screen import AttentionScreen
from ui.screens.modules.meditation_screen import MeditationScreen
from ui.screens.modules.yoga_screen import YogaScreen
from ui.screens.modules.dual_task_screen import DualTaskScreen

class MainWindow(ScreenManager):
    pass

from kivymd.uix.screen import MDScreen

class DashboardScreen(MDScreen):
    pass

class BrainFitApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voice_assistant = VoiceAssistant()

    def build(self):
        apply_senior_theme(self)
        # Load KV file
        kv_path = Path(__file__).resolve().parent / "ui" / "main_window.kv"
        Builder.load_file(str(kv_path))
        return MainWindow()

    def on_start(self):
        # Initialize Database and seed content on app start
        init_db()
        seed_activities()
        
        # Check if first run
        from repositories.user_repo import UserRepository
        repo = UserRepository()
        user = repo.get_user()
        
        self.gamification = None
        self.recommendation = None
        self.current_session_activities = []
        
        self.root.on_current = self._on_screen_changed
        
        if not user:
            self.root.current = "onboarding"
        else:
            self.voice_assistant.language = user.language
            self.gamification = GamificationEngine(user.id)
            self.gamification.check_in()
            self.recommendation = RecommendationEngine(user.id)
            self.root.current = "dashboard"

    def _on_screen_changed(self, instance, value):
        if value == "dashboard":
            from repositories.user_repo import UserRepository
            repo = UserRepository()
            user = repo.get_user()
            
            if user:
                if self.gamification is None:
                    from engines.gamification_engine import GamificationEngine
                    self.gamification = GamificationEngine(user.id)
                    self.gamification.check_in()
                
                if self.recommendation is None:
                    from engines.recommendation_engine import RecommendationEngine
                    self.recommendation = RecommendationEngine(user.id)
                    
                stats = self.gamification.get_stats()
                dashboard = self.root.get_screen("dashboard")
                if hasattr(dashboard, 'ids'):
                    if 'points_label' in dashboard.ids:
                        dashboard.ids.points_label.text = f"Total Points: {stats.get('total_points', 0)}"
                    if 'streak_label' in dashboard.ids:
                        dashboard.ids.streak_label.text = f"Current Streak: {stats.get('current_streak', 0)} days"

    def start_dynamic_session(self):
        print("Starting personalized session...")
        self.voice_assistant.speak("Let's start your personalized session.")
        self.current_session_activities = self.recommendation.get_daily_recommendation()
        self.play_next_activity()

    def play_next_activity(self):
        if not self.current_session_activities:
            self.gamification.add_points(50)
            self.voice_assistant.speak("Session complete. Great job today!")
            self.root.current = "dashboard"
            return
            
        activity = self.current_session_activities.pop(0)
        self.recommendation.log_activity_completion(activity["id"])
        
        template_id = activity["template_id"]
        # Map template_id to screen name
        screen_map = {
            "cognitive_grid": "cognitive_template",
            "cognitive_quiz": "cognitive_template",
            "physical_pose": "physical_template",
            "physical_template": "physical_template",
            "audio_guide": "audio_template",
            "audio_template": "audio_template"
        }
        screen_name = screen_map.get(template_id)
        if screen_name and self.root.has_screen(screen_name):
            screen = self.root.get_screen(screen_name)
            screen.activity_data = activity
            self.root.current = screen_name
        else:
            print(f"Template {template_id} not implemented yet.")
            self.play_next_activity() # Skip
    
    def toggle_voice(self):
        if self.voice_assistant.is_listening:
            self.voice_assistant.stop_listening()
        else:
            self.voice_assistant.listen(self._on_voice_command)
    
    def _on_voice_command(self, text: str):
        print(f"User said: {text}")

if __name__ == "__main__":
    BrainFitApp().run()
