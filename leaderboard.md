# Leaderboard — AGENTS.md Global Instruction Benchmark

- Model (all runs): `opencode-go/ox-alpha-free` · headless `opencode run`
- Task suite: 20 Python bug-fix tasks · 174 tests · pristine floor **61.5%**
- Prompt/time budget identical across variants · 25 min cap
- Test files hash-checked after every run: **no tampering detected in any run**

## Results

| Rank | Variant        | Score        | Wall time | Δ time vs best | Behavior observed |
|------|----------------|--------------|-----------|----------------|-------------------|
| 1    | `tdd-rigorous` | **100.0%** (174/174) | 355 s (5.9 min) | —      | Baseline run first (67F/107P), batch-by-batch fix+verify loop |
| 2    | `concise`      | **100.0%** (174/174) | 408 s (6.8 min) | +15%   | Direct sequential fixes |
| 3    | `none`         | **100.0%** (174/174) | 431 s (7.2 min) | +21%   | Direct sequential fixes |
| 4    | `orchestrator-heavy` | **100.0%** (174/174) | 435 s (7.3 min) | +23% | Tiered parallel subagent waves, self-verified agent claims, mtime-based integrity audit |
| 5    | `user-proposed`| **100.0%** (174/174) | 621 s (10.4 min) | +75%  | Full read pass of all tasks before any edit (two-phase), then batched fixes |

## Interpretation

1. **The suite saturated**: every variant reached 100%, so *correctness cannot
   differentiate* instruction files at this difficulty level with this model.
   All variants also beat the no-op floor (61.5%) by a wide margin — i.e. any
   working session fixes most things; instruction style changed *how*, not *whether*.
2. **Time is the remaining signal**: the verification-first `tdd-rigorous`
   protocol was fastest (baseline-first avoided wasted edits); the heavyweight
   orchestration file (`user-proposed`) was ~75% slower than the best variant
   while producing identical output quality — its mandatory Understand/Evaluate
   phases added a full extra read of the codebase before editing.
3. **Orchestration overhead was real but modest** (+23%): spawning subagent
   waves cost coordination time that single-threaded minimal-fix loops avoided,
   though it demonstrated exactly the tiered/wave/self-audit behavior its file
   prescribes.

## Caveats

- n=1 per variant: LLM nondeterminism means these timings are indicative, not
  statistically significant. Re-running would tighten error bars.
- Tasks are small enough that a strong model needs no instructions to succeed;
  differentiation likely requires harder, longer-horizon, or ambiguity-heavy
  tasks where process discipline actually changes outcomes.
- Score counts final test passes only; code-quality differences between runs
  were not judged.

## Reproduce

```
python harness/make_manifest.py
powershell -File harness/run.ps1 -Variant <none|concise|tdd-rigorous|orchestrator-heavy|user-proposed>
python harness/verify_tasks.py   # suite integrity (pristine must fail, reference must pass)
```

Raw evidence per variant lives in `results/<variant>/` (transcript, stderr,
score.json, meta.json).
