import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def display_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n" + "=" * 60)
    print("                    YOUR TO-DO LIST")
    print("=" * 60)

    for task in tasks:
        status = "✓ Completed" if task["completed"] else "○ Pending"
        print(f'{task["id"]}. {task["title"]} [{status}]')

    print("=" * 60)


def get_next_id(tasks):
    """Return the next available task ID."""
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(tasks):
    title = input("\nEnter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")


def update_task(tasks):
    if not tasks:
        print("\nNo tasks available to update.")
        return

    display_tasks(tasks)

    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        print("Task not found.")
        return

    new_title = input("Enter new task title: ").strip()

    if not new_title:
        print("Task title cannot be empty.")
        return

    task["title"] = new_title
    save_tasks(tasks)
    print("Task updated successfully!")


def delete_task(tasks):
    if not tasks:
        print("\nNo tasks available to delete.")
        return

    display_tasks(tasks)

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        print("Task not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted successfully!")


def complete_task(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return

    display_tasks(tasks)

    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        print("Task not found.")
        return

    task["completed"] = True
    save_tasks(tasks)
    print("Task marked as completed!")


def main():
    tasks = load_tasks()

    while True:
        print("\n" + "=" * 60)
        print("              PYTHON TO-DO LIST APPLICATION")
        print("=" * 60)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Completed")
        print("6. Exit")
        print("=" * 60)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            complete_task(tasks)
        elif choice == "6":
            print("\nThank you for using the To-Do List Application!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
