import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "companion.db")


def add_task(task_text: str):
    print("DATABASE PATH:", DB_PATH)
    print("DATABASE DIRECTORY EXISTS:", os.path.exists(os.path.dirname(DB_PATH)))

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    cursor.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task_text,)
    )

    connection.commit()
    connection.close()

def get_tasks():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    rows = cursor.execute("""
        SELECT id, task, completed
        FROM tasks
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "task": row[1],
            "completed": bool(row[2])
        }
        for row in rows
    ]

if __name__ == "__main__":
    add_task("Test task - finish DBMS assignment")
    print("Task saved successfully!")

