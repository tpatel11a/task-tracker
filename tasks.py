import sys
import json
import os
import urllib.request
import urllib.error
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Load secret key & configuration from .env file
load_dotenv()

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

def get_ai_advice():
    tasks = load_tasks()
    if not tasks:
        console.print("\n[yellow]⚠️ Add some tasks first before asking AI![/yellow]\n")
        return

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "YOUR_ACTUAL_API_KEY_HERE" in api_key:
        console.print("\n[bold red]❌ Error:[/bold red] Valid GEMINI_API_KEY not found in .env file!\n")
        return

    # Model is now configurable via .env (defaults to gemini-3.5-flash)
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    console.print(f"\n[bold blue]🤖 Asking Gemini AI ({model_name}) to analyze your tasks...[/bold blue]\n")

    prompt = f"Here is my current to-do list: {tasks}. Give me a 2-sentence plan on which task to prioritize first and why, plus a brief motivational tip."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    
    # Passing the key in the x-goog-api-key header prevents key exposure in URLs and logs
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # Safe candidate and content block parsing
            candidates = result.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and "text" in parts[0]:
                    advice = parts[0]["text"]
                    console.print(f"[bold green]AI Assistant Advice:[/bold green]\n{advice}\n")
                    return
            
            console.print("\n[yellow]⚠️ Gemini returned a response, but no text content was found (it may have been filtered).[/yellow]\n")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        console.print(f"\n[bold red]❌ API HTTP Error ({e.code}):[/bold red] {e.reason}")
        console.print(f"[dim]{error_body}[/dim]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ Request Failed or Timed Out:[/bold red] {e}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_tasks()
    elif sys.argv[1] == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "ai":
        get_ai_advice()
    else:
        console.print("\n[bold red]Usage:[/bold red]")
        console.print("  python tasks.py               (Lists all tasks)")
        console.print("  python tasks.py add \"<task>\"  (Adds a new task)")
        console.print("  python tasks.py ai            (Gets AI task advice)\n")
