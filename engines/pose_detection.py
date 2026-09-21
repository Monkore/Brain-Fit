import logging
import cv2
import numpy as np

logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    logger.warning("Mediapipe not installed. Pose detection disabled.")
    MEDIAPIPE_AVAILABLE = False

class PoseEngine:
    def __init__(self):
        if MEDIAPIPE_AVAILABLE:
            self.pose = mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                model_complexity=1 # 0, 1, 2. 1 is good balance for mobile
            )
        else:
            self.pose = None
            
    def process_frame(self, frame_np: np.ndarray):
        """
        Processes a BGR numpy array frame.
        Returns: (annotated_frame_np, score, feedback_string)
        """
        if not MEDIAPIPE_AVAILABLE or self.pose is None:
            return frame_np, 0, "Pose detection disabled"
            
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        results = self.pose.process(rgb_frame)
        
        rgb_frame.flags.writeable = True
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        score = 0
        feedback = "Adjusting..."
        
        if results.pose_landmarks:
            # Draw skeleton
            mp_drawing.draw_landmarks(
                bgr_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Simple heuristic for demonstration:
            # Check if shoulders are level
            landmarks = results.pose_landmarks.landmark
            l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            
            y_diff = abs(l_shoulder.y - r_shoulder.y)
            if y_diff < 0.05:
                score = 90
                feedback = "Good posture!"
            else:
                score = 50
                feedback = "Keep shoulders level"
        else:
            feedback = "No pose detected"
            
        return bgr_frame, score, feedback

    def close(self):
        if self.pose:
            self.pose.close()
