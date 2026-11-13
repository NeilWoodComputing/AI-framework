# Ticket: T-GATE-008 — Remove committed dev secrets from API.Framework

| Field | Value |
|-------|--------|
| ID | T-GATE-008 |
| Type | Cross-cutting (security fix) |
| Feature | pre-handoff-checks |
| Priority | High — first ticket (D1: fix first, before the gate blocks) |
| Owner | dev-bot (code / config); Neil (local values, rotation) |
| Specs | None; `plan.md` §2 (secrets table), D1 |
| Journey (optional) | — |

## User story

**As** Neil  
**I want** API.Framework's committed config and design-time factory to hold no credentials  
**So that** the secrets gate passes on its first run without allowlisting real secrets

## Full-stack scope

No UI controls or DB columns. Files: `ai-code-framework/api/API.Framework/Api.Framework/appsettings.json` (`ConnectionStrings.LoginConnection`, `Jwt.Secret`), `Api.Framework.Data/LoginDbContextFactory.cs` (fallback connection string), local-setup docs (README / AGENTS) for where dev values now come from.

## Work to do

1. Set `ConnectionStrings.LoginConnection` and `Jwt.Secret` in `appsettings.json` to empty (same pattern as `appsettings.Test.json`).
2. `LoginDbContextFactory`: remove the hard-coded fallback; read the connection string from configuration (user-secrets key `ConnectionStrings:LoginConnection`, env var `ConnectionStrings__LoginConnection`) and throw a clear message naming that setting when it is missing (default, Neil may override).
3. Document local setup: .NET user-secrets for dev (`dotnet user-secrets` on Api.Framework, keys `ConnectionStrings:LoginConnection` and `Jwt:Secret`), or env vars `ConnectionStrings__LoginConnection` and `Jwt__Secret`; names only, no values (default, Neil may override).
4. **Action for Neil (not an agent):** rotate the exposed dev DB password and Jwt secret, then set his local values via user-secrets or env vars. Agents never read or write the values.
5. Run the secrets check (T-GATE-003) and `dotnet build` / `dotnet ef` design-time commands to confirm.

## Acceptance criteria

### Scenario: S1 — No credentials in committed config

```gherkin
Given appsettings.json after this ticket
When the secrets check runs
Then ConnectionStrings.LoginConnection and Jwt.Secret are not reported
```

### Scenario: S2 — Factory fails clearly without configuration

```gherkin
Given no connection string in configuration or the agreed env var
When a design-time EF command uses LoginDbContextFactory
Then it fails with a message naming the missing setting
And no hard-coded connection string is used
```

### Scenario: S3 — Factory works with the env var or user-secrets

```gherkin
Given Neil has set the agreed env var or user-secret locally
When dotnet ef migrations has-pending-model-changes runs
Then it connects using that value
```

### Scenario: S4 — Local setup is documented without values

```gherkin
Given the API.Framework local setup docs after this ticket
When a developer reads them
Then they name the settings to provide and how (user-secrets or env vars)
And no value is written in the docs
```

Checklist (derived from scenarios):

- [ ] `appsettings.json` credentials empty
- [ ] Factory fallback removed; clear error
- [ ] Docs name settings only
- [ ] Neil: local values set, exposed credentials rotated

## Out of scope

- Production secret management
- `appsettings.Test.json` (already empty)

## Notes

- Stable ID for DevOps upsert: `T-GATE-008`
- In scope (D1, Neil 2026-10-09 10:32 BST: fix first). Neil rotates the exposed dev DB password and Jwt secret (his action, not an agent's). Setting names are Plan Bot's default (Neil may override).
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D1.
- Amendment (2026-10-09, Neil approved; plan.md §6): `DefaultUserSeeder`'s admin password literal (found by the secrets scan, not in the planned list) moved to the `DefaultUser:Password` setting, seeding skipped when unset — a deviation for review. Test-only API settings use user-level env vars `APIFW_TEST_ConnectionStrings__LoginConnection` and `APIFW_TEST_Jwt__Secret`, read by `Program.cs` / `LoginDbContextFactory` only when the environment is Test. Names only.
