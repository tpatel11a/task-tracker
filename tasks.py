import sys
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\n📋 No tasks yet! Add one using: python tasks.py add \"Buy groceries\"\n")
        return
    print("\n📋 Your Tasks:")
    for idx, task in enumerate(tasks, 1):
        print(f"  {idx}. {task}")
    print()

def add_task(task_text):
    tasks = load_tasks()
    tasks.append(task_text)
    save_tasks(tasks)
    print(f"\n✅ Added task: \"{task_text}\"\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    else:
        print("\nUsage:")
        print("  python tasks.py               (Lists all tasks)")
        print("  python tasks.py add \"<task>\"  (Adds a new task)\n")
