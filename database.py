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
            note TEXT,
            playlist TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_journal(emotion, source, note, playlist):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO emotion_journal (
            time,
            emotion,
            source,
            note,
            playlist
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%H:%M - %d/%m/%Y"),
        emotion,
        source,
        note,
        playlist
    ))

    conn.commit()
    conn.close()


def load_journal():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT time, emotion, source, note, playlist
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