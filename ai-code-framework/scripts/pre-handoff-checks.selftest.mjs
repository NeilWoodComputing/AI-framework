#!/usr/bin/env node
// Self-test for pre-handoff-checks.mjs (T-GATE-002..005 acceptance; D16: Review Bot verifies with planted violations).
//   node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs [--out <dir>] [--write-fixtures] [--skip-record]
// Generates the fixture targets byte for byte (line endings and BOMs are part of the fixtures, so they are generated
// here rather than edited by hand) into a temp folder (os.tmpdir(), or --out <dir>), runs the runner against each one
// and checks the result. The committed copy in scripts/fixtures/pre-handoff/ is only compared, never rewritten,
// unless --write-fixtures is given (review F-06). Planted "secrets" are fake strings that contain PLANTED; the test
// fails if any of them is printed. --skip-record skips the one full real-target gate run used to test --record.
// --probe cases use temp-only fixtures (OUT/probe) and a preload guard that logs child_process calls, fs writes and
// secret-pattern reads; probe-redirect.mjs is run against fixtures/redirect-attacks.json with a safe and an unsafe sample.
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RUNNER = path.join(HERE, 'pre-handoff-checks.mjs');
const COMMITTED = path.join(HERE, 'fixtures', 'pre-handoff');
const FRAMEWORK_ROOT = path.resolve(HERE, '..', '..');
const UI_DIR = path.join(FRAMEWORK_ROOT, 'ai-code-framework', 'ui', 'UI.NextJs.Framework');
const argv = process.argv.slice(2);
const optValue = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; };
const WRITE_COMMITTED = argv.includes('--write-fixtures');
const SKIP_RECORD = argv.includes('--skip-record');
const OUT = optValue('--out') ? path.resolve(optValue('--out')) : fs.mkdtempSync(path.join(os.tmpdir(), 'pre-handoff-selftest-'));
const FX = path.join(OUT, 'fixtures');
const SECRET_FILE_RE = [/^\.env/i, /^secrets\.json$/i, /\.pfx$/i, /\.pem$/i, /\.key$/i]; // compared by name only
const CRLF = (s) => s.replace(/\r?\n/g, '\r\n');
const LF = (s) => s.replace(/\r\n/g, '\n');
const BOM = '\ufeff';
const PARA = 'The pre-handoff gate runs every mechanical check before the implementing agent hands a feature to review, so line endings, secrets and duplicated documentation never reach a reviewer as findings again.';
const PARA_WRAPPED = 'THE PRE-HANDOFF GATE runs every mechanical check before the implementing\nagent hands a feature to review, so line endings, secrets and duplicated\ndocumentation never reach a reviewer as findings again.';
const SHORT = 'Run the gate before every hand-off to review.';
const FENCE = '```powershell\nnode ai-code-framework/scripts/pre-handoff-checks.mjs --target all --json --record handoff.md now please\n```';

