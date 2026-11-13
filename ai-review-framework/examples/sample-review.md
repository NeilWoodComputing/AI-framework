> **Illustrative example only.** A shortened report for a hypothetical direct hand-off of the Library sample "Add | Edit Book" (`templates/yaml/form-modal-sample.yaml` in the planning framework). The files, line numbers and finding are invented to show the shape of `templates/review-report.md`. Nothing here describes code in `ai-code-framework/`.

# Review: DIRECT-add-edit-book-1 — Add | Edit Book

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 1) |
| Trigger | direct-handoff |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git |
| Linked tickets | T-BOOK-001 |
| Feature(s) | `ai-planning-framework/work/add-edit-book/` |
| Specs reviewed | `specs/add-edit-book.yaml` |
| Active API / UI | api-framework / nextjs |
| Rule sets applied | API.Framework `.cursor/rules` + Next.js `.cursor/rules` |
| Reviewer agent | ai-review-framework (the reviewing agent) |
| Review date | 11/11/2026 10:00 (Europe/London) |
| Review iteration | 1 |
| Approvals (source) | none |

## Verdict

**Request changes**

| Code verdict | Test verdict | Final |
|--------------|--------------|-------|
| request-changes (provisional until the test review) | not yet | not yet |

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 1 | 0 | 0 | 0 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`.

## Summary

The form renders the Title control and saves it through the Catalogue service. Title is specified as `Book.Title` and the entity persists `Book.Name`, so the mapping is wrong. That is a Blocker.

## Review scope

How the scope was built: Plan scope — started from the `implementation` manifest in `handoff.md` (2 files).

| Repo | File | Class | Reason | Tickets / spec items it implements |
|------|------|-------|--------|------------------------------------|
| ui | `src/features/catalogue/add-edit-book/ui-schemas/book.ui-schema.json` | ui | manifest | T-BOOK-001; Title |
| api | `Api.Framework.Data/Models/Book.cs` | api | manifest | T-BOOK-001; Book.Title |

- Manifest: 2 files · Discovered: 0
- Whole files reviewed: yes (plan scope)
- Round type: first review
- Not implemented: none
- Excluded: none

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-01 | Blocker | Data mapping | `Api.Framework.Data/Models/Book.cs:12` | The stored column is `Name`. The spec says `Book.Title`. | `specs/add-edit-book.yaml` → Title → `Book.Title` | Persist Title on `Book.Title` and map the record property to that column. |

## Spec conformance (per control)

Spec: `specs/add-edit-book.yaml` — Form Modal — Add | Edit Book

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| Details | Title | Keyed Input → text | Yes ✓ | Yes ✓ | ✓ | 1–200 ✓ | "Enter a title" ✓ | Match | |

## Data mapping (per control)

| Control | Spec: Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status |
|---------|------------------------------|------------|------------------|--------|---------------------------|-----------|--------|
| Title | Catalogue · `Book.Title` | `#/properties/title` | `BookRecord.Title` | n/a (no downstream mapper) | `Book.Name` | none | Mismatch |

## Acceptance criteria coverage (per scenario)

| Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) | Notes |
|-------------|----------|--------|-------------------|-------------------|-------|
| T-BOOK-001/S1 | Title is saved | Missing | | none | F-01 |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| Title is mandatory | Enforced server-side | schema `required` |

## Tests

| Rule / scenario | Test | Status |
|-----------------|------|--------|
| T-BOOK-001/S1 | none | Untested |

Execution:

| Suite | Command | Result |
|-------|---------|--------|
| Active API unit | `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release` | not run - example |
| Active UI unit | `npm test` | not run - example |

A `not run` here withholds final approval on its own. This example is already Request changes because of F-01.

## Test review

Not done yet: no test report. A claimed scenario with no executed test would be request-changes once that review runs.

## Checks run

| Check | Command | Where run | Result | Files written / notes |
|-------|---------|-----------|--------|-----------------------|
| API unit tests | `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release` | API.Framework | not run - example | none |
| UI unit tests | `npm test` | UI.NextJs.Framework | not run - example | none |

## Changes since last review

Iteration 1: n/a.

## Decisions for the human owner

- none

## Out of scope / pre-existing notes

- none

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (round 1).</sub>
