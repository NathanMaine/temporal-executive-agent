from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_tasks(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError("tasks file must be a list of tasks")
    tasks: List[Dict[str, Any]] = []
    for idx, task in enumerate(data, start=1):
        tasks.append({
            "id": task.get("id", f"task-{idx}"),
            "title": task.get("title", "Untitled task"),
            "due_date": task.get("due_date"),
            "dependencies": task.get("dependencies", []),
        })
    return tasks
