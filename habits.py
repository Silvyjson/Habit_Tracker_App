#A HABIT TRACKING APPLICATION PROGRAM WRITTEN IN PYTHON
########################################################

#Import python datetime module
import datetime
from datetime import date
from datetime import timedelta
#Import python sqlite3 module for database management
import sqlite3

#Create and establish a connection to the database
dbconnection = sqlite3.connect("MyHabitTrackerDatabase")
dbcursor = dbconnection.cursor()

#Create Habits table for storing user habits
dbcursor.execute("CREATE TABLE IF NOT EXISTS Habits (ID INTEGER PRIMARY KEY AUTOINCREMENT, HabitName TEXT NOT NULL, HabitPeriod TEXT NOT NULL, CreationDate TEXT NOT NULL, LastCompleted TEXT, Streak INTEGER NOT NULL, HabitStatus TEXT NOT NULL)")

#Create Tasks table for storing completed habit tasks record
dbcursor.execute("CREATE TABLE IF NOT EXISTS Tasks (TaskID INTEGER PRIMARY KEY AUTOINCREMENT, HabitID INTEGER, Task TEXT NOT NULL, Periodicity TEXT NOT NULL, TaskLogDate TEXT NOT NULL, Streak INTEGER NOT NULL, TaskStatus TEXT NOT NULL)")

#Create an OOP class named MyHabits
class MyHabits:
    #Define the name, period, date and status properties for the class
    def __init__(self, habitName, habitPeriod, creationDate, habitStatus):
        self.habitName = habitName
        self.habitPeriod = habitPeriod
        self.creationDate = creationDate
        self.habitStatus = habitStatus

    #Create a new habit
    def addHabit(self):
        #Print the Habit Name
        print("Habit: " + self.habitName)
        #Print the Habit Period
        if self.habitPeriod == 1:
            self.habitPeriod = "Daily"
        elif self.habitPeriod == 2:
            self.habitPeriod = "Weekly"
        else:
            print("INVALID INPUT FOR HABIT PERIOD")
        print("Habit Period: " + self.habitPeriod)
        #Print the Habit Entry Date
        print("Date: " + f"{self.creationDate}")
        #Print the Habit Status
        print("Habit Status: " + F"{self.habitStatus}")
        #Insert the Habit into the Habits Table in the Database
        
        query = "INSERT INTO Habits (HabitName, HabitPeriod, CreationDate, LastCompleted, Streak, HabitStatus) VALUES (?, ?, ?, ?, ?, ?)"
        queryValues = (self.habitName, self.habitPeriod, self.creationDate, "NULL", 0, 'Active')
        dbcursor.execute(query, queryValues)
        dbconnection.commit()
        print(dbcursor.rowcount, "Habit Created.")

    #Remove a habit
    def removeHabit():
        query = "SELECT ID, HabitName FROM Habits WHERE HabitStatus = ?"
        status = ('Active', )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
        #List all active habits to User
        print("MY CURRENT HABITS")
        for x in habits:
            print(x)
        removeID = int(input("Enter habit ID number to remove habit: "))
        dbcursor.execute("SELECT ID FROM Habits WHERE HabitStatus = 'Active'")
        activeHabitsID = dbcursor.fetchall()
        for i in activeHabitsID:
            if i[0] == removeID:
                query = "UPDATE Habits SET HabitStatus = 'Inactive' WHERE ID = ?"
                id = (removeID, )
                dbcursor.execute(query, id)
                print("HABIT REMOVED")
            else:
                print("INVALID HABIT ID")

    #LIST ALL USER HABITS
    def listAllHabits():
        query = "SELECT * FROM Habits WHERE HabitStatus = ?"
        status = ('Active', )
        dbcursor.execute(query, status)
        habits = dbcursor.fetchall()
        #Display Habits to User
        print("MY HABITS RECORD")
        print("----------------")
        print("----------------")
        for x in habits:
            print(x)
            print("----------------")
            print("----------------")
            

    #LIST HABITS BY PERIODICITY
    def listHabitsByPeriodicity(period):
        if period == 1:
            query = "SELECT * FROM Habits WHERE HabitPeriod = ? AND HabitStatus = ?"
            params = ("Daily", 'Active', )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall()
            #Display Habits to User
            for x in habits:
                print(x)
        elif period == 2:
            query = "SELECT * FROM Habits WHERE HabitPeriod = ? AND HabitStatus = ?"
            params = ("Weekly", 1, )
            dbcursor.execute(query, params)
            habits = dbcursor.fetchall()
            #Display Habits to User
            for x in habits:
                print(x)
        else:
            print("INVALID INPUT")

    #TASK MANAGEMENT

    #CHECK OFF/LOG A HABIT TASK AS COMPLETED
    def CheckOffTask():
        # Display existing habit record to user
        MyHabits.listAllHabits()
        
        # Prompt user for the habit ID which he/she wants to check off its task
        id = int(input("ENTER HABIT ID TO LOG TASK AS COMPLETED: "))
        
        # Validate the habit ID against the database Habits table record
        query = "SELECT * FROM Habits WHERE ID = ? AND Habitstatus = ?"
        params = (id, 'Active', )
        habit = dbcursor.execute(query, params).fetchone()
        
        if habit:
            habitID = habit[0]
            task = habit[1]
            periodicity = habit[2]
            logDate = datetime.datetime.now().strftime("%x")
            
            # Initialize current streak
            currentStreak = 1
            
            # Check streak based on periodicity
            if periodicity == "Daily":
                # Check if the task was completed yesterday
                yesterday = (datetime.datetime.now() - timedelta(days=1)).strftime("%x")
                query1 = "SELECT Streak FROM Tasks WHERE HabitID = ? AND Periodicity = ? AND TaskLogDate = ?"
                queryValues1 = (habitID, "Daily", yesterday)
                dbcursor.execute(query1, queryValues1)
                streak = dbcursor.fetchone()
                
                if streak:
                    currentStreak += streak[0]

            elif periodicity == "Weekly":
                # Check if the task was completed during the current week
                today = datetime.datetime.now()
                week_start = today - timedelta(days=today.weekday())  # Monday of this week
                week_end = week_start + timedelta(days=6)  # Sunday of this week

                query1 = "SELECT Streak FROM Tasks WHERE HabitID = ? AND Periodicity = ? AND TaskLogDate BETWEEN ? AND ?"
                queryValues1 = (habitID, "Weekly", week_start.strftime("%x"), week_end.strftime("%x"))
                dbcursor.execute(query1, queryValues1)
                streak = dbcursor.fetchone()

                if streak:
                    currentStreak += streak[0]

            # Check if the task has already been completed for today (or week)
            query2 = "SELECT COUNT(*) FROM Tasks WHERE HabitID = ? AND TaskLogDate = ? AND TaskStatus = ?"
            queryValues2 = (habitID, logDate, "Completed")
            dbcursor.execute(query2, queryValues2)
            taskLogCount = dbcursor.fetchone()[0]

            if taskLogCount == 0:
                # Log the completed task
                query3 = "INSERT INTO Tasks (HabitID, Task, Periodicity, TaskLogDate, Streak, TaskStatus) VALUES (?, ?, ?, ?, ?, ?)"
                queryValues3 = (habitID, task, periodicity, logDate, currentStreak, "Completed")
                dbcursor.execute(query3, queryValues3)

                # Update the habit's last completed date and streak
                query4 = "UPDATE Habits SET LastCompleted = ?, Streak = ? WHERE ID = ?"
                queryValues4 = (logDate, currentStreak, habitID)
                dbcursor.execute(query4, queryValues4)
                dbconnection.commit()

                print(f"Task '{task}' for habit ID {habitID} completed! Streak updated to {currentStreak}.")
            else:
                print(f"You've already completed and logged this task for the {periodicity.lower()}.")
        else:
            print("Habit ID Error")

    #LIST ALL COMPLETED TASKS ON THIS DAY
    def GetCompletedTasks():
        x = datetime.datetime.now()
        logDate = x.strftime("%x")
        query = "SELECT * FROM Tasks WHERE TaskLogDate = ?"
        param = (logDate, )
        dbcursor.execute(query, param)
        tasks = dbcursor.fetchall()
        #Display Habits to User
        print("TASKS COMPLETED TODAY")
        print("----------------------")
        print("----------------------")
        for x in tasks: 
            print(f"TASKID {x[0]}: {x}")
            print("----------------------")
            print("----------------------")

    def listAllTasks():
        query = "SELECT * FROM Tasks"
        dbcursor.execute(query)
        tasks = dbcursor.fetchall()

        # Display tasks with TASKID label
        print("ALL TASKS")
        print("----------------------")
        for task in tasks:
            print(f"TASKID {task[0]}: {task}")
            print("----------------------")


