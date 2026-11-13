# Skill: plan-tests-from-tickets

Turn the feature's ticket scenarios into a test plan with one traceable test per Given / When / Then.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `tickets` | Yes | `tickets/T-<DOMAIN>-NNN-*.md` — `### Scenario: S<n> — <title>` blocks (explicit IDs) and Work to do |
| `specs` | Yes | `specs/*.yaml` — controls, mandatory flags, validation messages, mappings |
| `plan` | Yes | `plan.md` — decisions and out-of-scope list |
| `handoff` | Yes | `implementation` manifest (what was built, where) |

## Steps

1. **Read the explicit scenario IDs** (`testing.scenario_ids: explicit`). For each ticket, take the ID from each heading `### Scenario: S<n> — <title>`: the `S<n>` straight after `Scenario:`, then a separator (em dash `—`, en dash `–` or hyphen `-`; an optional `(was …)` note may sit between the ID and the separator, for example `### Scenario: S2 (was T-ANIMAL-003 S10) — …`). The reference is `T-<DOMAIN>-NNN/S<n>` (the same form as `handoff.md` `testing.results`, the manifest `scenarios` and the review report).
   - **Never invent numbers from heading order.** A ticket's IDs are whatever its headings say; they are never renumbered.
   - **Gaps are fine** (for example T-ANIMAL-003 has S2–S9 then S12–S15 because S1, S10 and S11 moved to T-ANIMAL-008). Plan only the IDs that are there.
   - **`(was …)` notes are fine.** Keep the note in the plan's Title column so old references can be traced; tag the test with the new ID only.
   - **A ticket with no explicit `S<n>` IDs** (headings like `### Scenario: Create animal with valid fields`) is **Blocked — scenario IDs not frozen**. List its scenarios by title for reference with no ID, mark them Blocked, raise it with the planning agent (`agents.planning.name`, today Plan Bot), and do not write tests for them until the IDs are frozen.
   - **A heading you cannot read cleanly** (for example a garbled separator from an encoding problem) still counts if `S<n>` follows `Scenario:`; flag the ticket to the planning agent.
2. **Pick the layer** for each scenario:
   - **Unit** — service / API behaviour with no UI step: validation messages, uniqueness, soft delete, audit fields, policies, mappers.
   - **API e2e** — a service / API scenario with no UI step, run through the real API with Playwright's `request` fixture (status codes, policies, persisted values the API returns). Use it as well as, or instead of, a blocked unit test.
   - **UI e2e** — any scenario with a user step ("I open", "I click", "I see").
   - **Several layers** — a scenario whose Then also asserts persisted columns: e2e for what the user sees and what the API returns; unit for columns the API does not expose (for example `NormalizedName`, `IsDeleted`).
   - **Covered by `<ticket>/S<n>`** — only when another scenario's test proves this one in full; that test carries both tags.
   - **Not automated** — only with a stated reason (for example a migration-only check covered by review). Never silently.
3. **Name the test.** Unit: `{Action}_{Condition}_{Expected}` with `[Trait("Ticket", "T-<DOMAIN>-NNN")]` and `[Trait("Scenario", "T-<DOMAIN>-NNN/S<n>")]`. E2E: the scenario title from the ticket, tagged `@T-<DOMAIN>-NNN @T-<DOMAIN>-NNN/S<n>`. `<n>` is always the ticket's explicit ID.
4. **Group e2e scenarios into batches.** A batch is one feature file (or describe block / scenario group), usually per ticket or per screen. Name it `{feature}.{batch}` (for example `animals.form`) and give it:
   - its own state keys `{feature}.{batch}.{state}` (for example `animals.form.bessie-exists`); every scenario's first step uses one of them;
   - a default state (usually `empty`) that the master reset seeds, and its dependencies (normally `personas.<feature>`);
   - a **footprint**: the fixed rows it seeds and the natural keys its scenarios create (for example Names "Bessie", "Ziggy");
   - the personas it uses.
   Batches whose footprints overlap run serially; say so in the plan. List new keys for the implementing agent.
5. **Map users to role personas** (`<feature>-<role>`): one per distinct permission set the scenarios need (for example `animals-tester` with `animals_write`, `animals-viewer` without). When a scenario names a real person (a display name or email), use a role persona **only if the spec's population source is generic** (for example "UpdatedBy → User.DisplayName, fallback User.Email"), and flag the ticket to the planning agent to genericise the wording. If the spec itself requires that person, ask; do not invent.
6. **Copy values exactly** from the scenario and spec: names, dates, messages. Where a scenario uses a relative date ("today"), say how the test pins it (server clock in unit tests; a date safely in the past in e2e) and flag time-zone sensitivity noted in the plan's decisions.
7. **List gaps and questions.** Untestable or contradictory scenarios, and tickets without explicit scenario IDs, go to the planning agent. Missing scaffolding, reset keys, handlers or personas go to the implementing agent (owner `code`): mark those rows **Waiting** / **Blocked**; the testing agent does not build them.
8. Fill `templates/test-plan.md` into `tests/test-plan.md`.

## Quality checks

- [ ] Every scenario has exactly one row; every row cites its explicit `<ticket>/S<n>`
- [ ] No ID invented from heading order; gaps and `(was …)` notes kept as the ticket has them
- [ ] Tickets without explicit IDs are **Blocked — scenario IDs not frozen** and raised with the planning agent
- [ ] Layer chosen per the rules above; "Not automated" rows have reasons
- [ ] Values and messages copied verbatim; nothing invented
- [ ] Every e2e scenario has a batch and a first-step key owned by that batch; footprints and overlaps listed
- [ ] Personas are role-based; real-person names flagged to the planning agent
- [ ] Out-of-scope items from `plan.md` are not planned
