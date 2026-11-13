---
# handoff.md: pipeline state for ONE feature. Rules: handoff/README.md
# Copy to <output.work_dir>/<feature>/handoff.md. Only the current `owner` edits
# this file, except the `testing` section, which the testing agent (test-bot) may
# write while review-bot owns the feature (handoff/README.md -> Testing alongside review). On every transition, update this front matter AND append a row to
# History. Paths are relative to this feature folder unless they start with ai-.
handoff_version: 1
example: false                # true = illustrative only; never picked up
feature: shared-paging
feature_path: ai-planning-framework/work/shared-paging   # output.work_dir/<feature>
stage: in-review              # planned | in-development | in-review | changes-requested | approved | merged
owner: review-bot             # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config; test-bot is never an owner)
pickup: accepted              # pending (handed over, not started) | accepted (owner is working it)
waiting_on: "Test Bot: T-PAGING-007 on PostgreSQL (needs Neil to start local PostgreSQL on localhost:5432, down since the PC restart), then Review Bot test review for the final verdict. Provisional code verdict approve-with-comments (reviews/DIRECT-shared-paging-1-review.md: 0 Major, 1 Minor F-01, 6 Nit). Optional follow-ups: Dev Bot F-01, F-04..F-06; Plan Bot F-02, F-03; 008 Phase 2 after Phase 1 approval (parkable)"
updated_at: 2026-10-09T19:05:00+01:00   # ISO 8601 with offset, e.g. 2026-10-08T10:40:00+01:00
updated_by: review-bot        # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config)
parked: false                 # true = the human owner has paused this feature; read-only for every agent until resumed (handoff/README.md rule 13)
parked_at: null               # ISO 8601 with offset, set when parked
parked_by: null               # human (only the human owner parks or resumes)

routes:                       # the route actually used (from handoff in the config)
  plan_to_code: direct        # devops | direct   (set by the planning agent at hand-off)
  code_to_review: direct      # pr | direct       (set by the implementing agent at hand-off)
  code_to_test: direct        # direct            (set by the implementing agent at the same hand-off; the testing agent runs alongside the review)
  review_feedback: direct     # direct

tickets:                      # every T-<DOMAIN>-NNN in tickets/; id must match the filename
  - id: T-PAGING-001
    file: tickets/T-PAGING-001-api-shared-paging-area.md
    devops_work_item_id: null
  - id: T-PAGING-002
    file: tickets/T-PAGING-002-api-animals-search-and-sort.md
    devops_work_item_id: null
  - id: T-PAGING-003
    file: tickets/T-PAGING-003-api-reference-data-query.md
    devops_work_item_id: null
  - id: T-PAGING-004
    file: tickets/T-PAGING-004-ui-entity-grid-set-filters.md
    devops_work_item_id: null
  - id: T-PAGING-005
    file: tickets/T-PAGING-005-ui-animals-search-box.md
    devops_work_item_id: null
  - id: T-PAGING-006
    file: tickets/T-PAGING-006-rules-paging.md
    devops_work_item_id: null
  - id: T-PAGING-007
    file: tickets/T-PAGING-007-tests-paging-e2e.md
    devops_work_item_id: null
  - id: T-PAGING-008
    file: tickets/T-PAGING-008-phase2-other-lists.md
    devops_work_item_id: null

devops:                       # only when plan_to_code = devops
  board_url: null
  published_at: null

