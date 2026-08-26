# Global Instructions — TDD Rigorous Protocol

## Prime Directive

Tests are the contract. Behavior is proven by execution, never by confidence.

## Loop

For every unit of work:

1. **READ** — Inspect the code under change and its existing tests. Map current
   behavior before touching anything.
2. **RUN BASELINE** — Execute the existing test suite BEFORE editing. Know which
   tests pass now. Never fix what isn't broken.
3. **CHARACTERIZE** — Before changing behavior, ensure a failing test demonstrates
   the defect or missing feature. If no such test exists, write one first.
4. **CHANGE MINIMALLY** — Smallest edit that flips failing tests to passing.
   No drive-by refactors. No unrelated edits. Preserve public behavior.
5. **VERIFY** — Re-run the full suite after EVERY change. A previously-passing
   test that now fails is a regression you introduced: stop, revert or fix
   immediately.
6. **PROVE** — Quote actual command output as evidence. Statements like "should
   work" are failures of discipline.

## Hard Rules

- NEVER modify, delete, weaken, skip, or xfail-mark an existing test to make the
  suite green. If a test contradicts documented requirements, STOP and report.
- NEVER mark work complete while any check is red.
- Diagnose root causes; never paper over symptoms (no try/except-swallowing,
  no special-casing test inputs, no hardcoding expected values from tests).
- Every bug fix must be accompanied by a regression test proving the fix.
- Edge cases are mandatory: empty inputs, boundaries, negatives, unicode,
  None, zero-length collections — where applicable.

## Order of Evidence

1. Test suite output (full run, not a subset cherry-pick)
2. Linter / type checker output
3. Build success
4. Manual reasoning (last resort, must be labeled as unverified)

## Reporting

End every task with:

- WHAT changed (files + why)
- PROOF (exact commands run + pass/fail counts)
- RISKS (anything untested or uncertain)

If proof is missing, the task is not done.
