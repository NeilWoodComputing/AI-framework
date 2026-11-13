# Ticket: T-GATE-003 — Secrets scan and allowlist

| Field | Value |
|-------|--------|
| ID | T-GATE-003 |
| Type | Cross-cutting (security tooling) |
| Feature | pre-handoff-checks |
| Priority | High |
| Owner | dev-bot |
| Specs | None; `plan.md` §5.2 (secrets rules) |
| Journey (optional) | — |

## User story

**As** Neil  
**I want** committed config, code and docs scanned for real credentials before every hand-off  
**So that** a password or key is never committed again (6 of 6 manage-animals review rounds flagged one)

## Full-stack scope

No UI controls or DB columns. Files: the `secrets` check in the runner (in `ai-code-framework/scripts/`, D15), `pre-handoff-allowlist.json`, fixture files for the tests.

## Work to do

1. Implement the `secrets` check (Node `.mjs`, no dependencies, D4):
   - JSON key walk for `appsettings*.json`, `launchSettings.json` and other committed `*.json` config: non-empty value under a credential key, or any value with a non-empty `Password=` / `Pwd=`.
   - Code (`*.cs`, `*.ts`, `*.tsx`, `*.js`, `*.mjs`, `*.cjs`): string **literals** with non-empty `Password=` / `Pwd=`, private key blocks, literals assigned to key / secret / password names.
   - Docs (`*.md`, `*.mdc`): non-empty `Password=` / `Pwd=`, private key blocks.
2. Never print or log a value: output `file:line`, key path, rule id only. Never open `.env*`, `secrets.json`, `*.pfx`, `*.pem`, `*.key`; skip `review.scope_exclude` paths.
3. Allowlist file with entries `{ path, rule, key | line_hint, reason, owner, expires }` (no values). Expired entries fail. Dev Bot proposes entries with reason and expiry; real credentials need Neil's OK; Review Bot checks new entries each round (D13).
4. Where a target is not a git repo, scan the working tree (D14) and say so in the output.
5. Seed the allowlist only with agreed non-secrets (e.g. the test signing key literal named "not a secret" in `AnimalPoliciesTests.cs`); no entries for the existing dev secrets (D1: removed by T-GATE-008).

## Acceptance criteria

### Scenario: S1 — Non-empty connection-string password in appsettings fails

```gherkin
Given a fixture appsettings.json whose ConnectionStrings value contains a non-empty Password=
When the secrets check runs
Then it fails
And it reports the file, the key path ConnectionStrings.<name> and the rule id
And the password value does not appear anywhere in the output
```

### Scenario: S2 — Non-empty secret key fails, empty passes

```gherkin
Given a fixture appsettings file with Jwt.Secret set to a non-empty value
When the secrets check runs
Then it fails naming Jwt.Secret
Given the same file with Jwt.Secret set to ""
When the secrets check runs
Then it passes for that key
```

### Scenario: S3 — Hard-coded fallback connection string in C# fails

```gherkin
Given a fixture .cs file with GetConnectionString(...) ?? a string literal containing a non-empty Password=
When the secrets check runs
Then it fails with the file and line, and no value is printed
```

### Scenario: S4 — Values read from the environment or a request pass

```gherkin
Given code like Environment.GetEnvironmentVariable(persona.PasswordEnvVar), process.env[envVar] or Password = record.Password
And docs that mention "secret" or "password" in prose without a value
And appsettings keys Jwt.Issuer and Jwt.Audience with non-empty values
When the secrets check runs
Then none of these are reported
```

### Scenario: S5 — Allowlisted entry passes; expired entry fails

```gherkin
Given an allowlist entry for a path, rule and key with a reason, owner and a future expires date
When the secrets check finds that exact item
Then it is reported as allowlisted and the check passes
When the expires date is in the past
Then the check fails and names the expired entry
```

### Scenario: S6 — Secret files are never opened

```gherkin
Given .env.local, secrets.json and a *.pfx file in a target
When the secrets check runs
Then it does not open or read them
And they are listed only as skipped by pattern
```

### Scenario: S7 — Working tree scanned when the target is not in git

```gherkin
Given a target folder that is not a git repository
When the secrets check runs
Then it scans the working tree minus review.scope_exclude
And the output states "not a git repo: working tree scanned"
```

### Scenario: S8 — Current targets give the expected result

```gherkin
Given API.Framework and UI.NextJs.Framework as they are when this ticket is built
When the secrets check runs on both
Then, before T-GATE-008, it reports appsettings.json ConnectionStrings.LoginConnection, appsettings.json Jwt.Secret and the LoginDbContextFactory fallback
And after T-GATE-008 it reports none of them
And it reports nothing else
```

Checklist (derived from scenarios):

- [ ] JSON, code and docs rules implemented; known false positives covered by tests
- [ ] No value ever printed; secret files never opened
- [ ] Allowlist with reason / owner / expiry; expiry enforced
- [ ] Works without git

## Out of scope

- Scanning git history (no repos yet)
- Rotating credentials (Neil)
- gitleaks or other third-party tools (D4: Node script)

## Notes

- Stable ID for DevOps upsert: `T-GATE-003`
- Known at planning (key names only): `appsettings.json` `ConnectionStrings.LoginConnection` (non-empty `Password=`), `Jwt.Secret` (non-empty); `LoginDbContextFactory.cs` line 29 fallback literal (non-empty `Password=`). `appsettings.Test.json` secrets are empty. False-positive shapes: `AuthController.cs:56`, `PersonasUnit.cs:45`, `e2e/setup/auth.setup.ts:63`, `e2e/setup/sign-in-child.cjs:41`, `e2e/support/personas.ts:36`, `TokenService.cs:94`, `e2e/README.md:35`.
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D1, D4, D11, D13, D14, D15.
