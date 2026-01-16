import sqlite3
from datetime import datetime

DB_NAME = "rumourshield.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_text TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        keywords TEXT,
        factchecks TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_check(input_text, prediction, confidence, keywords, factchecks):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO checks (input_text, prediction, confidence, keywords, factchecks, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        input_text,
        prediction,
        confidence,
        ",".join(keywords) if keywords else "",
        str(factchecks),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_history(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, input_text, prediction, confidence, keywords, created_at
    FROM checks
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r[0],
            "input_text": r[1],
            "prediction": r[2],
            "confidence": r[3],
            "keywords": r[4],
            "created_at": r[5]
        })

    return history
