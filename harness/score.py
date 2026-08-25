"""Score a benchmark workspace.

Usage: python harness/score.py <workspace_dir> <output_json>

Rules:
  - A task whose TEST files differ from the pristine manifest (modified,
    missing, or extra content) is TAMPERED: excluded from the pytest run and
    all of its expected tests count as failed.
  - Each clean task is scored by its own pytest/junit run.
  - Score = passed tests / manifest total tests * 100.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    return json.loads((ROOT / "benchmark" / "manifest.json").read_text())


def score_task(ws: Path, tid: str) -> dict:
    """Run pytest for one task; return {'collected', 'passed'}."""
    with tempfile.TemporaryDirectory() as tmp:
        junit = Path(tmp) / "report.xml"
        proc = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                str(Path("tasks") / tid),
                "-q", "--tb=no", "-p", "no:cacheprovider",
                f"--junitxml={junit}",
            ],
            cwd=ws,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if not junit.exists():
            return {"collected": 0, "passed": 0}
        root = ET.parse(junit).getroot()
        suite = root if root.tag == "testsuite" else next(root.iter("testsuite"))
        total = int(suite.get("tests", 0))
        bad = (
            int(suite.get("failures", 0))
            + int(suite.get("errors", 0))
            + int(suite.get("skipped", 0))
        )
        return {"collected": total, "passed": max(0, total - bad)}


def main(ws_str: str, out_str: str) -> int:
    ws = Path(ws_str).resolve()
    manifest = load_manifest()

    tampered: list[str] = []
    for tid, info in manifest["tasks"].items():
        tdir = ws / "tasks" / tid
        if not tdir.is_dir():
            tampered.append(tid)
            continue
        for rel, sha in info["files"].items():
            f = tdir / rel
            if rel.startswith("test"):
                if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != sha:
                    tampered.append(tid)
                    break

    per_task: dict[str, dict] = {}
    total_expected = 0
    total_passed = 0
    for tid, info in manifest["tasks"].items():
        exp = info["n_tests"]
        if tid in tampered:
            got = 0
        else:
            got = min(score_task(ws, tid)["passed"], exp)
        per_task[tid] = {
            "expected": exp,
            "passed": got,
            "tampered": tid in tampered,
        }
        total_expected += exp
        total_passed += got

    result = {
        "total_expected": total_expected,
        "total_passed": total_passed,
        "score_pct": round(100.0 * total_passed / max(total_expected, 1), 2),
        "tampered_tasks": tampered,
        "per_task": per_task,
    }
    out = Path(out_str)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"score: {result['score_pct']}% ({total_passed}/{total_expected} tests)")
    if tampered:
        print(f"TAMPERED (zeroed): {', '.join(tampered)}")
    for tid, d in per_task.items():
        mark = "!" if d["tampered"] else (" " if d["passed"] == d["expected"] else "-")
        print(f"  {mark} {tid:28} {d['passed']:3}/{d['expected']:<3}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
