import ctypes
import time
import sqlite3
import os
from datetime import date
from ctypes import wintypes


def get_active_window_title():

    user32 = ctypes.windll.user32

    hwnd = user32.GetForegroundWindow()

    length = user32.GetWindowTextLengthW(hwnd)

    if length == 0:
        return ""

    buffer = ctypes.create_unicode_buffer(length + 1)

    user32.GetWindowTextW(
        hwnd,
        buffer,
        length + 1
    )

    return buffer.value

def get_active_process_name():

    user32 = ctypes.windll.user32

    hwnd = user32.GetForegroundWindow()

    process_id = wintypes.DWORD()

    user32.GetWindowThreadProcessId(
        hwnd,
        ctypes.byref(process_id)
    )

    try:
        process = __import__("psutil").Process(process_id.value)
        return process.name()

    except Exception:
        return ""

def categorize_process(process_name):

    process_name = process_name.lower()

    if process_name in ["code.exe"]:
        return "Focused Work"

    if process_name in ["chrome.exe", "msedge.exe", "firefox.exe"]:
        return "Browser"

    if process_name in ["powerpnt.exe", "winword.exe"]:
        return "Productivity"

    if process_name in ["spotify.exe"]:
        return "Entertainment"

    return "Other"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "companion.db")


def record_activity(category, seconds):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_activity (
            activity_date TEXT NOT NULL,
            category TEXT NOT NULL,
            seconds REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (activity_date, category)
        )
    """)

    cursor.execute("""
        INSERT INTO daily_activity (activity_date, category, seconds)
        VALUES (?, ?, ?)
        ON CONFLICT(activity_date, category)
        DO UPDATE SET seconds = seconds + excluded.seconds
    """, (
        date.today().isoformat(),
        category,
        seconds
    ))

    connection.commit()
    connection.close()

def get_daily_activity():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_activity (
            activity_date TEXT NOT NULL,
            category TEXT NOT NULL,
            seconds REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (activity_date, category)
        )
    """)

    cursor.execute("""
        SELECT category, seconds
        FROM daily_activity
        WHERE activity_date = ?
        ORDER BY seconds DESC
    """, (date.today().isoformat(),))

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "category": row[0],
            "seconds": row[1]
        }
        for row in rows
    ]

if __name__ == "__main__":

    print("Activity tracker started.")
    print("Press Ctrl+C to stop.\n")

    last_process = None
    last_time = time.time()

    activity_totals = {}
    while True:

        current_process = get_active_process_name()
        current_time = time.time()

        if current_process != last_process:

            if last_process:
                elapsed = current_time - last_time
                category = categorize_process(last_process)

                activity_totals[category] = (
                activity_totals.get(category, 0)
                + elapsed
            )

                record_activity(category, elapsed)

                print(
                f"{last_process} ({category}) "
                f"was active for {elapsed:.1f} seconds"
            )

            current_category = categorize_process(current_process)

            print(
            f"Now active: {current_process} "
            f"→ {current_category}"
        )

            last_process = current_process
            last_time = current_time

        time.sleep(5)