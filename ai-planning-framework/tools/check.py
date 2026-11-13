#!/usr/bin/env python3
"""
check.py: one command that verifies ai-planning-framework. Exit code 0 = all checks pass.

Runs wherever Python 3.10+ with openpyxl, PyYAML and jsonschema is installed (the PC
or the agent box):

    py tools/check.py                 # Windows (from the ai-planning-framework folder)
    python3 tools/check.py            # Linux / macOS
    python3 tools/check.py --only schema,golden
    python3 tools/check.py --update-golden    # after an INTENDED output change; review the diff

Checks (see tools/README.md):
  schema    every page spec validates (strict); expected-invalid cases fail as expected
  profiles  every projects/*/project.yaml and the active profile (project.profile) validate; framework_version matches VERSION
  golden    regenerate every manifest entry and compare cell-by-cell with tests/golden/
  stored    stored workbooks (templates/out/, examples/, feature excel/) match their golden
  layout    fixed starter cells match templates/excel/page-spec-templates.xlsx
  starter   the starter workbook is byte-for-byte unchanged (sha256)
  encoding  text files are UTF-8, no BOM, no mixed line endings, no mojibake
  terms     no project-specific terms outside the allowed folders
  slugs     no feature slug exists in more than one work folder
  crossref  (warnings) services / permissions in specs match the project profile

The tool only reads, except --update-golden, which writes under tests/golden/ only.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import io
import json
import re
import sys
from pathlib import Path

FW = Path(__file__).resolve().parent.parent          # ai-planning-framework
ROOT = FW.parent                                      # ai-framework root (shared config)
sys.path.insert(0, str(FW / "generators"))

try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:  # pragma: no cover
    pass

try:
    import yaml
    import openpyxl
    import jsonschema
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(f"missing dependency: {exc.name}. Install with: python -m pip install -r requirements.txt\n")
    sys.exit(2)

import excel_spec as gen  # noqa: E402

STARTER = FW / "templates" / "excel" / "page-spec-templates.xlsx"
STARTER_SHA256 = "0227b0b6ba4c9bbc2cae09ab285ccfda6be79e1e5a13478b5425ced8932db3e0"
MANIFEST = FW / "tests" / "manifest.yaml"
TERMS = FW / "tests" / "leftover-terms.yaml"
PROFILE_SCHEMA = FW / "schemas" / "project-profile.schema.json"
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".py", ".txt", ".ps1", ".editorconfig", ""}
MOJIBAKE = re.compile("\u00e2\u20ac|\u00c3[\u0080-\u00bf\u00a9\u00a8]|\ufffd")


def rel(p: Path) -> str:
    return p.resolve().relative_to(FW).as_posix()


def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


class Report:
    def __init__(self) -> None:
        self.errors: dict[str, list[str]] = {}
        self.warnings: dict[str, list[str]] = {}
        self.ran: list[str] = []

    def err(self, section: str, msg: str) -> None:
        self.errors.setdefault(section, []).append(msg)

    def warn(self, section: str, msg: str) -> None:
        self.warnings.setdefault(section, []).append(msg)


# ---------------------------------------------------------------------------
# Workbook signature (cell-level; ignores file timestamps / zip metadata)
# ---------------------------------------------------------------------------
def _num(v):
    return round(v, 3) if isinstance(v, float) else v


def signature(wb) -> dict:
    out = {}
    for ws in wb.worksheets:
        cells = {}
        for row in ws.iter_rows():
            for c in row:
                if c.value is None and not c.has_style:
                    continue
                fill = c.fill.fgColor.rgb if c.fill is not None and c.fill.fill_type else None
                b = c.border
                cells[c.coordinate] = [
                    c.value if not isinstance(c.value, float) else _num(c.value),
                    bool(c.font.b), c.font.name, _num(c.font.sz), fill,
                    c.alignment.horizontal, c.alignment.vertical, bool(c.alignment.wrap_text),
                    b.left.style, b.right.style, b.top.style, b.bottom.style,
                ]
        out[ws.title] = {
            "cells": cells,
            "merges": sorted(str(m) for m in ws.merged_cells.ranges),
            "widths": {k: _num(v.width) for k, v in sorted(ws.column_dimensions.items()) if v.width},
            "heights": {str(k): _num(v.height) for k, v in sorted(ws.row_dimensions.items()) if v.height},
            "validations": sorted([str(dv.sqref), dv.formula1] for dv in ws.data_validations.dataValidation),
            "gridlines": bool(ws.sheet_view.showGridLines),
        }
    return out


def sig_of_bytes(data: bytes) -> dict:
    return signature(openpyxl.load_workbook(io.BytesIO(data)))


def diff_sig(a: dict, b: dict, limit: int = 8) -> list[str]:
    diffs = []
    if list(a) != list(b):
        diffs.append(f"sheets {list(a)} != {list(b)}")
    for s in a:
        if s not in b:
            continue
        for k in ("merges", "widths", "heights", "validations", "gridlines"):
            if a[s][k] != b[s][k]:
                diffs.append(f"{s}: {k} differ")
        ca, cb = a[s]["cells"], b[s]["cells"]
        for coord in sorted(set(ca) | set(cb)):
            if ca.get(coord) != cb.get(coord):
                diffs.append(f"{s}!{coord}: {ca.get(coord)} != {cb.get(coord)}")
    return diffs[:limit] + ([f"... {len(diffs) - limit} more"] if len(diffs) > limit else [])


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------
def manifest() -> dict:
    return load_yaml(MANIFEST)


def entry_golden(m: dict, e: dict) -> Path:
    g = m["groups"][e["group"]]
    name = e.get("golden") or (Path(e["spec"]).stem + ".json")
    return FW / g["golden_dir"] / name


def generate(m: dict, e: dict, validate: bool = True):
    """Return (workbook bytes, spec, profile, validation errors)."""
    spec_path = FW / e["spec"]
    spec = gen.load_spec(spec_path)
    errors = gen.validate_spec(spec) if validate else []
    profile = gen.load_profile(FW / m["groups"][e["group"]]["profile"])
    spec["_feature_module_label"] = gen.feature_module_label(profile)
    wb = gen.build_workbook(spec)
    return gen.workbook_bytes(wb), spec, profile, errors


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def all_spec_files() -> list[Path]:
    pats = ["templates/yaml/*.yaml", "examples/*/yaml/*.yaml", "tests/cases/*.yaml"]
    files = [p for pat in pats for p in FW.glob(pat)]
    for d in work_dirs():
        files += list(d.glob("*/specs/*.yaml"))
    return sorted(set(p.resolve() for p in files))


def check_schema(r: Report, m: dict) -> None:
    manifest_specs = {(FW / e["spec"]).resolve() for e in m["entries"]}
    for p in all_spec_files():
        try:
            spec = gen.load_spec(p)
        except Exception as exc:
            r.err("schema", f"{rel(p)}: cannot load: {exc}")
            continue
        for msg in gen.validate_spec(spec):
            r.err("schema", f"{rel(p)}: {msg}")
        for path in gen.deprecated_fields(spec):
            r.warn("schema", f"{rel(p)}: deprecated field {path}")
        if p not in manifest_specs:
            r.warn("schema", f"{rel(p)}: no golden (add it to tests/manifest.yaml)")
    for case in m.get("expect_invalid") or []:
        p = FW / case["spec"]
        try:
            msgs = gen.validate_spec(gen.load_spec(p))
        except Exception as exc:
            msgs = [str(exc)]
        if not msgs:
            r.err("schema", f"{case['spec']}: expected to FAIL validation but passed")
            continue
        joined = "\n".join(msgs)
        for want in case.get("errors") or []:
            if want not in joined:
                r.err("schema", f"{case['spec']}: expected an error containing {want!r}; got: {msgs}")


def show(p: Path) -> str:
    """Path relative to the framework, or to the ai-framework root when it lives outside."""
    p = p.resolve()
    try:
        return p.relative_to(FW).as_posix()
    except ValueError:
        return p.relative_to(ROOT).as_posix()


def profile_paths() -> list[Path]:
    """Framework defaults under projects/, plus the active profile named by the shared config."""
    paths = sorted(FW.glob("projects/*/project.yaml"))
    seen = {p.resolve() for p in paths}
    cfg_rel = ((shared_config().get("project") or {}).get("profile") or "").strip()
    if not cfg_rel:
        return paths
    cfg_path = (ROOT / cfg_rel).resolve()
    if cfg_path.is_file() and cfg_path not in seen:
        paths.append(cfg_path)
    return paths


def check_profiles(r: Report) -> None:
    schema = json.loads(PROFILE_SCHEMA.read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema)
    version = (FW / "VERSION").read_text(encoding="utf-8").strip()
    major_minor = ".".join(version.split(".")[:2])
    cfg_rel = ((shared_config().get("project") or {}).get("profile") or "").strip()
    if cfg_rel and not (ROOT / cfg_rel).is_file():
        r.err("profiles", f"{cfg_rel}: project.profile not found")
    for p in profile_paths():
        data = load_yaml(p) or {}
        for e in sorted(v.iter_errors(data), key=lambda e: list(e.absolute_path)):
            r.err("profiles", f"{show(p)}: {gen.format_error(e)}")
        fv = str(data.get("framework_version") or "")
        if fv and fv != major_minor:
            r.warn("profiles", f"{show(p)}: framework_version {fv} but VERSION is {version}")


def check_golden(r: Report, m: dict, update: bool, cache: dict) -> None:
    for e in m["entries"]:
        try:
            data, spec, profile, errs = generate(m, e)
        except Exception as exc:
            r.err("golden", f"{e['spec']}: generation failed: {exc}")
            continue
        cache[e["spec"]] = (data, spec, profile)
        sig = sig_of_bytes(data)
        g = entry_golden(m, e)
        if update:
            g.parent.mkdir(parents=True, exist_ok=True)
            g.write_text(json.dumps(sig, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            continue
        if not g.is_file():
            r.err("golden", f"{e['spec']}: golden {rel(g)} missing (run --update-golden)")
            continue
        want = json.loads(g.read_text(encoding="utf-8"))
        d = diff_sig(json.loads(json.dumps(sig)), want)
        if d:
            r.err("golden", f"{e['spec']} differs from {rel(g)}: " + "; ".join(d))


def check_stored(r: Report, m: dict) -> None:
    for e in m["entries"]:
        out = e.get("output")
        if not out:
            continue
        p = FW / out
        g = entry_golden(m, e)
        if not p.is_file():
            r.err("stored", f"{out}: missing (regenerate it)")
            continue
        if not g.is_file():
            continue
        d = diff_sig(json.loads(json.dumps(sig_of_bytes(p.read_bytes()))), json.loads(g.read_text(encoding="utf-8")))
        if d:
            r.err("stored", f"{out} is out of date vs {rel(g)}: " + "; ".join(d))


LAYOUT = {  # starter sheet -> (rows to compare, cells whose starter text is a placeholder value)
    "Modal Template": (range(2, 7), {"B3", "C5", "C3"}),
    "Wizard Template": (range(2, 7), {"B3", "C5"}),
    "Grid Page Template": (list(range(2, 8)) + [9], set()),
    "Import Template": (range(2, 27), {"C2", "G6", "G7", "G8", "G9", "G11", "C13", "C14", "C15", "C17", "C18",
                                       "C19", "C20", "C22", "G17", "G18", "G19", "G20", "G22"}),
}


def check_layout(r: Report, m: dict, cache: dict) -> None:
    ref = openpyxl.load_workbook(STARTER)
    for e in m["entries"]:
        if not e.get("layout") or e["spec"] not in cache:
            continue
        data, spec, profile = cache[e["spec"]]
        page_type = gen.normalise(spec)["page_type"]
        sheet = gen.SHEET_FOR_TYPE[page_type]
        rows, skip = LAYOUT[sheet]
        rows = list(rows)
        grid = sheet == "Grid Page Template"
        buttons = gen.normalise(spec)["_buttons"]
        if grid and page_type != "Paginated Grid" and not spec.get("search_filters"):
            rows = [x for x in rows if x != 9]
        aliases = {"Unity Feature": gen.feature_module_label(profile), "SectionTitle": "Section Title"}
        g = openpyxl.load_workbook(io.BytesIO(data)).active
        rs = ref[sheet]
        for row in rows:
            for col in range(2, 15):
                c = rs.cell(row, col)
                if c.value is None or c.coordinate in skip:
                    continue
                if grid and row <= 7 and col >= 9 + 3 * len(buttons):
                    continue  # starter shows two button blocks; a spec may have fewer
                want = aliases.get(str(c.value).strip(), str(c.value).strip())
                got = str(g.cell(row, col).value or "").strip()
                if got != want:
                    r.err("layout", f"{e['spec']} vs '{sheet}' {c.coordinate}: want {want!r} got {got!r}")
        for i in range(1, 15):
            L = openpyxl.utils.get_column_letter(i)
            rw = round(rs.column_dimensions[L].width or 0, 1)
            gw = round(g.column_dimensions[L].width or 0, 1)
            if rw != gw and not (grid and i >= 8):
                r.err("layout", f"{e['spec']}: column {L} width {gw} != starter {rw}")


def check_starter(r: Report) -> None:
    h = hashlib.sha256(STARTER.read_bytes()).hexdigest()
    if h != STARTER_SHA256:
        r.err("starter", f"templates/excel/page-spec-templates.xlsx changed (sha256 {h}); it must stay byte-for-byte")


def text_files():
    for p in sorted(FW.rglob("*")):
        if p.is_file() and (p.suffix.lower() in TEXT_EXT) and ".git" not in p.parts and "__pycache__" not in p.parts:
            yield p


def check_encoding(r: Report) -> None:
    for p in text_files():
        b = p.read_bytes()
        name = rel(p)
        if b.startswith(b"\xef\xbb\xbf"):
            r.err("encoding", f"{name}: has a UTF-8 BOM")
        try:
            t = b.decode("utf-8")
        except UnicodeDecodeError as exc:
            r.err("encoding", f"{name}: not valid UTF-8 ({exc})")
            continue
        crlf = t.count("\r\n")
        lf = t.count("\n") - crlf
        if crlf and lf:
            r.err("encoding", f"{name}: mixed line endings ({crlf} CRLF, {lf} LF)")
        if MOJIBAKE.search(t) and name != "tools/check.py":
            line = t[: MOJIBAKE.search(t).start()].count("\n") + 1
            r.err("encoding", f"{name}:{line}: looks like mojibake (double-encoded UTF-8 or U+FFFD)")


def check_terms(r: Report) -> None:
    cfg = load_yaml(TERMS)
    excl = cfg.get("exclude") or []
    terms = [(re.compile(t["pattern"], 0 if t.get("case_sensitive") else re.I), t) for t in cfg["terms"]]
    for p in text_files():
        name = rel(p)
        if any(fnmatch.fnmatch(name, pat) for pat in excl):
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for rx, t in terms:
                if rx.search(line) and not any(fnmatch.fnmatch(name, a) for a in t.get("allow_in") or []):
                    r.err("terms", f"{name}:{n}: {t['pattern']!r}: {line.strip()[:120]}")


def shared_config() -> dict:
    p = ROOT / "ai-framework.config.yaml"
    return (load_yaml(p) or {}) if p.is_file() else {}


def work_dirs() -> list[Path]:
    cfg = shared_config()
    out = cfg.get("output") or {}
    names = list(out.get("work_dirs") or [])
    for extra in (out.get("work_dir"), (cfg.get("project") or {}).get("work_dir")):
        if extra and extra not in names:
            names.append(extra)
    if not names:
        names = ["ai-planning-framework/work"]
    return [ROOT / n for n in names if (ROOT / n).is_dir()]


def check_slugs(r: Report) -> None:
    if not (ROOT / "ai-framework.config.yaml").is_file():
        r.warn("slugs", "ai-framework.config.yaml not found next to the framework; only ai-planning-framework/work checked")
    seen: dict[str, list[str]] = {}
    for d in work_dirs():
        for sub in d.iterdir():
            if sub.is_dir() and not sub.name.startswith((".", "_")):
                seen.setdefault(sub.name, []).append(d.relative_to(ROOT).as_posix())
    for slug, dirs in sorted(seen.items()):
        if len(dirs) > 1:
            r.err("slugs", f"feature slug {slug!r} exists in more than one work folder: {dirs} (RULES.md R8)")


def _walk(o, key, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key and isinstance(v, str) and v.strip():
                acc.add(v.strip())
            _walk(v, key, acc)
    elif isinstance(o, list):
        for i in o:
            _walk(i, key, acc)
    return acc


def permission_regex(profile: dict):
    perm = profile.get("permissions") or {}
    pattern = perm.get("pattern")
    if not pattern:
        return None
    actions = perm.get("actions") or []
    rx = re.escape(pattern).replace(re.escape("{entity}"), "[a-z][a-z0-9]*(?:_[a-z0-9]+)*?")
    rx = rx.replace(re.escape("{action}"), "(?:" + "|".join(map(re.escape, actions)) + ")" if actions else "[a-z]+")
    return re.compile("^" + rx + "$")


def check_crossref(r: Report, m: dict, cache: dict) -> None:
    for e in m["entries"]:
        if not m["groups"][e["group"]].get("cross_check") or e["spec"] not in cache:
            continue
        _, spec, profile = cache[e["spec"]]
        services = {s.get("name") for s in (profile.get("services") or [])}
        if services:
            for s in sorted(_walk(spec, "service", set()) - services):
                r.warn("crossref", f"{e['spec']}: service {s!r} is not in the profile's services")
        rx = permission_regex(profile)
        if rx:
            for p in sorted(_walk(spec, "required_permission", set())):
                if not rx.match(p):
                    r.warn("crossref", f"{e['spec']}: permission {p!r} does not match {profile['permissions']['pattern']!r}")


SECTIONS = ["schema", "profiles", "golden", "stored", "layout", "starter", "encoding", "terms", "slugs", "crossref"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Verify ai-planning-framework (exit 0 = pass).")
    ap.add_argument("--only", help="comma-separated sections: " + ",".join(SECTIONS))
    ap.add_argument("--update-golden", action="store_true", help="rewrite tests/golden/ from the current generator")
    ap.add_argument("-v", "--verbose", action="store_true", help="list every warning")
    a = ap.parse_args(argv)
    only = set(a.only.split(",")) if a.only else set(SECTIONS)
    unknown = only - set(SECTIONS)
    if unknown:
        ap.error(f"unknown section(s): {sorted(unknown)}")
    r, m, cache = Report(), manifest(), {}
    if "golden" not in only and ({"layout", "crossref"} & only):
        only.add("golden")  # layout / crossref reuse the regenerated workbooks
    steps = [
        ("schema", lambda: check_schema(r, m)),
        ("profiles", lambda: check_profiles(r)),
        ("golden", lambda: check_golden(r, m, a.update_golden, cache)),
        ("stored", lambda: check_stored(r, m)),
        ("layout", lambda: check_layout(r, m, cache)),
        ("starter", lambda: check_starter(r)),
        ("encoding", lambda: check_encoding(r)),
        ("terms", lambda: check_terms(r)),
        ("slugs", lambda: check_slugs(r)),
        ("crossref", lambda: check_crossref(r, m, cache)),
    ]
    for name, fn in steps:
        if name not in only:
            continue
        try:
            fn()
        except Exception as exc:  # a crashing check is a failure, never a pass
            r.err(name, f"check crashed: {type(exc).__name__}: {exc}")
        errs, warns = r.errors.get(name, []), r.warnings.get(name, [])
        status = "FAIL" if errs else "PASS"
        print(f"{status:4}  {name:9} errors={len(errs)} warnings={len(warns)}")
        for msg in errs:
            print(f"      ERROR  {msg}")
        for msg in (warns if a.verbose else warns[:3]):
            print(f"      warn   {msg}")
        if not a.verbose and len(warns) > 3:
            print(f"      ... {len(warns) - 3} more warnings (-v to list)")
    if a.update_golden:
        print("golden files rewritten: review the diff before keeping them")
    failed = any(r.errors.values())
    print("RESULT: " + ("FAIL" if failed else "PASS") + f"  (framework {(FW / 'VERSION').read_text(encoding='utf-8').strip() if (FW / 'VERSION').is_file() else '?'})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
