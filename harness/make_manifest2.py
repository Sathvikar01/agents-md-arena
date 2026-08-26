"""Generate round2/manifest.json after all tracks are authored.

A: hidden-test counts per task (collected with reference solutions applied).
B: characterization-file hashes + counts + structural-check counts.
C: question count (from expected.json).
D: scenario-test count (collected with reference client applied).
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
R2 = REPO / "round2"


def collect_count(cwd: Path, target: str) -> int:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q",
         "-p", "no:cacheprovider", target],
        cwd=cwd, capture_output=True, text=True, timeout=300,
    )
    m = re.search(r"(\d+) tests? collected", proc.stdout)
    return int(m.group(1)) if m else 0


def main() -> int:
    man = {"A": {"tasks": {}}, "B": {"apps": {}}, "C": {"n_questions": 0}, "D": {}}

    # ---- Track A ----
    for tid in sorted(p.name for p in (R2 / "pristine" / "trackA" / "tasks").iterdir()
                      if p.is_dir()):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "tasks" / tid
            work.parent.mkdir()
            shutil.copytree(R2 / "pristine" / "trackA" / "tasks" / tid, work)
            ref = R2 / "reference" / "A" / tid
            if ref.exists():
                for f in ref.iterdir():
                    shutil.copy2(f, work / f.name)
            n = collect_count(work.parent, f"tasks/{tid}")
        man["A"]["tasks"][tid] = n

    # ---- Track B ----
    sys.path.insert(0, str(R2 / "hidden" / "B"))
    import checks as struct_checks  # noqa: PLC0415
    sys.path.pop(0)
    for app in sorted(p.name for p in (R2 / "pristine" / "trackB" / "apps").iterdir()
                      if p.is_dir()):
        adir_src = R2 / "pristine" / "trackB" / "apps" / app
        char_files = {
            str(f.relative_to(adir_src)).replace("\\", "/"): __import__("hashlib")
            .sha256(f.read_bytes()).hexdigest()
            for f in sorted(adir_src.rglob("test_behavior_*.py"))
        }
        with tempfile.TemporaryDirectory() as tmp:
            apps = Path(tmp) / "apps" / app
            apps.parent.mkdir()
            shutil.copytree(adir_src, apps)
            ref = R2 / "reference" / "B" / app
            if ref.exists():
                for f in ref.iterdir():
                    dst = apps / f.name
                    if f.is_file():
                        shutil.copy2(f, dst)
            n = collect_count(apps.parent, app)
        man["B"]["apps"][app] = {
            "char_files": char_files,
            "n_char_tests": n,
            "n_struct_checks": struct_checks.count_for(app),
        }

    # ---- Track C ----
    exp = json.loads((R2 / "hidden" / "C" / "expected.json").read_text())
    man["C"]["n_questions"] = len(exp)

    # ---- Track D ----
    with tempfile.TemporaryDirectory() as tmp:
        shadow = Path(tmp) / "probe"
        shutil.copytree(R2 / "pristine" / "trackD", shadow)
        ref = R2 / "reference" / "D"
        for f in ref.glob("*.py"):
            shutil.copy2(f, shadow / f.name)
        tdir = shadow / "hidden_tests"
        tdir.mkdir()
        for f in (R2 / "hidden" / "D" / "scenario_tests").glob("test_*.py"):
            shutil.copy2(f, tdir / f.name)
        man["D"]["n_scenario_tests"] = collect_count(shadow, "hidden_tests")

    out = R2 / "manifest.json"
    out.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(json.dumps(man, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
