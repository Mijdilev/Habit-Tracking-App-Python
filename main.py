# main.py
import json
from datetime import datetime
from habit_tracker import HabitTracker
from habit import Habit


def load_data(filename="habits.json"):
    """
    Loads habit data from a JSON file.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return HabitTracker.from_json(data)
    except FileNotFoundError:
        print("No existing data found, creating a new Habit Tracker.")
        return HabitTracker()  # Return an empty HabitTracker, not None
    except json.JSONDecodeError:
        print("Error decoding JSON. Creating a new Habit Tracker.")
        return HabitTracker()


def save_data(habit_tracker, filename="habits.json"):
    """
    Saves habit data to a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(habit_tracker.to_json(), f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def main():
    """
    Main function to run the Habit Tracker App with a CLI.
    """
    habit_tracker = load_data()  # Load data from JSON file

    while True:
        print("\nHabit Tracker Menu:")
        print("1. Add Habit")
        print("2. Mark Habit as Completed")
        print("3. List All Habits")
        print("4. List Habits by Periodicity")
        print("5. Get Longest Streak for All Habits")
        print("6. Get Longest Streak for a Habit")
        print("7. Edit/Delete Habit")
        print("8. Quit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter habit name: ")
                periodicity = input("Enter habit periodicity (e.g., daily, weekly, monthly): ")
                date_str = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(date_str, "%Y-%m-%d")
                habit = Habit(name, periodicity, start_date)
                habit_tracker.add_habit(habit)
                print("Habit added successfully.")
            elif choice == "2":
                name = input("Enter habit name: ")
                date_str = input("Enter completion date (YYYY-MM-DD): ")
                completion_date = datetime.strptime(date_str, "%Y-%m-%d")

                habit_to_mark = None  # find habit
                for habit in habit_tracker.habits:
                    if habit.name == name:
                        habit_to_mark = habit
                        break

                if habit_to_mark:
                    try:
                        habit_to_mark.mark_completed(completion_date)
                        print("Habit marked as completed.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print(f"Habit with name '{name}' not found.")

            elif choice == "3":
                all_habits = habit_tracker.get_all_habits()
                if all_habits:
                    print("\nAll Habits:")
                    for habit in all_habits:
                        print(habit)  # Use the __repr__ method of Habit
                else:
                    print("No habits tracked yet.")
            elif choice == "4":
                periodicity = input("Enter periodicity to filter by: ")
                habits_by_periodicity = habit_tracker.get_habits_by_periodicity(periodicity)
                if habits_by_periodicity:
                    print(f"\nHabits with periodicity '{periodicity}':")
                    for habit in habits_by_periodicity:
                        print(habit)
                else:
                    print(f"No habits found with periodicity '{periodicity}'.")
            elif choice == "5":
                longest_streak = habit_tracker.get_longest_streak_all_habits()
                print(f"Longest streak for all habits: {longest_streak} days")
            elif choice == "6":
                name = input("Enter habit name: ")
                longest_streak = habit_tracker.get_longest_streak_for_habit(name)
                if longest_streak > 0:
                    habit = None
                    for h in habit_tracker.habits:
                        if h.name == name:
                            habit = h
                            break
                    if habit:
                        print(f"Longest streak for habit '{name}': {habit.get_streak_duration_string(longest_streak)}")
                    else:
                        print(f"Longest streak for habit '{name}': {longest_streak} days")  # added default
                else:
                    print(f"Habit with name '{name}' not found.")
            elif choice == "7":
                name = input("Enter the name of the habit to edit/delete: ")
                print("1. Edit Habit")
                print("2. Delete Habit")
                edit_choice = input("Enter your choice: ")
                if edit_choice == "1":
                    new_name = input("Enter the new name: ")
                    new_periodicity = input("Enter the new periodicity")
                    date_str = input("Enter the new start date (YYYY-MM-DD): ")
                    new_start_date = None
                    if date_str:
                        new_start_date = datetime.strptime(date_str, "%Y-%m-%d")
                    try:
                        habit_tracker.edit_habit(name, new_name, new_periodicity, new_start_date)
                        print("Habit edited successfully.")
                    except ValueError as e:
                        print(f"Error: {e}")
                elif edit_choice == "2":
                    try:
                        habit_tracker.delete_habit(name)
                        print("Habit deleted successfully.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid choice. Please try again.")
            elif choice == "8":
                save_data(habit_tracker)  # Save data to JSON file before quitting
                print("Exiting Habit Tracker. Your data has been saved.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid value.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
