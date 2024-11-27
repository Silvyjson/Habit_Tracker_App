from datetime import datetime, timedelta
from db_manager import create_connection

# Initialize database connection
dbconnection = create_connection()
dbcursor = dbconnection.cursor()

# Helper function to format date
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# ANALYTICS FUNCTIONS

# Get longest streak
def get_longest_streak():
    result = dbcursor.execute("SELECT habit_name, MAX(streak) FROM Habits WHERE habit_status = 'active'").fetchone()
    return {"habit_name": result[0], "streak": result[1]} if result else None

# Get all active habits by period
def get_habits_by_period(periodicity):
    period_map = {1: "daily", 2: "weekly"}
    period = period_map.get(periodicity)
    query = "SELECT habit_name FROM Habits WHERE habit_period = ? AND habit_status = 'active'"
    dbcursor.execute(query, (period,))
    return [habit[0] for habit in dbcursor.fetchall()]

# Helper to calculate missed counts
def calculate_missed_counts(habit_name, habit_period, creation_date, interval):
    current_date = datetime.now()
    habit_start_date = max(current_date - timedelta(days=30), datetime.strptime(creation_date, "%Y-%m-%d"))
    
    if habit_period == 'daily':
        tracked_units = (current_date - habit_start_date).days + 1
        query = "SELECT COUNT(DISTINCT task_log_date) FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?"
    elif habit_period == 'weekly':
        # Calculate all ISO weeks in the date range
        start_week = habit_start_date.isocalendar()[1]
        end_week = current_date.isocalendar()[1]
        tracked_units = end_week - start_week + 1

        # Count distinct weeks with logs
        query = "SELECT COUNT(DISTINCT strftime('%Y-%W', task_log_date)) FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?"
    else:
        raise ValueError("Unsupported habit period")
    
    completed_units = dbcursor.execute(
        query,
        (habit_name, habit_start_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"))
    ).fetchone()[0]
    
    return tracked_units, completed_units

# Get struggled habits over the last month
def get_struggled_habits():
    struggled_habits = []
    query = "SELECT habit_name, creation_date, habit_period FROM Habits WHERE habit_status = 'active'"
    
    for habit_name, creation_date, habit_period in dbcursor.execute(query).fetchall():
         # Calculate how long the habit has been active
        habit_creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
        days_since_creation = (datetime.now() - habit_creation_date).days

        # Determine the interval for tracking missed units
        if habit_period == 'daily':
            interval = min(days_since_creation, 30)
        elif habit_period == 'weekly':
            creation_iso_week = habit_creation_date.isocalendar()[1]
            current_iso_week = datetime.now().isocalendar()[1]
            interval = min(current_iso_week - creation_iso_week + 1, 4)
        else:
            raise ValueError("Unsupported habit period")
    
        tracked_units, completed_units = calculate_missed_counts(habit_name, habit_period, creation_date, interval)

        if completed_units < interval:
            struggled_habits.append(f"The {habit_period} habit {habit_name} has struggled for the past {interval} {'days' if habit_period == 'daily' else 'weeks'} with {tracked_units - completed_units} missed units within this month.")

    return struggled_habits

# Get missed habits from creation date to today
def get_missed_habits():
    missed_habits = []
    query = "SELECT habit_name, creation_date, habit_period FROM Habits WHERE habit_status = 'active'"
    
    for habit_name, creation_date, habit_period in dbcursor.execute(query).fetchall():
        tracked_units, completed_units = calculate_missed_counts(habit_name, habit_period, creation_date, interval=None)
        
        if completed_units < tracked_units:
            missed_habits.append(f"The {habit_period} habit {habit_name} was missed {tracked_units - completed_units} times since its creation")
    return missed_habits

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
