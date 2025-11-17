import sqlite3
import uuid
import os
from pathlib import Path
DB_NAME = Path(__file__).resolve().parent.parent / "data" / "data.db"

# Inserting user in the sessions table in db
def create_session(username):
    session_id = str(uuid.uuid4())
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("INSERT INTO sessions(username, session_id) VALUES(?, ?)", (username, session_id) )
    con.commit()
    con.close()
    return session_id

# Finding user by session id
def get_user_by_session(session_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else None

    
# Deleting session to log out the users
def delete_session(session_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
    con.commit()
    con.close()