const fixtures = {
  'api-bad': { // rules: api-framework (CRLF)
    'appsettings.json': CRLF('{\n  "ConnectionStrings": {\n    "LoginConnection": "Host=localhost;Database=fixture;Username=fixture;Password=PLANTED-pw-0001"\n  },\n  "Jwt": {\n    "Issuer": "system-login",\n    "Audience": "system-login",\n    "Secret": "PLANTED-jwt-0002-0123456789abcdef0123456789"\n  }\n}\n'),
    'LoginDbContextFactory.cs': CRLF('public class LoginDbContextFactory\n{\n    public string Get(string? configured) => configured\n        ?? "Host=localhost;Port=5432;Database=fixture;Username=fixture;Password=PLANTED-pw-0003";\n}\n'),
    'LfFile.cs': 'namespace Fixture;\n\npublic class LfFile { }\n',
    'Bom.cs': BOM + CRLF('namespace Fixture;\n\npublic class Bom { }\n'),
    'Mixed.cs': 'namespace Fixture;\r\n\npublic class Mixed { }\r\n',
    'NoNewline.cs': CRLF('namespace Fixture;\n\npublic class NoNewline { }'),
    'notes.md': CRLF('# Notes\n\n-----BEGIN RSA PRIVATE KEY-----\nPLANTED-key-0005\n-----END RSA PRIVATE KEY-----\n'),
    'README.md': CRLF(`# Fixture API\n\n${PARA}\n\n${SHORT}\n\n${FENCE}\n`),
    'docs/setup.md': CRLF(`# Setup\n\n${PARA_WRAPPED}\n\n${SHORT}\n\n${FENCE}\n`),
    '.env.local': 'Password=PLANTED-env-0004\n', // wrong endings + secret: must be skipped, never opened
    'secrets.json': '{ "Jwt": { "Secret": "PLANTED-secretsjson-0006" } }', // never opened
    'cert.pfx': 'PLANTED-pfx-0007', // never opened
    'bin/Release/Generated.cs': '"Password=PLANTED-bin-0008"\n', // build output: excluded
    // F-01: comments + trailing commas must not hide a credential; an unparseable file fails
    'appsettings.Commented.json': CRLF('{\n  // Local settings (fixture)\n  "Jwt": {\n    /* the issuer is public */\n    "Issuer": "system-login",\n    "Secret": "PLANTED-jwt-commented-0010",\n  },\n}\n'),
    'appsettings.Broken.json': CRLF('{\n  "Jwt": {\n    "Secret": "PLANTED-jwt-broken-0011"\n\n'),
    // F-02: an ALL_CAPS value under a credential key is a value, not an env-var name
    'appsettings.Caps.json': CRLF('{\n  "Api": {\n    "ApiKey": "PLANTED_CAPS_KEY_0012"\n  }\n}\n'),
  },
  'api-good': { // every false-positive shape from the plan; one allowlisted test key
    'appsettings.json': CRLF('{\n  "ConnectionStrings": {\n    "LoginConnection": ""\n  },\n  "Jwt": {\n    "Issuer": "system-login",\n    "Audience": "system-login",\n    "Secret": "",\n    "AccessTokenMinutes": 60\n  },\n  "TestData": {\n    "KeyEnvVar": "E2E_TEST_DATA_KEY"\n  }\n}\n'),
    'Personas.cs': CRLF('public sealed class Personas\n{\n    public const string PasswordEnvVar = "E2E_ANIMALS_TESTER_PASSWORD";\n    public const string PasswordSetting = "DefaultUser:Password";\n    public string? Password { get; set; }\n\n    public void Load(Record record, Persona persona)\n    {\n        Password = Environment.GetEnvironmentVariable(persona.PasswordEnvVar);\n        Password = record.Password;\n        var connection = $"Host={host};Password={password}";\n        var reason = active ? "invalid_password" : "inactive";\n    }\n\n    private const string InvalidRefreshToken = "The refresh token is invalid or has expired.";\n    private void Unused()\n    {\n    }\n}\n'),
    'TestKey.cs': CRLF('public static class TestKey\n{\n    // A dummy signing key for unit tests - not a secret.\n    private const string SigningKey = "fixture-unit-test-signing-key-0123456789abcdef";\n}\n'),
    // F-01 / F-02: comments, trailing commas, a URL containing // and explicit env references all pass
    'appsettings.Development.json': CRLF('{\n  // Development overrides (fixture): values come from user-secrets\n  "Api": { "BaseUrl": "https://localhost:7188/", },\n  "Jwt": {\n    "Secret": "${JWT_SECRET}", /* reference, not a value */\n    "SigningKey": "%JWT_SIGNING_KEY%",\n    "ClientSecret": "$(CLIENT_SECRET)",\n  },\n}\n'),
    'README.md': CRLF('# Fixture API (clean)\n\nSet the secret and the password through user-secrets or environment variables; never commit them. The connection string uses `Password=<value>` as a placeholder only.\n'),
  },
  'nextjs-bad': { // rules: nextjs (LF)
    // D11 (as in the real UI config): e2e/ is not linted (Playwright has its own config) but is scanned for secrets
    'eslint.config.mjs': 'export default [\n  { ignores: ["e2e/**"] },\n  { files: ["**/*.js"], rules: { "no-debugger": "error", "no-unused-vars": "warn" } },\n];\n',
    'e2e/debug.js': 'export function e2eStop() {\n  debugger;\n}\n',
    'e2e/support/login.ts': 'export const testerPassword = "PLANTED-e2e-0014";\n',
    'caps-token.ts': 'export const apiToken = "PLANTED_CAPS_TOKEN_0013";\n', // F-02 in code
    'bad-lint.js': 'export function stop() {\n  debugger;\n}\n',
    'warn-only.js': 'export function warnOnly() {\n  const unused = 1;\n}\n',
    'tsconfig.json': '{\n  "compilerOptions": { "strict": true, "noEmit": true, "skipLibCheck": true },\n  "include": ["*.ts"]\n}\n',
    'type-error.ts': 'export const count: number = "not a number";\n',
    'crlf.ts': CRLF('export const crlf = 1;\n'),
    'README.md': BOM + `# Fixture UI\n\n${PARA}\n`,
    'AGENTS.md': `# Agents\n\n${PARA}\n`,
    'api-client.ts': 'export const apiKey = "PLANTED-apikey-0009";\n',
  },
  'nextjs-good': {
    'eslint.config.mjs': 'export default [\n  { files: ["**/*.js"], rules: { "no-debugger": "error" } },\n];\n',
    'ok.js': 'export function ok() {\n  return process.env.E2E_ANIMALS_TESTER_PASSWORD ? "set" : "unset";\n}\n',
    'tsconfig.json': '{\n  "compilerOptions": { "strict": true, "noEmit": true, "skipLibCheck": true },\n  "include": ["*.ts"]\n}\n',
    'ok.ts': 'export function passwordFor(envVar: string, env: Record<string, string | undefined>): string | undefined {\n  const password = env[envVar];\n  return password;\n}\n',
    'README.md': '# Fixture UI (clean)\n\nThe persona password is read from an environment variable whose name is in the persona file.\n',
    '.cursor/rules/x.mdc': `---\ndescription: mirror\n---\n\n${PARA}\n`,
    '.claude/rules/x.md': `${PARA}\n`,
  },
  'nextjs-unit-fail': { // F-07: a failing unit run fails the gate (vitest-style summary, exit 1)
    'package.json': '{\n  "name": "fixture-unit-fail",\n  "private": true,\n  "scripts": {\n    "test": "node unit-fail.mjs"\n  }\n}\n',
    'unit-fail.mjs': "console.log(' Test Files  1 failed (1)');\nconsole.log('      Tests  1 failed | 2 passed (3)');\nprocess.exit(1);\n",
  },
};

function writeFixtures(FX) {
  fs.rmSync(FX, { recursive: true, force: true });
  for (const [name, files] of Object.entries(fixtures)) {
    for (const [rel, content] of Object.entries(files)) {
      const f = path.join(FX, name, rel); fs.mkdirSync(path.dirname(f), { recursive: true });
      fs.writeFileSync(f, content, 'utf8');
    }
  }
  const future = '2099-12-31'; const past = '2020-01-01';
  const entry = (expires) => ([
    { target: 'api-framework', path: 'TestKey.cs', rule: 'secret-code-literal', key: 'SigningKey', reason: 'Dummy unit-test signing key, named "not a secret" (fixture)', owner: 'dev-bot', expires },
    { target: 'nextjs', paths: ['.cursor/rules/x.mdc', '.claude/rules/x.md'], rule: 'docs-dup', reason: 'Intentional Cursor / Claude rule mirror (fixture)', owner: 'dev-bot', expires: future },
  ]);
  fs.writeFileSync(path.join(FX, 'allowlist.fixture.json'), JSON.stringify({ version: 1, entries: entry(future) }, null, 2) + '\n');
  fs.writeFileSync(path.join(FX, 'allowlist.expired.json'), JSON.stringify({ version: 1, entries: entry(past) }, null, 2) + '\n');
  // F-07: schema problems (a value present, expires missing)
  fs.writeFileSync(path.join(FX, 'allowlist.schema-bad.json'), JSON.stringify({ version: 1, entries: [
    { target: 'api-framework', path: 'TestKey.cs', rule: 'secret-code-literal', key: 'SigningKey', value: 'PLANTED-allowvalue-0015', reason: 'schema fixture: has a value', owner: 'dev-bot', expires: future },
    { target: 'api-framework', path: 'Other.cs', rule: 'secret-code-literal', key: 'ApiKey', reason: 'schema fixture: no expires', owner: 'dev-bot' },
  ] }, null, 2) + '\n');
  // F-03: unexpired entries that match nothing (secret-* fails, others warn)
  fs.writeFileSync(path.join(FX, 'allowlist.unused.json'), JSON.stringify({ version: 1, entries: [
    ...entry(future),
    { target: 'api-framework', path: 'Gone.cs', rule: 'secret-code-literal', key: 'ApiKey', reason: 'unused fixture: the literal was removed', owner: 'dev-bot', expires: future },
    { target: 'api-framework', paths: ['README.md', 'docs/gone.md'], rule: 'docs-dup', reason: 'unused fixture: the duplicate was removed', owner: 'dev-bot', expires: future },
  ] }, null, 2) + '\n');
  fs.writeFileSync(path.join(FX, 'README.md'), [
    '# pre-handoff fixtures',
    '',
    'Generated by `../../pre-handoff-checks.selftest.mjs --write-fixtures` (do not edit by hand: line endings and BOMs are part of the fixtures).',
    'The self-test itself works on a temp copy and only checks that this folder is in step with it.',
    'Planted values are fake and contain PLANTED. Run the self-test, or run the runner on one fixture, for example:',
    '',
    '```powershell',
    'node ai-code-framework/scripts/pre-handoff-checks.mjs --target api-framework --path ai-code-framework/scripts/fixtures/pre-handoff/api-bad --checks eol,secrets,docs-dup --allowlist ai-code-framework/scripts/fixtures/pre-handoff/allowlist.fixture.json',
    '```',
    '',
  ].join('\n'));
}

