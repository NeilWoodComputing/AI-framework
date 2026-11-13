---
# EXAMPLE ONLY. This file shows what a filled handoff.md looks like for the
# sample add-edit-contact feature. No approval, build or review has happened.
# `example: true` means no agent picks it up. Rules: handoff/README.md
handoff_version: 1
example: true                 # illustrative only; never picked up
feature: add-edit-contact
feature_path: ai-planning-framework/work/add-edit-contact
stage: in-development
owner: human                  # PARKED by Neil 2026-10-09 11:20 (was dev-bot); stage kept (rule 13)
pickup: pending               # handed to Dev Bot; Dev Bot has not started
waiting_on: "PARKED by Neil 2026-10-09 11:20; resume only on Neil's go-ahead"
updated_at: 2026-10-09T12:34:13+01:00
updated_by: plan-bot           # on Neil's instruction
parked: true                  # handoff/README.md rule 13: read-only for every agent until Neil resumes it
parked_at: 2026-10-09T11:20:00+01:00
parked_by: human

routes:
  plan_to_code: direct        # tickets.enabled is false, so no board
  code_to_review: null        # Dev Bot sets this at hand-off (default direct); Review Bot then reviews automatically
  review_feedback: direct

tickets:
  - id: T-CONTACT-001
    file: tickets/T-CONTACT-001-add-edit-contact.md
    devops_work_item_id: null
  - id: T-CONTACT-002
    file: tickets/T-CONTACT-002-manage-contacts.md
    devops_work_item_id: null

devops:
  board_url: null
  published_at: null

code:
  api:
    repo: ai-code-framework/api/Unity.API
    branch: null              # Dev Bot: feat/T-CONTACT-001/add-edit-contact (handoff.branch_pattern.direct)
    base_branch: null
    head_commit: null
  ui:
    repo: ai-code-framework/ui/UI.NextJs.Framework
    branch: null
    base_branch: null
    head_commit: null
  build: null
  tests: null
  verification: []

implementation:
  # EXAMPLE ENTRIES ONLY: illustrative of the manifest Dev Bot records at self-review /
  # hand-off. Nothing has been built; these files do not exist. In a real file at this
  # stage (pickup: pending) the lists would still be empty.
  recorded_at: null
  api:
    - path: Unity.API/Controllers/V2/ContactsController.cs
      change: added
      tickets: [T-CONTACT-001, T-CONTACT-002]
      spec_pages: [add-edit-contact, manage-contacts]
      controls: [Name, Job Title / Department, Email Address, Telephone, Organisation, Primary Contact, Active, Last Amended, + Add Contact, View / Edit / Delete]
      db: ["Contacts:Contact.Name", "Contacts:Contact.JobTitleDepartment", "Contacts:Contact.EmailAddress", "Contacts:Contact.Telephone", "Contacts:Contact.OrganisationId", "Contacts:Contact.PrimaryContact", "Contacts:Contact.IsActive", "Contacts:Contact.LastAmendedOn", "Contacts:Contact.LastAmendedBy"]
    - path: Unity.API/Mapping/ContactMapper.cs
      change: added
      tickets: [T-CONTACT-001, T-CONTACT-002]
      spec_pages: [add-edit-contact, manage-contacts]
      controls: [Name, Job Title / Department, Email Address, Telephone, Organisation, Primary Contact, Active]
      db: ["Contacts:Contact.Name", "Contacts:Contact.JobTitleDepartment", "Contacts:Contact.EmailAddress", "Contacts:Contact.Telephone", "Contacts:Contact.OrganisationId", "Contacts:Contact.PrimaryContact", "Contacts:Contact.IsActive"]
    - path: Unity.Entities/Records/ContactRecord.cs
      change: added
      tickets: [T-CONTACT-001]
      spec_pages: [add-edit-contact]
      controls: [Name, Job Title / Department, Email Address, Telephone, Organisation, Primary Contact, Active]
      db: ["Contacts:Contact.Name", "Contacts:Contact.JobTitleDepartment", "Contacts:Contact.EmailAddress", "Contacts:Contact.Telephone", "Contacts:Contact.OrganisationId", "Contacts:Contact.PrimaryContact", "Contacts:Contact.IsActive"]
  ui:
    - path: src/features/contacts/add-edit-contact-form/AddEditContactForm.tsx
      change: added
      tickets: [T-CONTACT-001]
      spec_pages: [add-edit-contact]
      controls: [Name, Job Title / Department, Email Address, Telephone, Organisation, Primary Contact, Active]
      db: []
    - path: src/features/contacts/manage-contacts-grid/ManageContactsGrid.tsx
      change: added
      tickets: [T-CONTACT-002]
      spec_pages: [manage-contacts]
      controls: [Name, Job Title / Department, Primary Contact, Active, Last Amended, + Add Contact, View / Edit / Delete]
      db: []
    - path: src/config/api-routes.ts
      change: modified
      tickets: [T-CONTACT-001, T-CONTACT-002]
      spec_pages: [add-edit-contact, manage-contacts]
      controls: []
      db: []
  tests:
    - path: Unity.API.Tests/Controllers/ContactsControllerTests.cs
      repo: api
      change: added
      tickets: [T-CONTACT-001, T-CONTACT-002]
      scenarios: [T-CONTACT-001/S1, T-CONTACT-001/S2, T-CONTACT-001/S3, T-CONTACT-001/S5]
  migrations: []              # Contact is owned by the downstream Contacts service, not UnityContext, so no migration

