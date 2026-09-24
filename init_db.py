import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "study.db"

print("init_db.py is here:", Path(__file__).resolve())
print("Database will be here:", DATABASE)

connection = sqlite3.connect(DATABASE)

connection.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
""")

connection.commit()
connection.close()

print("Database initialized!")