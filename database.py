import sqlite3
from datetime import datetime

DB_NAME = "mind_melody.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS emotion_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            emotion TEXT,
            source TEXT,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_journal(emotion, source, note):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO emotion_journal (time, emotion, source, note)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%H:%M - %d/%m/%Y"),
        emotion,
        source,
        note
    ))

    conn.commit()
    conn.close()

def load_journal():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT time, emotion, source, note
        FROM emotion_journal
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    return rows

def clear_journal():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM emotion_journal")

    conn.commit()
    conn.close()