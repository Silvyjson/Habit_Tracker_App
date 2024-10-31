#A HABIT TRACKING APPLICATION PROGRAM WRITTEN IN PYTHON
########################################################
from my_habits import MyHabits
from db_manager import create_connection, create_tables
import datetime

dbconnection = create_connection()
dbcursor = dbconnection.cursor()

# Create tables if not already created
create_tables(dbcursor)

#APP NAVIGATION KEYS
print("ENTER 1 TO CREATE A NEW HABIT")
print("ENTER 2 TO REMOVE A HABIT")
print("ENTER 3 TO LIST ALL HABITS")
print("ENTER 4 TO LIST HABITS BY PERIODICITY")
print("ENTER 5 TO LOG/CHECK OFF A COMPLETED HABIT TASK")
print("ENTER 6 TO VIEW TASKS COMPLETED TODAY")
print("ENTER 7 TO ANALYZE YOUR HABITS")
print("ENTER 8 TO CHECK MISSED HABITS")
print("ENTER 9 TO VIEW THE LONGEST STREAK FOR A SPECIFIC HABIT")
print("ENTER 10 TO VIEW ALL TASKS")
try:
    Menu = int(input("PLEASE ENTER A DIGIT BETWEEN 1 - 10: "))
except ValueError:
    print("Invalid input! Please enter a digit between 1 and 10.")
    exit()


if Menu == 1:
    #CREATE/ADD A NEW HABIT
    newHabit = MyHabits(input("Enter A Habit: "), int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")), datetime.datetime.now(), 1)
    newHabit.add_habit()
  
    
elif Menu == 2:
    #REMOVE A HABIT
    MyHabits.remove_habit()
    

elif Menu == 3:
    #LIST ALL USER HABITS
    MyHabits.list_all_habits()


elif Menu == 4:
    #LIST HABITS BY PERIODICITY
    MyHabits.list_habits_by_periodicity(int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: ")))

elif Menu == 5:
    #LOG/CHECK OFF COMPLETED HABIT TASK
    MyHabits.check_off_task()

elif Menu == 6:
    #LIST TASKS COMPLETED TODAY
    MyHabits.get_completed_tasks()

elif Menu == 7:
    # ANALYZE USER HABITS
    MyHabits.analyze_habits()

elif Menu == 8:
    # CHECK MISSED HABITS
    MyHabits.check_missed_habits()

elif Menu == 9:
    # VIEW THE LONGEST STREAK FOR A SPECIFIC HABIT
    habit_name = input("Enter the habit name: ")
    MyHabits.get_longest_streak_for_habit(habit_name)

elif Menu == 10:
    # LIST ALL TASKS
    MyHabits.list_all_tasks()

else:
    print("INVALID MENU NAVIGATION COMMAND!")

dbconnection.close()