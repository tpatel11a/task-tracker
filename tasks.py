import sys
import json
import os
import urllib.request
import urllib.error
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

TASKS_FILE = "tasks.json"
console = Console()

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        data = json.load(f)
    
    normalized = []
    for item in data:
        if isinstance(item, str):
            normalized.append({"text": item, "completed": False})
        else:
            normalized.append(item)
    return normalized

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("\n[yellow]📋 No tasks yet![/yellow] Add one using: [bold green]python tasks.py add \"Build feature\"[/bold green]\n")
        return
    
    table = Table(title="📋 Your Task List", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Status", width=10)
    table.add_column("Task Description", style="cyan")

    for idx, task in enumerate(tasks, 1):
        status = "[bold green]DONE[/bold green]" if task.get("completed") else "[yellow]PENDING[/yellow]"
        text = f"[strike]{task['text']}[/strike]" if task.get("completed") else task['text']
        table.add_row(str(idx), status, text)

    console.print()
    console.print(table)
    console.print()

def add_task(task_text):
    tasks = load_tasks()
    tasks.append({"text": task_text, "completed": False})
    save_tasks(tasks)
    console.print(f"\n[bold green]✅ Added task:[/bold green] \"{task_text}\"\n")

def mark_done(task_idx):
    tasks = load_tasks()
    if 1 <= task_idx <= len(tasks):
        tasks[task_idx - 1]["completed"] = True
        save_tasks(tasks)
        console.print(f"\n[bold green]🎉 Task #{task_idx} marked as completed![/bold green]\n")
    else:
        console.print(f"\n[bold red]❌ Invalid task ID:[/bold red] #{task_idx}\n")

def delete_task(task_idx):
    tasks = load_tasks()
    if 1 <= task_idx <= len(tasks):
        removed = tasks.pop(task_idx - 1)
        save_tasks(tasks)
        console.print(f"\n[bold red]🗑️ Deleted task #{task_idx}:[/bold red] \"{removed['text']}\"\n")
    else:
        console.print(f"\n[bold red]❌ Invalid task ID:[/bold red] #{task_idx}\n")

def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "YOUR_ACTUAL_API_KEY_HERE" in api_key:
        console.print("\n[bold red]❌ Error:[/bold red] Valid GEMINI_API_KEY not found in .env file!\n")
        return None

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode("utf-8"))
            candidates = result.get("candidates", [])
            if candidates and isinstance(candidates, list):
                first_candidate = candidates[0]
                content = first_candidate.get("content", {})
                parts = content.get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"]
            return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        console.print(f"\n[bold red]❌ API HTTP Error ({e.code}):[/bold red] {e.reason}")
        console.print(f"[dim]{error_body}[/dim]\n")
        return None
    except Exception as e:
        console.print(f"\n[bold red]❌ Request Failed or Timed Out:[/bold red] {e}\n")
        return None

def get_ai_advice():
    tasks = load_tasks()
    if not tasks:
        console.print("\n[yellow]⚠️ Add some tasks first before asking AI![/yellow]\n")
        return

    console.print("\n[bold blue]🤖 Asking Gemini AI to prioritize your tasks...[/bold blue]\n")
    prompt = f"Here is my current to-do list: {tasks}. Give me a 2-sentence plan on which task to prioritize first and why, plus a brief motivational tip."
    advice = call_gemini(prompt)
    if advice:
        console.print(f"[bold green]AI Assistant Advice:[/bold green]\n{advice}\n")

def breakdown_task(task_idx):
    tasks = load_tasks()
    if not (1 <= task_idx <= len(tasks)):
        console.print(f"\n[bold red]❌ Invalid task ID:[/bold red] #{task_idx}\n")
        return

    target_task = tasks[task_idx - 1]["text"]
    console.print(f"\n[bold blue]🤖 Breaking down Task #{task_idx} (\"{target_task}\") into steps...[/bold blue]\n")
    
    prompt = f"Break down this task into 3-4 short, actionable sub-steps with checkboxes (e.g., - [ ] step): '{target_task}'"
    subtasks = call_gemini(prompt)
    if subtasks:
        console.print(f"[bold cyan]Sub-step Plan for Task #{task_idx}:[/bold cyan]\n{subtasks}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "done" and len(sys.argv) > 2 and sys.argv[2].isdigit():
        mark_done(int(sys.argv[2]))
    elif sys.argv[1] == "delete" and len(sys.argv) > 2 and sys.argv[2].isdigit():
        delete_task(int(sys.argv[2]))
    elif sys.argv[1] == "ai":
        get_ai_advice()
    elif sys.argv[1] == "breakdown" and len(sys.argv) > 2 and sys.argv[2].isdigit():
        breakdown_task(int(sys.argv[2]))
    else:
        console.print("\n[bold red]Usage:[/bold red]")
        console.print("  python tasks.py                 (Lists all tasks)")
        console.print("  python tasks.py add \"<task>\"    (Adds a new task)")
        console.print("  python tasks.py done <id>       (Marks a task complete)")
        console.print("  python tasks.py delete <id>     (Deletes a task)")
        console.print("  python tasks.py ai              (Gets AI task advice)")
        console.print("  python tasks.py breakdown <id>  (Breaks down a task into sub-steps)\n")
