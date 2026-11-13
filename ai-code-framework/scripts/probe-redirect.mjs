#!/usr/bin/env node
// Open-redirect probe for return-path guards (reviewer helper next to pre-handoff-checks.mjs --probe). Node 22, no
// dependencies.
//
//   node ai-code-framework/scripts/probe-redirect.mjs --module <file.js|file.mjs> --export <name> [--attacks <file>] [--json]
//
// Imports ONLY the named module (its own top-level code runs, so point it at a small pure guard module) and calls
// <export>(input) once per entry in fixtures/redirect-attacks.json. It starts no child processes and writes nothing;
// the only output is stdout. A result is judged:
//   rejected  null / undefined / false / '' returned, or the call threw
//   safe      a string that is a same-origin root-relative path: starts with a single '/', no '\', no control
//             characters, resolves to the same origin, and does not decode (once or twice) to '//' or '/\'
//   unsafe    anything else (also: true returned for an input that is itself unsafe, for boolean isSafe* checks)
// Exit 0 = no unsafe result, 1 = at least one unsafe result, 2 = usage / load error. Output names the attack id and
// category only, never the returned value.
// TypeScript: the module must be JavaScript. Build it first, or on Node 22.6+ run with type stripping when the file
// uses only erasable syntax and its imports carry file extensions:
//   node --experimental-strip-types ai-code-framework/scripts/probe-redirect.mjs --module src/lib/safe-redirect.ts --export safeRedirectPath
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ORIGIN = 'http://probe.invalid';

function usage(msg) {
  if (msg) console.error(`probe-redirect: ${msg}`);
  console.error('usage: node probe-redirect.mjs --module <file.js|file.mjs> --export <name> [--attacks <file>] [--json]');
  process.exit(2);
}
function parseArgs(argv) {
  const a = { module: null, exportName: null, attacks: path.join(HERE, 'fixtures', 'redirect-attacks.json'), json: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const next = () => { if (i + 1 >= argv.length) usage(`missing value for ${k}`); return argv[++i]; };
    if (k === '--module') a.module = path.resolve(next());
    else if (k === '--export') a.exportName = next();
    else if (k === '--attacks') a.attacks = path.resolve(next());
    else if (k === '--json') a.json = true;
    else if (k === '-h' || k === '--help') usage();
    else usage(`unknown argument ${k}`);
  }
  if (!a.module || !a.exportName) usage('--module and --export are required');
  return a;
}
const decodeOnce = (s) => { try { return decodeURIComponent(s); } catch { return null; } };
export function isSameOriginRootRelative(s) {
  if (typeof s !== 'string' || !s.startsWith('/') || s.startsWith('//')) return false;
  if (/[\\\u0000-\u001f\u007f]/.test(s)) return false;
  let u; try { u = new URL(s, `${ORIGIN}/`); } catch { return false; }
  if (u.origin !== ORIGIN) return false;
  const resolved = u.pathname + u.search + u.hash;
  if (resolved.startsWith('//') || resolved.startsWith('/\\')) return false;
  for (let d = s, i = 0; i < 2; i++) { // a later decode must not turn the path into //host, /\host or a control char
    const n = decodeOnce(d); if (n === null || n === d) break; d = n;
    if (/[\u0000-\u001f\u007f]/.test(d)) return false;
    const slashed = d.replace(/\\/g, '/');
    if (slashed.startsWith('//')) return false;
    let p; try { p = new URL(slashed, `${ORIGIN}/`); } catch { return false; }
    if (p.origin !== ORIGIN || p.pathname.startsWith('//')) return false;
  }
  return true;
}
export function judge(input, result, threw) {
  if (threw || result === null || result === undefined || result === false || result === '') return 'rejected';
  if (result === true) return isSameOriginRootRelative(input) ? 'safe' : 'unsafe';
  return isSameOriginRootRelative(result) ? 'safe' : 'unsafe';
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let data;
  try { data = JSON.parse(fs.readFileSync(args.attacks, 'utf8')); } catch { usage(`cannot read the attack list ${args.attacks}`); }
  const attacks = Array.isArray(data?.attacks) ? data.attacks : [];
  if (!attacks.length) usage('the attack list has no attacks');
  let mod;
  try { mod = await import(pathToFileURL(args.module).href); } catch (e) {
    usage(`cannot import ${args.module} (${e.code || 'error'})${/\.(ts|tsx|mts|cts)$/i.test(args.module) ? ': TypeScript needs a JS build, or node --experimental-strip-types (Node 22.6+)' : ''}`);
  }
  const fn = mod[args.exportName] ?? mod.default?.[args.exportName];
  if (typeof fn !== 'function') usage(`${args.exportName} is not an exported function of ${args.module}`);
  const results = [];
  for (const a of attacks) {
    let r; let threw = false;
    try { r = await fn(a.input); } catch { threw = true; }
    const verdict = judge(a.input, r, threw);
    // a safe control that is rejected or collapsed to '/' is over-strict (a warning, not a failure)
    const overStrict = a.expect === 'safe' && (verdict === 'rejected' || (verdict === 'safe' && r === '/' && a.input !== '/'));
    results.push({ id: a.id, category: a.category, expect: a.expect, verdict, ...(overStrict ? { over_strict: true } : {}) });
  }
  const unsafe = results.filter((r) => r.verdict === 'unsafe');
  const overStrict = results.filter((r) => r.over_strict);
  const report = { module: path.basename(args.module), export: args.exportName, attacks: results.length, unsafe: unsafe.length, safe_controls_over_strict: overStrict.length, result: unsafe.length ? 'fail' : 'pass', results };
  if (args.json) console.log(JSON.stringify(report, null, 2));
  else {
    for (const r of unsafe) console.log(`    UNSAFE ${r.id} (${r.category})`);
    for (const r of overStrict) console.log(`    WARNING over-strict ${r.id} (${r.category}): a safe control was rejected or replaced by /`);
    console.log(`probe-redirect ${report.module}#${report.export} -> ${report.result} (${results.length} attacks, ${unsafe.length} unsafe, ${overStrict.length} over-strict)`);
  }
  process.exit(unsafe.length ? 1 : 0);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
