# Ticket: {{ticket_id}} — {{title}}

<!--
Stable ID rules (required):
- ticket_id format: T-<DOMAIN>-NNN  e.g. T-BOOK-001
- Filename: T-<DOMAIN>-NNN-<short-slug>.md  e.g. T-BOOK-001-add-edit-book.md
- Heading ID must match the filename prefix.
- Upsert: when regenerating or publishing to the ticket tracker (tickets.target), update by this ID — never create a duplicate for the same T-<DOMAIN>-NNN.
- Do not invent Service / Target DB Table / Target DB Column values; copy only from linked specs/excel.
-->

| Field | Value |
|-------|--------|
| ID | {{ticket_id}} |
| Type | Schema / Service API / UI page / Page (Paginated Grid) / Paginated grid / Manage list / Cross-cutting |
| Feature | {{feature}} |
| Priority | {{priority}} |
| Specs | {{spec_paths}} |
| Journey (optional) | {{journey_id}} |

## User story

**As a** {{persona}}  
**I want** {{capability}}  
**So that** {{benefit}}

## Full-stack scope

List every field in scope with mapping (**only** values present in the YAML/Excel specs):

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| {{label}} | {{control_type}} | {{service}} | {{table}} | {{column}} |

## Work to do

1. {{task_1}}
2. {{task_2}}

## Acceptance criteria

Use Given / When / Then (And optional). Prefer one scenario block per behaviour. Every heading has an explicit ID `S<n>` (full ID `{{ticket_id}}/S<n>`) that tests are tagged with. Never renumber or reuse an ID; a moved scenario notes `(was <ticket>/S<n>)` (`skills/generate-tickets/SKILL.md` → Scenario IDs).

### Scenario: S1 — {{scenario_1_name}}

```gherkin
Given {{precondition_1}}
And {{precondition_2}}
When {{action}}
Then {{ui_or_api_outcome}}
And {{persistence_outcome_naming_Service_Table_Column}}
```

### Scenario: S2 — {{scenario_2_name}}

```gherkin
Given {{precondition}}
When {{action}}
Then {{validation_or_enablement_outcome}}
And data is not written via {{service}} to {{table}}.{{column}}
```

### Scenario: S3 — {{scenario_3_name}}

```gherkin
Given {{precondition}}
When {{action}}
Then {{outcome}}
And {{optional_and}}
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel control row (enablement, mandatory, validation message)
- [ ] Data read/written via `{{service}}` to `{{table}}.{{column}}` as asserted in Then/And
- [ ] Implementation stays framework-agnostic unless the repo already standardises a stack

## Out of scope

- {{out_of_scope}}

## Notes

- Stable ID for tracker upsert: `{{ticket_id}}`
- {{notes}}
