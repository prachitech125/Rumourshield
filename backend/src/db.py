import sqlite3
import json
from datetime import datetime

DB_PATH = "rumourshield.db"

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL,
            keywords TEXT,
            factchecks TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_check(input_text, prediction, confidence, keywords, factchecks):
    """Save a check to the database"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO checks (input_text, prediction, confidence, keywords, factchecks)
        VALUES (?, ?, ?, ?, ?)
    """, (
        input_text,
        prediction,
        confidence,
        json.dumps(keywords),
        json.dumps(factchecks)
    ))
    conn.commit()
    conn.close()

def get_history(limit=10):
    """Get check history from database"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, input_text, prediction, confidence, keywords, factchecks, timestamp
        FROM checks
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "input_text": row[1],
            "prediction": row[2],
            "confidence": row[3],
            "keywords": json.loads(row[4]) if row[4] else [],
            "factchecks": json.loads(row[5]) if row[5] else [],
            "timestamp": row[6]
        })
    
    return history