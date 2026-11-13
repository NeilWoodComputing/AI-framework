# Journey: {{journey_id}} — {{title}}

| Field | Value |
|-------|--------|
| Actor | {{actor}} |
| Goal | {{goal}} |
| Trigger | {{trigger}} |
| Primary pages | {{page_titles}} |
| Source specs | {{spec_paths}} |

## Happy path

1. **{{step_name}}** — Page: {{page}} / {{wizard_step_or_action}}
   - UI: {{controls_or_columns}}
   - Data: Service `{{service}}` → `{{table}}.{{column_or_source}}`
   - Outcome: {{outcome}}

2. …

## Alternate paths

- **Validation failure:** {{message_from_spec}}
- **Cancel / close:** {{behaviour}}
- **Authorisation denied:** {{behaviour}}

## Done when

- [ ] {{acceptance_1}}
- [ ] Persisted fields match Target DB Column / Population Source in the Excel spec
