import json
import datetime
import tkinter as tk
from tkinter import messagebox


def create_main_window(title="Basic TO-DO App", size="400x300"):
    root = tk.Tk()
    root.title = title
    root.geometry(size)
    root.mainloop()


create_main_window()


def load_tasks_from_file(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []


tasks = []
load_tasks_from_file()


def save_tasks_to_file(filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)


# Checks if a name is valid, returns true or false
def name_is_valid(name, tasks):
    for task in tasks:
        if name.lower().strip() == task["Name"].lower().strip():
            return False
    return True


# Checks if date is valid, returns date in a datetime format
def date_is_valid(date):
    if not date:
        return True
    try:
        current_year = datetime.datetime.now().year
        full_date_str = f"{date}/{current_year}"
        valid_date = datetime.datetime.strptime(full_date_str, "%d/%m/%Y")
        return valid_date.date()
    except ValueError:
        print("Invalid date format. Please enter the date in DD/MM format")


# Currently not used
# Checks if backlog is valid, returns true or false
def backlog_is_valid(backlog):
    valid_inputs = ["y", "n", "yes", "no"]
    return backlog.lower().strip() in valid_inputs


def create_task():

    backlog = False
    while True:
        name = input("Enter name: ").strip()
        if name and name_is_valid(name, tasks):
            break
        else:
            print("Name must be unique and not empty, please try again")

    information = input("Enter additional information about the task (optional): ")

    category = input("Which category is your task in: ")

    while True:
        due_date = input("Enter date of the format dd/mm (optional, if no due date is entered the task will be placed in the backlog): ").strip()
        valid_date = date_is_valid(due_date)
        if valid_date:
            due_date = valid_date
            break
        elif due_date == "":
            backlog = True
            break
        else:
            print("Date must formatted as DD/MM")
    """ (Redundant)
    while True:
        backlog = input("Do you want to place this task in the backlog?: ").strip()
        valid_backlog = backlog_is_valid()
        if backlog and valid_backlog:
            backlog = valid_backlog
            break
        else:
            print("Backlog must either yes or no, please try again.")
    """

    new_task = {"Name": name,
                "Information": information,
                "Category": category,
                "Due date": str(due_date) if due_date else None,
                "Backlog": backlog,
                "Status": "Not started"
                }
    tasks.append(new_task)
    save_tasks_to_file()
    print(f"{name} added to your to-do list successfully!")

def remove_task():
    remove = input("Which task would you like to remove?").strip()
    found = False
    for task in tasks[:]:
        if task["Name"].lower() == remove.lower():
            tasks.remove(task)
            found = True
            print(f"Task {task['Name']} removed")
    if found:
        save_tasks_to_file()
    else:
        print(f"Could not find task with the name: {remove}")


create_task()
save_tasks_to_file()


