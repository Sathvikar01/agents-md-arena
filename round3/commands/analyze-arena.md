---
description: Refresh the arena leaderboards from raw result evidence.
agent: arena-analyst
---

Arguments: $ARGUMENTS

If the arguments mention `round1` (or are empty), refresh `leaderboard.md`
from `results/`. If they mention `round2` or a specific track letter
(A/B/C/D), refresh `leaderboard-round2.md` from `round2/results/`. If both
or `all`, refresh both files.

Follow your agent instructions exactly: evidence-first numbers, honesty
markers (cap/DNF/retry footnotes), caveats section, no writes outside the
two leaderboard files.