code:                         # set by the implementing agent; repos from development.api/ui active paths
  api:
    repo: ai-code-framework/api/API.Framework
    branch: null              # handoff.branch_pattern; same name in every repo touched. Required for the PR route
                              # and direct_scope: diff; optional for direct_scope: plan (null if not a git repo)
    base_branch: null         # PR target / diff base (review.target_branch unless stated); not used by direct_scope: plan
    head_commit: null         # commit handed to review, when the repo is under git
  ui:
    repo: ai-code-framework/ui/UI.NextJs.Framework
    branch: null
    base_branch: null
    head_commit: null
  build: pass                 # pass | fail
  tests: pass                 # pass | fail  (existing tests and checks the implementing agent ran; scenario test results are in `testing`)
  verification:               # commands run, e.g. "dotnet test ... --filter ...", plus one line per pre-handoff check,
    - "pre-handoff: eol api-framework -> pass (232 files, 0 findings)"
    - "pre-handoff: secrets api-framework -> pass (232 files, 0 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup api-framework -> pass (22 docs, 0 findings, 59 allowlisted)"
    - "pre-handoff: unit api-framework -> pass (127 passed, 0 failed, 0 skipped, 0 findings)"
    - "pre-handoff: lint nextjs -> pass (154 files, 0 errors, 2 warnings, 0 findings)"
    - "pre-handoff: typecheck nextjs -> pass (0 errors, 0 findings)"
    - "pre-handoff: eol nextjs -> pass (236 files, 0 findings)"
    - "pre-handoff: secrets nextjs -> pass (236 files, 2 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup nextjs -> pass (17 docs, 0 findings)"
    - "pre-handoff: unit nextjs -> pass (35 passed, 0 failed, 8 files, 0 findings)"
    - "pre-handoff: api-framework: not a git repo: working tree scanned"
    - "pre-handoff: nextjs: not a git repo: working tree scanned"
                              # e.g. "pre-handoff: lint nextjs -> pass (0 errors, 4 warnings)" (never a secret value)
    - "dotnet build Api.Framework.sln --configuration Release --artifacts-path %TEMP%\\devbot-sp\\artifacts -> pass (0 errors, 5 existing warnings)"
    - "dotnet test Api.Framework.Tests (in place) -> pass (127 passed, 0 failed)"
    - "npm run typecheck / npm run lint / npm test (UI.NextJs.Framework) -> pass (0 errors, 2 existing lint warnings, vitest 35 passed)"
    - "e2e: npx tsc --noEmit -p tsconfig.json + npx bddgen -> pass"
    - "node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs -> pass"
    - "smoke vs own Test API (5189/7189) -> NOT RUN: PostgreSQL on localhost:5432 refused connections after the PC restart (no Postgres service or container running); no migration needed"
  pre_handoff_gate: pass      # pass | fail   result of the LAST pre-handoff run (config `verification`; feature-build stage 5).
                              # in-development / changes-requested -> in-review needs pass
  pre_handoff_gate_at: 2026-10-09T18:52:41+01:00   # ISO 8601 with offset of that run

