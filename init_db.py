import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "study.db"

print("init_db.py is here:", Path(__file__).resolve())
print("Database will be here:", DATABASE)

connection = sqlite3.connect(DATABASE)

connection.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
""")

connection.commit()
connection.close()

print("Database initialized!")