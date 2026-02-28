import sqlite3
import bcrypt

DB_PATH = "data/system.db"

def login_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, name, email, role, password FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if row:
        stored_hash = row[4]
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3]
            }
    return None


def add_user(name, email, password, role="member"):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, email, role, password) VALUES (?, ?, ?, ?)",
        (name, email, role, hashed)
    )

    conn.commit()
    conn.close()