implementation:               # MANIFEST of what the implementing agent built; the reviewing agent's starting point for direct_scope: plan
  # Filled by the implementing agent at self-review / hand-off. Hand-off is BLOCKED while every list is empty.
  # One entry per file that implements the plan: files created or changed for the feature, plus
  # existing files the feature relies on to render a control or persist a mapping (change: existing).
  # `path` is repo-relative under code.api.repo (api, migrations) or code.ui.repo (ui); tests say which.
  # Never list build output, node_modules, bin/obj, generated files or secret / .env files.
  recorded_at: 2026-10-09T18:52:36+01:00
  api:
    - path: Api.Framework.Services/Paging/PagingContracts.cs
      change: added
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S5]
    - path: Api.Framework.Services/Paging/PagingDefaults.cs
      change: added
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S1]
    - path: Api.Framework.Services/Paging/PageWindow.cs
      change: added
      tickets: [T-PAGING-001, T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S1, T-PAGING-001/S4, T-PAGING-003/S4]
    - path: Api.Framework.Services/Paging/SortMap.cs
      change: added
      tickets: [T-PAGING-001, T-PAGING-002, T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S2, T-PAGING-001/S3, T-PAGING-002/S6, T-PAGING-003/S3, T-PAGING-003/S4]
    - path: Api.Framework.Services/Paging/PagedQueryableExtensions.cs
      change: added
      tickets: [T-PAGING-001, T-PAGING-002, T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S4, T-PAGING-002/S6, T-PAGING-003/S4]
    - path: Api.Framework.Services/Directory/DirectoryContracts.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S5]
    - path: Api.Framework.Services/Animals/AnimalContracts.cs
      change: modified
      tickets: [T-PAGING-002]
      spec_pages: [manage-animals]
      controls: ["Search animals"]
      db: [Animals:Animal.NormalizedName]
      scenarios: [T-PAGING-002/S1, T-PAGING-002/S2, T-PAGING-002/S3, T-PAGING-002/S5]
    - path: Api.Framework.Services/Animals/AnimalService.cs
      change: modified
      tickets: [T-PAGING-002]
      spec_pages: [manage-animals]
      controls: ["Search animals", "Name", "Is Furry", "Has Hooves", "Date Born", "Last Amended"]
      db: [Animals:Animal.Name, Animals:Animal.NormalizedName, Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.DateBorn, Animals:Animal.UpdatedUtc, Animals:Animal.IsDeleted]
      scenarios: [T-PAGING-002/S1, T-PAGING-002/S2, T-PAGING-002/S4, T-PAGING-002/S6]
    - path: Api.Framework.Services/Animals/IAnimalService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework/Controllers/Animals/AnimalController.cs
      change: existing
      tickets: [T-PAGING-002]
      spec_pages: [manage-animals]
      controls: ["Search animals"]
      db: []
      scenarios: [T-PAGING-002/S5]
    - path: Api.Framework.Data/Models/Animal.cs
      change: existing
      tickets: [T-PAGING-002]
      spec_pages: [manage-animals]
      controls: ["Search animals"]
      db: [Animals:Animal.NormalizedName]
      scenarios: [T-PAGING-002/S1]
    - path: Api.Framework.Services/ReferenceData/ReferenceDataContracts.cs
      change: modified
      tickets: [T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-003/S1, T-PAGING-003/S2, T-PAGING-003/S5]
    - path: Api.Framework.Services/ReferenceData/ReferenceDataService.cs
      change: modified
      tickets: [T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-003/S1, T-PAGING-003/S2, T-PAGING-003/S3, T-PAGING-003/S4]
    - path: Api.Framework/Controllers/ReferenceData/ReferenceDataController.cs
      change: modified
      tickets: [T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-003/S5]
    - path: Api.Framework/Controllers/Directory/DirectoryControllers.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework/Controllers/Directory/TenantController.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework/Controllers/Examples/ComponentShowcaseController.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Directory/DirectoryService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Directory/IDirectoryService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Directory/ITenantService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Directory/TenantService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Examples/CatalogueContracts.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Examples/CatalogueItemService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Examples/ComponentShowcaseService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Examples/ICatalogueItemService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Examples/IComponentShowcaseService.cs
      change: modified
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: .cursor/rules/api-framework-services.mdc
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1, T-PAGING-006/S2]
    - path: .claude/rules/api-framework-services.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1, T-PAGING-006/S2]
    - path: .cursor/rules/api-framework-controllers.mdc
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .claude/rules/api-framework-controllers.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .cursor/rules/api-framework-ui-contract.mdc
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .claude/rules/api-framework-ui-contract.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .cursor/rules/api-framework-testing.mdc
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .claude/rules/api-framework-testing.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .cursor/skills/api-framework-entity-list/SKILL.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
    - path: .claude/skills/api-framework-entity-list/SKILL.md
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S1]
  ui:
    - path: src/framework/entity-framework/hooks/use-entity-grid-state.ts
      change: modified
      tickets: [T-PAGING-004, T-PAGING-005]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S1, T-PAGING-004/S2, T-PAGING-004/S3, T-PAGING-005/S3, T-PAGING-005/S4]
    - path: src/framework/entity-framework/hooks/use-entity-search-state.ts
      change: existing
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S3]
    - path: src/framework/entity-framework/grid/entity-grid-config.ts
      change: modified
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S4]
    - path: src/framework/entity-framework/index.ts
      change: modified
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S4]
    - path: src/framework/entity-framework/components/entity-grid/EntityGrid.tsx
      change: existing
      tickets: [T-PAGING-005]
      spec_pages: [manage-animals]
      controls: ["Search animals", "+ Add Animal"]
      db: []
      scenarios: [T-PAGING-005/S2]
    - path: src/framework/entity-framework/utils/normalize-paged-search-response.ts
      change: existing
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: src/features/reference-data/reference-data-types-grid/ReferenceDataTypesGrid.tsx
      change: modified
      tickets: [T-PAGING-004, T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S1, T-PAGING-004/S2]
    - path: src/features/animals/manage-animals/AnimalsGrid.tsx
      change: modified
      tickets: [T-PAGING-005]
      spec_pages: [manage-animals]
      controls: ["Search animals"]
      db: [Animals:Animal.NormalizedName]
      scenarios: [T-PAGING-005/S1, T-PAGING-005/S2, T-PAGING-005/S3, T-PAGING-005/S4, T-PAGING-005/S5]
    - path: src/features/animals/manage-animals/state/animals-search.data-provider.ts
      change: modified
      tickets: [T-PAGING-005]
      spec_pages: [manage-animals]
      controls: ["Search animals"]
      db: []
      scenarios: [T-PAGING-005/S1]
    - path: src/features/animals/manage-animals/use-animals-grid.tsx
      change: existing
      tickets: [T-PAGING-005]
      spec_pages: [manage-animals]
      controls: ["+ Add Animal"]
      db: []
      scenarios: [T-PAGING-005/S2, T-PAGING-005/S4]
    - path: src/features/test-harness/ComponentTestHarness.tsx
      change: modified
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: .cursor/rules/framework/nextjs-entity-grid.mdc
      change: modified
      tickets: [T-PAGING-006]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-006/S3]
  tests:                   # test SCAFFOLDING the implementing agent owns: Api.Framework.Tests project, Playwright / e2e setup, test-data fixtures. Scenario tests are recorded by the testing agent in testing.results
    - path: Api.Framework.Tests/Paging/PageWindowTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S1, T-PAGING-001/S4]
    - path: Api.Framework.Tests/Paging/SortMapTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S2, T-PAGING-001/S3]
    - path: Api.Framework.Tests/Paging/PagedBodyTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-001/S4, T-PAGING-001/S5]
    - path: Api.Framework.Tests/Animals/AnimalServiceSearchTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-002]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-002/S1, T-PAGING-002/S2, T-PAGING-002/S3, T-PAGING-002/S4, T-PAGING-002/S5, T-PAGING-002/S6]
    - path: Api.Framework.Tests/Animals/AnimalSearchSqlTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-002]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-002/S3]
    - path: Api.Framework.Tests/ReferenceData/ReferenceDataQueryTests.cs
      repo: api
      change: added
      tickets: [T-PAGING-003]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-003/S1, T-PAGING-003/S2, T-PAGING-003/S3, T-PAGING-003/S4, T-PAGING-003/S5]
    - path: src/framework/entity-framework/hooks/use-entity-grid-state.test.tsx
      repo: ui
      change: added
      tickets: [T-PAGING-004]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-004/S1, T-PAGING-004/S2, T-PAGING-004/S3, T-PAGING-004/S4]
    - path: src/features/animals/manage-animals/AnimalsGrid.test.tsx
      repo: ui
      change: added
      tickets: [T-PAGING-005]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-PAGING-005/S1, T-PAGING-005/S2, T-PAGING-005/S5]
  migrations: []          # none: Animal.NormalizedName already exists (plan.md §2); no entity or DbContext change
  # Entry shape (copy into the lists above):
  #  - path: Unity.API/Controllers/V2/<Name>Controller.cs
  #    repo: api               # api | ui  (tests only; api / migrations are always api, ui is ui)
  #    change: added           # added | modified | existing
  #    tickets: [T-<DOMAIN>-NNN]
  #    spec_pages: [<page>]    # specs/<page>.yaml
  #    controls: [<label>]     # spec control labels, manage-list columns or actions
  #    db: [<Service>:<Table>.<Column>]   # spec Service / Target DB Table / Target DB Column (or Population Source)
  #    scenarios: [T-<DOMAIN>-NNN/S1]     # mainly for tests

