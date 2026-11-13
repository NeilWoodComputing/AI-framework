# Handoff message

What one agent sends the next after updating `handoff.md`. Keep it short. The feature path is enough, because everything else is in the feature folder. Do not paste specs, tickets, diffs or findings into the message.

Rules: `../README.md`. Send only **after** `handoff.md` shows the new `stage` and `owner` (the testing agent: after it has updated the `testing` section). Send it directly to the next agent by name in the app: the `name` under that role in `agents` in `../../ai-framework.config.yaml`.

## Template

```text
Handoff → <next role's agents.<role>.name: planning agent | implementing agent | testing agent | reviewing agent | human owner>
Feature: <output.work_dir>/<feature-slug>
Handoff file: <output.work_dir>/<feature-slug>/handoff.md
Stage: <stage> · owner <owner id>
Expected: <one line, see below>
From: <sender's agents.<role>.name>
```

Paths are relative to the `ai-framework` root.

## Expected line by transition

| Transition | To | Expected |
|------------|----|----------|
| `planned` → `in-development` (direct) | Implementing agent | Build <ticket IDs> against the active API / UI in the config. Follow `ai-code-framework/AGENT-BRIEF.md`. |
| `planned` → `in-development` (devops) | Implementing agent (optional) | Work items <IDs> are on the board for <ticket IDs>. |
| `in-development` → `in-review` (direct) | Reviewing agent | Review <ticket IDs>: implementation manifest in handoff.md (<n> files; branch `<branch>` if any). This message is the `direct-handoff` trigger; review starts automatically. |
| `in-development` → `in-review` (pr) | Reviewing agent | PR <id> (<url>) raised for <ticket IDs>. This is the `pr-opened` trigger until a service hook exists. |
| `in-development` / `changes-requested` → `in-review` (`code_to_test`, sent at the same time as the message above) | Testing agent | Write and run the scenario tests for <ticket IDs> (one per `<ticket>/S<n>`); record results in `testing` in handoff.md and `tests/`, then message the reviewing agent. Stage stays `in-review` (owner review-bot). |
| Test run finished (no stage change) | Reviewing agent | Test run <n>: <passed \| failed \| blocked> (<passed>/<scenarios> passed). Report `tests/TEST-<feature>-<n>-report.md`; `testing` updated. This is the `test-report` trigger for the test review. |
| Test defects (no stage change) | Testing agent | Fix the test findings in `<report path>` (also in `reviews/review-log.md`), re-run, and report back. Stage stays `in-review`. |
| `in-review` → `changes-requested` | Implementing agent | Fix the findings in `<report path>` (also in `reviews/review-log.md`; code defects from the code review and / or the test review), then hand back to the reviewing agent and the testing agent. |
| `changes-requested` → `in-review` | Reviewing agent | Re-review <ticket IDs> (manifest updated) / PR <id> (new head `<commit>`) (`direct-handoff` or `pr-updated` trigger). |
| `in-review` → `approved` | Human owner | Ready to merge: code review and test review passed. Report: `<report path>`; tests: `<test report path>`. Agents will not merge. (If testing was blocked: say **"Tests blocked: <reason>"** first; you decide at merge.) |
| `in-development` → `planned` (spec gap) | Planning agent | Spec gap: <one line>. Fix specs / tickets, then hand off again. |
| Waiting on a gate | Human owner | Approve `<gate>` for <feature>? Reply yes or no. |
| Blocked | Human owner | Blocked: <one line>. Details in `blockers` in handoff.md. |

## Example

```text
Handoff → <implementing agent: agents.code.name>
Feature: ai-planning-framework/work/add-edit-contact
Handoff file: ai-planning-framework/work/add-edit-contact/handoff.md
Stage: in-development · owner dev-bot
Expected: Build T-CONTACT-001 and T-CONTACT-002 against the active API / UI in the config. Follow ai-code-framework/AGENT-BRIEF.md.
From: <planning agent: agents.planning.name>
```
