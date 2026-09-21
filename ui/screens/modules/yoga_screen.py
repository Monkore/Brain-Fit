from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import os
import cv2
import numpy as np

Builder.load_file(os.path.join(os.path.dirname(__file__), "yoga.kv"))

class YogaScreen(MDScreen):
    instruction = StringProperty("Stand up straight and face the camera")
    score = NumericProperty(0)
    time_left = NumericProperty(60)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        self.capture = None
        
    def on_enter(self, *args):
        self.score = 0
        self.time_left = 60
        self.instruction = "Loading camera..."
        
        # Lazy load engine to avoid blocking startup
        from engines.pose_detection import PoseEngine
        if not self.engine:
            self.engine = PoseEngine()
            
        # Start camera capture using cv2
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.instruction = "Camera not available"
            return
            
        self.instruction = "Hold your posture..."
        self.timer_event = Clock.schedule_interval(self.update_frame, 1.0 / 30.0) # 30 fps
        self.countdown_event = Clock.schedule_interval(self.tick, 1.0)
        
    def update_frame(self, dt):
        if not self.capture:
            return
            
        ret, frame = self.capture.read()
        if ret:
            # Process via MediaPipe Engine
            annotated_frame, frame_score, feedback = self.engine.process_frame(frame)
            
            # Update UI state
            self.instruction = feedback
            self.score = frame_score
            
            # Convert annotated frame back to texture for Kivy
            buf1 = cv2.flip(annotated_frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # Display image
            self.ids.cam_image.texture = image_texture

    def tick(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.finish_session()
            
    def finish_session(self):
        self.cleanup()
        print("Yoga session complete.")
        self.manager.current = "dashboard"
        
    def end_early(self):
        self.cleanup()
        self.manager.current = "dashboard"
        
    def cleanup(self):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
        if hasattr(self, 'countdown_event'):
            self.countdown_event.cancel()
        if self.capture:
            self.capture.release()
            self.capture = None
            
    def on_leave(self, *args):
        self.cleanup()
