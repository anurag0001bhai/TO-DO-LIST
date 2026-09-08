import json
import os

# ============================================================
#                 PYTHON TO-DO LIST APPLICATION
# ============================================================

DATA_FILE = "tasks.json"

# ANSI Colors
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"


# ============================================================
#                     UTILITY FUNCTIONS
# ============================================================

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Pause until the user presses Enter."""
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")


def print_header(title):
    """Print a beautiful section header."""
    print(f"\n{CYAN}{'═' * 65}{RESET}")
    print(f"{BOLD}{WHITE}{title.center(65)}{RESET}")
    print(f"{CYAN}{'═' * 65}{RESET}")


# ============================================================
#                     FILE HANDLING
# ============================================================

def load_tasks():
    """Load tasks from the JSON file."""

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

            # Make sure the loaded data is a list
            if isinstance(tasks, list):
                return tasks

            return []

    except (json.JSONDecodeError, OSError):
        print(f"{RED}⚠ Unable to read tasks file.{RESET}")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        print(f"{RED}⚠ Unable to save tasks.{RESET}")


# ============================================================
#                     TASK FUNCTIONS
# ============================================================

def get_next_id(tasks):
    """Return the next available task ID."""
    return max(
        (task["id"] for task in tasks),
        default=0
    ) + 1


def display_tasks(tasks):
    """Display all tasks in a clean table."""

    clear_screen()
    print_header("📋 YOUR TO-DO LIST")

    if not tasks:
        print(f"\n{YELLOW}   ○ No tasks found.{RESET}")
        print(f"{WHITE}   Add a task to get started!{RESET}")
        return

    completed = sum(
        1 for task in tasks if task["completed"]
    )

    pending = len(tasks) - completed

    print(
        f"\n{GREEN}✓ Completed: {completed}{RESET}"
        f"     {YELLOW}○ Pending: {pending}{RESET}"
        f"     {BLUE}Total: {len(tasks)}{RESET}\n"
    )

    print(
        f"{CYAN}"
        f"{'ID':<6}"
        f"{'STATUS':<15}"
        f"{'TASK':<40}"
        f"{RESET}"
    )

    print(f"{CYAN}{'─' * 65}{RESET}")

    for task in tasks:

        if task["completed"]:
            status = f"{GREEN}✓ Completed{RESET}"
            title = f"{GREEN}{task['title']}{RESET}"
        else:
            status = f"{YELLOW}○ Pending{RESET}"
            title = f"{WHITE}{task['title']}{RESET}"

        print(
            f"{BOLD}{task['id']:<6}{RESET}"
            f"{status:<24}"
            f"{title}"
        )

    print(f"\n{CYAN}{'═' * 65}{RESET}")


def find_task(tasks, task_id):
    """Find a task using its ID."""

    return next(
        (task for task in tasks if task["id"] == task_id),
        None
    )


# ============================================================
#                       ADD TASK
# ============================================================

def add_task(tasks):

    clear_screen()
    print_header("➕ ADD NEW TASK")

    title = input(
        f"\n{CYAN}Enter task title: {RESET}"
    ).strip()

    if not title:
        print(f"\n{RED}✗ Task title cannot be empty.{RESET}")
        pause()
        return

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    print(
        f"\n{GREEN}✓ Task added successfully!{RESET}"
    )

    print(
        f"{WHITE}Task ID: {task['id']}{RESET}"
    )

    pause()


# ============================================================
#                     UPDATE TASK
# ============================================================

def update_task(tasks):

    if not tasks:
        clear_screen()
        print_header("✏ UPDATE TASK")
        print(f"\n{YELLOW}No tasks available to update.{RESET}")
        pause()
        return

    display_tasks(tasks)

    try:
        task_id = int(
            input(
                f"\n{CYAN}Enter task ID to update: {RESET}"
            )
        )

    except ValueError:
        print(f"\n{RED}✗ Please enter a valid number.{RESET}")
        pause()
        return

    task = find_task(tasks, task_id)

    if not task:
        print(f"\n{RED}✗ Task not found.{RESET}")
        pause()
        return

    print(
        f"\n{WHITE}Current task: "
        f"{task['title']}{RESET}"
    )

    new_title = input(
        f"{CYAN}Enter new task title: {RESET}"
    ).strip()

    if not new_title:
        print(
            f"\n{RED}✗ Task title cannot be empty.{RESET}"
        )
        pause()
        return

    task["title"] = new_title
    save_tasks(tasks)

    print(
        f"\n{GREEN}✓ Task updated successfully!{RESET}"
    )

    pause()


# ============================================================
#                     DELETE TASK
# ============================================================

def delete_task(tasks):

    if not tasks:
        clear_screen()
        print_header("🗑 DELETE TASK")
        print(f"\n{YELLOW}No tasks available to delete.{RESET}")
        pause()
        return

    display_tasks(tasks)

    try:
        task_id = int(
            input(
                f"\n{CYAN}Enter task ID to delete: {RESET}"
            )
        )

    except ValueError:
        print(f"\n{RED}✗ Please enter a valid number.{RESET}")
        pause()
        return

    task = find_task(tasks, task_id)

    if not task:
        print(f"\n{RED}✗ Task not found.{RESET}")
        pause()
        return

    print(
        f"\n{YELLOW}Task selected: "
        f"{task['title']}{RESET}"
    )

    confirmation = input(
        f"{RED}Are you sure you want to delete it? (y/n): {RESET}"
    ).strip().lower()

    if confirmation != "y":
        print(f"\n{YELLOW}Deletion cancelled.{RESET}")
        pause()
        return

    tasks.remove(task)
    save_tasks(tasks)

    print(
        f"\n{GREEN}✓ Task deleted successfully!{RESET}"
    )

    pause()


# ============================================================
#                  COMPLETE / UNCOMPLETE TASK
# ============================================================

def complete_task(tasks):

    if not tasks:
        clear_screen()
        print_header("✓ COMPLETE TASK")
        print(f"\n{YELLOW}No tasks available.{RESET}")
        pause()
        return

    display_tasks(tasks)

    try:
        task_id = int(
            input(
                f"\n{CYAN}Enter task ID: {RESET}"
            )
        )

    except ValueError:
        print(f"\n{RED}✗ Please enter a valid number.{RESET}")
        pause()
        return

    task = find_task(tasks, task_id)

    if not task:
        print(f"\n{RED}✗ Task not found.{RESET}")
        pause()
        return

    # Toggle completion status
    task["completed"] = not task["completed"]

    save_tasks(tasks)

    if task["completed"]:
        print(
            f"\n{GREEN}✓ Task marked as completed! 🎉{RESET}"
        )
    else:
        print(
            f"\n{YELLOW}○ Task marked as pending.{RESET}"
        )

    pause()


# ============================================================
#                        SEARCH TASK
# ============================================================

def search_task(tasks):

    clear_screen()
    print_header("🔍 SEARCH TASK")

    if not tasks:
        print(f"\n{YELLOW}No tasks available.{RESET}")
        pause()
        return

    keyword = input(
        f"\n{CYAN}Enter keyword to search: {RESET}"
    ).strip().lower()

    if not keyword:
        print(f"\n{RED}✗ Search keyword cannot be empty.{RESET}")
        pause()
        return

    results = [
        task
        for task in tasks
        if keyword in task["title"].lower()
    ]

    if not results:
        print(
            f"\n{YELLOW}○ No matching tasks found.{RESET}"
        )
        pause()
        return

    print(
        f"\n{GREEN}✓ {len(results)} task(s) found:{RESET}\n"
    )

    for task in results:

        if task["completed"]:
            status = f"{GREEN}✓ Completed{RESET}"
        else:
            status = f"{YELLOW}○ Pending{RESET}"

        print(
            f"{BOLD}{task['id']}.{RESET} "
            f"{task['title']} "
            f"[{status}]"
        )

    pause()


# ============================================================
#                    MAIN APPLICATION
# ============================================================

def main():

    tasks = load_tasks()

    while True:

        clear_screen()

        # Calculate statistics
        total = len(tasks)
        completed = sum(
            1 for task in tasks if task["completed"]
        )
        pending = total - completed

        print(
            f"{CYAN}"
            f"╔═══════════════════════════════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{CYAN}║{RESET}"
            f"{BOLD}{WHITE}"
            f"              📝 PYTHON TO-DO LIST"
            f"{RESET}"
            f"{CYAN}                         ║{RESET}"
        )

        print(
            f"{CYAN}╠═══════════════════════════════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{CYAN}║{RESET}"
            f"  {GREEN}✓ Completed: {completed:<5}{RESET}"
            f"  {YELLOW}○ Pending: {pending:<5}{RESET}"
            f"  {BLUE}Total: {total:<5}{RESET}"
            f"                  {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}╠═══════════════════════════════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}1.{RESET}  ➕ Add Task"
            f"                         {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}2.{RESET}  📋 View Tasks"
            f"                      {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}3.{RESET}  ✏  Update Task"
            f"                     {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}4.{RESET}  🗑  Delete Task"
            f"                     {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}5.{RESET}  ✓  Complete / Undo"
            f"                  {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}6.{RESET}  🔍 Search Tasks"
            f"                    {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}║{RESET}   {BOLD}7.{RESET}  🚪 Exit"
            f"                              {CYAN}║{RESET}"
        )

        print(
            f"{CYAN}╚═══════════════════════════════════════════════════════════════╝"
            f"{RESET}"
        )

        choice = input(
            f"\n{BOLD}{CYAN}➜ Enter your choice (1-7): {RESET}"
        ).strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            display_tasks(tasks)
            pause()

        elif choice == "3":
            update_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            complete_task(tasks)

        elif choice == "6":
            search_task(tasks)

        elif choice == "7":

            clear_screen()

            print(
                f"\n{CYAN}"
                f"╔═══════════════════════════════════════════════════════════════╗"
                f"{RESET}"
            )

            print(
                f"{CYAN}║{RESET}"
                f"{GREEN}{BOLD}"
                f"        👋 Thank you for using To-Do List!"
                f"{RESET}"
                f"{CYAN}             ║{RESET}"
            )

            print(
                f"{CYAN}║{RESET}"
                f"              Keep being productive! 🚀"
                f"                    {CYAN}║{RESET}"
            )

            print(
                f"{CYAN}"
                f"╚═══════════════════════════════════════════════════════════════╝"
                f"{RESET}"
            )

            break

        else:
            print(
                f"\n{RED}✗ Invalid choice. "
                f"Please select 1-7.{RESET}"
            )
            pause()


# ============================================================
#                       PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()