pull_requests: []             # when code_to_review = pr; one entry per repo
#  - repo: ai-code-framework/api/Unity.API
#    id: 1234
#    url: https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/1234
#    source_branch: feat/T-CONTACT-001/add-edit-contact
#    target_branch: <review.target_branch>

review:
  cycle: 0                    # +1 each time a code-review round ends with a final verdict or a change request (max handoff.max_review_cycles).
                              # Test-fix rounds do NOT count here (testing.failures_count_toward_review_cycles: false); see testing.test_fix_cycle
  report: reviews/DIRECT-shared-paging-1-review.md   # latest full report: reviews/PR-<id>-review.md | reviews/DIRECT-<branch-slug>-<n>-review.md
  log: reviews/review-log.md  # reviews/review-log.md (review.log_file); every code review and test review, both routes
  code_verdict: approve-with-comments   # PROVISIONAL code-review verdict until the test review: approve | approve-with-comments | request-changes
  test_verdict: null          # test review (testing.test_review): approve | request-changes | blocked-noted (testing blocked, approval allowed by default (2))
  verdict: null               # FINAL: approve | approve-with-comments only when testing.final_approval_requires are all met; request-changes otherwise
  routed_to: null             # who fixes the latest findings: code | testing | both (testing.defect_routing)
  reviewed_commits: {api: "not under git", ui: "not under git"}   # repo -> commit reviewed

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
    approved_by: human        # only from the human owner's explicit reply (Neil in chat, 2026-10-09 14:47 BST)
    approved_at: 2026-10-09T14:47:00+01:00
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

