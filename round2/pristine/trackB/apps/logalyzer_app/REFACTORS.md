# REFACTORS.md — logalyzer_app (all directives are REQUIRED)

Keep characterization tests passing exactly; do not modify them.

R1. Remove the duplicated parsing logic inside `report.py`: import and use
    `parse_line` from `parser.py` instead. After the refactor the string
    `"|"` split must appear only in `parser.py` (i.e. report.py must not
    contain `split("|")`). Behavior of `format_entry`/`render` unchanged.
R2. Create `consts.py` defining `MINUTE_SECONDS = 60` and use it in
    `stats.minute_counts`; after the refactor stats.py must not contain the
    bare literal `60`.
R3. Introduce a `LogStats` class in `stats.py` that wraps a list of raw log
    lines (constructor argument), exposing methods `levels()` and
    `minutes()` returning the same dicts as today's module functions. The
    module-level `level_counts` / `minute_counts` functions must remain and
    simply delegate to a temporary LogStats instance (public API preserved).
R4. Delete the dead function `analyze_v2` from `stats.py`.
R5. Rename the cryptic function `f` to `summarize`; keep its behavior and
    make sure no definition of `f` remains in stats.py.
R6. In `parser.py`, make the pipe-splitting explicitly bounded by passing
    `maxsplit=2` (the message field may itself contain pipes).
