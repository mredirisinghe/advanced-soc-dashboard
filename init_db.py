import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/soc.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    ip TEXT,

    attack_type TEXT,

    severity TEXT,

    mitre TEXT,

    endpoint TEXT,

    status_code TEXT,

    raw_log TEXT
)
""")

conn.commit()
conn.close()

print("✅ SOC Database Initialized")
