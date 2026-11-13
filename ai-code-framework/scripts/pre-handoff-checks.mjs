#!/usr/bin/env node
// Pre-handoff gate (pre-handoff-checks plan; tickets T-GATE-002..005). Node 22, no dependencies (D4).
//
//   node ai-code-framework/scripts/pre-handoff-checks.mjs [--target api-framework|nextjs|all]
//        [--feature <work/<feature> folder or its handoff.md>] [--record <handoff.md>] [--json]
//        [--checks lint,typecheck,eol,secrets,docs-dup,unit] [--path <dir>] [--allowlist <file>]
//        [--fix-eol]   (one-off normalisation, T-GATE-002 / D12: line endings, BOM, final newline only)
//        [--probe [--baseline <manifest.json>] [--baseline-print]]   (read-only reviewer scan: no spawns, no writes;
//        findings are file, rule and line only; not with --record or --fix-eol)
//
// Checks per target come from ai-framework.config.yaml `verification.targets` (mirrored in TARGETS below; keep
// the two in step). Exit 0 = every check passed (or every failure is allowlisted), 1 = gate failed, 2 = usage error.
// Never prints a secret value: findings are file:line, key path / identifier and rule id only. Never opens
// .env*, secrets.json, *.pfx, *.pem or *.key (review.scope_exclude); targets without git are scanned as a working
// tree (D14).
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SCRIPTS_DIR = path.dirname(fileURLToPath(import.meta.url));
const FRAMEWORK_ROOT = path.resolve(SCRIPTS_DIR, '..', '..'); // ai-framework/
const DEFAULT_ALLOWLIST = path.join(SCRIPTS_DIR, 'pre-handoff-allowlist.json');
const DOCS_DUP_MIN_WORDS = 25; // D8

// config: verification.targets (D5, D6, D11)
const TARGETS = {
  'api-framework': {
    path: 'ai-code-framework/api/API.Framework',
    eol: 'crlf',
    checks: ['eol', 'secrets', 'docs-dup', 'unit'],
    unit: { cmd: 'dotnet', args: ['test', 'Api.Framework.Tests/Api.Framework.Tests.csproj', '--configuration', 'Release', '--nologo'] },
    manifestKeys: ['api', 'migrations'],
  },
  nextjs: {
    path: 'ai-code-framework/ui/UI.NextJs.Framework',
    eol: 'lf',
    checks: ['lint', 'typecheck', 'eol', 'secrets', 'docs-dup', 'unit'],
    unit: { npmScript: 'test' },
    manifestKeys: ['ui'],
  },
};
const CHECK_ORDER = ['lint', 'typecheck', 'eol', 'secrets', 'docs-dup', 'unit'];

// review.scope_exclude + generated test output listed in the targets' .gitignore files
const EXCLUDED_DIRS = new Set(['bin', 'obj', 'node_modules', 'dist', 'build', 'coverage', 'TestResults', 'artifacts', 'out',
  '.git', '.vs', '.idea', 'playwright-report', 'cucumber-report', 'test-results', '.auth', '.features-gen']);
const EXCLUDED_DIR_RE = [/^\.next/, /^\..*-out$/];
const SECRET_FILE_RE = [/^\.env/i, /^secrets\.json$/i, /\.pfx$/i, /\.pem$/i, /\.key$/i]; // never opened
const EXCLUDED_FILE_RE = [/\.g\.cs$/i, /\.min\.js$/i, /^package-lock\.json$/i];
const CRLF_ALWAYS = /\.(ps1|psm1|psd1|cmd|bat)$/i; // D5
const TEXT_EXT = new Set(['.cs', '.csproj', '.sln', '.slnx', '.props', '.targets', '.json', '.md', '.mdc', '.ts', '.tsx', '.js', '.jsx',
  '.mjs', '.cjs', '.mts', '.cts', '.css', '.scss', '.html', '.yml', '.yaml', '.xml', '.config', '.feature', '.txt',
  '.ps1', '.psm1', '.psd1', '.cmd', '.bat', '.sh', '.http', '.editorconfig', '.gitattributes', '.gitignore']);
const TEXT_NAMES = new Set(['.editorconfig', '.gitattributes', '.gitignore', 'Dockerfile']);

// ---------------------------------------------------------------- args
function parseArgs(argv) {
  const a = { target: 'all', json: false, checks: null, path: null, allowlist: DEFAULT_ALLOWLIST, feature: null, record: null, fixEol: false, probe: false, baseline: null, baselinePrint: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const next = () => { if (i + 1 >= argv.length) usage(`missing value for ${k}`); return argv[++i]; };
    if (k === '--target') a.target = next();
    else if (k === '--json') a.json = true;
    else if (k === '--checks') a.checks = next().split(',').map((s) => s.trim()).filter(Boolean);
    else if (k === '--path') a.path = path.resolve(next());
    else if (k === '--allowlist') a.allowlist = path.resolve(next());
    else if (k === '--feature') a.feature = path.resolve(FRAMEWORK_ROOT, next());
    else if (k === '--record') a.record = path.resolve(FRAMEWORK_ROOT, next());
    else if (k === '--fix-eol') a.fixEol = true;
    else if (k === '--probe') a.probe = true;
    else if (k === '--baseline') a.baseline = path.resolve(next());
    else if (k === '--baseline-print') { a.baselinePrint = true; a.probe = true; }
    else if (k === '-h' || k === '--help') usage();
    else usage(`unknown argument ${k}`);
  }
  if (a.target !== 'all' && !TARGETS[a.target]) usage(`unknown target ${a.target}`);
  if (a.path && a.target === 'all') usage('--path needs --target api-framework|nextjs (the rule set to apply)');
  if (a.probe && (a.record || a.fixEol)) usage('--probe is read-only: it cannot be combined with --record or --fix-eol');
  if (a.baseline && !a.probe) usage('--baseline needs --probe');
  if (a.checks) for (const c of a.checks) if (!(a.probe ? PROBE_CHECKS : CHECK_ORDER).includes(c)) usage(`unknown check ${c}${a.probe ? ` (probe checks: ${PROBE_CHECKS.join(',')})` : ''}`);
  return a;
}
function usage(msg) {
  if (msg) console.error(`pre-handoff-checks: ${msg}`);
  console.error('usage: node pre-handoff-checks.mjs [--target api-framework|nextjs|all] [--feature <dir|handoff.md>] [--record <handoff.md>] [--json] [--checks a,b] [--path <dir>] [--allowlist <file>] [--fix-eol]');
  console.error('       node pre-handoff-checks.mjs --probe [--target api-framework|nextjs|all] [--path <dir>] [--json] [--checks utf8,bom,eol-mixed,eol-changed,open-redirect] [--baseline <manifest.json>] [--baseline-print]');
  console.error('       --probe is read-only (no child processes, no writes; refuses --record and --fix-eol); findings are file, rule and line only. See scripts/README.md.');
  process.exit(2);
}

