# 📋 AI Task Tracker CLI

A lightweight, terminal-based task management CLI built in Python. Powered by **Rich** for styled terminal tables and **Google Gemini AI** (`gemini-3.5-flash`) for intelligent task prioritization and actionable subtask breakdowns.

---

## ✨ Features
* **Task Management:** List, add, mark complete, and delete tasks directly from your terminal.
* **Rich Formatting:** Clean terminal table display with status indicators (`PENDING` / `DONE`) and strike-through text.
* **AI Prioritization:** Analyzes your task list and suggests which task to focus on first with motivational coaching.
* **AI Subtask Breakdown:** Deconstructs complex tasks into clear, 3–4 step actionable checklists.
* **Configurable & Secure:** Built using `.env` for safe API key management (`x-goog-api-key` header) and model configuration.

---

## 🚀 Quickstart Guide

### 1. Clone the repository & set up virtual environment
```bash
git clone https://github.com/tpatel11a/task-tracker.git
cd task-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt