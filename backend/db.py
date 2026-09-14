import sqlite3

DB_PATH = "applications.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
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
        )""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("database initialized")