function runGate(fixture, target, checks, allowlist = 'allowlist.fixture.json') {
  return runRaw(['--target', target, '--path', path.join(FX, fixture), '--checks', checks, '--allowlist', path.join(FX, allowlist), '--json']);
}
function runRaw(args) {
  const r = spawnSync(process.execPath, [RUNNER, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  const out = `${r.stdout}${r.stderr}`;
  let json = null; try { json = JSON.parse(r.stdout); } catch { /* reported below */ }
  return { code: r.status, out, json };
}

let failures = 0;
function expect(cond, msg) { console.log(`${cond ? 'ok  ' : 'FAIL'} ${msg}`); if (!cond) failures++; }
const check = (j, c) => j?.checks.find((x) => x.check === c);
const has = (j, c, pred) => (check(j, c)?.findings || []).some(pred);

function listFiles(root) {
  const out = [];
  const walk = (d) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const f = path.join(d, e.name); if (e.isDirectory()) walk(f); else out.push(path.relative(root, f).split(path.sep).join('/')); } };
  if (fs.existsSync(root)) walk(root);
  return out.sort();
}
function sameTree(a, b) { // byte compare; .env* / secrets.json / *.pfx|pem|key compared by name only (never opened)
  const fa = listFiles(a); const fb = listFiles(b);
  if (fa.join('|') !== fb.join('|')) return false;
  return fa.every((rel) => SECRET_FILE_RE.some((r) => r.test(path.posix.basename(rel))) || fs.readFileSync(path.join(a, rel)).equals(fs.readFileSync(path.join(b, rel))));
}

writeFixtures(FX);
console.log(`fixtures written to ${FX}`);
if (WRITE_COMMITTED) { writeFixtures(COMMITTED); console.log(`committed fixtures rewritten: ${COMMITTED}`); }
expect(sameTree(FX, COMMITTED), 'F-06: committed scripts/fixtures/pre-handoff/ is byte-identical to the generated temp copy (not rewritten by the self-test)');

// api-bad: secrets, CRLF/LF mismatch, BOM, mixed, final newline, duplicate paragraph
let r = runGate('api-bad', 'api-framework', 'eol,secrets,docs-dup');
expect(r.code === 1 && r.json?.gate === 'fail', 'api-bad: gate fails (exit 1)');
expect(!/PLANTED/.test(r.out), 'api-bad: no planted value appears in the output');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.json' && f.key === 'ConnectionStrings.LoginConnection' && f.rule === 'secret-connection-string-password'), 'secrets S1: appsettings ConnectionStrings.LoginConnection Password= reported');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.json' && f.key === 'Jwt.Secret'), 'secrets S2: Jwt.Secret reported');
expect(has(r.json, 'secrets', (f) => f.file === 'LoginDbContextFactory.cs' && f.line === 4), 'secrets S3: C# fallback connection string reported with file:line');
expect(has(r.json, 'secrets', (f) => f.file === 'notes.md' && f.rule === 'secret-private-key'), 'secrets: private key block in docs reported');
expect(!has(r.json, 'secrets', (f) => /Issuer|Audience/.test(f.key || '')), 'secrets S4: Jwt.Issuer / Jwt.Audience not reported');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.Commented.json' && f.key === 'Jwt.Secret' && f.rule === 'secret-json-credential' && f.line === 6), 'secrets F-01: Jwt.Secret in a JSON file with comments and trailing commas reported at line 6');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.Broken.json' && f.rule === 'secrets-json-unparsed'), 'secrets F-01: unparseable JSON fails with secrets-json-unparsed');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.Broken.json' && f.rule === 'secret-code-literal' && f.line === 3), 'secrets F-01: unparseable JSON still gets the line rules (Secret literal at line 3)');
expect(has(r.json, 'secrets', (f) => f.file === 'appsettings.Caps.json' && f.key === 'Api.ApiKey'), 'secrets F-02: ALL_CAPS value under a credential key reported');
expect(check(r.json, 'secrets')?.findings.length === 8, 'secrets: exactly 8 findings (nothing else)');
expect(['.env.local', 'cert.pfx', 'secrets.json'].every((p) => check(r.json, 'secrets')?.notes.some((n) => n.endsWith(p))), 'secrets S6: .env.local, secrets.json, *.pfx listed as skipped by pattern');
expect(!JSON.stringify(r.json).includes('bin/Release'), 'eol/secrets S4: bin/ output excluded');
expect(has(r.json, 'eol', (f) => f.file === 'LfFile.cs' && /expected crlf, found lf/.test(f.detail)), 'eol S2: LF file in a CRLF target reported');
expect(has(r.json, 'eol', (f) => f.file === 'Bom.cs' && f.rule === 'eol-bom'), 'eol S3: BOM reported');
expect(has(r.json, 'eol', (f) => f.file === 'Mixed.cs' && /mixed/.test(f.detail)), 'eol S3: mixed CRLF / LF reported');
expect(has(r.json, 'eol', (f) => f.file === 'NoNewline.cs' && /no final newline/.test(f.detail)), 'eol S3: missing final newline reported');
expect(!has(r.json, 'eol', (f) => f.file.startsWith('.env')), 'eol S4: .env* not reported');
const dup = check(r.json, 'docs-dup')?.findings || [];
expect(dup.length === 1 && dup[0].locations.map((l) => l.file).sort().join(',') === 'README.md,docs/setup.md', 'docs-dup S1+S3: one duplicate (wrapped, different case) across README.md and docs/setup.md');
expect(dup.length === 1 && /^"The pre-handoff gate runs every mechanical check before the implementing \.\.\."$/.test(dup[0].detail), 'docs-dup S1: first 10 words shown; S2: short sentence and code fence not reported');
expect(r.json?.targets['api-framework']?.note === 'not a git repo: working tree scanned', 'secrets S7: "not a git repo: working tree scanned"');

