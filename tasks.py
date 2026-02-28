import sqlite3

DB = "database.db"

def create_task(title, description, member_id, head_id, due_date, priority):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (
            title, description, member_id, head_id,
            due_date, priority, status
        )
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    """, (title, description, member_id, head_id, due_date, priority))
    conn.commit()
    conn.close()

def get_all_members():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users WHERE role='member'")
    data = cur.fetchall()
    conn.close()
    return data

def get_tasks_for_member(member_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, due_date, priority, status
        FROM tasks
        WHERE member_id=?
    """, (member_id,))
    data = cur.fetchall()
    conn.close()
    return data

def get_all_tasks():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, t.title, u.name, t.due_date, t.priority, t.status
        FROM tasks t
        JOIN users u ON t.member_id = u.id
    """)
    data = cur.fetchall()
    conn.close()
    return data

def mark_task_completed(task_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (task_id,)
    )
    conn.commit()
    conn.close()

def get_head_email(head_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT email FROM users WHERE id=?",
        (head_id,)
    )
    email = cur.fetchone()[0]
    conn.close()
    return email

def get_member_email(member_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT email, name FROM users WHERE id=?",
        (member_id,)
    )
    data = cur.fetchone()
    conn.close()
    return data
