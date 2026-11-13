# Security and data checklist

Applies to every review: the PR diff, or the files in scope on the direct route (plan scope or diff). Severities from `severity.md`. Judge secrets from the reviewed code; never open or print real secret files (`.env*` and the rest of `review.scope_exclude`) or token values. On a plan-scope review without git, "committed" cannot be checked; note that instead of guessing.

## Authorisation and scope

- [ ] C# API only: new or changed V2 controllers carry appropriate authorization attributes
- [ ] API.Framework: class-level `[Authorize]` plus `[Authorize(Policy = {Area}Policies.X)]` on every endpoint, schema endpoints included; policies registered in `Program.cs` with `RequireClaim(TokenService.PermissionClaimType, ...)` (the `permission` claim); `[AllowAnonymous]` only for sign-in, register, token and password-reset endpoints and the sign-in schema (`checklists/api-framework-checklist.md`)
- [ ] Reads and writes scoped to the caller's tenant / the parent organisation; IDs from the client are checked against that scope
- [ ] Fields with `editable: "No"` in the spec (a value filled from the parent record) are set or verified server-side, not trusted from the request body
- [ ] Permission-guarded UI routes (Angular: `PermissionRouteGuard`); the API still enforces access on its own

## Spec rules that must hold on the server

- [ ] Every `mandatory`, length and format rule enforced by the server schema or service, not only the client form
- [ ] Uniqueness rules ("unique to tenant", "unique per organisation", "only one … per …") checked server-side within the right scope — `unique*` validator + checker, service check and / or filtered unique index
- [ ] "Only one" rules that clear a previous value run atomically (one transaction) so two saves cannot both win
- [ ] Validation failures return the spec's exact message and make **no** write

## Soft delete and audit

- [ ] Spec says Soft Delete → the existing soft-delete flag is set; the row is not removed
- [ ] List, get-by-id and lookup queries exclude soft-deleted rows; uniqueness follows the spec for deleted rows
- [ ] No soft-delete or audit column invented; use the one in the spec or the existing entity
- [ ] Audit columns in the spec (e.g. `LastAmendedOn`, `LastAmendedBy`) set server-side from the caller's identity

## Input handling and injection

- [ ] No SQL built by concatenation or interpolation (`FromSqlRaw($"…")`); LINQ, parameters or `FromSqlInterpolated` used
- [ ] No `dangerouslySetInnerHTML` / `innerHTML` / `bypassSecurityTrust*` with user data
- [ ] URL segments and query values encoded; no user input in redirects without validation
  - probe `open-redirect-sink` findings (`--probe --json`, `loops/pr-review.md` stage 5) are leads, not proof: confirm or dismiss each by reading the code; clean output means "nothing obvious", not safe (single-file heuristic; custom guards and wrappers are not recognised)
  - where a redirect guard module exists, run `node ai-code-framework/scripts/probe-redirect.mjs --module <guard> --export <name, e.g. safeRedirectPath> --json` from the `ai-framework` root; it uses the attack list `ai-code-framework/scripts/fixtures/redirect-attacks.json` (`--attacks <file>` to name it). For a `.ts` guard use `node --experimental-strip-types` (Node 22.6+, erasable syntax only, imports with extensions); never build it to JS for this. It imports the module, so its top-level code runs: only run it on a plain guard module. Any `unsafe` result is a finding; `over-strict` is a note
- [ ] File / spreadsheet uploads validated before import (`csharp-api-bulk-import.mdc`)

## Secrets and configuration

- [ ] No tokens, keys, passwords or connection strings in code, `appsettings*.json`, `launchSettings.json`, `.env*` or test fixtures
- [ ] `.env.local` not committed; `.env.example` holds placeholders only
- [ ] Nothing secret in `NEXT_PUBLIC_*` variables
- [ ] Downstream base URLs in `appsettings.{EnvironmentName}.json`
- [ ] CORS not widened to `*` for credentialed requests

## Personal data

- [ ] Names, emails, telephone numbers and similar not written to logs (`ILogger`, `LoggingService`, `console.*`)
- [ ] Personal data not placed in URLs or query strings
- [ ] Error messages and API responses do not echo other users' or tenants' data
- [ ] Client storage (`sessionStorage`, cookies) holds only what the session needs