// api-good: false positives pass; allowlisted key passes
r = runGate('api-good', 'api-framework', 'eol,secrets,docs-dup');
expect(r.code === 0 && r.json?.gate === 'pass', 'api-good: gate passes (exit 0) - env / request / Issuer / prose / empty Secret not reported');
expect(!has(r.json, 'secrets', (f) => f.file === 'appsettings.Development.json'), 'secrets F-01/F-02: commented JSON with a // URL and ${NAME} / %NAME% / $(NAME) references passes');
expect((r.json?.warnings || []).length === 0 && (r.json?.problems || []).length === 0, 'allowlist F-03: no unused-entry report when every entry that can be judged matched');
expect((check(r.json, 'secrets')?.allowlisted || []).some((f) => f.key === 'SigningKey'), 'secrets S5: allowlisted entry reported as allowlisted');

// expired allowlist entry fails
r = runGate('api-good', 'api-framework', 'secrets', 'allowlist.expired.json');
expect(r.code === 1 && has(r.json, 'secrets', (f) => f.rule === 'allowlist-expired'), 'secrets S5: expired allowlist entry fails and is named');

// nextjs-bad: lint error, type error, CRLF in an LF target, BOM, duplicate paragraph, secret literal
r = runGate('nextjs-bad', 'nextjs', 'lint,typecheck,eol,secrets,docs-dup');
expect(r.code === 1 && r.json?.gate === 'fail', 'nextjs-bad: gate fails (exit 1)');
expect(!/PLANTED/.test(r.out), 'nextjs-bad: no planted value appears in the output');
expect(has(r.json, 'lint', (f) => f.file === 'bad-lint.js' && f.rule === 'lint:no-debugger' && f.line === 2), 'lint S2: error fails with file, line and rule');
expect(check(r.json, 'lint')?.counts.warnings === 1 && !has(r.json, 'lint', (f) => f.file === 'warn-only.js'), 'lint S3: warning counted, not failed (D3)');
expect(has(r.json, 'typecheck', (f) => f.file === 'type-error.ts' && f.line === 1), 'typecheck S4: type error fails with file and line');
expect(has(r.json, 'eol', (f) => f.file === 'crlf.ts' && /expected lf, found crlf/.test(f.detail)), 'eol S2: CRLF file in an LF target reported');
expect(has(r.json, 'eol', (f) => f.file === 'README.md' && f.rule === 'eol-bom'), 'eol S3: BOM reported (LF target)');
expect((check(r.json, 'docs-dup')?.findings || []).length === 1, 'docs-dup: README.md / AGENTS.md duplicate reported');
expect(has(r.json, 'secrets', (f) => f.file === 'api-client.ts' && f.key === 'apiKey' && f.rule === 'secret-code-literal'), 'secrets: credential literal in TS reported');
expect(has(r.json, 'secrets', (f) => f.file === 'caps-token.ts' && f.key === 'apiToken'), 'secrets F-02: ALL_CAPS literal assigned to a credential name in code reported');
expect(!has(r.json, 'lint', (f) => f.file.startsWith('e2e/')), 'D11 F-07: e2e/ not linted (debugger in e2e/debug.js not reported)');
expect(has(r.json, 'secrets', (f) => f.file === 'e2e/support/login.ts' && f.key === 'testerPassword'), 'D11 F-07: e2e/ scanned for secrets (literal in e2e/support/login.ts reported)');
expect(['lint', 'typecheck', 'eol', 'secrets', 'docs-dup'].every((c) => check(r.json, c)), 'runner S2: every check still runs and reports when one fails');

// nextjs-good: everything passes; mirror pair allowlisted
r = runGate('nextjs-good', 'nextjs', 'lint,typecheck,eol,secrets,docs-dup');
expect(r.code === 0 && r.json?.gate === 'pass', 'nextjs-good: gate passes (exit 0)');
expect((check(r.json, 'docs-dup')?.allowlisted || []).length === 1, 'docs-dup S4: allowlisted mirror pair passes and is reported as allowlisted');

// F-07: failing unit run
r = runGate('nextjs-unit-fail', 'nextjs', 'unit');
expect(r.code === 1 && has(r.json, 'unit', (f) => f.rule === 'unit-failed'), 'unit F-07: failing unit tests fail the gate (unit-failed)');
expect(check(r.json, 'unit')?.counts.failed === 1 && check(r.json, 'unit')?.counts.passed === 2, 'unit F-07: failed / passed counts parsed (1 failed, 2 passed)');

// F-07: allowlist schema problems
r = runGate('api-good', 'api-framework', 'secrets', 'allowlist.schema-bad.json');
expect(r.code === 1 && r.json?.gate === 'fail', 'allowlist F-07: schema problems fail the gate');
expect((r.json?.problems || []).some((p) => /entries\[0\]: must not contain a value/.test(p)), 'allowlist F-07: entry with a value reported');
expect((r.json?.problems || []).some((p) => /entries\[1\]: missing expires/.test(p)), 'allowlist F-07: entry without expires reported');
expect(!/PLANTED/.test(r.out), 'allowlist F-07: the value in the bad entry is not printed');