#APP NAVIGATION KEYS
print("ENTER 1 TO CREATE A NEW HABIT")
print("ENTER 2 TO REMOVE A HABIT")
print("ENTER 3 TO LIST ALL HABITS")
print("ENTER 4 TO LIST HABITS BY PERIODICITY")
print("ENTER 5 TO LOG/CHECK OFF A COMPLETED HABIT TASK")
print("ENTER 6 TO VIEW TASKS COMPLETED TODAY")
print("ENTER 7 TO VIEW ALL TASKS")
try:
    Menu = int(input("PLEASE ENTER A DIGIT BETWEEN 1 - 7: "))
except ValueError:
    print("Invalid input! Please enter a digit between 1 and 7.")
    exit()


if Menu == 1:
    #CREATE/ADD A NEW HABIT
    newHabit = MyHabits(input("Enter A Habit: "), int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")), datetime.datetime.now(), 1)
    newHabit.addHabit()
  
    
elif Menu == 2:
    #REMOVE A HABIT
    MyHabits.removeHabit()
    

elif Menu == 3:
    #LIST ALL USER HABITS
    MyHabits.listAllHabits()


elif Menu == 4:
    #LIST HABITS BY PERIODICITY
    MyHabits.listHabitsByPeriodicity(int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")))

elif Menu == 5:
    #LOG/CHECK OFF COMPLETED HABIT TASK
    MyHabits.CheckOffTask()

elif Menu == 6:
    #LIST TASKS COMPLETED TODAY
    MyHabits.GetCompletedTasks()

elif Menu == 7:
    # LIST ALL TASKS
    MyHabits.listAllTasks()

else:
    print("INVALID MENU NAVIGATION COMMAND!")

dbconnection.close()