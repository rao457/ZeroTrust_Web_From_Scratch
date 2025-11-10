import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent.parent / "data" / "data.db"

def init_db():
    """Create database and contacts table if not exists"""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contact (
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        print("📦 Database initialize")


def save_contact(name, email, message):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO contact (name, email, message) VALUES (?, ? , ?)",
            (name, email, message)
        )
    print(f"✅ Contact saved: {name}, {email}, {message}")

def save_user(username, email, password):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO users(username, email, password) VALUES(?, ?, ?)",
            (username, email, password)
        )
        print(f"✅ User saved {username} : {email}")

def get_user(username):
    """Fetching user by username in the db"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, email, password FROM users WHERE username = ?", (username,))
        return cur.fetchone()