# Test plan — <feature>

| Field | Value |
|-------|-------|
| Feature folder | <`feature_path` from `handoff.md`, e.g. `ai-planning-framework/projects/<project>/work/<feature>/` or `ai-planning-framework/work/<feature>/`> |
| Tickets | <T-<DOMAIN>-NNN, …> |
| Specs | <`specs/<page>.yaml`, …> |
| Active API / UI | <development.api.active> / <development.ui.active> |
| Unit test project | <Unity.API.Tests \| Api.Framework.Tests (approved 08/10/2026) \| Waiting — not created yet (owner `code`)> |
| E2E location | <`testing.e2e.nextjs.path` \| Waiting — scaffolding not created yet (owner `code`)> |
| Environment | Test · dedicated PostgreSQL `<api_framework_test>` · master reset once per run |
| Written by | <agents.testing.id> · <YYYY-MM-DD HH:mm GMT \| BST> |

## Personas

| Persona | Permissions | Display name | Password env var | Used by batches |
|---------|-------------|--------------|------------------|-----------------|
| `<feature>-<role>` | <exact permissions \| none> | <name \| none> | `E2E_<FEATURE>_<ROLE>_PASSWORD` | <batches> |

## Batches and reset keys

| Batch unit (feature file) | Keys (`{feature}.{batch}.{state}`) → data | Default state (master) | Depends on | Footprint | Serial with | Exists? |
|---------------------------|--------------------------------------------|------------------------|------------|-----------|-------------|---------|
| `<feature>.<batch>` (`<Batch>.feature`) | `<feature>.<batch>.<state>`: <rows, fixed GUIDs> | `<state>` (usually `empty`) | `personas.<feature>` | <fixed GUIDs; natural keys created> | <overlapping batches \| none> | Yes \| No — ask the implementing agent |

## Scenarios → tests

| Scenario | Title (from ticket) | Layer | Test (name / tag) | Reset key (first step) | Persona | Status |
|----------|---------------------|-------|-------------------|------------------------|---------|--------|
| T-<DOMAIN>-NNN/S<n> (explicit ID from the ticket heading) | <title, with any `(was …)` note> | Unit \| API e2e \| UI e2e \| Covered by <ref> \| Not automated | `<Action_Condition_Expected>` / `@T-<DOMAIN>-NNN/S1` | `<feature>.<batch>.<state>` | `<feature>-<role>` | Planned \| Written \| Waiting — <reason, owner> \| Blocked — <reason, owner> |

## Blocked — scenario IDs not frozen

Tickets with no explicit `### Scenario: S<n> — <title>` headings: titles for reference only, no IDs, no tests (`testing.scenario_ids: explicit`).

| Ticket | Scenario title (from ticket) | Intended layer | Status |
|--------|------------------------------|----------------|--------|
| T-<DOMAIN>-NNN | <title> | <layer> | Blocked — scenario IDs not frozen (planning agent) |

## Flags for the planning agent

- <ticket/S<n>>: names a real person ("<name>"); tested with `<persona>` because the spec's population source is generic; please reword generically.

## Not automated / questions

- <scenario>: <reason or question, and who it goes to>
