from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
import os
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "memory.kv"))

class MemoryScreen(MDScreen):
    instruction_text = StringProperty("Memorize these words:")
    phase = StringProperty("memorize") # 'memorize' or 'recall'
    score = NumericProperty(0)
    
    all_words = ["Apple", "House", "River", "Train", "Chair", "Clock", "Bread", "Table", "Dog", "Cat", "Sun", "Moon"]
    target_words = ListProperty([])
    selected_words = set()
    
    def on_enter(self, *args):
        self.score = 0
        self.selected_words = set()
        self.start_memorize_phase()
        
    def start_memorize_phase(self):
        self.phase = "memorize"
        self.instruction_text = "Memorize these words:"
        self.target_words = random.sample(self.all_words, 3)
        self.ids.word_1.text = self.target_words[0]
        self.ids.word_2.text = self.target_words[1]
        self.ids.word_3.text = self.target_words[2]
        
        # Hide the choices grid
        self.ids.recall_grid.opacity = 0
        self.ids.memorize_grid.opacity = 1
        self.ids.btn_next.opacity = 1
        self.ids.btn_next.text = "I'm Ready"
        
    def start_recall_phase(self):
        self.phase = "recall"
        self.instruction_text = "Tap the words you saw:"
        self.ids.memorize_grid.opacity = 0
        self.ids.recall_grid.opacity = 1
        self.ids.btn_next.opacity = 0
        
        # Prepare 6 options
        options = list(self.target_words)
        distractors = [w for w in self.all_words if w not in self.target_words]
        options.extend(random.sample(distractors, 3))
        random.shuffle(options)
        
        for i in range(1, 7):
            btn = self.ids[f"recall_btn_{i}"]
            btn.text = options[i-1]
            btn.md_bg_color = self.theme_cls.primary_color
            
    def toggle_word(self, btn):
        if self.phase == "recall":
            word = btn.text
            if word in self.selected_words:
                self.selected_words.remove(word)
                btn.md_bg_color = self.theme_cls.primary_color
            else:
                self.selected_words.add(word)
                btn.md_bg_color = (0.2, 0.8, 0.2, 1) # Green for selected
                
            if len(self.selected_words) == 3:
                self.check_results()
                
    def check_results(self):
        correct = 0
        for w in self.selected_words:
            if w in self.target_words:
                correct += 1
        
        self.score = correct * 33 # roughly 100 max
        print(f"Memory Game Complete! Correct: {correct}/3, Score: {self.score}")
        self.manager.current = "dashboard"

    def on_next(self):
        if self.phase == "memorize":
            self.start_recall_phase()
