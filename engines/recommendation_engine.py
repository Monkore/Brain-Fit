from core.database import get_connection
import random

class RecommendationEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        
    def get_daily_recommendation(self):
        """
        Returns a recommended set of activities (e.g. 1 physical, 1 cognitive, 1 audio)
        Prioritizes activities not played recently, balancing difficulty and mastery.
        """
        recommended_ids = []
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Fetch all activities, sort by last_played (null first) to ensure long-term rotation
            cursor.execute("""
                SELECT id, template_id, domain, name, category, parameters_json 
                FROM activities 
                ORDER BY last_played ASC NULLS FIRST
            """)
            activities = cursor.fetchall()
            
            # Group by domain
            domains = {"Physical": [], "Cognitive": [], "Audio": []}
            for a in activities:
                # Map template_id to a simpler domain for recommendation
                if a["template_id"] == "physical_template" or a["template_id"] == "physical_pose":
                    domains["Physical"].append(dict(a))
                elif a["template_id"] == "audio_template" or a["template_id"] == "audio_guide":
                    domains["Audio"].append(dict(a))
                else:
                    domains["Cognitive"].append(dict(a))
                    
            # Pick top 1 from each
            if domains["Cognitive"]: recommended_ids.append(domains["Cognitive"][0])
            if domains["Physical"]: recommended_ids.append(domains["Physical"][0])
            if domains["Audio"]: recommended_ids.append(domains["Audio"][0])
            
        return recommended_ids
        
    def log_activity_completion(self, activity_id, score=0):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE activities SET last_played = CURRENT_TIMESTAMP WHERE id = ?", (activity_id,))
            conn.commit()
