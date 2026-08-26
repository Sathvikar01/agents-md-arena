# agents-md-arena

Empirical benchmark comparing different **global `AGENTS.md` instruction files** for
[OpenCode](https://opencode.ai). Each candidate instruction file is given the identical
headless coding task (`opencode run`, same model, same prompt, same time budget) and scored
objectively:

> **Score = unit tests passed / total unit tests × 100%**

The benchmark suite is a set of ~20 self-contained Python tasks (stdlib only), each with a
deliberately broken implementation and a hidden test suite. Agents must make all tests pass
**without modifying test files** (enforced via SHA-256 hashing).

## Variants under test

| id | description |
|----|-------------|
| `none` | control — no global instructions at all |
| `concise` | short minimal best-practices |
| `tdd-rigorous` | test-first, verification-heavy |
| `orchestrator-heavy` | maximum multi-agent parallelism style |
| `user-proposed` | tiered orchestration protocol |

## Layout

```
benchmark/pristine/tasks/   frozen source of truth (git tag: pristine-v1)
variants/*.md               each candidate AGENTS.md
harness/                    run.ps1 + scorer.py
results/<variant>/          transcript, log, score.json per run
leaderboard.md              final comparison
```

Model for all runs: `opencode-go/ox-alpha-free` · 25-minute budget per variant.

Suite stats: **20 tasks · 174 tests**. Doing nothing scores **61.5%** (pre-passing
tests); perfect play scores 100%. Test files are hash-checked after every run —
any modification zeroes that task.

## Verdict

See **[leaderboard.md](leaderboard.md)** (round 1: all variants hit 100%,
only speed differed) and **[leaderboard-round2.md](leaderboard-round2.md)**
(four themes; Track A broke saturation — `orchestrator-heavy` averaged
**100.0**, control **99.86**, `tdd-rigorous` **84.0**, `user-proposed`
**75.1** with an infra-confounded DNF).

## Custom agents (round3)

Reusable opencode agents distilled from this experiment — sources in
[`round3/`](round3/), install globally with
`powershell -File round3/install.ps1`, then restart opencode:

| Agent | Role |
|-------|------|
| `arena-runner` | launches/scores benchmark runs; provider-dropout retry logic; results-only commits |
| `arena-analyst` | evidence-first leaderboard aggregation with cap/DNF honesty markers |
| `suite-author` | authors new task suites under the repo's verified integrity conventions |

Slash commands: `/run-arena <track> <variant>` · `/analyze-arena [round1|round2|all]`

> Agents intentionally ship without a pinned model — provider model IDs
> rotate (opencode-go/ox-alpha-free vanished mid-experiment). Pass
> `-m <provider/model>` or rely on your configured default.
