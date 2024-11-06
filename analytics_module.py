import datetime
from datetime import date, timedelta
from db_manager import create_connection

# Initialize database connection
dbconnection = create_connection()
dbcursor = dbconnection.cursor()

# Helper function to format date
def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# ANALYTICS FUNCTIONS

# Get longest streak
def get_longest_streak():
    result = dbcursor.execute("SELECT habit_name, MAX(streak) FROM Habits WHERE habit_status = 'active'").fetchone()
    return {"habit_name": result[0], "streak": result[1]} if result else None

# Get all active habits by period
def get_habits_by_period(periodicity):
    query = "SELECT habit_name FROM Habits WHERE habit_period = ? AND habit_status = 'active'"
    period_map = {1: "daily", 2: "weekly"}
    period = period_map.get(periodicity)
    dbcursor.execute(query, (period,))
    return [habit[0] for habit in dbcursor.fetchall()]

# Get struggled habits over the last month
def get_struggled_habits():
    last_month_start = (datetime.datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    query = "SELECT task_name FROM Tasks WHERE task_status = 'missed' AND task_log_date >= ?"
    dbcursor.execute(query, (last_month_start,))
    return [task[0] for task in dbcursor.fetchall()]

# Get missed habits based on Last_completed date
def get_missed_habits():
    current_date = get_current_date()
    query = "SELECT habit_name FROM Habits WHERE last_completed < ? AND habit_status = 'active'"
    dbcursor.execute(query, (current_date,))
    return [habit[0] for habit in dbcursor.fetchall()]

# DISPLAY FUNCTIONS

# Display data with headers
def display_data(header, data):
    print(header)
    print("----------------")
    for item in data:
        print(item)
    print("----------------")

# Display analytics summary
def display_analytics_summary():
    # Longest Streak
    longest_streak = get_longest_streak()
    if longest_streak:
        print(f"Longest streak: {longest_streak['streak']} days for habit '{longest_streak['habit_name']}'")
    else:
        print("No longest streak found.")

    # Current Daily Habits
    daily_habits = get_habits_by_period(1)
    display_data("Current Daily Habits:", daily_habits)

    # Current Weekly Habits
    weekly_habits = get_habits_by_period(2)
    display_data("Current Weekly Habits:", weekly_habits)

    # Struggled Habits Last Month
    struggled_habits = get_struggled_habits()
    display_data("Habits struggled last month:", struggled_habits)

    # Missed Habits
    missed_habits = get_missed_habits()
    display_data("Missed Habits:", missed_habits)

# Get longest streak for a specific habit
def get_longest_streak_for_habit(habit_name):
    query = "SELECT streak FROM Habits WHERE habit_name = ? AND habit_status = 'active'"
    dbcursor.execute(query, (habit_name,))
    result = dbcursor.fetchone()

    if result:
        print("Longest streak for habit", habit_name, "is", result[0])
    else:
        print("No active habit found with the name:", habit_name)
        
    return result[0] if result else 0


# LIST AND LOGGING FUNCTIONS

# List all habits
def list_all_habits():
    query = "SELECT * FROM Habits WHERE habit_status = 'active'"
    dbcursor.execute(query)
    return dbcursor.fetchall()

# List all tasks for a specific day
def get_completed_tasks_for_date(log_date):
    query = "SELECT * FROM Tasks WHERE task_log_date = ?"
    dbcursor.execute(query, (log_date,))
    return dbcursor.fetchall()

# List all tasks
def list_all_tasks():
    query = "SELECT * FROM Tasks"
    dbcursor.execute(query)
    return dbcursor.fetchall()
