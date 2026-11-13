# Review: <PR-<id> | DIRECT-<branch-slug>-<n> | DIRECT-<feature>-<n>> — <PR title or feature name>

| Field | Value |
|-------|-------|
| PR / hand-off | <PR-<id> — <PR title> (<link>) \| Direct hand-off — `handoff.md` (round <n>)> |
| Trigger | <pr-opened \| pr-updated \| direct-handoff \| test-report> |
| Review scope | <PR diff \| Plan scope (`direct_scope: plan`) \| Local diff (`direct_scope: diff`)> — details in **Review scope** |
| Source → target | `<source-branch>` → `<target-branch>` \| n/a (plan scope) |
| Provider | <azure-devops \| github \| cursor-origin \| local-git \| n/a (plan scope)> |
| Reviewed commit | `<short-sha>` (iteration <n>) \| per repo where under git, else "not under git" |
| Linked tickets | T-<DOMAIN>-NNN (<where found: title / branch / description>), … |
| Feature(s) | `<feature_path>/` (+ other features, if any) |
| Specs reviewed | `specs/<page>.yaml` (`excel/<page>.xlsx`), … |
| Active API / UI | <`development.api.active`> (`<its path>`) / <`development.ui.active`> (`<its path>`) |
| Rule sets applied | <the active API and UI rule sets, plus general practice only where no rule applies> |
| Reviewer agent | ai-review-framework (<agents.review.name>) |
| Review date | <DD/MM/YYYY HH:MM> (Europe/London) |
| Review iteration | <1> |
| Approvals (source) | <none \| what was approved, by whom, DD/MM/YYYY HH:MM - direct from the human owner \| per <agent name> (relayed)> |

## Verdict

**<Approve | Approve with comments | Request changes>**

| Code verdict | Test verdict | Final |
|--------------|--------------|-------|
| <approve \| approve-with-comments \| request-changes> (provisional until the test review) | <approve \| request-changes \| blocked-noted: "Tests blocked: <reason>" \| not yet> | <final verdict only when both approve, the run is not blocked, and the required unit commands passed; otherwise unset> |

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| <n> | <n> | <n> | <n> |

Severity threshold for Request changes: `<review.severity_threshold>`. Rules: `checklists/severity.md`.

## Summary

<3–6 sentences: what the PR does, what it was checked against, which rule sets applied, main reasons for the verdict.>

## Review scope

How the scope was built: <PR diff from `<provider>` \| Plan scope — started from the `implementation` manifest in `handoff.md` (<n> files), then searched `<api path>` and `<ui path>` for page names, routes, Services, Target DB Tables / Columns, ticket IDs and derived names \| Local diff `git diff <base>...<branch>`>.

| Repo | File | Class | Reason | Tickets / spec items it implements |
|------|------|-------|--------|------------------------------------|
| <api \| ui> | `<repo-relative path>` | <api \| ui \| tests \| migration \| config> | <manifest \| discovered (F-NN, manifest incomplete) \| diff \| dependency> | <T-<DOMAIN>-NNN; page / controls / `Table.Column`> |

- Manifest: <n> files · Discovered (not in manifest): <n> · Diff / dependency: <n>
- Whole files reviewed: <yes (plan scope) \| diff hunks + context (PR / local diff)>
- Round type: <first review \| scoped re-review (open findings + changed files) \| full pass (final round)>
- Not implemented (no file in scope): <none \| control / `Table.Column` → F-NN>
- Deferred by the ticket's out-of-scope list: <none \| item>
- Excluded: outside `review.scope_include` (only API / UI code is reviewed): <none \| files>; `review.scope_exclude` (build output, node_modules, bin / obj, generated, secrets / `.env`) <+ anything else skipped and why>

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-01 | <Blocker \| Major \| Minor \| Nit> | <Spec conformance \| Data mapping \| Acceptance criteria \| API standards \| UI standards \| Security \| Data integrity \| Tests> | `<path>:<line>` | <what is wrong and why it matters> | `<specs/page.yaml → section → control>` / `<rule file → heading>` / `<ticket → Scenario>` | <concrete change> |

## Spec conformance (per control)

Spec: `specs/<page>.yaml` — <Paginated Grid \| Embedded Grid Modal \| Form Modal \| Basic Form \| Wizard Modal \| Full-Page Wizard \| Import> — <page title>

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| <section> | <label> | <spec → code> | <Yes/No ✓/✗> | <Yes/No ✓/✗> | <✓/✗> | <spec → code> | <"exact text" ✓/✗> | <Match \| Mismatch \| Missing \| Extra \| Not in PR \| Not implemented \| Deferred> | <F-NN> |

Grid (Paginated Grid or Embedded Grid Modal, if any): `specs/<page>.yaml`

| Column / action | Population source / action on click | Display format / sortable | Status | Notes / finding |
|-----------------|-------------------------------------|---------------------------|--------|-----------------|
| <title> | `<Table.Column>` / <action> | <format> / <Yes/No> | <Match \| Mismatch \| Missing \| Extra \| Not in PR \| Not implemented \| Deferred> | <F-NN> |

## Data mapping (per control)

| Control | Spec: Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status |
|---------|------------------------------|------------|------------------|--------|---------------------------|-----------|--------|
| <label> | <Service> · `<Table>.<Column>` | `#/properties/<field>` | `<Record>.<Property>` | `<Mapper>:<line>` | `<Entity>.<Property>` | `<migration>` / n/a | <Mapped \| Mismatch \| Unmapped \| Extra \| Not in PR \| Not implemented> |

