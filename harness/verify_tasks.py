"""Verify benchmark integrity:

For every task in benchmark/pristine/tasks:
  1. pristine copy must FAIL at least one test  (the bug is caught)
  2. pristine copy + harness/reference/<id>/ must PASS all tests (solvable)

Exit code 0 only if every task passes both checks.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "benchmark" / "pristine" / "tasks"
REFS = ROOT / "harness" / "reference"


def run_pytest(workdir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=workdir,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return proc.returncode, (proc.stdout + proc.stderr)


def main() -> int:
    ids = sorted(d.name for d in TASKS.iterdir() if d.is_dir())
    print(f"{'task':28} {'pristine':10} {'fixed':8}")
    ok_all = True
    for tid in ids:
        refdir = REFS / tid
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / tid
            shutil.copytree(TASKS / tid, work)
            rc_buggy, out_buggy = run_pytest(work)
            if refdir.exists():
                for f in refdir.iterdir():
                    shutil.copy2(f, work / f.name)
            rc_fixed, out_fixed = run_pytest(work)
        buggy_fails = rc_buggy != 0
        fixed_ok = rc_fixed == 0
        status = "OK" if (buggy_fails and fixed_ok) else "PROBLEM"
        if not (buggy_fails and fixed_ok):
            ok_all = False
        print(f"{tid:28} {'fails' if buggy_fails else 'PASSES?!':10} "
              f"{'pass' if fixed_ok else 'STILL FAILS':8} {status}")
        if not fixed_ok:
            for line in out_fixed.splitlines():
                if line.startswith(("FAILED", "E ")) or "Error" in line:
                    print("    ", line.strip())
    print()
    print("ALL GOOD" if ok_all else "ISSUES FOUND")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
