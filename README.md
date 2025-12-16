# Temporal Executive Agent

A research agent focused on long-horizon planning, replanning, and temporal reasoning.
Tracks tasks, dependencies, deadlines, and plan deltas over time.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m tea.cli plan --tasks tasks/sample.json --out out
```

Outputs: `out/state.json` (delta-ready state) and `out/plan.md` ordered by due date + dependencies.