`Not in PR` applies to the PR route only. On the direct plan scope, an item with no implementing file is `Not implemented` (a finding), or `Deferred` when the ticket's out-of-scope list defers it.

Columns or properties in the reviewed code that are not in any linked spec:

- <none \| `Table.Column` in `<file>:<line>` → F-NN>

## Acceptance criteria coverage (per scenario)

| Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) | Notes |
|-------------|----------|--------|-------------------|-------------------|-------|
| T-<DOMAIN>-NNN/S1 | <name> | <Covered \| Partial \| Missing \| Out of PR scope> | `<file>:<line>` | `<test>` | <F-NN> |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| <a spec rule, e.g. a uniqueness rule> | <Enforced server-side \| Client only \| Not enforced> | `<file>:<line>` / F-NN |

## Tests

| Rule / scenario | Test | Status |
|-----------------|------|--------|
| <rule or T-…/S<n>> | `<TestClass.Method>` / none | <Tested \| Weak \| Untested> |

Execution (required; `skills/review-tests/SKILL.md` step 5). A `not run` or a fail is not a pass:

| Suite | Command | Result |
|-------|---------|--------|
| Active API unit | `<testing.unit for development.api.active>` | <pass \| fail (n) \| not run - reason> |
| Active UI unit | `<npm test, or the UI checklist's unit command>` | <pass \| fail (n) \| not run - reason> |

Suggested tests:

- `<Action>_<Condition>_<Expected>` in `<path>` — <arrange / act / assert in one line>

## Test review

Run <n>: `tests/TEST-<feature>-<n>-report.md` - `testing.status` <passed \| failed \| blocked>, `test_fix_cycle` <n> of 5 \| Not done yet: <reason>

| Check (`skills/review-tests/SKILL.md` **Test review**) | Result | Notes / finding |
|------------------------------------------------------|--------|-----------------|
| Every explicit scenario has a real test tagged with its explicit ID (two tags only if one test fully proves both) | <Pass \| F-NN \| n/a> | |
| Assertions check the Then | <Pass \| F-NN \| n/a> | |
| Nothing skipped, `@fixme` or weakened | <Pass \| F-NN \| n/a> | |
| E1 no front-end mocks; E5 batch reset first in every e2e scenario | <Pass \| F-NN \| n/a> | |
| Unit tests mock only backend boundaries | <Pass \| F-NN \| n/a> | |
| Not automated / Blocked rows have a reason and an owner; flaky reported as flaky, not retried | <Pass \| F-NN \| n/a> | |
| Safety gate shows `api_framework_test` before every reset | <Pass \| F-NN \| n/a> | |
| Password scan: count only, no secrets in reports, traces or logs; `e2e/.auth` not opened | <Pass \| F-NN \| n/a> | |
| Counts agree: report header, Results by ticket, `testing.summary`, `testing.results`, test-log row, per-scenario notes | <Pass \| F-NN \| n/a> | |
| `test_fix_cycle` counted correctly (max 5, separate from `review.cycle`) | <Pass \| F-NN \| n/a> | |
| Pass (partial) / Pass (on intent) notes read | <Pass \| F-NN \| n/a> | |

Routing: <none \| code defects to <agents.code.name> (stage `changes-requested`) \| test defects to the testing agent (stage stays `in-review`) \| test-fix limit reached: escalated to <agents.human.name>>

Checks run: see **Checks run**.

## Checks run

| Check | Command | Where run | Result | Files written / notes |
|-------|---------|-----------|--------|-----------------------|
| <lint \| typecheck \| unit tests \| build \| pre-handoff gate \| live check> | `<command>` | `<project folder>` | <pass \| fail (n) \| not run - reason> | <none \| cache or temp output \| test row created and deleted> |
| Probe (encoding, line endings, redirect sinks) | `node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target <api-framework \| nextjs \| all>` | `ai-framework` root | <pass \| findings (n): bom n / utf8-invalid n / eol-mixed n / open-redirect-sink n> | none (read-only); eol-changed <checked with handed-off baseline \| by diff \| Not verifiable> |
| Redirect guard | `node ai-code-framework/scripts/probe-redirect.mjs --module <guard> --export safeRedirectPath --json` | `ai-framework` root | <pass \| unsafe (n) \| not run - no guard module> | none; module top-level code runs |

Shared editing rules (`loops/pr-review.md` stage 5): encoding <Pass \| F-NN> / line endings <Pass \| F-NN> / targeted edits <Pass \| F-NN> / parked features and other frameworks <Pass \| F-NN> / SHA-256 before and after <Pass \| Not verifiable> / `py tools/check.py` <Pass \| F-NN \| Not applicable>

## Changes since last review

<Iteration 1: n/a. Later iterations: findings resolved, still open, new.>

## Decisions for <agents.human.name>

Open choices only the human owner can make, each with the options and a recommendation.

- <none \| decision - options - recommendation - what it blocks>

## Out of scope / pre-existing notes

These do not affect the verdict.

- <Suspected spec issues for the planning framework (do not block the change on these)>
- <Pre-existing issues in reviewed files that are unrelated to the plan: `<file>:<line>` — what>
- <Files outside the active API / UI codebases>
- <Tooling gaps, e.g. no UI test runner>

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: <Not published — provider does not support posting (provider <cursor-origin \| local-git>) \| Not published — `review.publish.enabled` is false \| Not applicable — direct hand-off \| Published <date> (inline: n, summary: yes/no, GitHub: COMMENT event, vote: none)>. Logged in `reviews/review-log.md` (round <n>).</sub>
