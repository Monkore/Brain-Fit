from typing import Optional, List
from core.database import get_connection
from models.checkin import Checkin

class CheckinRepository:
    @staticmethod
    def get_todays_checkin(user_id: int, date_str: str) -> Optional[Checkin]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_checkins WHERE user_id = ? AND date = ?", (user_id, date_str))
            row = cursor.fetchone()
            if row:
                return Checkin(**dict(row))
            return None

    @staticmethod
    def save_checkin(checkin: Checkin) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daily_checkins (user_id, date, mood, stress, anxiety, energy, focus, motivation, mental_fatigue, sleep_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (checkin.user_id, checkin.date, checkin.mood, checkin.stress, checkin.anxiety, checkin.energy, checkin.focus, checkin.motivation, checkin.mental_fatigue, checkin.sleep_hours))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_recent_checkins(user_id: int, limit: int = 7) -> List[Checkin]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_checkins WHERE user_id = ? ORDER BY date DESC LIMIT ?", (user_id, limit))
            rows = cursor.fetchall()
            return [Checkin(**dict(row)) for row in rows]
