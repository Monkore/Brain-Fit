from typing import Optional
from core.database import get_connection
from models.user import User

class UserRepository:
    @staticmethod
    def get_user() -> Optional[User]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return User(**dict(row))
            return None

    @staticmethod
    def create_user(user: User) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, age, gender, language, activity_level, sleep_duration, meditation_exp, exercise_freq)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user.name, user.age, user.gender, user.language, user.activity_level, user.sleep_duration, user.meditation_exp, user.exercise_freq))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_user(user: User):
        if user.id is None:
            raise ValueError("User ID cannot be None for update")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET 
                    name=?, age=?, gender=?, language=?, activity_level=?, 
                    sleep_duration=?, meditation_exp=?, exercise_freq=?
                WHERE id=?
            """, (user.name, user.age, user.gender, user.language, user.activity_level, user.sleep_duration, user.meditation_exp, user.exercise_freq, user.id))
            conn.commit()