// ---------------------------------------------------------------- files
const posix = (p) => p.split(path.sep).join('/');
function isSecretFile(name) { return SECRET_FILE_RE.some((r) => r.test(name)); }
function walk(root) {
  const files = []; const skippedSecretFiles = [];
  const stack = [root];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const full = path.join(dir, e.name);
      if (e.isSymbolicLink()) continue;
      if (e.isDirectory()) {
        if (EXCLUDED_DIRS.has(e.name) || EXCLUDED_DIR_RE.some((r) => r.test(e.name))) continue;
        stack.push(full);
      } else if (e.isFile()) {
        if (isSecretFile(e.name)) { skippedSecretFiles.push(posix(path.relative(root, full))); continue; } // never opened
        if (EXCLUDED_FILE_RE.some((r) => r.test(e.name))) continue;
        files.push(full);
      }
    }
  }
  files.sort();
  return { files, skippedSecretFiles: skippedSecretFiles.sort() };
}
function isText(file) {
  const base = path.basename(file);
  return TEXT_NAMES.has(base) || TEXT_EXT.has(path.extname(base).toLowerCase());
}
function readText(file) {
  const buf = fs.readFileSync(file);
  const bom = buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf;
  return { buf, bom, text: buf.toString('utf8', bom ? 3 : 0) };
}
function isGitRepo(dir) {
  let d = dir;
  for (;;) { if (fs.existsSync(path.join(d, '.git'))) return true; const p = path.dirname(d); if (p === d) return false; d = p; }
}

// ---------------------------------------------------------------- allowlist (D13)
function loadAllowlist(file) {
  if (!fs.existsSync(file)) return { entries: [], problems: [`allowlist not found: ${file}`] };
  let data;
  try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return { entries: [], problems: [`allowlist is not valid JSON: ${e.message}`] }; }
  const entries = Array.isArray(data.entries) ? data.entries : [];
  const problems = [];
  const today = new Date().toISOString().slice(0, 10);
  entries.forEach((e, i) => {
    e._id = `entries[${i}]`;
    for (const f of ['rule', 'reason', 'owner', 'expires']) if (!e[f]) problems.push(`allowlist ${e._id}: missing ${f}`);
    if (!e.path && !e.paths) problems.push(`allowlist ${e._id}: missing path / paths`);
    if (e.value !== undefined) problems.push(`allowlist ${e._id}: must not contain a value`);
    e._expired = !!e.expires && String(e.expires) < today;
    e._used = false;
  });
  return { entries, problems };
}
function allowlisted(allow, targetName, finding) {
  for (const e of allow.entries) {
    if (e.target && e.target !== targetName) continue;
    if (e.rule !== finding.rule) continue;
    if (finding.rule === 'docs-dup') {
      const set = new Set(e.paths || [e.path]);
      if (!finding.locations.every((l) => set.has(l.file))) continue;
    } else {
      if (e.path !== finding.file) continue;
      if (e.key && e.key !== finding.key) continue;
      if (e.line_hint && !(finding._lineText || '').includes(e.line_hint)) continue;
    }
    e._used = true;
    return e;
  }
  return null;
}

// ---------------------------------------------------------------- eol (T-GATE-002)
function expectedEol(target, rel) { return CRLF_ALWAYS.test(rel) ? 'crlf' : target.eol; }
function eolProblems(text, bom, want) {
  const crlf = (text.match(/\r\n/g) || []).length;
  const lf = (text.match(/(?<!\r)\n/g) || []).length;
  const cr = (text.match(/\r(?!\n)/g) || []).length;
  const out = [];
  if (bom) out.push('bom');
  if ((crlf && lf) || cr) out.push(`mixed (crlf ${crlf}, lf ${lf}${cr ? `, cr ${cr}` : ''})`);
  else if (want === 'crlf' && lf) out.push('expected crlf, found lf');
  else if (want === 'lf' && crlf) out.push('expected lf, found crlf');
  if (text.length && !text.endsWith('\n')) out.push('no final newline');
  return out;
}
function normalise(text, want) {
  let t = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  if (t.length && !t.endsWith('\n')) t += '\n';
  return want === 'crlf' ? t.replace(/\n/g, '\r\n') : t;
}
function checkEol(ctx) {
  const findings = []; let scanned = 0;
  for (const f of ctx.textFiles) {
    const rel = ctx.rel(f); const { text, bom } = readText(f); scanned++;
    const want = expectedEol(ctx.target, rel);
    for (const p of eolProblems(text, bom, want)) findings.push({ rule: p === 'bom' ? 'eol-bom' : 'eol', file: rel, line: 0, detail: p });
  }
  return { findings, counts: { files: scanned } };
}
function fixEol(ctx) {
  const changed = {}; let total = 0; const verifyFailures = [];
  for (const f of ctx.textFiles) {
    const rel = ctx.rel(f); const { buf, text, bom } = readText(f);
    const want = expectedEol(ctx.target, rel);
    const out = normalise(text, want);
    if (!bom && out === text) continue;
    // byte-level check (S5): identical once endings are normalised and the BOM stripped
    const a = normalise(text, 'lf'); const b = normalise(out, 'lf');
    if (a !== b) { verifyFailures.push(rel); continue; }
    fs.writeFileSync(f, out, 'utf8');
    const back = fs.readFileSync(f);
    if (back.toString('utf8') !== out || buf.equals(back)) { verifyFailures.push(rel); continue; }
    const ext = path.extname(rel).toLowerCase() || path.basename(rel);
    changed[ext] = (changed[ext] || 0) + 1; total++;
  }
  return { total, changed, verifyFailures };
}

