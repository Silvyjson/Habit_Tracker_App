#Import python datetime module
import datetime
from datetime import date
from datetime import timedelta
from db_manager import create_connection


dbconnection = create_connection()
dbcursor = dbconnection.cursor()

#Create an OOP class named MyHabits
class MyHabits:
    #Define the name, period, date and status properties for the class
    def __init__(self, habit_name, habit_period, creation_date, habit_status):
        self.habit_name = habit_name
        self.habit_period = habit_period
        self.creation_date = creation_date
        self.habit_status = habit_status

    #Create a new habit
    def add_habit(self):
        #Print the Habit Name
        print("Habit: " + self.habit_name)
        #Print the Habit Period

        # Define periodicity using a dictionary
        periodicity_map = {1: "daily", 2: "weekly"}
        self.habit_period = periodicity_map.get(self.habit_period, None)

        if self.habit_period is None:
            print("INVALID INPUT FOR HABIT PERIOD")
            return
            
        print("Habit Period: " + self.habit_period)
        #Print the Habit Entry Date
        print("Date: " + f"{self.creation_date}")
        #Print the Habit Status
        print("Habit Status: " + F"{self.habit_status}")
        #Insert the Habit into the Habits Table in the Database
        
        query = "INSERT INTO Habits (habit_name, habit_period, creation_date, Last_completed, streak, habit_status) VALUES (?, ?, ?, ?, ?, ?)"
        query_values = (self.habit_name, self.habit_period, self.creation_date, "none", 0, 'active')
        dbcursor.execute(query, query_values)
        dbconnection.commit()
        print(dbcursor.rowcount, "Habit Created.")

    #Remove a habit
    def remove_habit():
        query = "SELECT id, habit_name FROM Habits WHERE habit_status = ?"
        status = ('active', )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
       
        #List all active habits to User
        print("MY CURRENT HABITS")
        for x in habits:
            print(x)
       
        remove_id = int(input("Enter habit ID number to remove habit: "))
       
        # Check if the ID is valid before trying to update
        dbcursor.execute("SELECT id FROM Habits WHERE id = ? AND habit_status = 'active'", (remove_id,))
        active_habit = dbcursor.fetchone()
        
        if active_habit:
            # Update the habit status to inactive
            query = "UPDATE Habits SET habit_status = 'inactive' WHERE id = ?"
            id = (remove_id, )
            dbcursor.execute(query, id)
            print("HABIT REMOVED")
        else:
            print("INVALID HABIT ID")

    #LIST ALL USER HABITS
    def list_all_habits():
        query = "SELECT * FROM Habits WHERE habit_status = ?"
        status = ('active', )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
       
        #Display Habits to User
        print("MY HABITS RECORD")
        print("----------------")
        for x in habits:
            print(x)
            print("----------------")
            

    #LIST HABITS BY pERIODICITY
    def list_habits_by_periodicity(period):
        if period == 1:
            query = "SELECT * FROM Habits WHERE habit_period = ? AND habit_status = ?"
            params = ("daily", 'active', )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall() 
            #Display Habits to User
            for x in habits:
                print(x)
       
        elif period == 2:
            query = "SELECT * FROM Habits WHERE habit_period = ? AND habit_status = ?"
            params = ("weekly", 1, )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall()
            #Display Habits to User
            for x in habits:
                print(x)
        else:
            print("INVALID INPUT")

    #TASK MANAGEMENT

    #CHECK OFF/LOG A HABIT TASK AS cOMPLETED
    def check_off_task():
        # Display existing habit record to user
        MyHabits.list_all_habits()
        
        # Prompt user for the habit ID which he/she wants to check off its task
        id = int(input("ENTER HABIT ID TO LOG TASK AS COMPLETED: "))
        
        # Validate the habit ID against the database Habits table record
        query = "SELECT * FROM Habits WHERE id = ? AND habit_status = ?"
        params = (id, 'active', )
        habit = dbcursor.execute(query, params).fetchone()
        
        if habit:
            habit_id = habit[0]
            task = habit[1]
            periodicity = habit[2]
            log_date = datetime.datetime.now().strftime("%x")
            
            # Initialize current streak
            current_streak = 1
            
            # Check streak based on periodicity
            if periodicity == "daily":
                # Check if the task was completed yesterday
                yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime("%x")
                query1 = "SELECT streak FROM Tasks WHERE habit_id = ? AND periodicity = ? AND task_log_date = ?"
                query_values1 = (habit_id, "daily", yesterday)
                dbcursor.execute(query1, query_values1)
                streak = dbcursor.fetchone()
                
                if streak:
                    current_streak += streak[0]

            elif periodicity == "weekly":
                # Check if the task was completed during the current week
                today = datetime.datetime.now()
                week_start = today - timedelta(days=today.weekday())  # Monday of this week
                week_end = week_start + timedelta(days=6)  # Sunday of this week

                query1 = "SELECT streak FROM Tasks WHERE habit_id = ? AND periodicity = ? AND task_log_date BETWEEN ? AND ?"
                query_values1 = (habit_id, "weekly", week_start.strftime("%x"), week_end.strftime("%x"))
                dbcursor.execute(query1, query_values1)
                streak = dbcursor.fetchone()

                if streak:
                    current_streak += streak[0]

                # Check if the task has already been completed within the current week
                query2 = "SELECT COUNT(*) FROM Tasks WHERE habit_id = ? AND task_log_date BETWEEN ? AND ? AND task_status = ?"
                query_values2 = (habit_id, week_start.strftime("%x"), week_end.strftime("%x"), "completed")
                dbcursor.execute(query2, query_values2)
                task_log_count = dbcursor.fetchone()[0]

                if task_log_count > 0:
                    print(f"You've already completed and logged this task for the week.")
                    return

            # Check if the task has already been completed for today (or week for weekly habits)
            query2 = "SELECT COUNT(*) FROM Tasks WHERE habit_id = ? AND task_log_date = ? AND task_status = ?"
            query_values2 = (habit_id, log_date, "completed")
            dbcursor.execute(query2, query_values2)
            task_log_count = dbcursor.fetchone()[0]

            if task_log_count == 0:
                # Log the completed task
                query3 = "INSERT INTO Tasks (habit_id, task_name, periodicity, task_log_date, streak, task_status) VALUES (?, ?, ?, ?, ?, ?)"
                query_values3 = (habit_id, task, periodicity, log_date, current_streak, "completed")
                dbcursor.execute(query3, query_values3)

                # Update the habit's last completed date and streak
                query4 = "UPDATE Habits SET Last_completed = ?, streak = ? WHERE id = ?"
                query_values4 = (log_date, current_streak, habit_id)
                dbcursor.execute(query4, query_values4)
                dbconnection.commit()

                print(f"Task '{task}' for habit ID {habit_id} completed! streak updated to {current_streak}.")
            else:
                print(f"You've already completed and logged this task for the {periodicity.lower()}.")
        else:
            print("Habit ID Error")


    #LIST ALL cOMPLETED TASKS ON THIS DAY
    def get_completed_tasks():
        x = datetime.datetime.now()
        log_date = x.strftime("%x")
        query = "SELECT * FROM Tasks WHERE task_log_date = ?"
        param = (log_date, )
        dbcursor.execute(query, param)
        tasks = dbcursor.fetchall()
        #Display Habits to User
        print("TASKS COMPLETED TODAY")
        print("----------------------")
        for x in tasks: 
            print(f"TASKID {x[0]}: {x}")
            print("----------------------")

    # Analyzing habits: Longest streak, current habits, struggled habits
    def analyze_habits():
        # Get the longest streak
        longest_streak = dbcursor.execute("SELECT habit_name, MAX(streak) FROM Habits").fetchone()
        print(f"Longest streak: {longest_streak[1]} days for habit '{longest_streak[0]}'")

        # Get the list of current daily habits
        daily_habits = dbcursor.execute("SELECT habit_name FROM Habits WHERE habit_period = 'daily' AND habit_status = 'active'").fetchall()
        print("Current daily Habits:")
        for habit in daily_habits:
            print(habit[0])

        # Get the list of current weekly habits
        weekly_habits = dbcursor.execute("SELECT habit_name FROM Habits WHERE habit_period = 'weekly' AND habit_status = 'active'").fetchall()
        print("Current weekly Habits:")
        for habit in weekly_habits:
            print(habit[0])

        # Get habits where the user struggled last month
        last_month_start = (datetime.datetime.now() - timedelta(days=30)).strftime("%x")
        struggled_habits = dbcursor.execute(
            "SELECT task_name FROM Tasks WHERE task_status = 'missed' AND task_log_date >= ?",
            (last_month_start,)
        ).fetchall()
        print("Habits struggled last month:")
        for habit in struggled_habits:
            print(habit[0])

    # Check for missed habits
    def check_missed_habits():
        # Query for habits that should have been completed but were missed
        missed_habits = dbcursor.execute(
            "SELECT habit_name FROM Habits WHERE Last_completed < ? AND habit_status = 'active'",
            (datetime.datetime.now().strftime("%x"),)
        ).fetchall()
        
        print("Missed Habits:")
        for habit in missed_habits:
            print(habit[0])

    # Return the longest run streak for a specific habit
    def get_longest_streak_for_habit(habit_name):
        query = "SELECT streak FROM Habits WHERE habit_name = ?"
        dbcursor.execute(query, (habit_name,))
        streak = dbcursor.fetchone()
        
        if streak:
            print(f"The longest streak for habit '{habit_name}' is {streak[0]} days.")
        else:
            print(f"Habit '{habit_name}' not found.")


     # Log all existing tasks       
    def list_all_tasks():
        query = "SELECT * FROM Tasks"
        dbcursor.execute(query)
        tasks = dbcursor.fetchall()

        # Display tasks with TASKID label
        print("ALL TASKS")
        print("----------------------")
        for task in tasks:
            print(f"TASKID {task[0]}: {task}")
            print("----------------------")

