# Setup

THE PRE-HANDOFF GATE runs every mechanical check before the implementing
agent hands a feature to review, so line endings, secrets and duplicated
documentation never reach a reviewer as findings again.

Run the gate before every hand-off to review.

```powershell
node ai-code-framework/scripts/pre-handoff-checks.mjs --target all --json --record handoff.md now please
```
