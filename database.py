import sqlite3
from datetime import datetime

# 1. Connect to the Database (Creates a file 'jarvis_memory.db' automatically)
DB_NAME = "jarvis_memory.db"

def init_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            content TEXT,
            language TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(role, content, language="en"):
    """Saves a single message to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (timestamp, role, content, language) VALUES (?, ?, ?, ?)",
              (timestamp, role, content, language))
    conn.commit()
    conn.close()

def load_last_n_messages(n=10):
    """Loads context for the Brain (last N messages)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Get last N rows
    c.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    
    # We must reverse them because we grabbed them backwards (DESC)
    messages = [{"role": r[0], "content": r[1]} for r in rows]
    return messages[::-1]