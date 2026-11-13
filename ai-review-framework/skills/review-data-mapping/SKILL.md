# Skill: review-data-mapping

Check that every control's data reaches the **Service / Target DB Table / Target DB Column** named in the spec, end to end.

## Purpose

The planning specs say where each field lives in the database. This stage traces each control from the UI binding to the stored column and flags anything unmapped, renamed, missing a migration, or not in the spec. It is the heart of the full-stack review.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Control inventory with service / table / column and population sources |
| `diff` + `files` | Yes | Review scope from `gather-pr-context`: PR diff + files, or on the direct route the plan-scope files read whole (or local diff): API models, records, DTOs, mappers, EF entities, migrations, UI bindings |
| `stubs` | No | `stubs/ui-to-db.yaml` — cross-check only; the YAML spec wins |
| `checklist` | Yes | `checklists/full-stack-checklist.md` |

## The chain to trace

Use the chain for `development.api.active`. If the spec's Service name has no counterpart in that API, ask in the report rather than assuming.

### `api-framework` (the active default)

```text
UI binding            #/properties/<field> in the UI schema / form (camelCase)
   ↓
Record                Api.Framework.Services/Records ({Entity}Record)
   ↓
Service               Api.Framework.Services/{Area} ({Area}Service); database checks stay here
   ↓
Entity                Api.Framework.Data/Models + DbSet on LoginDbContext
   ↓
Column                ToTable / HasColumnName / HasMaxLength
   ↓
Migration             Api.Framework.Data/Migrations + LoginDbContextModelSnapshot
```

There is no downstream mapper. A field the schema owns is validated on the record; a database-only check (uniqueness and the like) runs in the area service. Details: `checklists/api-framework-checklist.md`.

### `csharp-api`

```text
UI binding            #/properties/<field> in the UI schema / form (camelCase)
   ↓
API record / DTO      Entities records folder (form records) or Controllers/V2/TempEntityModels (list / detail models)
   ↓
Mapper                API mapping folder  (UI record ↔ downstream request or local entity)
   ↓
Persistence           local: entity in data models + DbSet on DbContext, via a service in services / interfaces folders
                      downstream: the owning *RestService request model
   ↓
Column                entity property / [Column] / HasColumnName / HasMaxLength
   ↓
Migration             Data migrations folder (new or changed local columns) + model snapshot
```

Per `csharp-api-overview.mdc`, some entities are stored locally and some only exist downstream. Decide which branch applies from the spec's **Service** and the existing code. Details: `checklists/api-csharp-checklist.md`.

## Steps

1. For each control, write down the spec triple: `Service`, `Target DB Table`, `Target DB Column`. For grid columns (Paginated Grid, Embedded Grid Modal), the **Population Source** (`Table.Column`, sometimes two columns such as `LastAmendedOn & LastAmendedBy`).
2. Trace each link of the chain above. Record the file and line for each link.
3. Check, per control:
   - **Name** — the column is exactly the spec's column (for example `EmailAddress`, not `Email`). Property names may differ only where an explicit mapping says so.
   - **Table** — the entity maps to the spec's table (entity name, `[Table]`, `ToTable`).
   - **Service** — the write goes through the spec's service, not a different store.
   - **Type** — Switch / Boolean → `bool` / `bit`; Date → date type; dropdown → the stored `oneOf.const` type (for example an `Id`).
   - **Length** — `max_len_val` matches `HasMaxLength` / `nvarchar(n)` / `[MaxLength]`, or the column is at least as long.
   - **Nullability** — `mandatory: "Yes"` should not be silently nullable; optional fields must not be `NOT NULL` without a default.
   - **Mapper completeness** — where this API has a mapper, it copies the field both ways and preserves fields the section does not own. On API.Framework there is no downstream mapper; the record is what is validated and saved.
   - **Read path** — edit / view loads the stored value back into the same control.
4. For new or changed local columns: a migration exists where the active API checklist says migrations live, the designer and snapshot were updated by the tool, and it does not drop or rename a column holding data without a data step. `EnsureCreated` is not introduced.
5. For grids (Paginated Grid, Embedded Grid Modal): the list model property for each column is filled from its Population Source; the query applies the results-area filter (for example non-deleted rows for the parent record).
6. Look the other way too: list every column, entity property or migration change in the reviewed code (diff, or plan-relevant code on the direct plan scope) that is **not** in any linked spec.
7. Raise findings using `checklists/severity.md`:
   - Control with no persistence path, wrong table or column, wrong service, missing migration → **Blocker**
   - Destructive migration without a data step → **Blocker**
   - Column / property not in the spec → **Major** (ask whether the spec or the code should change)
   - Type, length or nullability mismatch, mapper drops or overwrites fields → **Major**
   - Stubs disagree with the spec but code matches the spec → note only

## Outputs

- Data mapping table rows: Control | Spec Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status (**Mapped** / **Mismatch** / **Unmapped** / **Extra** / **Not in PR** (PR route) / **Not implemented** (direct plan scope))
- Findings with `file:line` and spec reference

## Quality checks

- [ ] Every control and grid column has a row
- [ ] Every link in the chain has a file reference, or the gap is a finding
- [ ] New local columns have a migration; destructive changes called out
- [ ] Columns not in the spec are listed
- [ ] No Service / Table / Column invented — only values from the YAML are used as expectations
