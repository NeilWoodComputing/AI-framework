# ai-code-framework/scripts

## Pre-handoff gate

`pre-handoff-checks.mjs` is the pre-handoff gate the implementing agent runs in `loops/feature-build.md` stage 5 (plan: `ai-planning-framework/work/pre-handoff-checks/plan.md`; config: `verification` in `ai-framework.config.yaml`). Node 22, no dependencies. Run it from the `ai-framework` root:

```powershell
node ai-code-framework/scripts/pre-handoff-checks.mjs                       # every target, every check
node ai-code-framework/scripts/pre-handoff-checks.mjs --target nextjs       # one target
node ai-code-framework/scripts/pre-handoff-checks.mjs --feature ai-planning-framework/work/<feature> --record ai-planning-framework/work/<feature>/handoff.md
node ai-code-framework/scripts/pre-handoff-checks.mjs --json                # machine-readable result
node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target all   # reviewers: read-only probe (see below)
```

| Option | Meaning |
|--------|---------|
| `--target api-framework\|nextjs\|all` | Targets to check (default `all`) |
| `--feature <dir\|handoff.md>` | Run the target checks only for targets the feature's `implementation` manifest touches (all while it is empty); `secrets` still runs on both |
| `--record <handoff.md>` | Write `code.verification` (`pre-handoff:` lines replaced, other lines kept), `code.pre_handoff_gate` and `code.pre_handoff_gate_at`. Re-reads the file first, keeps its encoding and line endings, never touches `testing` |
| `--checks a,b` | Subset of `lint,typecheck,eol,secrets,docs-dup,unit` (not with `--record`) |
| `--path <dir>` | Apply a target's rules to another folder, e.g. a fixture (needs `--target`) |
| `--allowlist <file>` | Another allowlist (fixtures) |
| `--fix-eol` | One-off normalisation (T-GATE-002, D12): line endings, BOM and final newline only, verified per file. Only while no other feature is in development |
| `--probe` | Read-only reviewer scan (no child processes, no writes; not with `--record` or `--fix-eol`). See [Probe mode](#probe-mode-reviewers-read-only) |
| `--baseline <manifest.json>` | With `--probe`: report `eol-changed` against a manifest |
| `--baseline-print` | Print a baseline manifest to stdout (implies `--probe`; writes nothing) |

Output: one line per check, `<check> <target> -> pass|fail (<counts>)`, then each finding as `file:line`, rule and key path. Values are never printed. Exit 0 = pass, 1 = fail, 2 = usage error.

Settings the scan must never find committed: the API's `ConnectionStrings:LoginConnection` and `Jwt:Secret` (Development: user-secrets; Test: env vars `APIFW_TEST_ConnectionStrings__LoginConnection` / `APIFW_TEST_Jwt__Secret`, see `api/API.Framework/AGENTS.md`).

Secrets rules in short: JSON files are read as JSONC (`//` and `/* */` comments and trailing commas outside strings are ignored), then every key path is walked; a JSON file that still does not parse fails with `secrets-json-unparsed` (and still gets the line rules). A value under a credential-like key is reported unless it is empty or an explicit placeholder / reference: `<value>`, `${NAME}`, `%NAME%`, `$(NAME)`, `env:NAME`, `{name}`, `***`, `xxx`. A bare `ALL_CAPS` value is reported too; keep env-var names under keys ending in `EnvVar`, `Setting`, `Name` and similar.

Excluded everywhere: `review.scope_exclude` (build output, `node_modules`, `.next*`, `*.g.cs`, `package-lock.json`) and generated test output (`playwright-report`, `test-results`, `.auth`, `.features-gen`). `.env*`, `secrets.json`, `*.pfx`, `*.pem` and `*.key` are never opened; the secrets check lists them as skipped.

## Probe mode (reviewers, read-only)

`--probe` is a read-only scan for reviewers. It starts no child processes (no lint, tsc, `npm` or `dotnet`), writes, creates and deletes nothing, and uses only `readdirSync`, `readFileSync` and `statSync`. The walker and skip list are the gate's own: `.env*`, `secrets.json`, `*.pfx`, `*.pem` and `*.key` are never opened, and build output, `node_modules`, `.next*` and generated test output are skipped. The allowlist is not applied, so findings are raw. `--probe` together with `--record` or `--fix-eol` is refused with exit 2. Every finding is `{ file, rule, line }` only (`--json` adds `summary` counts, `by_rule`, `gate` and `problems`). Line text, matched values and secrets are never printed. Exit 0 = no findings, 1 = findings, 2 = usage error.

```powershell
node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target all                       # both targets
node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target nextjs --path <ui folder>  # another tree, LF rules
node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --baseline-print --target all > $env:TEMP\probe-baseline.json
node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target all --baseline $env:TEMP\probe-baseline.json
node ai-code-framework/scripts/probe-redirect.mjs --module <guard.js|guard.mjs> --export safeRedirectPath
```

| Rule | What it reports |
|------|-----------------|
| `utf8-invalid` | Not valid UTF-8 (`TextDecoder` fatal, plus a byte check for the first bad line) |
| `bom` | Starts with a UTF-8 BOM (line 1) |
| `eol-mixed` | CRLF and LF in one file, or any lone CR. The line is the first ending that differs from the first one |
| `eol-changed` | With `--baseline <manifest.json>` only: the dominant ending (`lf`, `crlf` or `none`) differs from the manifest (line 0). A `sha256` mismatch is counted in `summary.baseline_hash_changed`, files missing from it in `summary.not_in_baseline` |
| `open-redirect-sink` | A redirect sink whose argument comes from a user-controlled source with no recognised guard (see below) |

`--checks` takes the probe checks `utf8,bom,eol-mixed,eol-changed,open-redirect`. `--baseline-print` (implies `--probe`) prints `{ "version": 1, "files": { "<path>": { "eol": "lf|crlf|none", "sha256": "..." } } }` to stdout and writes nothing. Redirect it to a file yourself (`--baseline` reads UTF-8 and the UTF-16LE that Windows PowerShell 5 `>` writes). Paths are relative to the `ai-framework` root, or to `--path` when given. A hand-written manifest may be the bare `{ "<path>": { "eol": ... } }` map.

`open-redirect-sink` is a static heuristic on `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.mts`, `.cts` and `.cs` files. Comments and string contents are masked first.
- **Sinks:** `router.push` and `router.replace` (any `*Router`), `redirect(`, `permanentRedirect(`, `NextResponse.redirect`, `location`, `location.href`, `window.location` assignment, and `location.assign` and `location.replace`. In C#: `Redirect(`, `Response.Redirect(`, `RedirectPermanent*(`, `RedirectPreserveMethod(` and `new RedirectResult(`. `LocalRedirect` is the safe form.
- **Sources:** `searchParams`, `useSearchParams`, `query`, `params`, `URLSearchParams` and `location.search` or `location.hash`. In C#: `Request.Query`, `Request.Form`, `Request.Headers`, `QueryString` and `Query[`. A source also counts when it appears as a bare identifier named `returnUrl`, `returnTo`, `redirectTo`, `redirectUrl`, `redirectUri`, `redirect_uri`, `callbackUrl`, `next`, `from` or `redirect` that the file does not declare itself, such as a parameter. A source can sit in the sink expression, or in a variable assigned from one in the same file, followed through any chain of assignments.
- **Guards:** a call to `safeRedirect*`, `isSafe*`, `isLocalUrl`, `Url.IsLocalUrl`, `LocalRedirect*` or `sanitiseRedirect*` or `sanitizeRedirect*`, made in the expression or the variable chain, or on the sink line or the line above when it names the tainted variable. An argument that starts with a fixed literal path (`'/x...'`, `` `/x${...}` ``, `new URL('/x', base)`) or with `?` or `#` is treated as safe.
- **Limits:** it works one file at a time, with no imports, types, scopes or data flow across functions, so two same-named variables in different functions are merged. Regex literals, or an apostrophe in JSX text, can hide the rest of that line. Custom redirect wrappers and guards with other names are not recognised. Treat a finding as a lead to read, not proof, and clean output as "nothing obvious", not "safe".

`probe-redirect.mjs` checks a return-path guard dynamically. It imports only the module you name (its top-level code runs), calls `<export>(input)` once per entry in `fixtures/redirect-attacks.json`, and judges each result. A result is **rejected** when it is null, `false` or `''`, or the call throws. It is **safe** when it is a same-origin, root-relative path: one leading `/`, no `\` or control characters, and nothing that resolves, or decodes once or twice, to `//host` or `/\host`. It is **unsafe** otherwise. For boolean `isSafe*` checks, `true` judges the input itself.

The attack list covers:
- protocol-relative URLs (`//evil`, `///evil`)
- backslashes (`/\evil`, `\\evil`)
- dot segments (`/..//evil`, `/../..//evil`, `/.//evil`, `/a/../..//evil`)
- encoded forms (`%2F%2F`, `%5C%5C`, `/%2E%2E//`, double-encoded `%252F%252F`)
- schemes (`http:`, `https:`, `javascript:`, `JaVaScRiPt:`, `data:`, with and without leading whitespace)
- tab, CR and LF injection
- userinfo (`//good@evil`)
- non-root-relative input
- safe controls, expected `safe`, such as `/projects?x=1#y` and `/a/../b`

A safe control that comes back rejected or collapsed to `/` is reported as over-strict, as a warning. Output names the attack id and category only. Exit 0 = nothing unsafe, 1 = unsafe results, 2 = usage or load error. It starts no processes and writes nothing.

TypeScript modules need a JS build first. On Node 22.6+, `node --experimental-strip-types ai-code-framework/scripts/probe-redirect.mjs --module src/lib/safe-redirect.ts --export safeRedirectPath` works when the file uses only erasable syntax and its imports carry file extensions.

## Allowlist

`pre-handoff-allowlist.json` holds `{ target, path | paths, rule, key | line_hint, reason, owner, proposed, expires }` entries and never a value. The implementing agent proposes entries with a reason and an expiry. A real credential needs Neil's OK, and the reviewing agent checks new entries every round. An expired entry fails the gate. An unexpired entry that matched nothing (judged only when its check ran on every target it applies to) is listed: an unused `secret-*` entry fails the gate (remove it), any other unused entry is a `WARNING` line (`warnings` in `--json`, plus a `pre-handoff: allowlist -> N unused entries (warning)` line when recorded).

## Fixtures and self-test

`pre-handoff-checks.selftest.mjs` generates the fixtures into a temp folder (`os.tmpdir()`, or `--out <dir>`), runs the runner on each one, and checks that the committed copy in `fixtures/pre-handoff/` is byte-identical (it never rewrites it unless you pass `--write-fixtures`). `api-bad` and `nextjs-bad` hold planted violations (connection-string password, `Jwt.Secret`, a commented JSONC file, an unparseable JSON file, `ALL_CAPS` credential values, C# fallback literal, private key, TS credential literal, a secret under `e2e/`, LF in a CRLF target, CRLF in an LF target, BOM, mixed endings, missing final newline, duplicate paragraph, ESLint error, type error); `api-good` and `nextjs-good` hold the false-positive shapes and allowlisted items and must pass; `nextjs-unit-fail` has a failing unit run. It also covers allowlist schema problems, expired and unused entries, the D11 rules against the real UI config (`e2e/` not linted or type-checked), `--feature` touched targets, and `--record` against a temp handoff copy (one full real-target gate run; `--skip-record` leaves it out). Planted values are fake and contain `PLANTED`; the self-test fails if one is printed. The `--probe` cases use temp-only fixtures and run every probe through a preload guard that logs any `child_process` call, any fs write, mkdir or rm, and any read of a secret-pattern file. A non-probe unit run is the control that shows the guard sees spawns. The cases also compare a sha256 and mtime manifest of the scanned tree before and after, check that `--record` and `--fix-eol` are refused and that findings carry only `file`, `rule` and `line`, and cover `utf8-invalid`, `bom`, `eol-mixed` (including a lone CR), `eol-changed`, the `open-redirect-sink` positive and guarded cases (TS and C#), and `probe-redirect.mjs` against a safe and an F-01-shaped unsafe sample.

```powershell
node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs                   # temp copy, committed fixtures compared
node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs --write-fixtures  # after changing a fixture: rewrite the committed copy too
```
