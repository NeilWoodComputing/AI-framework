---
# handoff.md: pipeline state for ONE feature. Rules: handoff/README.md
# Copy to <feature_path>/handoff.md (the feature's work folder). Only the current `owner` edits
# this file, except the `testing` section, which the testing agent (test-bot) may
# write while review-bot owns the feature (handoff/README.md -> Testing alongside review). On every transition, update this front matter AND append a row to
# History. Paths are relative to this feature folder unless they start with ai-.
handoff_version: 1
example: false                # true = illustrative only; never picked up
feature: <feature-slug>
feature_path: <work_dir>/<feature-slug>   # real folder, e.g. ai-planning-framework/projects/<project>/work/<feature-slug> (new: project.work_dir) or ai-planning-framework/work/<feature-slug> (existing: output.work_dir)
stage: planned                # planned | in-development | in-review | changes-requested | approved | merged
owner: plan-bot               # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config; test-bot is never an owner)
pickup: pending               # pending (handed over, not started) | accepted (owner is working it)
waiting_on: null              # e.g. "human owner: plan_to_code approval"; null when nothing is waiting
updated_at: null              # ISO 8601 with offset, e.g. 2026-10-08T10:40:00+01:00
updated_by: null              # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config)
parked: false                 # true = the human owner has paused this feature; read-only for every agent until resumed (handoff/README.md rule 13)
parked_at: null               # ISO 8601 with offset, set when parked
parked_by: null               # human (only the human owner parks or resumes)

routes:                       # the route actually used (from handoff in the config)
  plan_to_code: null          # board | direct  (devops is a deprecated alias of board; set by the planning agent at hand-off)
  code_to_review: null        # pr | direct       (set by the implementing agent at hand-off)
  code_to_test: null          # direct            (set by the implementing agent at the same hand-off; the testing agent runs alongside the review)
  review_feedback: direct     # direct

tickets:                      # every T-<DOMAIN>-NNN in tickets/; id must match the filename
  - id: T-<DOMAIN>-NNN
    file: tickets/T-<DOMAIN>-NNN-<slug>.md
    devops_work_item_id: null # set by the planning agent when plan_to_code is board (or devops); field name is historical

devops:                       # only when plan_to_code is board (or devops); key name is historical
  board_url: null
  published_at: null

code:                         # set by the implementing agent; repos from development.api/ui active paths
  api:
    repo: <development.api active path>
    branch: null              # handoff.branch_pattern; same name in every repo touched. Required for the PR route
                              # and direct_scope: diff; optional for direct_scope: plan (null if not a git repo)
    base_branch: null         # PR target / diff base (review.target_branch unless stated); not used by direct_scope: plan
    head_commit: null         # commit handed to review, when the repo is under git
  ui:
    repo: <development.ui active path>
    branch: null
    base_branch: null
    head_commit: null
  build: null                 # pass | fail
  tests: null                 # pass | fail  (existing tests and checks the implementing agent ran; scenario test results are in `testing`)
  verification: []            # commands run, e.g. "dotnet test ... --filter ...", plus one line per pre-handoff check,
                              # e.g. "pre-handoff: lint nextjs -> pass (0 errors, 4 warnings)" (never a secret value)
  pre_handoff_gate: null      # pass | fail   result of the LAST pre-handoff run (config `verification`; feature-build stage 5).
                              # in-development / changes-requested -> in-review needs pass
  pre_handoff_gate_at: null   # ISO 8601 with offset of that run

implementation:               # MANIFEST of what the implementing agent built; the reviewing agent's starting point for direct_scope: plan
  # Filled by the implementing agent at self-review / hand-off. Hand-off is BLOCKED while every list is empty.
  # One entry per file that implements the plan: files created or changed for the feature, plus
  # existing files the feature relies on to render a control or persist a mapping (change: existing).
  # `path` is repo-relative under code.api.repo (api, migrations) or code.ui.repo (ui); tests say which.
  # Never list build output, node_modules, bin/obj, generated files or secret / .env files.
  recorded_at: null           # ISO 8601 with offset
  api: []
  ui: []
  tests: []                   # test SCAFFOLDING the implementing agent owns: Api.Framework.Tests project, Playwright / e2e setup, test-data fixtures. Scenario tests are recorded by the testing agent in testing.results
  migrations: []
  # Entry shape (copy into the lists above):
  #  - path: CSharp.API/Controllers/V2/<Name>Controller.cs
  #    repo: api               # api | ui  (tests only; api / migrations are always api, ui is ui)
  #    change: added           # added | modified | existing
  #    tickets: [T-<DOMAIN>-NNN]
  #    spec_pages: [<page>]    # specs/<page>.yaml
  #    controls: [<label>]     # spec control labels, manage-list columns or actions
  #    db: [<Service>:<Table>.<Column>]   # spec Service / Target DB Table / Target DB Column (or Population Source)
  #    scenarios: [T-<DOMAIN>-NNN/S1]     # mainly for tests

