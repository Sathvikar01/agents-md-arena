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