// ---------------------------------------------------------------- secrets (T-GATE-003)
const CRED_NAME = /(password|passwd|pwd|secret|token|apikey|api_key|signingkey|signing_key|privatekey|private_key|clientsecret|client_secret|accesskey|access_key|connectionstring)$/i;
const CRED_NAME_EXCLUDE = /(env|envvar|envname|setting|settings|name|names|header|route|path|url|label|placeholder|message|field|pattern|policy|permission|type|id|ids|minutes|days|hours|seconds|length|hint|key_env|var)$/i;
// Placeholders and explicit references only: <value>, ${NAME}, %NAME%, $(NAME), env:NAME, {name}, ***, xxx. A bare
// ALL_CAPS value is NOT treated as an env-var name (review F-02): a credential key holding one is reported.
const PLACEHOLDER = /^(<[^>]*>|\$\{[^}]*\}|%[^%]+%|\$\([^)]*\)|env:[A-Za-z_][\w.]*|\{[^}]*\}|\*+|x+|changeme|todo|null|undefined|none)$/i;
const CONN_PWD = /(?:^|[;\s"'`])(password|pwd)\s*=\s*([^;"'`\s]*)/gi;
const PRIVATE_KEY = /-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----/;
const CODE_EXT = new Set(['.cs', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.mts', '.cts']);
const DOC_EXT = new Set(['.md', '.mdc', '.txt', '.yml', '.yaml', '.xml', '.config', '.feature', '.http']);

function connPasswordValues(s) {
  const out = []; CONN_PWD.lastIndex = 0; let m;
  while ((m = CONN_PWD.exec(s))) {
    const v = m[2];
    if (v && !PLACEHOLDER.test(v) && !/^[{$<%]/.test(v)) out.push(m[1]);
  }
  return out;
}
function credentialValue(v) {
  if (typeof v !== 'string') return false;
  const s = v.trim();
  return s.length > 0 && !PLACEHOLDER.test(s);
}
function lineOf(text, index) { let n = 1; for (let i = 0; i < index && i < text.length; i++) if (text.charCodeAt(i) === 10) n++; return n; }
function lineTextAt(lines, n) { return lines[n - 1] || ''; }

// JSONC -> JSON (review F-01): blanks // and /* */ comments and trailing commas outside strings. Same length, newlines
// kept, so positions and line numbers still match the original text.
function stripJsonc(text) {
  const out = text.split(''); const n = text.length; let lastSig = -1; let i = 0;
  while (i < n) {
    const c = text[i];
    if (c === '"') {
      let j = i + 1;
      while (j < n && text[j] !== '"' && text[j] !== '\n') j += text[j] === '\\' ? 2 : 1;
      lastSig = Math.min(j, n - 1); i = j + 1; continue;
    }
    if (c === '/' && text[i + 1] === '/') { while (i < n && text[i] !== '\n' && text[i] !== '\r') out[i++] = ' '; continue; }
    if (c === '/' && text[i + 1] === '*') {
      const close = text.indexOf('*/', i + 2); const stop = close < 0 ? n : close + 2;
      for (; i < stop; i++) if (text[i] !== '\n' && text[i] !== '\r') out[i] = ' ';
      continue;
    }
    if ((c === '}' || c === ']') && lastSig >= 0 && text[lastSig] === ',') out[lastSig] = ' ';
    if (!/\s/.test(c)) lastSig = i;
    i++;
  }
  return out.join('');
}
function scanJson(rel, original, findings) {
  let data;
  const lines = original.split(/\r?\n/);
  const text = stripJsonc(original);
  try { data = JSON.parse(text); } catch (e) {
    // Still unparseable: fail (the credential-key walk could not run) and fall back to the line rules. The parser
    // message is not printed (it can quote file content); only the position is used.
    const pos = /position (\d+)/.exec(e.message);
    findings.push({ rule: 'secrets-json-unparsed', file: rel, line: pos ? lineOf(text, Number(pos[1])) : 0, key: null, detail: 'not valid JSON after removing comments and trailing commas: credential keys not checked' });
    scanLines(rel, text, findings, 'code');
    return;
  }
  const cursor = {}; // per key: next search position, so repeated keys map to later lines
  const locate = (key) => {
    const re = new RegExp(`"${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"\\s*:`, 'g');
    re.lastIndex = cursor[key] || 0; const m = re.exec(text);
    if (!m) return 0; cursor[key] = m.index + 1; return lineOf(text, m.index);
  };
  const visit = (node, keyPath) => {
    if (Array.isArray(node)) { node.forEach((v, i) => visit(v, `${keyPath}[${i}]`)); return; }
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) {
        const kp = keyPath ? `${keyPath}.${k}` : k;
        if (typeof v === 'string') {
          const line = locate(k);
          if (connPasswordValues(v).length) findings.push({ rule: 'secret-connection-string-password', file: rel, line, key: kp, _lineText: lineTextAt(lines, line) });
          else if (CRED_NAME.test(k) && !CRED_NAME_EXCLUDE.test(k) && credentialValue(v)) findings.push({ rule: 'secret-json-credential', file: rel, line, key: kp, _lineText: lineTextAt(lines, line) });
          else if (PRIVATE_KEY.test(v)) findings.push({ rule: 'secret-private-key', file: rel, line, key: kp, _lineText: lineTextAt(lines, line) });
        } else { if (v && typeof v === 'object') locate(k); visit(v, kp); }
      }
    }
  };
  visit(data, '');
}
// string literal assigned to a credential-like name: name = "x" | name: 'x' | name => `x` | "name": "x"
const ASSIGN_RE = /["']?\b([A-Za-z_$][\w$]*)["']?\s*(?:=>|[:=])\s*[@$]?(["'`])((?:\\.|(?!\2).)*)\2/g;
function scanLines(rel, text, findings, kind) {
  const lines = text.split(/\r?\n/);
  lines.forEach((ln, i) => {
    const line = i + 1;
    if (PRIVATE_KEY.test(ln)) findings.push({ rule: 'secret-private-key', file: rel, line, key: null, _lineText: ln });
    // Password= / Pwd= with a non-empty value: code only inside string literals; docs anywhere
    if (kind === 'code') {
      const lits = ln.match(/(["'`])(?:\\.|(?!\1).)*\1/g) || [];
      if (lits.some((l) => connPasswordValues(l.slice(1, -1)).length)) findings.push({ rule: 'secret-connection-string-password', file: rel, line, key: null, _lineText: ln });
    } else if (connPasswordValues(ln).length) {
      findings.push({ rule: 'secret-connection-string-password', file: rel, line, key: null, _lineText: ln });
    }
    if (kind === 'code') {
      ASSIGN_RE.lastIndex = 0; let m;
      while ((m = ASSIGN_RE.exec(ln))) {
        const name = m[1]; const value = m[3];
        if (!CRED_NAME.test(name) || CRED_NAME_EXCLUDE.test(name)) continue;
        if (!credentialValue(value) || /\$\{|\{[A-Za-z_]/.test(value)) continue; // interpolation reads a variable
        if (/\s/.test(value)) continue; // prose / user-facing message, not a credential
        if (ln.slice(0, m.index).trimEnd().endsWith('?')) continue; // ternary `cond ? "a" : "b"`, not `name: value`
        findings.push({ rule: 'secret-code-literal', file: rel, line, key: name, _lineText: ln });
      }
    }
  });
}
function checkSecrets(ctx) {
  const findings = []; let scanned = 0;
  for (const f of ctx.textFiles) {
    const rel = ctx.rel(f); const ext = path.extname(f).toLowerCase();
    const { text } = readText(f); scanned++;
    if (ext === '.json') scanJson(rel, text, findings);
    else if (CODE_EXT.has(ext)) scanLines(rel, text, findings, 'code');
    else if (DOC_EXT.has(ext)) scanLines(rel, text, findings, 'doc');
  }
  return { findings, counts: { files: scanned, skipped_secret_files: ctx.skippedSecretFiles.length }, notes: ctx.skippedSecretFiles.map((p) => `skipped by pattern (not opened): ${p}`) };
}

