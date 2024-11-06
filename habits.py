# A HABIT TRACKING APPLICATION PROGRAM WRITTEN IN PYTHON
from my_habits import MyHabits
from analytics_module import display_analytics_summary, get_longest_streak_for_habit
from db_manager import create_connection, create_tables

def main():
    # Initialize the database connection
    dbconnection = create_connection()
    dbcursor = dbconnection.cursor()

    # Create tables if not already created
    create_tables(dbcursor)

    # APP NAVIGATION KEYS
    print("ENTER 1 TO CREATE A NEW HABIT")
    print("ENTER 2 TO REMOVE A HABIT")
    print("ENTER 3 TO LIST ALL HABITS")
    print("ENTER 4 TO LIST HABITS BY PERIODICITY")
    print("ENTER 5 TO LOG/CHECK OFF A COMPLETED HABIT TASK")
    print("ENTER 6 TO VIEW TASKS COMPLETED")
    print("ENTER 7 TO VIEW ALL TASKS")
    print("ENTER 8 TO ANALYZE YOUR HABITS")
    print("ENTER 9 TO VIEW THE LONGEST STREAK FOR A SPECIFIC HABIT")
    print("0. Exit")

    # Get menu input from the user
    try:
        menu = int(input("PLEASE ENTER A DIGIT BETWEEN 0 - 9: "))
    except ValueError:
        print("Invalid input! Please enter a digit between 0 and 9.")
        return

    my_habits = MyHabits(dbcursor)

    if menu == 1:
        # CREATE/ADD A NEW HABIT
        try:
            habit_name = input("Enter A Habit: ")
            habit_period = int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: "))
            if habit_period not in [1, 2]:
                raise ValueError("Invalid period! Please enter 1 or 2.")
            my_habits.add_habit(habit_name, habit_period)
        except ValueError as e:
            print(e)

    elif menu == 2:
        # REMOVE A HABIT
        habit_id = int(input("Enter the ID of the habit to remove: "))
        my_habits.remove_habit(habit_id)
 

    elif menu == 3:
        # LIST ALL USER HABITS
        my_habits.list_all_habits()

    elif menu == 4:
        # LIST HABITS BY PERIODICITY
        try:
            habit_period = int(input("HABIT PERIOD: Enter 1 for Daily; 2 for Weekly: "))
            if habit_period not in [1, 2]:
                raise ValueError("Invalid period! Please enter 1 or 2.")
            my_habits.list_habits_by_periodicity(habit_period)
        except ValueError as e:
            print(e)

    elif menu == 5:
        # LOG/CHECK OFF COMPLETED HABIT TASK
        habit_id = int(input("Enter the ID of the habit to check off: "))
        my_habits.check_off_task(habit_id)

    elif menu == 6:
        # LIST TASKS COMPLETED TODAY
        my_habits.get_completed_tasks()

    elif menu == 7:
        # LIST ALL TASKS
        my_habits.list_all_tasks()

    elif menu == 8:
        # ANALYZE USER HABITS
        display_analytics_summary()

    elif menu == 9:
        # VIEW THE LONGEST STREAK FOR A SPECIFIC HABIT
        habit_name = input("Enter the habit name: ")
        get_longest_streak_for_habit(habit_name)

    elif menu == 0:
                print("Exiting the application. Goodbye!")
    else:
        print("INVALID MENU NAVIGATION COMMAND!")

    # Close the database connection
    dbconnection.close()

if __name__ == "__main__":
    main()
