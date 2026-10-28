import sys
import json
import os
from rich.console import Console
from rich.table import Table

TASKS_FILE = "tasks.json"
console = Console()

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
        console.print("\n[yellow]📋 No tasks yet![/yellow] Add one using: [bold green]python tasks.py add \"Buy groceries\"[/bold green]\n")
        return
    
    table = Table(title="📋 Your Task List", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task Description", style="cyan")

    for idx, task in enumerate(tasks, 1):
        table.add_row(str(idx), task)

    console.print()
    console.print(table)
    console.print()

def add_task(task_text):
    tasks = load_tasks()
    tasks.append(task_text)
    save_tasks(tasks)
    console.print(f"\n[bold green]✅ Added task:[/bold green] \"{task_text}\"\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    else:
        console.print("\n[bold red]Usage:[/bold red]")
        console.print("  python tasks.py               (Lists all tasks)")
        console.print("  python tasks.py add \"<task>\"  (Adds a new task)\n")