# Handoff: Shared paging

> **Now:** `in-review` · owner `review-bot` · pickup `accepted` · code review round 1 done 2026-10-09 19:05 BST: provisional **Approve with comments** (0 Major, 1 Minor, 6 Nit); waiting on Test Bot T-PAGING-007 (PostgreSQL down)
> **Next:** Review Bot reviews T-PAGING-001..006 (direct, plan scope); Test Bot runs T-PAGING-007 alongside on PostgreSQL; T-PAGING-008 after Phase 1 approval (parkable).

## Summary

One shared `Paging/` area in API.Framework (contracts, defaults, page window, whitelisted sort map with Id tie-break, paged-body helpers), typed queries with filters, and a debounced, page-1-resetting `setFilters` in the Next.js entity grid. Phase 1: Animals Name search (manage-animals decision 31) and the ReferenceData Types search fix. Phase 2 (parkable): Directory, Tenant, CatalogueItem, ComponentShowcase.

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs (source of truth) | `ai-planning-framework/work/manage-animals/specs/manage-animals.yaml` (search_filters) |
| Excel | `ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx` |
| Tickets | `tickets/T-PAGING-001` … `T-PAGING-008` |
| Review log | `reviews/review-log.md` |
| Test plan / reports (testing agent) | `tests/test-plan.md` / `tests/TEST-shared-paging-<n>-report.md` |

## Notes for the next owner

