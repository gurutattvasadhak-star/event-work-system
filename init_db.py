import sqlite3

DB = "database.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------- USERS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    head_id INTEGER
)
""")

# ---------------- TASKS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    member_id INTEGER,
    head_id INTEGER,
    due_date TEXT,
    priority TEXT,
    status TEXT
)
""")

# ---------------- DEFAULT HEAD ----------------
cur.execute("""
INSERT OR IGNORE INTO users (id, name, email, password, role)
VALUES (1, 'Head Admin', 'head@gmail.com', '1234', 'head')
""")

# ---------------- DEFAULT MEMBERS ----------------
members = [
    ('Member One', 'member1@gmail.com', '1234', 'member', 1),
    ('Member Two', 'member2@gmail.com', '1234', 'member', 1),
    ('Member Three', 'member3@gmail.com', '1234', 'member', 1),
    ('Member Four', 'member4@gmail.com', '1234', 'member', 1),
    ('Member Five', 'member5@gmail.com', '1234', 'member', 1),
]

cur.executemany("""
INSERT OR IGNORE INTO users (name, email, password, role, head_id)
VALUES (?, ?, ?, ?, ?)
""", members)

conn.commit()
conn.close()

print("✅ Database initialized successfully")