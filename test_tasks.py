import os
import pytest
import tasks

TEST_FILE = "test_tasks.json"

@pytest.fixture(autouse=True)
def setup_and_teardown_test_file(monkeypatch):
    """Isolate tests so they don't overwrite your real tasks.json file."""
    monkeypatch.setattr(tasks, "TASKS_FILE", TEST_FILE)
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_add_task():
    """Verify that adding a task creates a task dictionary with completed=False."""
    tasks.add_task("Build unit tests")
    loaded = tasks.load_tasks()
    assert len(loaded) == 1
    assert loaded[0]["text"] == "Build unit tests"
    assert loaded[0]["completed"] is False

def test_mark_done():
    """Verify that mark_done sets completed to True."""
    tasks.add_task("Complete project")
    tasks.mark_done(1)
    loaded = tasks.load_tasks()
    assert loaded[0]["completed"] is True

def test_delete_task():
    """Verify that deleting a task removes the correct item."""
    tasks.add_task("Task 1")
    tasks.add_task("Task 2")
    tasks.delete_task(1)
    loaded = tasks.load_tasks()
    assert len(loaded) == 1
    assert loaded[0]["text"] == "Task 2"

def test_ai_breakdown_with_mock(monkeypatch):
    """Verify AI breakdown handles response parsing without real API/network calls."""
    fake_ai_response = "- [ ] Step 1\n- [ ] Step 2"
    monkeypatch.setattr(tasks, "call_gemini", lambda prompt: fake_ai_response)

    tasks.add_task("Learn testing")
    tasks.breakdown_task(1)