// ---------------------------------------------------------------- docs-dup (T-GATE-004, D8)
function isDoc(rel) {
  const base = path.posix.basename(rel);
  if (['README.md', 'AGENTS.md', 'CLAUDE.md'].includes(base)) return true;
  if (/(^|\/)docs\/.*\.md$/i.test(rel)) return true;
  if (/(^|\/)\.cursor\/rules\/.*\.mdc$/i.test(rel)) return true;
  if (/(^|\/)\.claude\/rules\/.*\.md$/i.test(rel)) return true;
  return false;
}
function paragraphs(text) {
  const out = []; const lines = text.split(/\r?\n/);
  let buf = []; let start = 0; let fence = null; let i = 0;
  if (lines[0] === '---') { // front matter
    const end = lines.indexOf('---', 1); if (end > 0) i = end + 1;
  }
  const flush = () => { if (buf.length) out.push({ line: start + 1, text: buf.join(' ') }); buf = []; };
  for (; i < lines.length; i++) {
    const ln = lines[i];
    const f = ln.match(/^\s*(```|~~~)/);
    if (fence) { if (f && f[1] === fence) fence = null; continue; }
    if (f) { flush(); fence = f[1]; continue; }
    if (!ln.trim()) { flush(); continue; }
    if (!buf.length) start = i;
    buf.push(ln.trim());
  }
  flush();
  return out;
}
function checkDocsDup(ctx) {
  const seen = new Map(); let docs = 0;
  for (const f of ctx.textFiles) {
    const rel = ctx.rel(f); if (!isDoc(rel)) continue; docs++;
    for (const p of paragraphs(readText(f).text)) {
      const norm = p.text.toLowerCase().replace(/\s+/g, ' ').trim();
      const words = norm.split(' ').filter(Boolean);
      if (words.length < DOCS_DUP_MIN_WORDS) continue;
      if (!seen.has(norm)) seen.set(norm, { first: p.text.split(/\s+/).slice(0, 10).join(' '), locations: [] });
      seen.get(norm).locations.push({ file: rel, line: p.line });
    }
  }
  const findings = [];
  for (const g of seen.values()) if (g.locations.length > 1) findings.push({ rule: 'docs-dup', file: g.locations[0].file, line: g.locations[0].line, detail: `"${g.first} ..."`, locations: g.locations });
  return { findings, counts: { docs } };
}

// ---------------------------------------------------------------- tool checks (lint, typecheck, unit)
function run(cmd, args, cwd) {
  // npm is npm.cmd on Windows (needs a shell); node / dotnet run directly, so paths with spaces stay intact
  const shell = process.platform === 'win32' && cmd === 'npm';
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', shell, maxBuffer: 64 * 1024 * 1024, env: { ...process.env, FORCE_COLOR: '0', NO_COLOR: '1' } });
  return { code: r.status ?? 1, stdout: r.stdout || '', out: `${r.stdout || ''}${r.stderr || ''}${r.error ? r.error.message : ''}` };
}
function pkgScripts(dir) { try { return JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8')).scripts || {}; } catch { return {}; } }
function nodeBin(dir, rel) {
  for (const base of [dir, path.join(FRAMEWORK_ROOT, TARGETS.nextjs.path)]) { const p = path.join(base, 'node_modules', rel); if (fs.existsSync(p)) return p; }
  return null;
}
function checkLint(ctx) {
  const scripts = pkgScripts(ctx.dir);
  const r = scripts.lint
    ? run('npm', ['run', '--silent', 'lint', '--', '--format', 'json'], ctx.dir)
    : (() => { const b = nodeBin(ctx.dir, 'eslint/bin/eslint.js'); return b ? run(process.execPath, [b, '.', '--format', 'json'], ctx.dir) : { code: 1, out: 'eslint not found' }; })();
  const so = r.stdout ?? r.out; const s = so.indexOf('['); const e = so.lastIndexOf(']');
  let results = null; try { results = JSON.parse(so.slice(s, e + 1)); } catch { /* fall through */ }
  if (!results) return { findings: [{ rule: 'lint-run', file: '.', line: 0, detail: `eslint did not run (exit ${r.code}): ${r.out.trim().split(/\r?\n/).slice(-3).join(' | ')}` }], counts: { errors: 'n/a' } };
  const findings = []; let errors = 0; let warnings = 0;
  for (const f of results) {
    errors += f.errorCount + (f.fatalErrorCount || 0); warnings += f.warningCount;
    for (const m of f.messages) if (m.severity === 2) findings.push({ rule: `lint:${m.ruleId || 'fatal'}`, file: posix(path.relative(ctx.dir, f.filePath)), line: m.line || 0, detail: m.message });
  }
  return { findings, counts: { files: results.length, errors, warnings } };
}
function checkTypecheck(ctx) {
  const scripts = pkgScripts(ctx.dir);
  let r;
  if (scripts.typecheck) r = run('npm', ['run', '--silent', 'typecheck'], ctx.dir);
  else { const b = nodeBin(ctx.dir, 'typescript/bin/tsc'); r = b ? run(process.execPath, [b, '--noEmit', '-p', '.'], ctx.dir) : { code: 1, out: 'tsc not found' }; }
  const findings = [];
  for (const ln of r.out.split(/\r?\n/)) {
    const m = ln.match(/^(.+?)\((\d+),\d+\): error (TS\d+): (.*)$/);
    if (m) findings.push({ rule: `typecheck:${m[3]}`, file: posix(m[1].trim()), line: Number(m[2]), detail: m[4] });
  }
  if (r.code !== 0 && !findings.length) findings.push({ rule: 'typecheck-run', file: '.', line: 0, detail: `tsc exit ${r.code}: ${r.out.trim().split(/\r?\n/).slice(-3).join(' | ')}` });
  return { findings, counts: { errors: findings.length } };
}
function checkUnit(ctx) {
  const u = ctx.target.unit; let r;
  if (u.npmScript) {
    if (!pkgScripts(ctx.dir)[u.npmScript]) return { findings: [{ rule: 'unit-missing', file: 'package.json', line: 0, detail: `no "${u.npmScript}" script` }], counts: {} };
    r = run('npm', ['run', '--silent', u.npmScript], ctx.dir);
    const t = r.out.match(/Tests\s+(?:(\d+) failed \| )?(\d+) passed(?: \((\d+)\))?/);
    const files = r.out.match(/Test Files\s+.*?\((\d+)\)/);
    const counts = { passed: t ? Number(t[2]) : 0, failed: t && t[1] ? Number(t[1]) : (r.code ? 'n/a' : 0), files: files ? Number(files[1]) : 'n/a' };
    return { findings: r.code ? [{ rule: 'unit-failed', file: '.', line: 0, detail: `npm run ${u.npmScript} exit ${r.code}` }] : [], counts };
  }
  if (!fs.existsSync(path.join(ctx.dir, u.args[1]))) return { findings: [{ rule: 'unit-missing', file: u.args[1], line: 0, detail: 'test project not found' }], counts: {} };
  r = run(u.cmd, u.args, ctx.dir);
  const m = r.out.match(/Failed:\s*(\d+),\s*Passed:\s*(\d+),\s*Skipped:\s*(\d+),\s*Total:\s*(\d+)/);
  const counts = m ? { passed: Number(m[2]), failed: Number(m[1]), skipped: Number(m[3]) } : { passed: 'n/a', failed: 'n/a' };
  return { findings: r.code ? [{ rule: 'unit-failed', file: '.', line: 0, detail: `dotnet test exit ${r.code}` }] : [], counts };
}
const CHECKS = { lint: checkLint, typecheck: checkTypecheck, eol: checkEol, secrets: checkSecrets, 'docs-dup': checkDocsDup, unit: checkUnit };

// ---------------------------------------------------------------- touched targets (implementation manifest, S6)
function touchedTargets(featurePath) {
  const file = fs.existsSync(featurePath) && fs.statSync(featurePath).isDirectory() ? path.join(featurePath, 'handoff.md') : featurePath;
  const text = fs.readFileSync(file, 'utf8');
  const fm = text.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---/); if (!fm) return null;
  const lines = fm[1].split(/\r?\n/);
  const start = lines.findIndex((l) => /^implementation:/.test(l)); if (start < 0) return null;
  const block = []; for (let i = start + 1; i < lines.length && (/^\s/.test(lines[i]) || !lines[i].trim()); i++) block.push(lines[i]);
  const lists = {}; let cur = null;
  for (const l of block) {
    const k = l.match(/^ {2}(api|ui|tests|migrations):\s*(\[\])?/);
    if (k) { cur = k[1]; lists[cur] = []; continue; }
    if (/^ {2}\S/.test(l)) { cur = null; continue; }
    if (cur && /^ {4}- /.test(l)) lists[cur].push({ repo: null });
    if (cur && /^ {6}repo:\s*(api|ui)/.test(l) && lists[cur].length) lists[cur][lists[cur].length - 1].repo = l.match(/repo:\s*(api|ui)/)[1];
  }
  const t = new Set();
  if ((lists.api || []).length || (lists.migrations || []).length || (lists.tests || []).some((e) => e.repo === 'api')) t.add('api-framework');
  if ((lists.ui || []).length || (lists.tests || []).some((e) => e.repo === 'ui')) t.add('nextjs');
  return t.size ? t : null; // empty manifest: cannot tell, run everything
}

// ---------------------------------------------------------------- record (handoff.md code.verification, D9)
function recordInHandoff(file, lines, gate, at) {
  const before = fs.readFileSync(file);
  const bom = before[0] === 0xef && before[1] === 0xbb && before[2] === 0xbf;
  let text = before.toString('utf8', bom ? 3 : 0);
  const nl = text.includes('\r\n') ? '\r\n' : '\n';
  const fmEnd = text.indexOf(`${nl}---`, 4);
  let fm = text.slice(0, fmEnd); const rest = text.slice(fmEnd);
  const testingBefore = (fm.match(/\ntesting:[\s\S]*?(?=\n\S)/) || [''])[0];
  const fl = fm.split(nl);
  const codeIdx = fl.findIndex((l) => /^code:/.test(l)); if (codeIdx < 0) throw new Error('no code: block in handoff.md');
  let end = codeIdx + 1; while (end < fl.length && (/^\s/.test(fl[end]) || !fl[end].trim())) end++;
  const vi = fl.findIndex((l, i) => i > codeIdx && i < end && /^ {2}verification:/.test(l)); if (vi < 0) throw new Error('no code.verification in handoff.md');
  const existing = []; let j = vi + 1;
  const inline = fl[vi].match(/^ {2}verification:\s*\[(.*)\]/);
  if (inline && inline[1].trim()) inline[1].split(/",\s*"/).forEach((s) => existing.push(s.replace(/^"|"$/g, '')));
  while (j < end && /^ {4}- /.test(fl[j])) { existing.push(fl[j].replace(/^ {4}- /, '').replace(/^"|"$/g, '').replace(/\\"/g, '"')); j++; }
  const kept = existing.filter((s) => !s.startsWith('pre-handoff:'));
  const all = [...kept, ...lines];
  const q = (s) => `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
  const comment = (fl[vi].match(/(\s+#.*)$/) || ['', ''])[1];
  const newBlock = [`  verification:${comment}`, ...all.map((s) => `    - ${q(s)}`)];
  fl.splice(vi, j - vi, ...newBlock);
  const setField = (name, value) => {
    const i = fl.findIndex((l) => new RegExp(`^ {2}${name}:`).test(l)); if (i < 0) throw new Error(`no code.${name} in handoff.md`);
    const c = (fl[i].match(/^ {2}\S+:\s*\S+(\s+#.*)$/) || ['', ''])[1];
    fl[i] = `  ${name}: ${value}${c}`;
  };
  setField('pre_handoff_gate', gate); setField('pre_handoff_gate_at', at);
  fm = fl.join(nl);
  if ((fm.match(/\ntesting:[\s\S]*?(?=\n\S)/) || [''])[0] !== testingBefore) throw new Error('refusing to write: testing section would change');
  const now = fs.readFileSync(file); if (!now.equals(before)) throw new Error('handoff.md changed on disk while recording; re-run');
  fs.writeFileSync(file, (bom ? '\ufeff' : '') + fm + rest, 'utf8');
}

// ---------------------------------------------------------------- probe (read-only reviewer mode)
// --probe: a read-only scan for reviewers. It calls only fs.readdirSync / readFileSync / statSync (through walk() and
// the helpers below): no child processes, no writes, no allowlist (findings are raw). Findings are { file, rule, line }
// only; line text, matched values and secrets are never printed. Rules: utf8-invalid, bom, eol-mixed (CRLF + LF, or any
// lone CR), eol-changed (dominant style differs from --baseline <manifest.json>) and open-redirect-sink (heuristic).
const PROBE_CHECKS = ['utf8', 'bom', 'eol-mixed', 'eol-changed', 'open-redirect'];
const REDIRECT_EXT = new Set(['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.mts', '.cts', '.cs']);

function probeLineAt(starts, index) { // 1-based line of a character / byte index (starts: sorted line-start offsets)
  let lo = 0; let hi = starts.length - 1;
  while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (starts[mid] <= index) lo = mid; else hi = mid - 1; }
  return lo + 1;
}
function probeLineStarts(s) { const out = [0]; for (let i = 0; i < s.length; i++) if (s.charCodeAt(i) === 10) out.push(i + 1); return out; }
// First invalid UTF-8 byte offset (overlong forms, surrogates and > U+10FFFF are invalid), or -1.
function firstInvalidUtf8(buf) {
  for (let i = 0; i < buf.length;) {
    const b = buf[i];
    if (b < 0x80) { i++; continue; }
    let need; let min;
    if (b >= 0xc2 && b <= 0xdf) { need = 1; min = 0x80; } else if (b >= 0xe0 && b <= 0xef) { need = 2; min = 0x800; } else if (b >= 0xf0 && b <= 0xf4) { need = 3; min = 0x10000; } else return i;
    if (i + need >= buf.length) return i; // truncated sequence at the end of the file
    let cp = b & (0x3f >> need);
    for (let k = 1; k <= need; k++) { const c = buf[i + k]; if ((c & 0xc0) !== 0x80) return i; cp = (cp << 6) | (c & 0x3f); }
    if (cp < min || cp > 0x10ffff || (cp >= 0xd800 && cp <= 0xdfff)) return i;
    i += need + 1;
  }
  return -1;
}
// Line endings from the raw bytes: counts, dominant style and the first line whose ending differs from the first one.
function probeEol(buf) {
  let crlf = 0; let lf = 0; let cr = 0; let first = null; let firstOdd = 0; let line = 1;
  for (let i = 0; i < buf.length; i++) {
    let kind = null;
    if (buf[i] === 13) { if (buf[i + 1] === 10) { kind = 'crlf'; i++; } else kind = 'cr'; } else if (buf[i] === 10) kind = 'lf';
    if (!kind) continue;
    if (kind === 'crlf') crlf++; else if (kind === 'lf') lf++; else cr++;
    if (!first) first = kind;
    if (!firstOdd && (kind === 'cr' || kind !== first)) firstOdd = line;
    line++;
  }
  const dominant = !(crlf + lf + cr) ? 'none' : crlf >= lf && crlf >= cr ? 'crlf' : lf >= cr ? 'lf' : 'cr';
  return { crlf, lf, cr, dominant, mixedLine: (crlf && lf) || cr ? (firstOdd || 1) : 0 };
}

// --- open-redirect heuristic. Comments are blanked (same length, newlines kept), then a second copy has string
// contents blanked too (quotes and template ${...} code kept), so sinks / declarations are matched on code only and
// the expressions are read back from the comment-free text at the same offsets.
function probeLex(text, cs) {
  const n = text.length; const code = text.split(''); const mask = text.split('');
  const blank = (arr, a, b) => { for (let k = a; k < b && k < n; k++) if (arr[k] !== '\n' && arr[k] !== '\r') arr[k] = ' '; };
  const tpl = []; let depth = 0; let i = 0;
  const readTemplate = (j) => { // j: first char inside a template literal (or just after an interpolation's closing brace)
    let k = j;
    while (k < n) {
      if (text[k] === '\\') { k += 2; continue; }
      if (text[k] === '`') { blank(mask, j, k); return k + 1; }
      if (text[k] === '$' && text[k + 1] === '{') { blank(mask, j, k); depth++; tpl.push(depth); return k + 2; }
      k++;
    }
    blank(mask, j, n); return n;
  };
  while (i < n) {
    const c = text[i]; const d = text[i + 1];
    if (c === '/' && d === '/') { let j = i; while (j < n && text[j] !== '\n') j++; blank(code, i, j); blank(mask, i, j); i = j; continue; }
    if (c === '/' && d === '*') { const e = text.indexOf('*/', i + 2); const j = e < 0 ? n : e + 2; blank(code, i, j); blank(mask, i, j); i = j; continue; }
    if (c === '{') { depth++; i++; continue; }
    if (c === '}') { if (tpl.length && tpl[tpl.length - 1] === depth) { tpl.pop(); depth--; i = readTemplate(i + 1); continue; } depth--; i++; continue; }
    if (c === '`' && !cs) { i = readTemplate(i + 1); continue; }
    if (c === '"' || c === "'") {
      const verbatim = cs && c === '"' && (text[i - 1] === '@' || (text[i - 1] === '$' && text[i - 2] === '@') || (text[i - 1] === '@' && text[i - 2] === '$'));
      let j = i + 1;
      while (j < n && text[j] !== '\n') {
        if (verbatim) { if (text[j] === '"') { if (text[j + 1] === '"') { j += 2; continue; } break; } j++; continue; }
        if (text[j] === '\\') { j += 2; continue; }
        if (text[j] === c) break;
        j++;
      }
      blank(mask, i + 1, j); i = j + 1; continue; // an unterminated ' or " (JSX text, regex literal) stops at the line end
    }
    i++;
  }
  return { code: code.join(''), mask: mask.join('') };
}
// End offset of a call's argument list (start: just after the opening parenthesis), on the masked text.
function probeCallEnd(mask, start) {
  let d = 1;
  for (let i = start; i < mask.length && i < start + 4000; i++) { const c = mask[i]; if ('([{'.includes(c)) d++; else if (')]}'.includes(c)) { d--; if (!d) return i; } }
  return Math.min(mask.length, start + 4000);
}
// End offset of an expression (assignment right-hand side): ';' or a line end at depth 0, unless the expression
// obviously continues (trailing / leading operator).
function probeExprEnd(mask, start) {
  let d = 0;
  for (let i = start; i < mask.length && i < start + 4000; i++) {
    const c = mask[i];
    if ('([{'.includes(c)) d++;
    else if (')]}'.includes(c)) { if (!d) return i; d--; }
    else if (!d && (c === ';' || c === ',')) return i;
    else if (!d && c === '\n') {
      const before = mask.slice(start, i).trimEnd(); const after = mask.slice(i + 1, i + 200).trimStart();
      if (/(\?\?|\|\||&&|[?:+=(,.])$/.test(before) || /^(\?\?|\|\||&&|[?:.+])/.test(after)) continue;
      return i;
    }
  }
  return Math.min(mask.length, start + 4000);
}
const RX_STRONG_JS = /\b(searchParams|useSearchParams|query|params|URLSearchParams|location\s*\.\s*(search|hash))\b/;
const RX_STRONG_CS = /\b(Request\s*\.\s*(Query|Form|Headers)|QueryString|Query\s*\[)/;
const RX_GUARD = /\b(safeRedirect\w*|isSafe\w*|isLocalUrl|IsLocalUrl|LocalRedirect\w*|saniti[sz]eRedirect\w*)\s*\(/;
const NAME_SOURCES = new Set(['returnUrl', 'ReturnUrl', 'returnURL', 'returnTo', 'redirectTo', 'redirectUrl', 'redirect_uri', 'redirectUri', 'callbackUrl', 'callbackURL', 'next', 'from', 'redirect']);
// literal starts that cannot leave the origin: '/x...' (x a path character), '?...' or '#...' (same page), incl. new URL('/x', base)
const RX_SAFE_PREFIX = /^(?:new\s+URL\s*\(\s*)?[$@]{0,2}(['"`])(?:\/[A-Za-z0-9_~-]|[?#])/;
// identifiers used in an expression: string contents dropped (template ${...} and C# {...} interpolations kept)
function probeIdents(expr, cs) {
  let s = ''; let i = 0; const n = expr.length;
  while (i < n) {
    const c = expr[i];
    if (c === '"' || c === "'" || c === '`') {
      const interp = c === '`' || (cs && c === '"' && expr[i - 1] === '$');
      let j = i + 1; let keep = '';
      while (j < n && expr[j] !== c) {
        if (expr[j] === '\\' && !cs) { j += 2; continue; }
        if (interp && (expr[j] === '{' || (expr[j] === '$' && expr[j + 1] === '{'))) {
          const open = expr.indexOf('{', j); let d = 1; let k = open + 1;
          for (; k < n && d; k++) { if (expr[k] === '{') d++; else if (expr[k] === '}') d--; }
          keep += ` ${expr.slice(open + 1, k - 1)} `; j = k; continue;
        }
        j++;
      }
      s += ` ${keep} `; i = j + 1; continue;
    }
    s += c; i++;
  }
  const bare = []; const re = /(^|[^\w$.])([A-Za-z_$][\w$]*)(?!\s*\()/g; let m;
  while ((m = re.exec(s))) { bare.push(m[2]); re.lastIndex = m.index + m[0].length; }
  return { stripped: s, bare };
}
function scanRedirects(text, cs) {
  const { code, mask } = probeLex(text, cs);
  const starts = probeLineStarts(text);
  const strong = cs ? RX_STRONG_CS : RX_STRONG_JS;
  // declarations and plain re-assignments: name(s) -> right-hand side
  const decls = [];
  const declRe = cs
    ? /\b(?:var|string\??|String|Uri\??|object)\s+([A-Za-z_]\w*)\s*=(?![=>])/g
    : /\b(?:const|let|var)\s+([A-Za-z_$][\w$]*|\{[^}]*\}|\[[^\]]*\])\s*(?::[^=;\n]+)?=(?![=>])/g;
  const reassignRe = /(^|[;{}(\s])([A-Za-z_$][\w$]*)\s*(?:\?\?=|\|\|=|=)(?![=>])/g;
  const names = (lhs) => {
    if (!/^[{[]/.test(lhs)) return [lhs];
    return lhs.slice(1, -1).split(',').map((p) => p.split('=')[0].trim()).map((p) => (p.includes(':') ? p.split(':')[1].trim() : p).replace(/^\.\.\./, '')).filter((p) => /^[A-Za-z_$][\w$]*$/.test(p));
  };
  let m;
  while ((m = declRe.exec(mask))) {
    const s = m.index + m[0].length; const e = probeExprEnd(mask, s);
    for (const nm of names(m[1])) decls.push({ name: nm, expr: code.slice(s, e) });
  }
  while ((m = reassignRe.exec(mask))) {
    if (/^(const|let|var|return|typeof|case|default|in|of|new|await|yield|else)$/.test(m[2])) continue;
    const before = mask.slice(Math.max(0, m.index - 12), m.index + m[1].length);
    if (/\b(const|let|var|string\??|String|Uri\??|object)\s*$/.test(before)) continue;
    const s = m.index + m[0].length; const e = probeExprEnd(mask, s);
    decls.push({ name: m[2], expr: code.slice(s, e) });
  }
  const declared = new Set(decls.map((d) => d.name));
  const tainted = new Set();
  const exprTainted = (expr) => {
    const { stripped, bare } = probeIdents(expr, cs);
    const hits = bare.filter((id) => tainted.has(id) || (NAME_SOURCES.has(id) && !declared.has(id)));
    if (strong.test(stripped)) hits.push('(source)');
    return hits;
  };
  for (let changed = true, guard = 0; changed && guard < 50; guard++) {
    changed = false;
    for (const d of decls) {
      if (tainted.has(d.name) || RX_GUARD.test(d.expr)) continue; // a guard call in the chain cleans the value
      if (exprTainted(d.expr).length) { tainted.add(d.name); changed = true; }
    }
  }
  // sinks
  const sinks = [];
  const callSinks = cs
    ? [/\b(?:Redirect|RedirectPermanent|RedirectPreserveMethod|RedirectPermanentPreserveMethod)\s*\(/g, /\bnew\s+RedirectResult\s*\(/g]
    : [/\b[\w$]*[rR]outer\s*\.\s*(?:push|replace)\s*\(/g, /\b(?:permanentRedirect|redirect)\s*\(/g, /\blocation\s*\.\s*(?:assign|replace)\s*\(/g];
  for (const re of callSinks) {
    re.lastIndex = 0;
    while ((m = re.exec(mask))) {
      if (/\b(function|def|void|IActionResult|ActionResult|Task<[^>]*>)\s*$/.test(mask.slice(Math.max(0, m.index - 40), m.index))) continue; // a definition, not a call
      const s = m.index + m[0].length; sinks.push({ at: m.index, expr: code.slice(s, probeCallEnd(mask, s)) });
    }
  }
  if (!cs) {
    const assign = /(^|[^\w$.]|\b(?:window|document|globalThis|self|top)\s*\.\s*)location(?:\s*\.\s*href)?\s*=(?![=>])/g;
    while ((m = assign.exec(mask))) {
      if (/\b(const|let|var)\s*$/.test(mask.slice(Math.max(0, m.index - 8), m.index + m[1].length))) continue;
      const s = m.index + m[0].length; sinks.push({ at: m.index, expr: code.slice(s, probeExprEnd(mask, s)) });
    }
  }
  const out = [];
  for (const k of sinks) {
    const arg = k.expr.trim();
    if (!arg || RX_SAFE_PREFIX.test(arg) || RX_GUARD.test(arg)) continue;
    const hits = exprTainted(arg); if (!hits.length) continue;
    const line = probeLineAt(starts, k.at);
    // a guard call on the sink line or the line above that mentions a tainted identifier (if (isSafe(x)) ...)
    const near = code.slice(starts[Math.max(0, line - 2)], starts[line] ?? code.length);
    const ids = hits.filter((h) => h !== '(source)');
    const g = new RegExp(RX_GUARD.source, 'g'); let gm; let guarded = false;
    while ((gm = g.exec(near))) { const a = near.slice(gm.index + gm[0].length, gm.index + gm[0].length + 300); if (!ids.length || ids.some((id) => new RegExp(`\\b${id.replace(/\$/g, '\\$')}\\b`).test(a))) { guarded = true; break; } }
    if (!guarded) out.push(line);
  }
  return [...new Set(out)].sort((a, b) => a - b);
}

function probeFiles(dir) { // walk() + text filter; walk() only uses readdirSync and never opens secret-pattern files
  const { files, skippedSecretFiles } = walk(dir);
  return { textFiles: files.filter(isText), skippedSecretFiles };
}
function probeTargets(args) {
  let names = args.target === 'all' ? Object.keys(TARGETS) : [args.target];
  if (args.feature && args.target === 'all') { const t = touchedTargets(args.feature); if (t) names = names.filter((n) => t.has(n)); }
  return names.map((name) => {
    const dir = args.path || path.join(FRAMEWORK_ROOT, TARGETS[name].path);
    const base = args.path || FRAMEWORK_ROOT; // finding paths: relative to --path, else to the ai-framework root
    let ok = false; try { ok = fs.statSync(dir).isDirectory(); } catch { /* reported */ }
    return { name, dir, ok, rel: (f) => posix(path.relative(base, f)) };
  });
}
function probeLoadBaseline(file) {
  let data;
  try { // UTF-8 (BOM or not) or UTF-16LE with BOM (what Windows PowerShell 5 `>` writes)
    const raw = fs.readFileSync(file);
    data = JSON.parse(raw[0] === 0xff && raw[1] === 0xfe ? raw.toString('utf16le', 2) : raw.toString('utf8', raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf ? 3 : 0));
  } catch { usage(`--baseline: cannot read ${file} as JSON`); }
  const files = data && typeof data.files === 'object' && !Array.isArray(data.files) ? data.files : data;
  const map = new Map();
  for (const [k, v] of Object.entries(files || {})) if (v && typeof v === 'object' && ['lf', 'crlf', 'cr', 'none'].includes(v.eol)) map.set(k, v);
  if (!map.size) usage(`--baseline: no { "<path>": { "eol": "lf|crlf|none" } } entries in ${file}`);
  return map;
}
function probeMain(args) {
  const at = isoNow();
  const targets = probeTargets(args);
  if (args.baselinePrint) { // manifest to stdout only; the reviewer redirects it to a file
    const files = {};
    for (const t of targets) {
      if (!t.ok) usage(`path not found ${t.dir}`);
      for (const f of probeFiles(t.dir).textFiles) { const buf = fs.readFileSync(f); files[t.rel(f)] = { eol: probeEol(buf).dominant, sha256: crypto.createHash('sha256').update(buf).digest('hex') }; }
    }
    console.log(JSON.stringify({ version: 1, kind: 'pre-handoff-probe-baseline', at, root: args.path ? '--path' : 'ai-framework', files }, null, 2));
    process.exit(0);
  }
  const baseline = args.baseline ? probeLoadBaseline(args.baseline) : null;
  const want = new Set(args.checks || PROBE_CHECKS);
  const report = { mode: 'probe', read_only: true, at, gate: 'pass', targets: {}, checks: PROBE_CHECKS.filter((c) => want.has(c) && (c !== 'eol-changed' || baseline)), summary: {}, findings: [], problems: [] };
  let scanned = 0; let hashChanged = 0; let notInBaseline = 0;
  for (const t of targets) {
    if (!t.ok) { report.problems.push(`${t.name}: path not found`); continue; }
    const { textFiles, skippedSecretFiles } = probeFiles(t.dir);
    report.targets[t.name] = { text_files: textFiles.length, skipped_secret_files: skippedSecretFiles.length };
    for (const f of textFiles) {
      const rel = t.rel(f); const buf = fs.readFileSync(f); scanned++;
      const add = (rule, line) => report.findings.push({ file: rel, rule, line });
      const bad = firstInvalidUtf8(buf);
      let utf8ok = bad < 0;
      if (utf8ok) { try { new TextDecoder('utf-8', { fatal: true }).decode(buf); } catch { utf8ok = false; } }
      if (!utf8ok && want.has('utf8')) { let line = 1; for (let i = 0; i < bad && i < buf.length; i++) if (buf[i] === 10) line++; add('utf8-invalid', bad < 0 ? 0 : line); }
      if (want.has('bom') && buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) add('bom', 1);
      const eol = probeEol(buf);
      if (want.has('eol-mixed') && eol.mixedLine) add('eol-mixed', eol.mixedLine);
      if (baseline && want.has('eol-changed')) {
        const b = baseline.get(rel);
        if (!b) notInBaseline++;
        else {
          if (b.eol !== eol.dominant) add('eol-changed', 0);
          if (b.sha256 && b.sha256 !== crypto.createHash('sha256').update(buf).digest('hex')) hashChanged++;
        }
      }
      const ext = path.extname(f).toLowerCase();
      if (want.has('open-redirect') && REDIRECT_EXT.has(ext)) {
        const text = buf.toString('utf8', buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf ? 3 : 0);
        for (const line of scanRedirects(text, ext === '.cs')) add('open-redirect-sink', line);
      }
    }
  }
  const byRule = {}; for (const f of report.findings) byRule[f.rule] = (byRule[f.rule] || 0) + 1;
  report.summary = { files: scanned, findings: report.findings.length, by_rule: byRule };
  if (baseline) { report.summary.baseline_hash_changed = hashChanged; report.summary.not_in_baseline = notInBaseline; }
  if (report.findings.length || report.problems.length) report.gate = 'fail';
  if (args.json) console.log(JSON.stringify(report, null, 2));
  else {
    for (const [n, t] of Object.entries(report.targets)) console.log(`probe ${n}: ${t.text_files} text files (${t.skipped_secret_files} secret-pattern files skipped, not opened)`);
    for (const f of report.findings) console.log(`    FAIL ${f.rule} ${f.file}:${f.line}`);
    for (const p of report.problems) console.log(`PROBLEM ${p}`);
    const rules = Object.entries(byRule).map(([k, v]) => `${k} ${v}`).join(', ');
    console.log(`probe -> ${report.gate} (${report.findings.length} findings${rules ? `: ${rules}` : ''}; read-only) (${at})`);
  }
  process.exit(report.gate === 'pass' ? 0 : 1);
}

// ---------------------------------------------------------------- main
function isoNow() {
  const d = new Date(); const off = -d.getTimezoneOffset(); const s = off >= 0 ? '+' : '-'; const p = (n) => String(Math.abs(n)).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}${s}${p(Math.trunc(off / 60))}:${p(off % 60)}`;
}
function allowlistCheck(rule) {
  if (rule === 'docs-dup') return 'docs-dup';
  if (rule.startsWith('secret')) return 'secrets';
  if (rule.startsWith('eol')) return 'eol';
  if (rule.startsWith('lint:')) return 'lint';
  if (rule.startsWith('typecheck:')) return 'typecheck';
  return null;
}
function fmtCounts(c) { return Object.entries(c).map(([k, v]) => `${v} ${k.replace(/_/g, ' ')}`).join(', '); }

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.probe) { probeMain(args); return; } // read-only: exits inside
  const at = isoNow();
  const allow = loadAllowlist(args.allowlist);
  let names = args.target === 'all' ? Object.keys(TARGETS) : [args.target];
  let touched = null;
  if (args.feature && args.target === 'all') touched = touchedTargets(args.feature);
  const report = { at, gate: 'pass', allowlist: posix(path.relative(FRAMEWORK_ROOT, args.allowlist)), targets: {}, checks: [], problems: [...allow.problems], warnings: [] };
  const ran = new Set(); // `${target}|${check}` pairs that ran, for the unused-entry report (review F-03)

  for (const name of names) {
    const target = TARGETS[name];
    const dir = args.path || path.join(FRAMEWORK_ROOT, target.path);
    if (!fs.existsSync(dir)) { report.problems.push(`${name}: path not found ${dir}`); continue; }
    const { files, skippedSecretFiles } = walk(dir);
    const textFiles = files.filter(isText);
    const git = isGitRepo(dir);
    report.targets[name] = { path: posix(args.path ? dir : target.path), git, note: git ? 'git repo: working tree scanned' : 'not a git repo: working tree scanned', textFiles: textFiles.length };
    const ctx = { name, target, dir, textFiles, skippedSecretFiles, rel: (f) => posix(path.relative(dir, f)) };

    if (args.fixEol) {
      const r = fixEol(ctx);
      report.checks.push({ check: 'fix-eol', target: name, result: r.verifyFailures.length ? 'fail' : 'pass', counts: { changed: r.total, ...r.changed }, findings: r.verifyFailures.map((f) => ({ rule: 'fix-eol-verify', file: f, line: 0 })) });
      continue;
    }
    const targetIsTouched = !touched || touched.has(name);
    let checks = target.checks.filter((c) => targetIsTouched || c === 'secrets'); // secrets always runs on both (S6)
    if (args.checks) checks = checks.filter((c) => args.checks.includes(c));
    for (const check of CHECK_ORDER.filter((c) => checks.includes(c))) {
      let r;
      try { r = CHECKS[check](ctx); } catch (e) { r = { findings: [{ rule: `${check}-error`, file: '.', line: 0, detail: e.message }], counts: {} }; }
      const open = []; const allowed = [];
      for (const f of r.findings) { const e = allowlisted(allow, name, f); if (e) { allowed.push({ ...f, allowlist: e._id }); if (e._expired) open.push({ ...f, rule: 'allowlist-expired', detail: `${e._id} (${e.rule} ${e.path || (e.paths || []).join(' + ')}) expired ${e.expires}` }); } else open.push(f); }
      const counts = { ...r.counts, findings: open.length }; if (allowed.length) counts.allowlisted = allowed.length;
      report.checks.push({ check, target: name, result: open.length ? 'fail' : 'pass', counts, findings: open, allowlisted: allowed, notes: r.notes || [] });
      ran.add(`${name}|${check}`);
    }
  }
  const where = (e) => `${e.rule} ${e.path || (e.paths || []).join(' + ')}`;
  for (const e of allow.entries) if (e._expired && !e._used) report.problems.push(`allowlist ${e._id} (${where(e)}) expired ${e.expires}`);
  // Unused, unexpired entries (review F-03): only judged when the entry's check ran on every target it can apply to,
  // and not for --path runs with the default allowlist (its paths belong to the real targets, not the --path folder).
  // An unused secret-* entry fails the gate (remove it: the value it covered is gone); any other unused entry warns.
  if (!(args.path && args.allowlist === DEFAULT_ALLOWLIST)) {
    for (const e of allow.entries) {
      if (e._expired || e._used || !e.rule) continue;
      const check = allowlistCheck(e.rule); if (!check) continue;
      const applies = e.target ? [e.target] : Object.keys(TARGETS);
      if (!applies.every((t) => ran.has(`${t}|${check}`))) continue;
      const msg = `allowlist ${e._id} (${where(e)}) matched nothing; remove it`;
      if (e.rule.startsWith('secret')) report.problems.push(msg); else report.warnings.push(msg);
    }
  }
  if (report.problems.length || report.checks.some((c) => c.result === 'fail')) report.gate = 'fail';

  // strip internal fields (line text is never output)
  for (const c of report.checks) for (const list of [c.findings, c.allowlisted || []]) for (const f of list) delete f._lineText;

  const summary = report.checks.map((c) => `pre-handoff: ${c.check} ${c.target} -> ${c.result} (${fmtCounts(c.counts)})`);
  for (const [n, t] of Object.entries(report.targets)) summary.push(`pre-handoff: ${n}: ${t.note}`);
  if (report.warnings.length) summary.push(`pre-handoff: allowlist -> ${report.warnings.length} unused entr${report.warnings.length === 1 ? 'y' : 'ies'} (warning)`);
  if (args.json) console.log(JSON.stringify(report, null, 2));
  else {
    for (const c of report.checks) {
      console.log(`${c.check} ${c.target} -> ${c.result} (${fmtCounts(c.counts)})`);
      for (const f of c.findings) {
        const where = f.locations ? f.locations.map((l) => `${l.file}:${l.line}`).join(', ') : `${f.file}${f.line ? `:${f.line}` : ''}`;
        console.log(`    FAIL ${f.rule} ${where}${f.key ? ` [${f.key}]` : ''}${f.detail ? ` ${f.detail}` : ''}`);
      }
      for (const f of c.allowlisted || []) console.log(`    allowlisted ${f.rule} ${f.locations ? f.locations.map((l) => `${l.file}:${l.line}`).join(', ') : `${f.file}:${f.line}`}${f.key ? ` [${f.key}]` : ''} (${f.allowlist})`);
      for (const n of c.notes || []) console.log(`    note ${n}`);
    }
    for (const [n, t] of Object.entries(report.targets)) console.log(`${n}: ${t.note} (${t.textFiles} text files)`);
    for (const w of report.warnings) console.log(`WARNING ${w}`);
    for (const p of report.problems) console.log(`PROBLEM ${p}`);
    console.log(`pre-handoff gate -> ${report.gate} (${at})`);
  }
  if (args.record) {
    if (args.fixEol || args.checks || args.path) { console.error('--record needs a full run (no --fix-eol, --checks or --path)'); process.exit(2); }
    recordInHandoff(args.record, summary, report.gate, at);
    if (!args.json) console.log(`recorded in ${posix(path.relative(FRAMEWORK_ROOT, args.record))}: code.verification (${summary.length} lines), code.pre_handoff_gate: ${report.gate}, code.pre_handoff_gate_at: ${at}`);
  }
  process.exit(report.gate === 'pass' ? 0 : 1);
}

main();
