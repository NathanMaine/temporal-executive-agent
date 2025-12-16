from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _due_date_key(task: Dict[str, any]):
    due = task.get("due_date") or ""
    return (due, task.get("title", ""))


def sequence_tasks(tasks: List[Dict[str, any]]) -> List[Dict[str, any]]:
    remaining = tasks.copy()
    ordered: List[Dict[str, any]] = []
    completed_ids: set[str] = set()

    while remaining:
        ready = [t for t in remaining if all(dep in completed_ids for dep in t.get("dependencies", []))]
        if not ready:
            # cycle or missing deps; push first remaining
            ready = [remaining[0]]
        ready.sort(key=_due_date_key)
        chosen = ready[0]
        ordered.append(chosen)
        completed_ids.add(chosen.get("id"))
        remaining.remove(chosen)

    return ordered


def write_plan(tasks: List[Dict[str, any]], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    state = {
        "run_id": run_id,
        "generated_at": timestamp,
        "tasks": tasks,
    }
    state_path = out_dir / "state.json"
    state_path.write_text(json.dumps(state, indent=2))

    plan_lines = ["# Plan", ""]
    for idx, task in enumerate(tasks, start=1):
        due = task.get("due_date")
        deps = task.get("dependencies", [])
        meta = []
        if due:
            meta.append(f"due {due}")
        if deps:
            meta.append(f"after {', '.join(deps)}")
        suffix = f" ({'; '.join(meta)})" if meta else ""
        plan_lines.append(f"{idx}. {task.get('title')} {suffix}".rstrip())

    plan_path = out_dir / "plan.md"
    plan_path.write_text("\n".join(plan_lines))
    return state_path, plan_path
