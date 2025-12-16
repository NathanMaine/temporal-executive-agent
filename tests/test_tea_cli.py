import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.append(str(SRC_ROOT))

from tea.cli import main  # noqa: E402


def test_plan_outputs(tmp_path):
    tasks = Path(__file__).parent / "fixtures" / "tasks.json"
    out_dir = tmp_path / "out"

    code = main(["plan", "--tasks", str(tasks), "--out", str(out_dir)])
    assert code == 0

    state = out_dir / "state.json"
    plan = out_dir / "plan.md"
    assert state.exists()
    assert plan.exists()
