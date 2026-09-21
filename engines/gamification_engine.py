import json
from datetime import datetime, timedelta
from core.database import get_connection

class GamificationEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        self._ensure_record()
        
    def _ensure_record(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM gamification WHERE user_id=?", (self.user_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO gamification (user_id, total_points, current_streak, longest_streak, badges_json)
                    VALUES (?, 0, 0, 0, '[]')
                """, (self.user_id,))
                conn.commit()
                
    def check_in(self):
        """Called daily to update streaks."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_active_date, current_streak, longest_streak FROM gamification WHERE user_id=?", (self.user_id,))
            row = cursor.fetchone()
            
            today = datetime.now().date()
            if row and row["last_active_date"]:
                last_active = datetime.strptime(row["last_active_date"], "%Y-%m-%d").date()
                delta = (today - last_active).days
                
                if delta == 1:
                    new_streak = row["current_streak"] + 1
                elif delta == 0:
                    new_streak = row["current_streak"] # Already checked in
                else:
                    new_streak = 1 # Broken streak
            else:
                new_streak = 1
                
            longest = max(new_streak, row["longest_streak"] if row else 0)
            
            cursor.execute("""
                UPDATE gamification SET
                current_streak=?, longest_streak=?, last_active_date=?
                WHERE user_id=?
            """, (new_streak, longest, today.strftime("%Y-%m-%d"), self.user_id))
            conn.commit()
            
            return new_streak

    def add_points(self, points):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE gamification SET total_points = total_points + ? WHERE user_id=?", (points, self.user_id))
            conn.commit()

    def get_stats(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gamification WHERE user_id=?", (self.user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
        return {}