pull_requests: []

review:
  cycle: 0
  report: null                # first round: reviews/DIRECT-feat-T-CONTACT-001-add-edit-contact-1-review.md (DIRECT-add-edit-contact-1-review.md if no branch)
  log: null                   # reviews/review-log.md, created on the first review round
  verdict: null
  reviewed_commits: {}

approvals:
  plan_to_code:
    required: true
    approved_by: Neil Wood (example)
    approved_at: 2026-10-08T10:00:00+01:00
  code_to_review:
    required: false
    approved_by: null
    approved_at: null
  merge:
    required: true
    approved_by: null
    approved_at: null

blockers: []                  # ad-hoc 'parked' blocker removed: parked: true replaces it (rule 13)
---

# Handoff: Add | Edit Contact

> **EXAMPLE.** Illustrative only, to show the format. Nothing below has actually been approved, built or reviewed.

> **Now:** `in-development` · owner `human` · pickup `pending` · **PARKED by Neil 2026-10-09 11:20; resume only on Neil's go-ahead**
> **Next:** Dev Bot builds T-CONTACT-001 and T-CONTACT-002 against Unity.API + Next.js, then messages Review Bot (`direct`), which reviews automatically and logs to `reviews/review-log.md`.

## Summary

Manage Contacts list modal plus an Add | Edit | View Contact Basic Form. Every field is persisted through the **Contacts** service to the **Contact** table.

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs (source of truth) | `specs/add-edit-contact.yaml`, `specs/manage-contacts.yaml` |
| Excel | `excel/add-edit-contact.xlsx`, `excel/manage-contacts.xlsx` |
| Journeys | `journeys/j-contact-add-edit.md` |
| Tickets | `tickets/T-CONTACT-001-add-edit-contact.md`, `tickets/T-CONTACT-002-manage-contacts.md` |
| UI ↔ DB stubs | `stubs/ui-to-db.yaml` |
| Review log | `reviews/review-log.md` (none yet; created on the first review round) |
| Review reports | `reviews/DIRECT-<branch-slug>-<n>-review.md` or `DIRECT-add-edit-contact-<n>-review.md` (none yet) |

## Notes for the next owner

- Open questions in `plan.md`: defaults on Add are assumed Active = true, Primary Contact = false; soft-delete confirmation copy is still to be confirmed.
- Only one Primary Contact per organisation: enforce it server-side (T-CONTACT-001, scenario "Setting Primary Contact clears the previous primary").
- Organisation is pre-populated from the Manage Contacts parent and is read-only on the form.
- Hand-off to Review Bot is `direct` with `review.direct_scope: plan`: fill in `implementation` (every file that implements the plan), use branch `feat/T-CONTACT-001/add-edit-contact` in Unity.API and record its head commit, then message Review Bot. Review Bot reviews all code relevant to the plan; the review starts on that message and nobody needs to ask for it.
- `UI.NextJs.Framework` is not a git repo yet. That is fine for this route: plan-scope reviews do not need git. Leave `code.ui.branch` null and list the UI files in the manifest. It only becomes a blocker if the route changes to `pr` or `direct_scope: diff`.

## History

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | 2026-10-08T09:50:00+01:00 | — → planned | — → plan-bot | — | plan-bot | Planning complete: 2 specs, 2 workbooks, 1 journey, 2 tickets, stubs |
| 2 | 2026-10-08T09:52:00+01:00 | planned | plan-bot → human | gate plan_to_code | plan-bot | Asked Neil to approve plan and tickets for hand-off |
| 3 | 2026-10-08T10:00:00+01:00 | planned | human → plan-bot | gate plan_to_code approved | human | Neil approved (example) |
| 4 | 2026-10-08T10:05:00+01:00 | planned → in-development | plan-bot → dev-bot | plan_to_code: direct | plan-bot | Messaged Dev Bot with the feature path |
| 5 | 2026-10-09T11:23:17+01:00 | in-development (unchanged) | dev-bot → human | — (parked) | plan-bot | PARKED by Neil 2026-10-09 11:20; resume only on Neil's go-ahead. No parked convention in handoff/README.md or the template, so stage kept, owner human, waiting_on set, blocker 'parked' added |
| 6 | 2026-10-09T12:34:13+01:00 | in-development (unchanged) | human (unchanged) | — (parked flag) | plan-bot | Converted to the new parked flag (handoff/README.md rule 13, Neil 2026-10-09 11:47): parked: true, parked_at 2026-10-09T11:20:00+01:00, parked_by human; owner human and waiting_on kept; ad-hoc 'parked' blocker removed as redundant |
