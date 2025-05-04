import sqlite3

DATABASE = 'app.db'

def migrate():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            # Add the 'is_admin' column if it doesn't exist
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;")
            print("Migration successful: 'is_admin' column added.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Migration skipped: 'is_admin' column already exists.")
            else:
                raise e

if __name__ == "__main__":
    migrate()