// F-03: unused, unexpired entries
r = runGate('api-good', 'api-framework', 'secrets,docs-dup', 'allowlist.unused.json');
expect(r.code === 1 && (r.json?.problems || []).some((p) => /entries\[2\].*Gone\.cs.*matched nothing/.test(p)), 'allowlist F-03: unused secret-* entry fails the gate and is named');
expect((r.json?.warnings || []).some((p) => /entries\[3\].*docs-dup.*matched nothing/.test(p)) && !(r.json?.problems || []).some((p) => /entries\[3\]/.test(p)), 'allowlist F-03: unused docs-dup entry is a warning, not a failure');
expect(!(r.json?.warnings || []).concat(r.json?.problems || []).some((p) => /entries\[1\]/.test(p)), 'allowlist F-03: entry for a target whose check did not run is not judged');
r = runRaw(['--target', 'api-framework', '--path', path.join(FX, 'api-good'), '--checks', 'secrets', '--allowlist', path.join(FX, 'allowlist.unused.json')]);
expect(/WARNING allowlist entries\[3\]/.test(r.out) || /PROBLEM allowlist entries\[2\]/.test(r.out), 'allowlist F-03: text output lists unused entries');

// D11 F-07: the real UI config ignores e2e/ for lint and typecheck
try {
  const { ESLint } = createRequire(path.join(UI_DIR, 'package.json'))('eslint');
  const eslint = new ESLint({ cwd: UI_DIR });
  expect(await eslint.isPathIgnored(path.join(UI_DIR, 'e2e', 'support', 'fixture.ts')) && !(await eslint.isPathIgnored(path.join(UI_DIR, 'src', 'fixture.ts'))), 'D11 F-07: real UI eslint config ignores e2e/** and lints src/');
} catch (e) { expect(false, `D11 F-07: real UI eslint config could not be loaded (${e.message})`); }
const uiTsconfig = JSON.parse(fs.readFileSync(path.join(UI_DIR, 'tsconfig.json'), 'utf8'));
expect((uiTsconfig.exclude || []).includes('e2e'), 'D11 F-07: real UI tsconfig excludes e2e');
expect(!(uiTsconfig.include || []).some((p) => /^\.next-(?!test\/)/.test(p)), 'F-05: real UI tsconfig has no scratch .next-* build-dir includes (only .next/ and .next-test/)');

// F-07: --feature runs only touched targets (secrets always on both)
const HF = path.join(OUT, 'handoff');
fs.mkdirSync(HF, { recursive: true });
const manifest = (api, ui) => `---\nfeature: selftest\nimplementation:\n  api:${api ? '\n    - path: "Program.cs"\n      change: modified' : ' []'}\n  ui:${ui ? '\n    - path: "README.md"\n      change: modified' : ' []'}\n  migrations: []\n  tests: []\n---\n\n# Handoff\n`;
fs.writeFileSync(path.join(HF, 'api-only.md'), manifest(true, false));
r = runRaw(['--target', 'all', '--feature', path.join(HF, 'api-only.md'), '--checks', 'eol,secrets', '--json']);
const pairs = (j) => (j?.checks || []).map((c) => `${c.check}:${c.target}`).sort().join(',');
expect(pairs(r.json) === 'eol:api-framework,secrets:api-framework,secrets:nextjs', `--feature F-07: api-only manifest -> eol on api-framework only, secrets on both (got ${pairs(r.json)})`);
fs.writeFileSync(path.join(HF, 'empty.md'), manifest(false, false));
r = runRaw(['--target', 'all', '--feature', path.join(HF, 'empty.md'), '--checks', 'eol,secrets', '--json']);
expect(pairs(r.json) === 'eol:api-framework,eol:nextjs,secrets:api-framework,secrets:nextjs', '--feature F-07: empty manifest -> every target runs');

