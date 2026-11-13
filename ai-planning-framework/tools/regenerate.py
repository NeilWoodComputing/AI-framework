#!/usr/bin/env python3
"""
regenerate.py: rewrite the stored sample workbooks from tests/manifest.yaml.

    py tools/regenerate.py              # Windows (from the ai-planning-framework folder)
    python3 tools/regenerate.py         # Linux / macOS
    python3 tools/regenerate.py --group samples

Writes every manifest entry's `output` with that entry's group profile. Outputs under a work
folder (work/) are skipped: regenerate a feature's excel/ with
generators/excel_spec.py as part of that feature's planning stage. Run tools/check.py afterwards.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402  (shares manifest loading and generation with check.py)


def is_work_path(p: str) -> bool:
    parts = Path(p).parts
    return parts[0] == "work" or (parts[0] == "projects" and "work" in parts)


def main(argv=None) -> int:
    m = check.manifest()
    ap = argparse.ArgumentParser(description="Regenerate stored sample / example workbooks from tests/manifest.yaml.")
    ap.add_argument("--group", choices=sorted(m["groups"]), help="only this manifest group")
    a = ap.parse_args(argv)
    failed = 0
    for e in m["entries"]:
        out = e.get("output")
        if not out or is_work_path(out) or (a.group and e["group"] != a.group):
            continue
        data, _, _, errors = check.generate(m, e)
        if errors:
            failed += 1
            print(f"SKIP  {e['spec']}: invalid spec, nothing written")
            for msg in errors:
                print(f"      - {msg}")
            continue
        path = check.FW / out
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"Wrote {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
