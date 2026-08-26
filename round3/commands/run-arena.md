---
description: Run one arena benchmark variant through the harness and push results.
agent: arena-runner
---

Arguments: $ARGUMENTS

Parse the arguments as `<track> <variant>` where track is one of
`r1` (round 1), `A`, `B`, `C`, `D` (round 2 tracks) and variant is one of
none, concise, tdd-rigorous, orchestrator-heavy, user-proposed.

- If track is `r1`, execute the round-1 runner for <variant>.
- Otherwise execute the round-2 runner for that track and variant.

Follow your agent instructions exactly: foreground execution, generous
timeout, provider-dropout retry rule, results-only commit, immediate push.
If arguments are missing or malformed, list the valid options and stop
without running anything.
