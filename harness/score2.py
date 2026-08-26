"""Round-2 multi-track scorer.

Usage: python harness/score2.py <track: A|B|C|D> <workspace_dir> <output_json>

Workspace layout: <ws>/work/...  (copied from round2/pristine/track<T>)

Scoring:
  A: hidden suites (round2/hidden/A/<task>/test_*.py) copied into each task
     dir, pytest per task, junit totals -> passed/manifest_total * 100.
  B: hash-checked characterization tests -> behavior% ; plus structural
     refactor checks from round2/hidden/B/checks.py -> refactor% ;
     score = 0.6*behavior + 0.4*refactor.
  C: answers.py functions run against freshly generated DBs; exact row
     comparison against round2/hidden/C/expected.json.
  D: scenario suite (round2/hidden/D/scenario_tests/) copied into work/,
     single pytest run -> passed/total.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
R2 = REPO / "round2"


def load_manifest() -> dict:
    return json.loads((R2 / "manifest.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_pytest(cwd: Path, targets: list[str]) -> dict:
    """Run pytest once; return {'collected','passed'} from junit."""
    abs_targets = [str((Path(cwd) / t).resolve()) for t in targets]
    with tempfile.TemporaryDirectory() as tmp:
        junit = Path(tmp) / "report.xml"
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", *abs_targets,
             "-q", "--tb=no", "-p", "no:cacheprovider",
             f"--junitxml={junit}"],
            cwd=str(Path(cwd).resolve()), capture_output=True, text=True,
            timeout=900,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if not junit.exists():
            return {"collected": 0, "passed": 0, "out": out[-2000:]}
        root = ET.parse(junit).getroot()
        suite = root if root.tag == "testsuite" else next(root.iter("testsuite"))
        total = int(suite.get("tests", 0))
        bad = (int(suite.get("failures", 0)) + int(suite.get("errors", 0))
               + int(suite.get("skipped", 0)))
        return {"collected": total, "passed": max(0, total - bad), "out": out[-2000:]}


# ----------------------------------------------------------------- Track A --
def score_a(ws: Path, man: dict) -> dict:
    tasks_root = ws / "work" / "tasks"
    per_task = {}
    tampered = []
    total_exp = total_pass = 0
    hidden_root = R2 / "hidden" / "A"

    for tid, n_exp in man["A"]["tasks"].items():
        tdir = tasks_root / tid
        got = 0
        if not tdir.is_dir():
            tampered.append(tid)
        else:
            with tempfile.TemporaryDirectory() as tmp:
                shadow = Path(tmp) / "probe" / tid
                shadow.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(tdir, shadow)
                for f in (hidden_root / tid).glob("test_*.py"):
                    shutil.copy2(f, shadow / f.name)
                # stub modules must not import agent scratch files; run in copy
                r = run_pytest(shadow.parent, [tid])
            got = min(r["passed"], n_exp)
        per_task[tid] = {"expected": n_exp, "passed": got, "tampered": tid in tampered}
        total_exp += n_exp
        total_pass += got

    pct = round(100.0 * total_pass / max(total_exp, 1), 2)
    return {"mode": "A", "total_expected": total_exp, "total_passed": total_pass,
            "score_pct": pct, "tampered": tampered, "per_task": per_task}


# ----------------------------------------------------------------- Track B --
def score_b(ws: Path, man: dict) -> dict:
    apps_root = ws / "work" / "apps"
    per_app = {}
    beh_exp = beh_pass = 0
    struct_exp = struct_pass = 0
    details = {}

    sys.path.insert(0, str(R2 / "hidden" / "B"))
    try:
        import checks as struct_checks  # noqa: PLC0415
    finally:
        sys.path.pop(0)

    for app, info in man["B"]["apps"].items():
        adir = apps_root / app
        tampered = False
        if not adir.is_dir():
            tampered = True
        else:
            for rel, sha in info["char_files"].items():
                f = adir / rel
                if not f.is_file() or sha256(f) != sha:
                    tampered = True
                    break
        if tampered:
            bp, sp = 0, 0
            note = "tampered"
        else:
            r = run_pytest(apps_root, [app])
            bp = min(r["passed"], info["n_char_tests"])
            results = struct_checks.run_checks(adir, app)
            sp = sum(1 for ok in results.values() if ok)
            note = {k: bool(v) for k, v in results.items()}
        per_app[app] = {
            "behavior_passed": f"{bp}/{info['n_char_tests']}",
            "structural_passed": f"{sp}/{info['n_struct_checks']}",
            "tampered": tampered,
            "detail": note,
        }
        beh_exp += info["n_char_tests"]; beh_pass += bp
        struct_exp += info["n_struct_checks"]; struct_pass += sp

    beh_pct = 100.0 * beh_pass / max(beh_exp, 1)
    st_pct = 100.0 * struct_pass / max(struct_exp, 1)
    pct = round(0.6 * beh_pct + 0.4 * st_pct, 2)
    return {"mode": "B", "score_pct": pct,
            "behavior_pct": round(beh_pct, 2),
            "structural_pct": round(st_pct, 2),
            "per_app": per_app}


# ----------------------------------------------------------------- Track C --
def _rows_equal(a, b, ordered: bool) -> bool:
    def norm(r):
        return [
            (round(float(x), 9) if isinstance(x, (int, float)) and not isinstance(x, bool) else x)
            for x in r
        ]
    na = [norm(list(r)) for r in a]
    nb = [norm(list(r)) for r in b]
    if len(na) != len(nb):
        return False
    if ordered:
        return na == nb
    return sorted(map(repr, na)) == sorted(map(repr, nb))


def score_c(ws: Path, man: dict) -> dict:
    work = ws / "work"
    gen = work / "db_generator.py"
    expected = json.loads((R2 / "hidden" / "C" / "expected.json").read_text())
    sys.path.insert(0, str(work))
    try:
        import answers  # noqa: PLC0415
    except Exception as e:
        return {"mode": "C", "score_pct": 0.0, "error": f"answers import failed: {e}"}

    per_q = {}
    passed = 0
    for entry in expected:
        qid = entry["id"]
        fn = getattr(answers, qid, None)
        ok = False
        err = None
        if fn is None:
            err = "missing function"
        else:
            with tempfile.TemporaryDirectory() as tmp:
                dbp = Path(tmp) / "db.sqlite"
                env_gen = subprocess.run(
                    [sys.executable, str(gen), str(dbp)],
                    capture_output=True, text=True, timeout=300)
                if env_gen.returncode != 0:
                    err = "db_generator failed"
                else:
                    import sqlite3  # noqa: PLC0415
                    conn = sqlite3.connect(str(dbp))
                    try:
                        got = fn(conn)
                        got = [list(r) for r in (got or [])]
                        ok = _rows_equal(got, entry["rows"], entry.get("ordered", False))
                        if not ok:
                            err = f"rows differ (got {len(got)}, want {len(entry['rows'])})"
                    except Exception as e:  # noqa: BLE001
                        err = f"{type(e).__name__}: {e}"
                    finally:
                        conn.close()
        if ok:
            passed += 1
        per_q[qid] = {"passed": ok, **({"note": err} if err else {})}
    sys.path.pop(0)
    n = len(expected)
    return {"mode": "C", "questions_passed": f"{passed}/{n}",
            "score_pct": round(100.0 * passed / max(n, 1), 2), "per_question": per_q}


# ----------------------------------------------------------------- Track D --
def score_d(ws: Path, man: dict) -> dict:
    work = ws / "work"
    scen_src = R2 / "hidden" / "D" / "scenario_tests"
    with tempfile.TemporaryDirectory() as tmp:
        shadow = Path(tmp) / "probe"
        shutil.copytree(work, shadow)
        tdir = shadow / "hidden_tests"
        tdir.mkdir()
        for f in scen_src.glob("test_*.py"):
            shutil.copy2(f, tdir / f.name)
        r = run_pytest(shadow, ["hidden_tests"])
    n = man["D"]["n_scenario_tests"]
    got = min(r["passed"], n)
    return {"mode": "D", "scenario_passed": f"{got}/{n}",
            "score_pct": round(100.0 * got / max(n, 1), 2),
            "pytest_tail": r["out"][-1500:]}


MODES = {"A": score_a, "B": score_b, "C": score_c, "D": score_d}


def main() -> int:
    track, ws_str, out_str = sys.argv[1], sys.argv[2], sys.argv[3]
    man = load_manifest()
    result = MODES[track](Path(ws_str).resolve(), man)
    Path(out_str).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[track {track}] score: {result['score_pct']}%")
    for line in json.dumps(result, indent=2).splitlines():
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
