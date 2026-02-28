import sqlite3

DB = "database.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Change password for head
cur.execute("""
UPDATE users
SET password = '1234'
WHERE email = 'head@gmail.com'
""")

conn.commit()
conn.close()

print("✅ Head password updated successfully")