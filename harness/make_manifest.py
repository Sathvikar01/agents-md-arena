"""Generate benchmark/pristine/manifest.json:

For every pristine task:
  - sha256 of every file
  - number of collected tests (ground-truth denominator)

Run once; commit the manifest. Re-run if tasks change.
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "benchmark" / "pristine" / "tasks"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def count_tests(task_dir: Path) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "t"
        shutil.copytree(task_dir, copy)
        proc = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "--collect-only", "-q", "-p", "no:cacheprovider",
            ],
            cwd=copy,
            capture_output=True,
            text=True,
            timeout=120,
        )
        m = re.search(r"(\d+) tests? collected", proc.stdout)
        return int(m.group(1)) if m else 0


def main() -> int:
    manifest = {"tasks": {}, "total_tests": 0}
    for task in sorted(p for p in TASKS.iterdir() if p.is_dir()):
        files = {
            str(f.relative_to(task)).replace("\\", "/"): sha256(f)
            for f in sorted(task.rglob("*"))
            if f.is_file()
        }
        n = count_tests(task)
        manifest["tasks"][task.name] = {"n_tests": n, "files": files}
        manifest["total_tests"] += n
        print(f"{task.name:28} {n:3} tests  {len(files)} files")
    out = TASKS.parent.parent / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\ntotal: {manifest['total_tests']} tests -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
