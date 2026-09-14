import os
import sqlite3

# the file used when nothing else is specified
DEFAULT_DB_PATH = "applications.db"


def db_path():
    # tests point this at a throwaway file by setting DB_PATH
    return os.environ.get("DB_PATH", DEFAULT_DB_PATH)


def get_db():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            link TEXT,
            status TEXT NOT NULL DEFAULT 'applied',
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("database initialized")