// F-07: --record against a temp handoff copy
const recordFile = path.join(HF, 'record.md');
const testingBlock = 'testing:\n  stage: not-started   # Test Bot owns this\n  results: []\n';
const recordBefore = `---\nfeature: selftest\ncode:\n  verification:          # build / test / lint lines\n    - "dotnet build -> 0 errors"\n    - "pre-handoff: old line from an earlier run"\n  pre_handoff_gate: fail          # pass | fail\n  pre_handoff_gate_at: 2020-01-01T00:00:00+00:00\n${testingBlock}---\n\n# Handoff\n`;
fs.writeFileSync(recordFile, recordBefore);
r = runRaw(['--target', 'all', '--checks', 'eol', '--record', recordFile]);
expect(r.code === 2 && fs.readFileSync(recordFile, 'utf8') === recordBefore, '--record F-07: refused (exit 2, file untouched) for a partial run (--checks)');
if (SKIP_RECORD) console.log('skip --record full run (--skip-record)');
else {
  r = runRaw(['--target', 'all', '--record', recordFile]);
  const after = fs.readFileSync(recordFile, 'utf8');
  const gateLine = (after.match(/^ {2}pre_handoff_gate: (\w+)\s+# pass \| fail$/m) || [])[1];
  expect([0, 1].includes(r.code) && gateLine === (r.code === 0 ? 'pass' : 'fail'), `--record F-07: code.pre_handoff_gate written with its comment and matches the exit code (${gateLine}, exit ${r.code})`);
  expect(/^ {2}pre_handoff_gate_at: \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d$/m.test(after) && !after.includes('2020-01-01T00:00:00'), '--record F-07: code.pre_handoff_gate_at refreshed (ISO 8601 with offset)');
  expect(after.includes('    - "dotnet build -> 0 errors"') && !after.includes('old line from an earlier run') && /- "pre-handoff: secrets nextjs -> /.test(after) && /- "pre-handoff: unit api-framework -> /.test(after), '--record F-07: other verification lines kept, old pre-handoff lines replaced by this run');
  expect(after.includes(testingBlock) && after.endsWith('---\n\n# Handoff\n') && !after.includes('\r'), '--record F-07: testing section, body and LF endings unchanged');
  expect(!/PLANTED/.test(r.out + after), '--record F-07: nothing planted printed or recorded');
}

// ---------------------------------------------------------------- --probe (read-only reviewer mode)
// Probe fixtures live only in the temp folder (not in the committed fixtures/pre-handoff/ copy). Every probe run goes
// through a preload guard that logs any child_process call, any fs write / mkdir / rm, and any read of a
// secret-pattern file; the tree's sha256 + mtime manifest is compared before and after.
const PX = path.join(OUT, 'probe');
const probeFixtures = {
  'probe-nextjs': {
    'bad-utf8.ts': Buffer.concat([Buffer.from('export const a = 1;\n'), Buffer.from([0xc3, 0x28]), Buffer.from('\n')]),
    'bom.ts': `${BOM}export const b = 1;\n`,
    'mixed.ts': 'export const m = 1;\nexport const n = 2;\r\nexport const o = 3;\n',
    'lone-cr.ts': 'export const c = 1;\nexport const d = 2;\rexport const e = 3;\n',
    'changed.ts': 'export const changed = 1;\n',
    'redirect-bad.ts': [
      "const from = searchParams.get('from');",
      'router.push(from);', // 2: variable assigned from a source
      'export function go(returnUrl: string) { window.location.href = returnUrl; }', // 3: return-URL parameter
      "export const mw = () => NextResponse.redirect(new URL(req.nextUrl.searchParams.get('next') ?? '/', req.url));", // 4: source in the expression
      'const target = from;',
      'redirect(target);', // 6: chain of two variables
      '',
    ].join('\n'),
    'redirect-guarded.ts': [
      "const from = safeRedirectPath(searchParams.get('from'));",
      'router.push(from);', // guard in the variable chain
      "router.replace(isSafeRedirect(next) ? next : '/');", // guard in the expression
      'router.push(`/projects/${params.id}`);', // fixed path prefix
      "redirect('/login');", // literal
      'if (isSafeReturn(next)) router.push(next);', // guard on the sink line
      '// router.push(searchParams.get("from")) in a comment',
      'const message = "router.push(searchParams.get(1))";', // in a string
      'return NextResponse.redirect(new URL(`/login?from=${encodeURIComponent(path)}`, req.url));', // fixed path prefix
      '',
    ].join('\n'),
    '.env.local': 'Password=PLANTED-probe-env-0101\n', // never opened
    'node_modules/pkg/index.js': "router.push(searchParams.get('x'));\n", // excluded folder
    '.next/server/page.js': "router.push(searchParams.get('x'));\n", // excluded folder
  },
  'probe-api': {
    'AccountController.cs': CRLF([
      'public class AccountController : Controller',
      '{',
      '    public IActionResult Back() => Redirect(Request.Query["returnUrl"]);', // 3
      '    public IActionResult Login(string returnUrl) => Redirect(returnUrl);', // 4
      '    public IActionResult Local(string returnUrl) => LocalRedirect(returnUrl);',
      '    public IActionResult Checked(string returnUrl)',
      '    {',
      '        if (Url.IsLocalUrl(returnUrl))',
      '            return Redirect(returnUrl);',
      '        return Redirect("/");',
      '    }',
      '    private const string Path = @"C:\\temp\\";',
      '}',
      '',
    ].join('\n')),
    'secrets.json': '{ "Jwt": { "Secret": "PLANTED-probe-secrets-0102" } }', // never opened
  },
  'probe-clean': {
    'ok.ts': "export const ok = (p: string) => router.push(`/projects/${p}`);\n",
    'README.md': '# Clean\n',
  },
};
for (const [name, files] of Object.entries(probeFixtures)) {
  for (const [rel, content] of Object.entries(files)) { const f = path.join(PX, name, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, content); }
}
fs.writeFileSync(path.join(PX, 'baseline.json'), JSON.stringify({ version: 1, files: { 'changed.ts': { eol: 'crlf' }, 'mixed.ts': { eol: 'lf' } } }, null, 2) + '\n');
fs.writeFileSync(path.join(PX, 'safe-sample.mjs'), [
  'export function safeRedirectPath(raw) {',
  "  if (typeof raw !== 'string' || /[\\u0000-\\u001f\\u007f\\\\]/.test(raw)) return '/';",
  "  if (!raw.startsWith('/') || raw.startsWith('//')) return '/';",
  "  let u; try { u = new URL(raw, 'http://local.invalid'); } catch { return '/'; }",
  "  if (u.origin !== 'http://local.invalid') return '/';",
  '  const out = u.pathname + u.search + u.hash;',
  "  let d = out; for (let i = 0; i < 2; i++) { try { d = decodeURIComponent(d); } catch { return '/'; } if (/^\\/[\\/\\\\]/.test(d) || /[\\u0000-\\u001f]/.test(d) || new URL(d.replace(/\\\\/g, '/'), 'http://local.invalid').pathname.startsWith('//')) return '/'; }",
  "  return out.startsWith('//') ? '/' : out;",
  '}',
  '',
].join('\n'));
fs.writeFileSync(path.join(PX, 'unsafe-sample.mjs'), [
  '// the F-01 shape: checks the raw value, then resolves dot segments, which can produce //host',
  'export function safeRedirectPath(raw) {',
  "  if (typeof raw !== 'string' || !raw.startsWith('/') || raw.startsWith('//')) return '/';",
  "  const u = new URL(raw, 'http://local.invalid');",
  '  return u.pathname + u.search + u.hash;',
  '}',
  '',
].join('\n'));
const GUARD = path.join(OUT, 'probe-guard.mjs');
fs.writeFileSync(GUARD, [
  "import { createRequire, syncBuiltinESMExports } from 'node:module';",
  'const require = createRequire(import.meta.url);',
  "const cp = require('node:child_process'); const fs = require('node:fs');",
  "const hit = (what) => process.stderr.write(`PROBE-GUARD ${what}\\n`);",
  "for (const k of ['spawn', 'spawnSync', 'exec', 'execSync', 'execFile', 'execFileSync', 'fork']) { const o = cp[k]; cp[k] = function (...a) { hit(`child_process.${k}`); return o.apply(this, a); }; }",
  "for (const k of ['writeFileSync', 'writeFile', 'appendFileSync', 'appendFile', 'mkdirSync', 'mkdir', 'mkdtempSync', 'rmSync', 'rm', 'rmdirSync', 'unlinkSync', 'unlink', 'renameSync', 'rename', 'copyFileSync', 'cpSync', 'truncateSync', 'utimesSync', 'chmodSync', 'symlinkSync', 'linkSync', 'createWriteStream']) { if (typeof fs[k] === 'function') fs[k] = function () { hit(`fs.${k}`); throw new Error(`probe guard: fs.${k} blocked`); }; }",
  "for (const k of ['writeFile', 'appendFile', 'mkdir', 'rm', 'rmdir', 'unlink', 'rename', 'copyFile', 'cp', 'truncate', 'open']) { if (typeof fs.promises[k] === 'function') { const o = fs.promises[k]; fs.promises[k] = function (...a) { if (k === 'open' && (a[1] === undefined || a[1] === 'r')) return o.apply(this, a); hit(`fs.promises.${k}`); throw new Error('probe guard: blocked'); }; } }",
  "const openSync = fs.openSync; fs.openSync = function (p, flags, ...rest) { if (flags !== undefined && flags !== 'r' && flags !== 0) { hit('fs.openSync(write)'); throw new Error('probe guard: blocked'); } return openSync.call(this, p, flags, ...rest); };",
  "const SECRET = [/^\\.env/i, /^secrets\\.json$/i, /\\.pfx$/i, /\\.pem$/i, /\\.key$/i];",
  "const readFileSync = fs.readFileSync; fs.readFileSync = function (p, ...rest) { const b = typeof p === 'string' ? p.split(/[\\\\/]/).pop() : ''; if (SECRET.some((r) => r.test(b))) hit(`read-secret-pattern-file ${b}`); return readFileSync.call(this, p, ...rest); };",
  'syncBuiltinESMExports();',
  '',
].join('\n'));
function guarded(script, args) {
  const r = spawnSync(process.execPath, ['--import', pathToFileURL(GUARD).href, script, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  let json = null; try { json = JSON.parse(r.stdout); } catch { /* checked by the caller */ }
  return { code: r.status, out: `${r.stdout}${r.stderr}`, stderr: r.stderr, json, violations: (r.stderr.match(/^PROBE-GUARD .*$/gm) || []) };
}
function treeManifest(root) { // rel -> sha256 + mtime; secret-pattern files by size + mtime only (never opened)
  const out = {};
  const walkT = (d) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const f = path.join(d, e.name); if (e.isDirectory()) walkT(f); else { const st = fs.statSync(f); const rel = path.relative(root, f).split(path.sep).join('/'); out[rel] = `${st.mtimeMs}|${st.size}|${SECRET_FILE_RE.some((x) => x.test(e.name)) ? '-' : crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')}`; } } };
  walkT(root); return JSON.stringify(out);
}
const probeRun = (fixture, target, extra = []) => guarded(RUNNER, ['--probe', '--target', target, '--path', path.join(PX, fixture), ...extra]);
const pf = (j, pred) => (j?.findings || []).some(pred);
const before = treeManifest(PX);

// the guard itself works: a normal (non-probe) unit run is seen spawning
r = guarded(RUNNER, ['--target', 'nextjs', '--path', path.join(FX, 'nextjs-unit-fail'), '--checks', 'unit', '--allowlist', path.join(FX, 'allowlist.fixture.json'), '--json']);
expect(r.violations.some((v) => /child_process\.spawnSync/.test(v)), 'probe guard: control run (non-probe unit check) is detected spawning, so the guard can see spawns');

// refusals
const refusedBefore = treeManifest(PX);
r = probeRun('probe-nextjs', 'nextjs', ['--record', path.join(PX, 'baseline.json')]);
expect(r.code === 2 && /--probe is read-only: it cannot be combined with --record or --fix-eol/.test(r.out), 'probe: --probe --record refused (exit 2, clear message)');
r = probeRun('probe-nextjs', 'nextjs', ['--fix-eol']);
expect(r.code === 2 && /--probe is read-only/.test(r.out), 'probe: --probe --fix-eol refused (exit 2)');
r = guarded(RUNNER, ['--fix-eol', '--baseline-print', '--target', 'nextjs', '--path', path.join(PX, 'probe-nextjs')]);
expect(r.code === 2, 'probe: --baseline-print --fix-eol refused (exit 2)');
r = guarded(RUNNER, ['--target', 'nextjs', '--path', path.join(PX, 'probe-nextjs'), '--baseline', path.join(PX, 'baseline.json')]);
expect(r.code === 2 && /--baseline needs --probe/.test(r.out), 'probe: --baseline without --probe refused (exit 2)');
expect(treeManifest(PX) === refusedBefore, 'probe: refused runs changed nothing (sha256 + mtime manifest identical)');

// LF target: encoding, endings, eol-changed, open-redirect
r = probeRun('probe-nextjs', 'nextjs', ['--json', '--baseline', path.join(PX, 'baseline.json')]);
expect(r.code === 1 && r.json?.mode === 'probe' && r.json?.gate === 'fail', 'probe nextjs: fails (exit 1) on planted findings');
expect(r.violations.length === 0, `probe nextjs: no spawn, no write, no secret-pattern file read (guard saw ${r.violations.length ? r.violations.join('; ') : 'nothing'})`);
expect((r.json?.findings || []).length > 0 && r.json.findings.every((f) => Object.keys(f).sort().join(',') === 'file,line,rule'), 'probe --json: every finding has exactly file, rule, line');
expect(!/PLANTED|searchParams|safeRedirectPath|export const/.test(r.out), 'probe: no line text, values or planted secrets in the output');
expect(pf(r.json, (f) => f.rule === 'utf8-invalid' && f.file === 'bad-utf8.ts' && f.line === 2), 'probe utf8-invalid: bad-utf8.ts first bad line 2');
expect(pf(r.json, (f) => f.rule === 'bom' && f.file === 'bom.ts' && f.line === 1), 'probe bom: bom.ts');
expect(pf(r.json, (f) => f.rule === 'eol-mixed' && f.file === 'mixed.ts' && f.line === 2), 'probe eol-mixed: CRLF + LF in mixed.ts at line 2');
expect(pf(r.json, (f) => f.rule === 'eol-mixed' && f.file === 'lone-cr.ts' && f.line === 2), 'probe eol-mixed: lone CR in lone-cr.ts at line 2');
expect(pf(r.json, (f) => f.rule === 'eol-changed' && f.file === 'changed.ts') && !pf(r.json, (f) => f.rule === 'eol-changed' && f.file === 'mixed.ts'), 'probe eol-changed: changed.ts (baseline crlf, now lf) reported; mixed.ts (still dominant lf) not');
const sinks = (r.json?.findings || []).filter((f) => f.rule === 'open-redirect-sink');
expect(sinks.filter((f) => f.file === 'redirect-bad.ts').map((f) => f.line).join(',') === '2,3,4,6', `probe open-redirect-sink: redirect-bad.ts lines 2,3,4,6 (got ${sinks.filter((f) => f.file === 'redirect-bad.ts').map((f) => f.line).join(',')})`);
expect(!sinks.some((f) => f.file === 'redirect-guarded.ts'), 'probe open-redirect-sink: guarded, literal, prefixed, commented and string cases in redirect-guarded.ts not reported');
expect(!(r.json?.findings || []).some((f) => /node_modules|\.next|\.env/.test(f.file)), 'probe: node_modules/, .next/ and .env* skipped');
expect(r.json?.targets?.nextjs?.skipped_secret_files === 1 && r.json?.summary?.by_rule?.['open-redirect-sink'] === 4, 'probe --json: summary counts (by_rule) and skipped secret-pattern files present');

// CRLF target: C# sinks
r = probeRun('probe-api', 'api-framework', ['--json', '--checks', 'open-redirect,eol-mixed,bom,utf8']);
expect(r.violations.length === 0, 'probe api: no spawn, no write, no secret-pattern file read');
expect((r.json?.findings || []).map((f) => `${f.rule}:${f.line}`).join(',') === 'open-redirect-sink:3,open-redirect-sink:4', `probe api: Redirect(Request.Query[...]) and Redirect(returnUrl) reported; LocalRedirect and Url.IsLocalUrl-guarded not (got ${(r.json?.findings || []).map((f) => `${f.rule}:${f.line}`).join(',')})`);

// clean tree passes; human output gives the same three fields
r = probeRun('probe-clean', 'nextjs', ['--json']);
expect(r.code === 0 && r.json?.gate === 'pass' && r.violations.length === 0, 'probe clean: passes (exit 0), read-only');
r = probeRun('probe-nextjs', 'nextjs');
expect(r.code === 1 && /^ {4}FAIL bom bom\.ts:1$/m.test(r.out) && /^probe -> fail \(/m.test(r.out) && r.violations.length === 0, 'probe text output: "FAIL <rule> <file>:<line>" lines and a probe -> fail summary');

// --baseline-print: manifest to stdout only, then reusable as --baseline
r = guarded(RUNNER, ['--baseline-print', '--target', 'nextjs', '--path', path.join(PX, 'probe-nextjs')]);
expect(r.code === 0 && r.violations.length === 0 && r.json?.files?.['changed.ts']?.eol === 'lf' && /^[0-9a-f]{64}$/.test(r.json?.files?.['changed.ts']?.sha256 || '') && !r.json?.files?.['.env.local'], '--baseline-print: prints { files: { path: { eol, sha256 } } } to stdout, read-only, secret-pattern files left out');
const printed = path.join(OUT, 'baseline-printed.json'); fs.writeFileSync(printed, JSON.stringify(r.json));
r = probeRun('probe-nextjs', 'nextjs', ['--json', '--checks', 'eol-changed', '--baseline', printed]);
expect(r.code === 0 && r.json?.summary?.baseline_hash_changed === 0, '--baseline round trip: an unchanged tree has no eol-changed findings and no hash changes');
const printed16 = path.join(OUT, 'baseline-printed-utf16.json');
fs.writeFileSync(printed16, Buffer.concat([Buffer.from([0xff, 0xfe]), Buffer.from(fs.readFileSync(printed, 'utf8'), 'utf16le')]));
r = probeRun('probe-nextjs', 'nextjs', ['--json', '--checks', 'eol-changed', '--baseline', printed16]);
expect(r.code === 0 && r.json?.summary?.not_in_baseline === 0, '--baseline: a UTF-16LE manifest (Windows PowerShell 5 `>` redirect) is read too');

expect(treeManifest(PX) === before, 'probe: scanned tree unchanged after every probe run (sha256 + mtime manifest identical)');

// probe-redirect against the attack list
const PROBE_REDIRECT = path.join(HERE, 'probe-redirect.mjs');
const attacks = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures', 'redirect-attacks.json'), 'utf8')).attacks;
const cats = new Set(attacks.map((a) => a.category));
expect(['protocol-relative', 'backslash', 'dot-segments', 'encoded', 'scheme', 'control-chars', 'userinfo', 'safe-control'].every((c) => cats.has(c)) && attacks.every((a) => a.id && typeof a.input === 'string' && ['safe', 'reject'].includes(a.expect)), `redirect-attacks.json: ${attacks.length} attacks, every category present, each with id, input and expect`);
expect(['/..//evil.example', '/../..//evil.example', '/.//evil.example', '/a/../..//evil.example', '/%2E%2E//evil.example', '%252F%252Fevil.example', '//good.example@evil.example', '/\t/evil.example', ' javascript:alert(1)'].every((i) => attacks.some((a) => a.input === i && a.expect === 'reject')), 'redirect-attacks.json: Review Bot F-01 dot-segment, encoded, userinfo, tab and leading-space vectors listed as reject');
r = guarded(PROBE_REDIRECT, ['--module', path.join(PX, 'safe-sample.mjs'), '--export', 'safeRedirectPath', '--json']);
expect(r.code === 0 && r.json?.unsafe === 0 && r.json?.safe_controls_over_strict === 0 && r.violations.length === 0, `probe-redirect: safe sample passes every attack, no over-strict control, read-only (unsafe ${r.json?.unsafe}, over-strict ${r.json?.safe_controls_over_strict})`);
expect((r.json?.results || []).every((x) => Object.keys(x).every((k) => ['id', 'category', 'expect', 'verdict', 'over_strict'].includes(k))) && !/evil\.example/.test(r.out), 'probe-redirect --json: results carry id, category, expect and verdict only (no inputs or returned values)');
r = guarded(PROBE_REDIRECT, ['--module', path.join(PX, 'unsafe-sample.mjs'), '--export', 'safeRedirectPath', '--json']);
const unsafeCats = new Set((r.json?.results || []).filter((x) => x.verdict === 'unsafe').map((x) => x.category));
expect(r.code === 1 && unsafeCats.has('dot-segments') && r.violations.length === 0, `probe-redirect: the F-01-shaped sample fails (exit 1) on dot segments (unsafe categories: ${[...unsafeCats].join(', ')})`);
r = guarded(PROBE_REDIRECT, ['--module', path.join(PX, 'safe-sample.mjs'), '--export', 'missing']);
expect(r.code === 2, 'probe-redirect: a missing export is a usage error (exit 2)');

if (!optValue('--out')) fs.rmSync(OUT, { recursive: true, force: true });
console.log(failures ? `\nself-test FAILED (${failures})` : '\nself-test passed');
process.exit(failures ? 1 : 0);
