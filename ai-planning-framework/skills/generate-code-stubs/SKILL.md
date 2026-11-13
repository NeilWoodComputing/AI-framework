# Skill: generate-code-stubs

Emit **framework-agnostic** placeholders that mirror UI field ↔ DB column mapping from the page specs. Optional final step in the loop.

## Purpose

Give engineers typed interfaces and stub modules without choosing React/Vue/.NET/etc. Stubs exist to preserve the full-stack contract from the Excel/YAML.

## Config first

Read `ai-framework.config.yaml` at the `ai-framework` root (`../ai-framework.config.yaml` from the planning-framework root; its paths are relative to the `ai-framework` root):

- Write stubs to `<feature_dir>/stubs/` (`<feature_dir>` = the feature folder; see AGENT-BRIEF.md, *Where features live*)
- Read the project profile (`project.profile`): if `stacks` lists hint files, read `stacks/<name>.md` beside this skill for naming only (type names, casing, file layout); stubs stay framework-agnostic. This skill is the only reader of those files; add one for any other stack (`dotnet-efcore`, `nextjs` and `angular` exist)
- Note the active API / UI folder from `development.api.active` and `development.ui.active` in the stubs `README.md` so later code work knows its target; stubs themselves stay framework-agnostic unless the user asks for framework code
- If `active` does not match an option, or the path is missing, stop and report rather than guessing

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `page_specs` | Yes | YAML specs with service + table + column |
| `output_dir` | Yes | `<feature_dir>/stubs/` |

## Outputs

Suggested layout (adjust names to the domain):

```text
<feature_dir>/stubs/
  README.md                 # how stubs map to Excel; active API/UI from config
  models/<Table>.md         # or .ts/.py interfaces — field list from columns
  services/<Service>.md     # operations: get/save for entities
  pages/<PageTitle>.md      # steps → controls → binds to model fields
  mappings/ui-to-db.yaml    # Control Label → service.table.column
```

Use interfaces / pseudocode only, for example:

```text
interface Book {
  title: string;             // UI: Title → Book.Title
  isbn: string;              // UI: ISBN → Book.Isbn
}
```

## Steps

1. Collect unique `target_db_table` values; one model stub each.
2. Collect fields from `target_db_column` + control metadata (mandatory, formats).
3. Group operations by `service`.
4. For each wizard page, list steps and control→field bindings.
5. For manage/list, stub a query DTO from Population Source columns and action handlers.
6. Write `mappings/ui-to-db.yaml` as the canonical bridge, starting from `templates/stubs/ui-to-db.yaml`.
7. Do **not** generate framework components, ORM migrations, or real SQL unless asked later.

## Quality checks

- [ ] Every control with a DB mapping appears in `ui-to-db.yaml`
- [ ] Model fields align with Target DB Column names
- [ ] No dependency on a specific UI or backend framework
- [ ] README points back to the Excel/YAML source
- [ ] Output under `<feature_dir>/stubs/`; active API/UI noted from config

## Anti-patterns

- Generating React/Angular components “for convenience”
- Dropping Service/Table/Column in favour of UI-only props
- Inventing columns not present in the spec
- Treating a stack hint file as a rule: hints only shape names, never add framework code