- Approved by Neil 2026-10-09 14:47 BST; all 15 answers accepted (plan.md §6 P5–P19).
- Start condition met: system-rename merged on Neil's word at 14:47 BST (plan.md §8).
- ReferenceData UI already resets to page 1; the fix is the API (`SearchText`) and the debounce (plan.md §2).
- Unity.API `ToPagedList` / Contacts: heads-up only, no ticket (Q10).
- Dev Bot 2026-10-09: no migration (`Animal.NormalizedName` already exists). P18: `normalizePagedSearchResponse` NOT trimmed: the parked add-edit-contact (example) plans a Manage Contacts grid in UI.NextJs.Framework against Unity.API Contacts, whose paging shape differs.
- Animals sort: non-name keys sort ties by Name ascending, then Id (SortMap `.ThenBy`; Neil's agreed design). T-PAGING-002/S6 reads "DateBorn descending then Id": with the Name secondary the order is DateBorn desc, then Name, then Id. Plan Bot may want to reword S6.
- Npgsql turns the search into `normalized_name LIKE @p` with `%`, `_` and `\` escaped by the provider (unit test `AnimalSearchSqlTests`), so they match literally; to be proven on PostgreSQL in T-PAGING-007.
- Search boxes for e2e: Animals `[data-tid="animals-search"]` (placeholder "Search animals…", aria-label "Search animals", maxLength 100); Reference Data `[data-tid="reference-data-search"]` (now maxLength 100). Debounce 300 ms (`filterDebounceMs`), one request, pageIndex 0, sort and page size kept. API params: `search` on `GET Animal`, `searchText` on `GET ReferenceData`.
- Smoke test against a Dev Bot Test API (5189/7189) was NOT run: local PostgreSQL (localhost:5432) refused connections after the PC restart and no Postgres service or container was running. Neil needs to start it before T-PAGING-007.
- The Reference Data Types grid still keeps search / page / sort in the URL (existing `useAuthenticatedEntitySearch`; plan §2 said no grid does). Unchanged here (P2: API + debounce fix only).

## History

Append one row per transition or pickup. Newest last. Never edit earlier rows. The owner writes History; the testing agent does not (its runs are in `tests/test-log.md`, and the reviewing agent records each test review here).

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | 2026-10-09T14:00:18+01:00 | — → planned | — → plan-bot | — | plan-bot | Planned from Dev Bot's design (Neil 2026-10-09 13:53 BST). Spot-check done (plan.md §2; one claim corrected: ReferenceData UI already resets to page 1). Tickets T-PAGING-001…008; manage-animals spec search_filters + Excel updated and decision 31 added. NOT approved; parked false; waiting on Neil for §7 Q1–Q15 and plan_to_code; start after system-rename is merged |
| 2 | 2026-10-09T15:58:57+01:00 | planned (unchanged) | plan-bot → dev-bot | plan_to_code · direct | plan-bot | Neil 2026-10-09 14:47 BST: all 15 suggested answers accepted (plan.md §6 P5–P19, §7 marked answered) and plan approved (approvals.plan_to_code human 14:47). system-rename treated as merged 14:47, so the start-condition blocker is cleared. Ticket notes and the manage-animals spec comments no longer say "defaults pending"; spec display text unchanged, so the xlsx is not regenerated. Dev Bot builds T-PAGING-001..006; Test Bot 007; 008 Phase 2 after Phase 1 approval (parkable) |
| 3 | 2026-10-09T16:16:00+01:00 | planned → in-development | dev-bot | plan_to_code · direct (approved 14:47) | dev-bot | Picked up (pickup: accepted). Plan Bot handed over with owner dev-bot / pickup pending and approvals.plan_to_code recorded but left stage `planned`; set `in-development` on acceptance (same as pre-handoff-checks / system-rename). Design check against Dev Bot's agreed design done: no contradictions. Building T-PAGING-001..006 in plan order; 007 is Test Bot's; 008 not started (Phase 2, after Phase 1 approval) |
| 4 | 2026-10-09T18:54:00+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review · direct; code_to_test · direct (option B); pre-handoff gate pass (2026-10-09T18:52:41+01:00) | dev-bot | T-PAGING-001..006 built (008 not started; 007 Test Bot). Shared Paging/ area (contracts moved from Directory with the same names and JSON, PagingDefaults 20/200, PageWindow adjusts, SortMap with case-insensitive keys, fallback, per-key ThenBy and final Id tie-break, ToPagedBodyAsync / ToPagedBody); AnimalQuery.Search (StringLength 100, NormalizedName contains) and SortMap (non-name keys then Name then Id); ReferenceDataQuery.SearchText on Types (type key or display name) plus Types / Items sort maps, private window and Reverse() removed; UI setFilters (300 ms debounce, page 1, latest response wins), maxPageSize 200, Types grid debounced, Animals search box animals-search; rules in .cursor + .claude (+ entity-list skill) and nextjs-entity-grid. No migration. P18: normalizePagedSearchResponse kept. Manifest api 36 / ui 12 / tests 8 / migrations 0. Api.Framework.Tests 127 pass, vitest 35 pass, e2e tsc + bddgen ok, gate selftest ok. Smoke NOT run (local PostgreSQL down after the PC restart). Interrupted 16:25-18:48 BST (PC offline); state re-checked, nothing half-written |
| 5 | 2026-10-09T19:05:00+01:00 | in-review (unchanged) | review-bot (unchanged) | pickup + code review · direct (option B); provisional code verdict | review-bot | Picked up (pickup: accepted). Code review round 1 (direct_scope: plan, 56 manifest files vs Dev Bot's pre-edit originals and the 11:20 backup): provisional **Approve with comments**; test_verdict / verdict null until T-PAGING-007 and the test review. PagedQuery / PagingModel / PagedBody moved with identical members (JSON pinned by JsonShape_IsUnchanged; no CustomSchemaIds); PageWindow adjusts (0/neg → 20, >200 → 200, neg index → 0, Skip saturates); SortMap typed whitelist, case-insensitive, unknown → default, desc only on "desc", ascending secondary + final Id; Animals search NormalizedName contains → Npgsql parameterised LIKE with % and _ escaped (model-only SQL test); ReferenceData Types SearchText, Reverse() gone; UI setFilters 300 ms / page 1 / latest wins; Animals box matches decision 31; manage-animals grid behaviours untouched; P18 normalizer kept (live, add-edit-contact reason holds). Gate on a copy 18:59 and in place check-only 19:01: pass (API 127/127, vitest 35/35); self-test 64/64; no unit test needs PostgreSQL. Findings: F-01 Minor (SystemUiCorsTests .sln walk-up fails with an out-of-tree output, reproduced 125/2; interacts with system-rename F-15), F-02..F-07 Nit, F-08 note. Not verified live: PostgreSQL, Test API and UIs down (nothing started). Nothing routed; no sign-in; no .env* opened; testing: untouched |
