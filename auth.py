import sqlite3
import bcrypt

DB = "database.db"

def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password BLOB,
        role TEXT
    )
    """)

    # TASKS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        member_id INTEGER,
        head_id INTEGER,
        due_date TEXT,
        priority TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

# Ensure DB exists
init_db()

# ADD USER
def add_user(name, email, password, role):
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed, role)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()


# LOGIN USER
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, password, role FROM users WHERE email=?",
        (email,)
    )

    row = cur.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[3]):
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[4]
        }

    return None
