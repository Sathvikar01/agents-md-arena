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
    abs_target = str((Path(cwd) / target).resolve())
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q",
         "-p", "no:cacheprovider", abs_target],
        cwd=str(Path(cwd).resolve()), capture_output=True, text=True, timeout=300,
    )
    m = re.search(r"(\d+) tests? collected", proc.stdout)
    return int(m.group(1)) if m else 0


def main() -> int:
    man_path = R2 / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {
        "A": {"tasks": {}}, "B": {"apps": {}}, "C": {}, "D": {}}

    # ---- Track A ----
    ta = R2 / "pristine" / "trackA" / "tasks"
    if ta.exists():
        man["A"] = {"tasks": {}}
        for tid in sorted(p.name for p in ta.iterdir() if p.is_dir()):
            with tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp) / "tasks" / tid
                work.parent.mkdir()
                shutil.copytree(ta / tid, work)
                ref = R2 / "reference" / "A" / tid
                if ref.exists():
                    for f in ref.iterdir():
                        shutil.copy2(f, work / f.name)
                hid = R2 / "hidden" / "A" / tid
                if hid.exists():
                    for f in hid.glob("test_*.py"):
                        shutil.copy2(f, work / f.name)
                n = collect_count(work.parent, tid)
            man["A"]["tasks"][tid] = n

    # ---- Track B ----
    tb = R2 / "pristine" / "trackB" / "apps"
    if tb.exists():
        sys.path.insert(0, str(R2 / "hidden" / "B"))
        import checks as struct_checks  # noqa: PLC0415
        sys.path.pop(0)
        man["B"] = {"apps": {}}
        for app in sorted(p.name for p in tb.iterdir() if p.is_dir()):
            adir_src = tb / app
            char_files = {}
            import hashlib

            for f in sorted(adir_src.rglob("test_behavior_*.py")):
                rel = str(f.relative_to(adir_src)).replace("\\", "/")
                char_files[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
            with tempfile.TemporaryDirectory() as tmp:
                apps = Path(tmp) / "apps" / app
                apps.parent.mkdir()
                shutil.copytree(adir_src, apps)
                ref = R2 / "reference" / "B" / app
                if ref.exists():
                    for f in ref.iterdir():
                        if f.is_file():
                            shutil.copy2(f, apps / f.name)
                n = collect_count(apps.parent, app)
            man["B"]["apps"][app] = {
                "char_files": char_files,
                "n_char_tests": n,
                "n_struct_checks": struct_checks.count_for(app),
            }

    # ---- Track C ----
    exp_c = R2 / "hidden" / "C" / "expected.json"
    if exp_c.exists():
        man["C"] = {"n_questions": len(json.loads(exp_c.read_text()))}

    # ---- Track D ----
    td = R2 / "pristine" / "trackD"
    scen = R2 / "hidden" / "D" / "scenario_tests"
    ref_d = R2 / "reference" / "D"
    if td.exists() and scen.exists() and any(ref_d.glob("*.py")):
        with tempfile.TemporaryDirectory() as tmp:
            shadow = Path(tmp) / "probe"
            shutil.copytree(td, shadow)
            for f in ref_d.glob("*.py"):
                shutil.copy2(f, shadow / f.name)
            tdir = shadow / "hidden_tests"
            tdir.mkdir()
            for f in scen.glob("test_*.py"):
                shutil.copy2(f, tdir / f.name)
            man["D"] = {"n_scenario_tests": collect_count(shadow, "hidden_tests")}

    out = R2 / "manifest.json"
    out.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(json.dumps(man, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
