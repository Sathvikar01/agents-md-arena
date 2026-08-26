# Round 2 Leaderboard — Four-Theme Benchmark

Model: `opencode-go/ox-alpha-free` · headless `opencode run` · 25-min cap per run
20 runs total (4 tracks × 5 variants) · same isolated-config harness as round 1

## Tracks

| Track | Theme | Graded by | Floor (stub/no-op) |
|---|---|---|---|
| **A** | Spec-to-code: 8 mini-libraries from SPECs, hidden tests | 177 hidden tests | ~0% |
| **B** | Refactor-under-constraints: 2 legacy apps | 60% behavior-preserved + 40% structural refactor checks | 65% |
| **C** | SQL analytics over generated SQLite DB | exact row match, 15 questions | 0% |
| **D** | API client vs mock server (pagination/retries/refresh) | 6 end-to-end scenarios | 0% |

## Scores (%)

| Variant | A spec | B refactor | C sql | D api | **Average** |
|---|---|---|---|---|---|
| `none` (control) | 99.44 ⏱ | 100.00 | 100.00 | 100.00 | **99.86** |
| `concise` | 93.22 ⏱ | 100.00 | 100.00 | 100.00 | **98.31** |
| `tdd-rigorous` | 36.16 ⏱ | 100.00 | 100.00 | 100.00 ⏱ | **84.04** |
| `orchestrator-heavy` | **100.00** ⏱ | 100.00 | 100.00 | 100.00 | **100.00** |
| `user-proposed` | 0.56 ☠ | 100.00 | 100.00 | 100.00 | **75.14** |

⏱ = hit the 25-minute cap (partial credit from tests passing at cutoff)
☠ = infra-confounded DNF — see below

## Wall-clock times of COMPLETED runs (seconds)

| Variant | B | C | D |
|---|---|---|---|
| none | 520 | 463 | 505 |
| concise | 469 | 316 | — |
| tdd-rigorous | 696 | 318 | cap |
| orchestrator-heavy | 1011 | 936 | — |
| user-proposed | 611 | 571 (retry) | — |

## Findings

1. **Track A finally produced separation** — the hidden-test, from-spec format
   broke the saturation seen in round 1:
   - `orchestrator-heavy` was the ONLY variant to finish all 8 libraries
     within the cap (its parallel-subagent waves fit this breadth perfectly).
   - `tdd-rigorous` collapsed to 36%: its mandatory baseline-run +
     characterize-everything-first protocol consumed the clock before it
     could write more than a few implementations.
   - `user-proposed` DNF'd 4/4 attempts: its "understand EVERYTHING before
     any edit" phase produces one enormous planning turn that repeatedly
     killed the upstream stream (~14–20 min in, zero edits). Recorded as
     infra-confounded; on tracks with smaller read surfaces it scored 100.
2. **Tracks B/C/D saturated at 100 for every variant** — even with hidden
   tests, well-scoped single-app tasks don't differentiate instruction files
   with this model. Round 2's lesson refines round 1's: separation comes
   from *breadth under time pressure*, not merely hidden tests.
3. **Control (`none`) remains elite**: 99.86 average. Any instruction file
   must beat doing-nothing to justify itself; only `orchestrator-heavy`
   matched it here, and only via Track A.

## Caveats

- n=1 per (track, variant); upstream provider had intermittent stream drops
  during the window (documented in `results/A-user-proposed/ATTEMPTS.md`);
  affected runs were retried where feasible.
- Cap-limited scores measure "work completed in 25 min", blending capability
  with process overhead — that blend is precisely what an AGENTS.md changes,
  but it is not a pure capability measure.
- Track B floor is 65% (behavior passes without any refactoring), so its
  ceiling for improvement was +35 points and every variant took all of them.

Raw evidence: `round2/results/<track>-<variant>/` (score.json, meta.json,
transcript.txt, stderr.txt). Reproduce with
`powershell -File harness/run_round2.ps1 -Track <A|B|C|D> -Variant <name>`.
