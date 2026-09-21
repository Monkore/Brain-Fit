import sqlite3
from pathlib import Path
import logging

from core.config import DB_PATH

logger = logging.getLogger(__name__)

def get_connection():
    """Returns a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT,
        language TEXT,
        activity_level TEXT,
        sleep_duration TEXT,
        meditation_exp TEXT,
        exercise_freq TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS daily_checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT NOT NULL,
        mood INTEGER,
        stress INTEGER,
        anxiety INTEGER,
        energy INTEGER,
        focus INTEGER,
        motivation INTEGER,
        mental_fatigue INTEGER,
        sleep_hours REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

    CREATE TABLE IF NOT EXISTS activities (
        id TEXT PRIMARY KEY,
        domain TEXT NOT NULL,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        base_difficulty INTEGER,
        template_id TEXT NOT NULL,
        parameters_json TEXT,
        last_played TIMESTAMP,
        mastery_level REAL DEFAULT 0.0
    );

    CREATE TABLE IF NOT EXISTS gamification (
        user_id INTEGER PRIMARY KEY,
        total_points INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        last_active_date TEXT,
        badges_json TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

    CREATE TABLE IF NOT EXISTS family_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        relation TEXT,
        photo_path TEXT,
        memories_json TEXT
    );

    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

    CREATE TABLE IF NOT EXISTS session_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        activity_id TEXT,
        "order" INTEGER,
        status TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (id),
        FOREIGN KEY (activity_id) REFERENCES activities (id)
    );

    CREATE TABLE IF NOT EXISTS performance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_activity_id INTEGER,
        score INTEGER,
        accuracy REAL,
        duration_seconds INTEGER,
        difficulty_feedback TEXT,
        enjoyment_feedback TEXT,
        energy_after TEXT,
        timestamp TEXT,
        FOREIGN KEY (session_activity_id) REFERENCES session_activities (id)
    );
    
    CREATE TABLE IF NOT EXISTS analytics_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT NOT NULL,
        resilience_score INTEGER,
        speed_score INTEGER,
        memory_score INTEGER,
        attention_score INTEGER,
        executive_score INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """
    try:
        with get_connection() as conn:
            conn.executescript(schema)
            conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    # Test DB init
    logging.basicConfig(level=logging.INFO)
    init_db()
    print("Database created at:", DB_PATH)
