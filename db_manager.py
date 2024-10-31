# Import python sqlite3 module for database management
import sqlite3

# Create and establish a connection to the database
def create_connection():
    return sqlite3.connect("MyHabitTrackerDatabase")

def create_tables(dbcursor):
    # Create Habits table for storing user habits
    dbcursor.execute("""
        CREATE TABLE IF NOT EXISTS Habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            habit_period TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            last_completed TEXT,
            streak INTEGER NOT NULL,
            habit_status TEXT NOT NULL
        )
    """)

    # Create Tasks table for storing completed habit tasks record
    dbcursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            task_name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            task_log_date TEXT NOT NULL,
            streak INTEGER NOT NULL,
            task_status TEXT NOT NULL
        )
    """)
