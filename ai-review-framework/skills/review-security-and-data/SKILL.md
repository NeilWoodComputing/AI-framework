# Skill: review-security-and-data

Check authorisation, tenant and organisation scoping, server-side validation, secrets, personal data, injection and soft delete in the changed code.

## Purpose

Specs often carry rules that only hold if the server enforces them: uniqueness within an organisation, read-only fields, soft delete. This stage makes sure they cannot be bypassed by calling the API directly, and that the change does not leak data or secrets.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Spec validation rules, editable flags, grid row actions and filters |
| `diff` + `files` | Yes | Review scope from `gather-pr-context`: PR diff + files, or on the direct route the plan-scope files read whole (or local diff): controllers, services, validators, queries, entities, config files, UI data calls |
| `checklist` | Yes | `checklists/security-checklist.md` |

## Steps

1. **Collect spec-driven rules.** From the YAML, list every rule that mentions: unique, only one, per organisation, unique to tenant, pre-populated, not user-editable, soft delete, non-deleted. Each must be enforced on the server.
2. **Authorisation.** Apply the authorisation items in `checklists/security-checklist.md` for the active API only. No anonymous endpoints added without a stated reason.
3. **Tenant / organisation scope.**
   - Reads and writes are scoped to the caller's tenant or the parent organisation, not to an ID the client could change.
   - A field marked `editable: "No"` (for example Organisation, pre-populated from the parent context) is set or checked by the server; a changed value in the request body is ignored or rejected.
   - Uniqueness ("unique to tenant", "only one primary per organisation") is checked server-side within that scope — for Unity.API through a `unique*` custom validator with its checker interface registered, a service check, and / or a filtered unique index. "Only one" rules that clear a previous value run in the same transaction.
4. **Server-side validation.** Every `mandatory`, length, format and custom rule from the spec is enforced by the server schema (`required`, `minLength`, `maxLength`, `format`, `constraints`) or service — not only by the client form (react-hook-form / JSON Forms).
5. **Secrets.** No tokens, keys, passwords or connection strings in code, `appsettings*.json`, `launchSettings.json`, `.env*` or test fixtures. `.env.local` not committed. Nothing secret behind a `NEXT_PUBLIC_` variable. Downstream base URLs in `appsettings.{EnvironmentName}.json` (Unity.API UI-contract rule). Do not open or print real secret files (`review.scope_exclude`); judge from the reviewed code.
6. **Personal data (PII).** Contact names, emails and telephone numbers are personal data: not written to logs, not in URLs or query strings, not echoed in error messages, not stored client-side beyond what the session needs.
7. **Injection.** No SQL built by string concatenation or interpolation (`FromSqlRaw($"…")`); use LINQ, parameters or `FromSqlInterpolated`. No `dangerouslySetInnerHTML` / `innerHTML` with user data. URL segments and query values are encoded.
   - **Open redirects.** Take the stage 5 probe's `open-redirect-sink` findings on in-scope files as leads and read each sink: it is a finding only when a user-controlled value (query, params, form, header) can reach the redirect without a guard that keeps it a same-origin, root-relative path. The probe is a single-file heuristic (custom guards and wrappers are not recognised, and clean output is not proof), so also read redirect code it does not flag. Where a redirect guard module exists, run `probe-redirect.mjs` against it with `fixtures/redirect-attacks.json` as in `checklists/security-checklist.md`: an `unsafe` result is a finding, `over-strict` a note.
8. **Soft delete.** Where the spec says "Soft Delete" or "non-deleted": delete sets the existing soft-delete flag rather than removing the row; list and get-by-id queries exclude deleted rows; uniqueness checks follow the spec's rule for deleted rows. Use the soft-delete column the codebase already has — do not invent one; if none exists and the spec needs it, that is a data-mapping finding.
9. **Audit columns** named in the spec (for example `LastAmendedOn & LastAmendedBy`) are set by the server from the caller's identity, not taken from the request.
10. Raise findings using `checklists/severity.md`: cross-tenant read / write, missing authorisation, committed secret, injection → **Blocker**; client-only enforcement of a mandatory, uniqueness or read-only rule, hard delete where soft delete is specified, PII in logs → **Major** (Blocker if it lets data be corrupted); hardening suggestions → **Minor**.

## Outputs

- Findings with area `Security` or `Data integrity`, `file:line`, reference (spec rule, rule file or `checklists/security-checklist.md` item) and a suggested fix
- A list of spec-driven rules with **Enforced server-side** / **Client only** / **Not enforced**

## Quality checks

- [ ] Every spec rule about uniqueness, scope, read-only or soft delete has a status
- [ ] Every new or changed endpoint checked for the active API's authorisation (`checklists/security-checklist.md`) and scoping
- [ ] Reviewed code (diff or plan-scope files) scanned for secrets without opening real secret files
- [ ] PII not logged or exposed
- [ ] Every `open-redirect-sink` lead in scope confirmed or dismissed by reading the code; any redirect guard module run through `probe-redirect.mjs`
- [ ] No soft-delete or audit column invented
