import json
import datetime
import tkinter as tk
from tkinter import messagebox


def load_tasks_from_file(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []


tasks = []
load_tasks_from_file()

def create_task_window():
    create_window = tk.Toplevel()
    create_window.title("New Task")

    tk.Label(create_window, text="Title: ").pack(pady=5)
    name_entry = tk.Entry(create_window)
    name_entry.pack(pady=5)

    tk.Label(create_window, text="Additional Information: ").pack(pady=5)
    name_entry = tk.Entry(create_window)
    name_entry.pack(pady=5)

    tk.Label(create_window, text="Category: ").pack(pady=5)
    name_entry = tk.Entry(create_window)
    name_entry.pack(pady=5)

    tk.Label(create_window, text="Due date (DD/MM): ").pack(pady=5)
    name_entry = tk.Entry(create_window)
    name_entry.pack(pady=5)

    def create_task():
        while True:
            name = input("Enter name: ").strip()
            if name and name_is_valid(name, tasks):
                break
            else:
                print("Name must be unique and not empty, please try again")

        information = input("Enter additional information about the task (optional): ")

        category = input("Which category is your task in: ")

        while True:
            due_date = input(
                "Enter date of the format dd/mm (optional, if no due date is entered the task will be placed in the backlog): ").strip()
            valid_date = date_is_valid(due_date)
            if valid_date or due_date == "":
                due_date = valid_date
                break
            else:
                print("Date must formatted as DD/MM")

        new_task = {"Name": name,
                    "Information": information,
                    "Category": category,
                    "Due date": str(due_date) if due_date else None,
                    "Status": "Not started"
                    }
        tasks.append(new_task)
        save_tasks_to_file()
        print(f"{name} added to your to-do list successfully!")

    create_task()


def create_main_window(title="Basic TO-DO App", size="400x300"):
    root = tk.Tk()
    root.title = title
    root.geometry(size)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    create_task_button = tk.Button(button_frame, text="New Task", command=create_task_window())
    create_task_button.pack(side=tk.LEFT, padx=5)

    not_started_frame = tk.Frame(root, width=200, height=100)
    not_started_frame.pack(side=tk.LEFT, padx=10, pady=10)

    in_progress_frame = tk.Frame(root, width=200, height=100)
    in_progress_frame.pack(side=tk.LEFT, padx=10, pady=10)

    finished_frame = tk.Frame(root, width=200, height=100)
    finished_frame.pack(side=tk.LEFT, padx=10, pady=10)

    label_not_started=tk.Label(not_started_frame, text="Not started")
    label_not_started.pack()

    label_not_started = tk.Label(in_progress_frame, text="In progress")
    label_not_started.pack()

    label_finished = tk.Label(finished_frame, text="Finished")
    label_finished.pack()

    def display_task():
        for task in not_started_frame.winfo_children()[1:]:
            task.destroy()
        for task in in_progress_frame.winfo_children()[1:]:
            task.destroy()
        for task in finished_frame .winfo_children()[1:]:
            task.destroy()

        for task in tasks:
            frame_task = tk.Frame(borderwidth=2, relief="solid", padx=10, pady=5)
            name_label = tk.Label(frame_task, text=f"{task['Name']}", font=("Arial", 10, "bold"))
            name_label.pack(anchor="w")
            information_label = tk.Label(frame_task, text=f"{task['Information']}")
            information_label.pack(anchor="w")
            due_date_label = tk.Label(frame_task, text=f"{task['Due date']}")
            due_date_label.pack(anchor="w")

            if task["Status"] == "Not started":
                frame_task.pack(in_=not_started_frame, fill="x", pady=5)
            elif task["Status"] == "In progress":
                frame_task.pack(in_=in_progress_frame, fill="x", pady=5)
            elif task["Status"] == "Finished":
                frame_task.pack(in_=finished_frame, fill="x", pady=5)

    display_task()
    root.mainloop()


create_main_window()


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


