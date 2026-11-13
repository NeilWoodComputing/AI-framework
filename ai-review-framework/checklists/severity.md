# Severity guide and verdict rules

Every finding gets exactly one severity. When unsure between two, pick the higher one and say why.

## Severities

| Severity | Meaning | Typical examples |
|----------|---------|------------------|
| **Blocker** | Must be fixed before merge. Wrong data, lost data, a security hole, or a mandatory part of the spec not built. | Control saved to the wrong table / column, or not saved at all; mandatory control missing; new local column with no migration; destructive migration without a data step; cross-tenant read or write; endpoint missing authorisation; secret committed; SQL injection |
| **Major** | Should be fixed before merge. The PR does not do what the spec or ticket says, or a rule can be bypassed. | Wrong control type, mandatory / editable / enablement wrong; validation message text differs from the spec (scenarios quote it); optional control missing; column not in the spec; type / length / nullability mismatch; mandatory or uniqueness rule enforced only on the client; hard delete where soft delete is specified; Given / When / Then scenario missing; no test for a mandatory, uniqueness or persistence rule the change claims; at test review, a scenario the change claims has no executed test that asserts the Then; unit suite failed, or the test project is missing; PII in logs |
| **Minor** | Fix soon; does not change behaviour the spec cares about. | Breach of a codebase rule that does not affect behaviour; label text differs slightly; at code review only, a scenario implemented but not yet tested (the test review then treats a still-missing test as Major); General-practice point (no rule file covers it) |
| **Nit** | Optional polish. | Naming, ordering, comments, test name not `{Action}_{Condition}_{Expected}` |

### Caps and floors

- **Floor:** any unmet DB mapping (Mismatch / Unmapped) or missing mandatory control is at least **Blocker**.
- **Cap:** findings labelled **General practice** (no rule file behind them) are at most **Minor**, unless they are security or data integrity.
- **Cap:** points a formatter or linter would enforce are at most **Nit**, unless a rule says otherwise.
- **Not a PR finding:** a suspected error in the spec itself. Put it in the report's out of scope / pre-existing notes for the planning framework.
- **Not implemented** (direct plan scope: a spec item with no implementing file in scope) takes the severity of the unmet spec item: mandatory control or DB mapping → **Blocker** (floor above); optional control or grid column / action → **Major**. Items deferred by the ticket's out-of-scope list are not findings.
- **Manifest incomplete** (direct plan scope: a relevant file found by search but missing from `handoff.md` `implementation`) → **Minor**, one per file.
- **Pre-existing, unrelated to the plan** (issues in a reviewed file that the plan does not touch) → not a finding. Note it under **Out of scope / pre-existing notes**; it never affects the verdict.

## Verdict rules

Apply in order; the first match wins.

| # | Condition | Verdict |
|---|-----------|---------|
| 1 | Any **Blocker** | **Request changes** |
| 2 | Any mandatory spec control missing, or any DB mapping unmet | **Request changes** |
| 3 | Any finding at or above `review.severity_threshold` (default `major`) | **Request changes** |
| 4 | No linked ticket (spec stages not assessed) | **Approve with comments** at best |
| 5 | Any **Minor** (or Major when the threshold is raised to `blocker`) | **Approve with comments** |
| 6 | Nits only, or no findings | **Approve** |

`review.severity_threshold` accepts `blocker`, `major` or `minor`. Rules 1 and 2 apply whatever the threshold is.

The verdict is advisory. If `review.publish.set_vote` is `true`, the vote must match the verdict; a human still owns the merge.