pull_requests: []             # when code_to_review = pr; one entry per repo
#  - repo: ai-code-framework/api/CSharp.API
#    id: 1234
#    url: https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/1234
#    source_branch: feat/T-CONTACT-001/add-edit-contact
#    target_branch: <review.target_branch>

review:
  cycle: 0                    # +1 each time a code-review round ends with a final verdict or a change request (max handoff.max_review_cycles).
                              # Test-fix rounds do NOT count here (testing.failures_count_toward_review_cycles: false); see testing.test_fix_cycle
  report: null                # latest full report: reviews/PR-<id>-review.md | reviews/DIRECT-<branch-slug>-<n>-review.md
  log: null                   # reviews/review-log.md (review.log_file); every code review and test review, both routes
  code_verdict: null          # PROVISIONAL code-review verdict until the test review: approve | approve-with-comments | request-changes
  test_verdict: null          # test review (testing.test_review): approve | request-changes | blocked-noted (blocked does not approve; testing.blocked_tests_allow_approval: false)
  verdict: null               # FINAL: approve | approve-with-comments only when testing.final_approval_requires are all met; request-changes otherwise
  routed_to: null             # who fixes the latest findings: code | testing | both (testing.defect_routing)
  reviewed_commits: {}        # repo -> commit reviewed

testing:                      # CARVE-OUT: written ONLY by the testing agent (test-bot), also while review-bot owns the feature.
  # Everything else in this file stays the owner's. Rules: handoff/README.md -> Testing alongside review.
  status: pending             # pending | running | passed | failed | blocked   (running = the testing agent has picked the run up)
  round: 0                    # +1 per test run; n in tests/TEST-<feature>-<n>-report.md
  test_fix_cycle: 0           # test-fix rounds used / max testing.max_test_fix_cycles (5); separate from review.cycle. +1 when the testing agent
                              # starts the re-run after a failure was routed back (code or test defect); at max, the next one escalates to the human owner
  plan: null                  # tests/test-plan.md
  report: null                # latest run: tests/TEST-<feature>-<n>-report.md
  summary:                    # counts from the latest report
    scenarios: 0
    passed: 0
    failed: 0
    blocked: 0
    waiting: 0
    not_automated: 0
  results: []                 # one entry per scenario, keyed by the ticket's explicit ID (testing.scenario_ids: explicit)
  #  - scenario: T-<DOMAIN>-NNN/S1
  #    layers: [unit, api-e2e, ui-e2e]
  #    tests: ["<repo-relative path>::<test name or @T-<DOMAIN>-NNN/S1 tag>"]
  #    result: pass           # pass | fail | blocked | waiting | not-automated
  #    note: null             # failure message + trace / screenshot path, or why blocked / not automated
  blockers: []                # - "<what> (needs: implementing agent | human owner; raised <ISO time>)"
  updated_at: null            # ISO 8601 with offset
  updated_by: null            # test-bot

approvals:                    # required = handoff.require_human_approval at the time of the gate
  plan_to_code:
    required: true
    approved_by: null         # only from the human owner's explicit reply
    approved_at: null
  code_to_review:
    required: false
    approved_by: null
    approved_at: null
  merge:
    required: true            # always; agents never merge
    approved_by: null
    approved_at: null

blockers: []                  # - "<what> (raised by <agent>, <ISO time>)"
---

# Handoff: <Feature name>

> **Now:** `<stage>` · owner `<owner>` · pickup `<pickup>`
> **Next:** <one line, e.g. "The implementing agent builds T-<DOMAIN>-NNN against the C# API + Next.js">

## Summary

<One or two lines: what is being delivered and which pages.>

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs (source of truth) | `specs/<page>.yaml` |
| Excel | `excel/<page>.xlsx` |
| Journeys | `journeys/<journey>.md` |
| Tickets | `tickets/T-<DOMAIN>-NNN-<slug>.md` |
| UI ↔ DB stubs | `stubs/ui-to-db.yaml` |
| Review log | `reviews/review-log.md` |
| Review reports | `reviews/PR-<id>-review.md` / `reviews/DIRECT-<branch-slug>-<n>-review.md` |
| Test plan (testing agent) | `tests/test-plan.md` |
| Test reports / log (testing agent) | `tests/TEST-<feature>-<n>-report.md` / `tests/test-log.md` |

## Notes for the next owner

- <Open questions from plan.md that affect build, decisions the human owner made, anything the next agent must know.>

## History

Append one row per transition or pickup. Newest last. Never edit earlier rows. The owner writes History; the testing agent does not (its runs are in `tests/test-log.md`, and the reviewing agent records each test review here).

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | <ISO time> | — → planned | — → plan-bot | — | plan-bot | Planning complete; tickets ready |
