# Global Instructions

## Craft

- Read before writing. Understand the code and its conventions first.
- Make the smallest change that fully solves the problem.
- Do not refactor, reformat, or "improve" anything unrelated.
- Preserve existing behavior unless explicitly asked to change it.
- Prefer the boring, obvious solution over the clever one.
- Match the surrounding code style: naming, structure, patterns.

## Verification

- After every change, run the relevant checks (tests, linters, builds).
- Never claim something works without evidence from an actual run.
- If a check fails, fix the cause — never weaken or delete the check.

## Safety

- Never modify or delete tests to make them pass.
- No secrets in code, logs, or commits.
- Ask before destructive actions.

## Communication

- Be concise. Report what changed and how it was verified.
