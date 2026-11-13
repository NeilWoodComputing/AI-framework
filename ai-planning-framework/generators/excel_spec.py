#!/usr/bin/env python3
"""
Generate page-spec Excel workbooks from YAML in the layout of the starter workbook
templates/excel/page-spec-templates.xlsx (the canonical layout reference).

Each page type follows one sheet of the starter:

  Form Modal, Basic Form          -> "Modal Template"
  Wizard Modal, Full-Page Wizard  -> "Wizard Template"
  Paginated Grid,
  Embedded Grid Modal             -> "Grid Page Template"
  Import                          -> "Import Template"

Cell positions, header blocks, button blocks, merges, column widths and spacer rows
match the starter. The fills keep the framework's pastel palette (see DECISIONS.md)
in place of the starter's dark-grey label cells. Framework-only blocks
(Route, Pagination, extra filter columns, Conditional Visibility, Notes) sit below or
to the right of the starter's blocks.

Wizard / form / import rows always include Service, Target DB Table, Target DB Column
unless include_service_db_columns is explicitly false (wizards / forms only).

The grid header label for feature_module comes from the project profile
(ui.feature_module_label, default 'Feature / Module'). The profile is --profile, or
project.profile in ../../ai-framework.config.yaml when that file exists.

The spec is validated against ../schemas/page-spec.schema.json first (strict: unknown or
misspelt fields are errors); errors name the field and nothing is written. --no-validate
skips this for a rough draft. Output is deterministic: the same YAML and profile give the
same .xlsx bytes (fixed document timestamps).

Usage:
  python excel_spec.py path/to/spec.yaml -o out.xlsx
  python excel_spec.py path/to/spec.yaml   # writes alongside YAML as <stem>.xlsx
  python excel_spec.py path/to/spec.yaml --profile ../projects/_template/project.yaml
  python excel_spec.py path/to/spec.yaml --no-validate     # draft only; not for hand-off
"""

from __future__ import annotations

import argparse
import functools
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    sys.exit(1)

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
except ImportError:
    sys.stderr.write("openpyxl required: pip install openpyxl\n")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Reference workbook (canonical layout). Column widths are read from it when it
# is present; the built-in copies below are used otherwise, so output is the same.
# ---------------------------------------------------------------------------
REFERENCE_WORKBOOK = Path(__file__).resolve().parent.parent / "templates" / "excel" / "page-spec-templates.xlsx"

SHEET_FOR_TYPE = {
    "Form Modal": "Modal Template",
    "Basic Form": "Modal Template",
    "Wizard Modal": "Wizard Template",
    "Full-Page Wizard": "Wizard Template",
    "Paginated Grid": "Grid Page Template",
    "Embedded Grid Modal": "Grid Page Template",
    "Import": "Import Template",
}

# Built-in copy of the starter's column widths (A..), used when the workbook is absent.
BUILTIN_WIDTHS = {
    "Modal Template": [1.4, 23.6, 18.9, 16.3, 15.1, 18.6, 14.9, 8.1, 14.9, 37.4, 28.4, 18.6, 24.0, 22.9],
    "Wizard Template": [1.4, 27.7, 24.9, 23.9, 15.1, 15.7, 17.3, 17.0, 15.7, 46.4, 35.6, 18.6, 24.0, 22.9],
    "Grid Page Template": [1.6, 22.0, 25.7, 26.1, 34.9, 24.7, 31.4, 3.7, 16.7, 25.6, 4.3, 17.0, 22.7, 14.6],
    "Import Template": [1.4, 17.0, 30.7, 14.3, 17.1, 15.9, 16.0, 21.0, 25.6, 15.3, 26.0, 25.0, 32.4, 28.1],
}
DEFAULT_WIDTH = 18.0

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "page-spec.schema.json"
FIXED_TIMESTAMP = "2000-01-01T00:00:00Z"      # written into docProps/core.xml for deterministic output
FIXED_ZIP_TIME = (2000, 1, 1, 0, 0, 0)

# Page types accepted as deprecated aliases (kept so older YAML still generates).
PAGE_TYPE_ALIASES = {"Modal": "Embedded Grid Modal"}

# ---------------------------------------------------------------------------
# Pastel palette (kept per decision 4) mapped onto the starter's label cells.
#   META      #E2EFDA  soft green    — page header labels, button blocks, Notes
#   STEP      #FCE4D6  soft peach    — wizard Step Title rows; grid Results Area
#   SECTION   #E2D5F1  soft lavender — Section Title rows; Conditional Visibility; Import validation title
#   HEADER    #D9E2F3  soft blue     — control / column / filter / actions / template-column header rows
#   ATTR      #DDEBF7  light blue    — grid attribute labels, Import panel labels, Pagination labels
# Value cells are white with bold text, as in the starter.
# ---------------------------------------------------------------------------
META_FILL = PatternFill("solid", fgColor="E2EFDA")
STEP_FILL = PatternFill("solid", fgColor="FCE4D6")
SECTION_FILL = PatternFill("solid", fgColor="E2D5F1")
HEADER_FILL = PatternFill("solid", fgColor="D9E2F3")
ATTR_FILL = PatternFill("solid", fgColor="DDEBF7")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")

FONT_NAME = "Aptos Narrow"
LABEL_FONT = Font(name=FONT_NAME, size=11)
VALUE_FONT = Font(name=FONT_NAME, size=11, bold=True)
BODY_FONT = Font(name=FONT_NAME, size=11)
THIN = Side(style="thin", color="000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top", horizontal="left")

SPACER = 7.5           # starter's thin spacer rows
LINE_HEIGHT = 15.0     # one line of 11pt text

BUTTON_ROWS = ["Button Label", "Button Type", "Visibility", "Enablement", "Req'd. Permission", "Click Action"]
BUTTON_KEYS = ["label", "type", "visibility", "enablement", "required_permission", "click_action"]

IMPORT_DEFAULT_DOWNLOAD = {
    "label": "Download Template",
    "type": "Primary Action",
    "visibility": "Always Visible",
    "enablement": "Always Enabled",
    "required_permission": "",
    "click_action": "Download template defined below",
}
IMPORT_DEFAULT_BUTTONS = [
    {"label": "Cancel", "type": "Additional Action", "visibility": "Always Visible",
     "enablement": "Always Enabled", "required_permission": "", "click_action": "Close page with no further action"},
    {"label": "Upload", "type": "Primary Action", "visibility": "Always Visible",
     "enablement": "Valid file added", "required_permission": "", "click_action": "Trigger validation logic"},
]
IMPORT_DEFAULT_PANEL = {
    "description": "A panel to allow the user to drag & drop files, or click to open Explorer",
    "text": "Drag & Drop completed upload template files here, or click to explore your files",
    "functional_requirements": (
        "Clicking the panel will open File Explorer with the file extension filter pre-set to .xls & .xlsx\n"
        "A file can be drag-dropped from a File Explorer window opened other than via clicking the panel\n"
        "If a file with an extension of .xls or .xlsx is added by either method, it will appear at the foot of "
        "the panel and display:\n- A file icon\n- The full filename including extension\n- A red X control\n\n"
        "If a file other than .xls or .xlsx is added by either of these methods, the file will not appear and an "
        "error message will be displayed\n"
        "Clicking the red X control will remove the file from the panel\n"
        "If a second file is added by either method, the original file will be replaced - only one file is "
        "allowed at a time"
    ),
}


# ---------------------------------------------------------------------------
# Spec normalisation (old field names stay valid)
# ---------------------------------------------------------------------------
def normalise(spec: dict) -> dict:
    s = dict(spec)
    pt = s.get("page_type") or ""
    if pt in PAGE_TYPE_ALIASES:   # reported by deprecated_fields()
        s["page_type"] = PAGE_TYPE_ALIASES[pt]
    # feature_module; older name system_feature is still accepted.
    s["_feature_module"] = next(
        (s.get(k) for k in ("feature_module", "system_feature") if s.get(k) not in (None, "")), ""
    )
    s["_sub_title"] = s.get("page_sub_title") if s.get("page_sub_title") not in (None, "") else (s.get("page_sub_text") or "")
    buttons = s.get("buttons")
    if not buttons and s.get("primary_action"):
        buttons = [s["primary_action"]]
    s["_buttons"] = [_norm_button(b) for b in (buttons or [])]
    return s


def _norm_button(b: dict) -> dict:
    out = dict(b)
    if out.get("click_action") in (None, "") and out.get("action"):
        out["click_action"] = out["action"]
    return out


def _parents(spec: dict) -> str:
    pages = spec.get("parent_pages") or []
    if isinstance(pages, str):
        return pages
    return ", ".join(str(p) for p in pages)


def _include_db(spec: dict) -> bool:
    if "include_service_db_columns" in spec:
        return bool(spec["include_service_db_columns"])
    return True


def _text(v: Any) -> Any:
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, list):
        v = ", ".join(str(x) for x in v)
    if isinstance(v, str):
        if ILLEGAL_CHARACTERS_RE.search(v):
            sys.stderr.write(f"warning: removed control characters Excel cannot store from {v[:40]!r}\n")
            v = ILLEGAL_CHARACTERS_RE.sub("", v)
        return v.strip("\n")
    return v


# ---------------------------------------------------------------------------
# Cell helpers
# ---------------------------------------------------------------------------
class Sheet:
    """Thin wrapper that records fixed row heights for the final height pass."""

    def __init__(self, ws, widths: list[float]):
        self.ws = ws
        self.widths = widths
        self.fixed_heights: dict[int, float] = {}

    def width(self, col: int) -> float:
        letter = get_column_letter(col)
        w = self.ws.column_dimensions[letter].width
        return w if w else DEFAULT_WIDTH

    def spacer(self, row: int, height: float = SPACER) -> None:
        self.fixed_heights[row] = height

    def _merge(self, row: int, col: int, end_col: int | None, end_row: int | None = None) -> None:
        end_col = end_col or col
        end_row = end_row or row
        if end_col > col or end_row > row:
            self.ws.merge_cells(start_row=row, start_column=col, end_row=end_row, end_column=end_col)
        for r in range(row, end_row + 1):
            for c in range(col, end_col + 1):
                self.ws.cell(row=r, column=c).border = BORDER

    def _fill(self, row: int, col: int, end_col: int | None, end_row: int | None, fill) -> None:
        for r in range(row, (end_row or row) + 1):
            for c in range(col, (end_col or col) + 1):
                self.ws.cell(row=r, column=c).fill = fill

    def label(self, row: int, col: int, text: str, fill=META_FILL, end_col: int | None = None,
              end_row: int | None = None, bold: bool = False) -> None:
        cell = self.ws.cell(row=row, column=col, value=text)
        cell.font = VALUE_FONT if bold else LABEL_FONT
        cell.alignment = WRAP
        self._fill(row, col, end_col, end_row, fill)
        self._merge(row, col, end_col, end_row)

    def value(self, row: int, col: int, val: Any, end_col: int | None = None, end_row: int | None = None,
              bold: bool = True) -> None:
        v = _text(val)
        cell = self.ws.cell(row=row, column=col, value=v if v not in ("",) else None)
        cell.font = VALUE_FONT if bold else BODY_FONT
        cell.alignment = WRAP
        self._fill(row, col, end_col, end_row, WHITE_FILL)
        self._merge(row, col, end_col, end_row)

    def header_row(self, row: int, headers: list[tuple[int, int | None, str]], fill=HEADER_FILL) -> None:
        for col, end_col, text in headers:
            self.label(row, col, text, fill=fill, end_col=end_col)

    def finish_heights(self) -> None:
        ws = self.ws
        merged_width: dict[tuple[int, int], float] = {}
        merged_rows: dict[tuple[int, int], int] = {}
        for rng in ws.merged_cells.ranges:
            w = sum(self.width(c) for c in range(rng.min_col, rng.max_col + 1))
            merged_width[(rng.min_row, rng.min_col)] = w
            merged_rows[(rng.min_row, rng.min_col)] = rng.max_row - rng.min_row + 1
        needed: dict[int, float] = {}
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is None or not isinstance(cell.value, (str, int, float)):
                    continue
                key = (cell.row, cell.column)
                width = merged_width.get(key, self.width(cell.column))
                chars_per_line = max(4.0, width * 0.9)
                lines = 0
                for part in str(cell.value).split("\n"):
                    lines += max(1, math.ceil(len(part) / chars_per_line))
                height = lines * LINE_HEIGHT / merged_rows.get(key, 1)
                needed[cell.row] = max(needed.get(cell.row, LINE_HEIGHT), height)
        for r, h in needed.items():
            if r in self.fixed_heights:
                continue
            if h > LINE_HEIGHT:
                ws.row_dimensions[r].height = min(409.0, h)
        for r, h in self.fixed_heights.items():
            ws.row_dimensions[r].height = h


@functools.lru_cache(maxsize=None)
def _reference_book():
    """The starter workbook, opened once per process (None when absent or unreadable)."""
    if not REFERENCE_WORKBOOK.is_file():
        return None
    try:
        return load_workbook(REFERENCE_WORKBOOK)
    except Exception as exc:  # fall back to the built-in widths, but say so
        sys.stderr.write(f"warning: cannot read {REFERENCE_WORKBOOK.name} ({exc}); using built-in column widths\n")
        return None


def _reference_widths(sheet_name: str) -> list[float]:
    wb = _reference_book()
    if wb is not None and sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        widths = []
        for i in range(1, 15):
            w = ws.column_dimensions[get_column_letter(i)].width
            widths.append(round(w, 1) if w else DEFAULT_WIDTH)
        return widths
    if wb is not None:
        sys.stderr.write(f"warning: sheet {sheet_name!r} not in {REFERENCE_WORKBOOK.name}; using built-in column widths\n")
    return list(BUILTIN_WIDTHS[sheet_name])


def _apply_widths(ws, widths: list[float]) -> None:
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------
def _control_headers(include_db: bool, list_form: bool = False) -> list[str]:
    headers = [
        "Column Label" if list_form else "Control Label",
        "Control Type",
        "Input Format",
        " Min. Len. / Val.",
        " Max. Len. / Val.",
        "Enablement",
        "Editable",
        "Mandatory",
        "Validation Rules / Other Functionality",
        "Validation Failure Message(s)",
    ]
    if include_db:
        headers += ["Service", "Target DB Table", "Target DB Column"]
    return headers


def _write_control_header(sh: Sheet, row: int, include_db: bool, list_form: bool = False) -> None:
    for i, h in enumerate(_control_headers(include_db, list_form), start=2):
        sh.label(row, i, h, fill=HEADER_FILL)


def _write_controls(sh: Sheet, row: int, controls: list[dict], include_db: bool, list_form: bool = False) -> int:
    """Control header row + one row per control; returns the next free row."""
    _write_control_header(sh, row, include_db, list_form)
    row += 1
    for ctrl in controls:
        _write_control_row(sh, row, ctrl, include_db)
        row += 1
    return row


def _write_control_row(sh: Sheet, row: int, ctrl: dict, include_db: bool) -> None:
    values = [
        ctrl.get("label"),
        ctrl.get("control_type"),
        ctrl.get("input_format"),
        ctrl.get("min_len_val"),
        ctrl.get("max_len_val"),
        ctrl.get("enablement", "Always"),
        ctrl.get("editable", "Yes"),
        ctrl.get("mandatory", "No"),
        ctrl.get("validation_rules"),
        ctrl.get("validation_failure_messages"),
    ]
    if include_db:
        values += [ctrl.get("service"), ctrl.get("target_db_table"), ctrl.get("target_db_column")]
    for i, v in enumerate(values):
        sh.value(row, 2 + i, v, bold=(i == 0))


def _write_header_two_row(sh: Sheet, spec: dict, page_type: str, title: str) -> None:
    """Modal / Wizard starter header: labels on row 2, values on row 3."""
    sh.spacer(1)
    sh.label(2, 2, "Page Type")
    sh.label(2, 3, "Page Title", end_col=6)
    sh.label(2, 7, "Page Sub-Title", end_col=10)
    sh.label(2, 11, "Required Permission", end_col=12)
    sh.label(2, 13, "Parent Page(s)", end_col=14)
    sh.value(3, 2, page_type)
    sh.value(3, 3, title, end_col=6)
    sh.value(3, 7, spec["_sub_title"], end_col=10)
    sh.value(3, 11, spec.get("required_permission") or "", end_col=12)
    sh.value(3, 13, _parents(spec))
    sh.ws.cell(row=3, column=14).border = BORDER
    sh.spacer(4)


def _write_button(sh: Sheet, row: int, lc: int, vc: int, ve: int | None, btn: dict) -> None:
    """One button block: six label rows in column lc, values in vc (merged to ve)."""
    for offset, (lbl, key) in enumerate(zip(BUTTON_ROWS, BUTTON_KEYS)):
        sh.label(row + offset, lc, lbl)
        sh.value(row + offset, vc, btn.get(key) or "", end_col=ve, bold=(key == "label"))


def _write_button_blocks(sh: Sheet, row: int, buttons: list[dict], slots: list[tuple[int, int, int]]) -> int:
    """Button blocks side by side (label column + merged value columns), six rows each."""
    if not buttons:
        return row
    for start in range(0, len(buttons), len(slots)):
        group = buttons[start:start + len(slots)]
        for btn, (lc, vc, ve) in zip(group, slots):
            _write_button(sh, row, lc, vc, ve, btn)
        row += len(BUTTON_ROWS) + 1
    return row


def _write_conditional(sh: Sheet, row: int, rules: list[dict], then_cols: tuple[int, int],
                       notes_cols: tuple[int, int], band_end: int) -> int:
    if not rules:
        return row
    sh.label(row, 2, "Conditional Visibility", fill=SECTION_FILL, end_col=band_end)
    row += 1
    sh.header_row(row, [(2, None, "When"), (then_cols[0], then_cols[1], "Then"), (notes_cols[0], notes_cols[1], "Notes")])
    row += 1
    for rule in rules:
        sh.value(row, 2, rule.get("when"))
        sh.value(row, then_cols[0], rule.get("then"), end_col=then_cols[1], bold=False)
        sh.value(row, notes_cols[0], rule.get("notes"), end_col=notes_cols[1], bold=False)
        row += 1
    return row + 1


def _write_notes(sh: Sheet, row: int, spec: dict, end_col: int) -> int:
    notes = spec.get("notes")
    if not notes:
        return row
    sh.label(row, 2, "Notes")
    sh.value(row, 3, str(notes).strip(), end_col=end_col, bold=False)
    return row + 2


# ---------------------------------------------------------------------------
# Form Modal / Basic Form — "Modal Template"
# ---------------------------------------------------------------------------
FORM_BUTTON_SLOTS = [(2, 3, 4), (6, 7, 9), (10, 11, 12), (13, 14, 14)]


def _write_section_row(sh: Sheet, row: int, sec: dict) -> None:
    sh.label(row, 2, "Section Title", fill=SECTION_FILL)
    sh.value(row, 3, sec.get("title") or "", end_col=5)
    sh.label(row, 6, "Section Visibility", fill=SECTION_FILL)
    sh.value(row, 7, sec.get("visibility") or "Always shown", end_col=9)
    sh.label(row, 10, "Additional Functionality", fill=SECTION_FILL)
    sh.value(row, 11, sec.get("additional_functionality") or "N/A", end_col=14)


def write_form(sh: Sheet, spec: dict) -> None:
    include_db = _include_db(spec)
    band_end = 14 if include_db else 11
    _write_header_two_row(sh, spec, spec["page_type"], spec.get("page_title") or "Untitled")

    sections = spec.get("sections") or []
    flat = spec.get("controls") or []
    row = 5
    if sections:
        for idx, sec in enumerate(sections):
            if idx:
                sh.spacer(row)
                row += 1
            _write_section_row(sh, row, sec)
            row = _write_controls(sh, row + 1, sec.get("controls") or [], include_db)
    else:
        row = _write_controls(sh, row, flat, include_db)

    row += 1  # blank row before buttons (starter row 12)
    row = _write_button_blocks(sh, row, spec["_buttons"], FORM_BUTTON_SLOTS)
    row = _write_conditional(sh, row, spec.get("conditional_visibility") or [], (3, 6), (7, band_end), band_end)
    _write_notes(sh, row, spec, band_end)


# ---------------------------------------------------------------------------
# Wizard Modal / Full-Page Wizard — "Wizard Template"
# ---------------------------------------------------------------------------
def _write_step_like_row(sh: Sheet, row: int, kind: str, item: dict, fill, dv: DataValidation) -> None:
    title_label = "Step Title" if kind == "Step" else "Section Title"
    extra_label = "Additional Step Functionality" if kind == "Step" else "Additional Section Functionality"
    sh.label(row, 2, title_label, fill=fill)
    sh.value(row, 3, item.get("title") or "", end_col=5)
    sh.label(row, 6, f"{kind} Format", fill=fill)
    sh.value(row, 7, item.get("format") or "Standard Form", end_col=8)
    dv.add(f"G{row}:H{row}")
    sh.label(row, 9, f"{kind} Visibility", fill=fill)
    sh.value(row, 10, item.get("visibility") or "Always shown")
    sh.label(row, 11, extra_label, fill=fill)
    sh.value(row, 12, item.get("additional_functionality") or "N/A", end_col=14)


def write_wizard(sh: Sheet, spec: dict) -> None:
    include_db = _include_db(spec)
    band_end = 14 if include_db else 11
    title = spec.get("page_title") or spec.get("wizard_name") or "Untitled"
    _write_header_two_row(sh, spec, spec["page_type"], title)

    dv = DataValidation(type="list", formula1='"Standard Form,List Form"', allow_blank=True)
    sh.ws.add_data_validation(dv)

    row = 5
    for step in spec.get("steps") or []:
        _write_step_like_row(sh, row, "Step", step, STEP_FILL, dv)
        row += 1
        controls = step.get("controls") or []
        sections = step.get("sections") or []
        if controls or not sections:
            row = _write_controls(sh, row, controls, include_db, step.get("format") == "List Form")
        for sec in sections:
            sh.spacer(row)
            _write_step_like_row(sh, row + 1, "Section", sec, SECTION_FILL, dv)
            row = _write_controls(sh, row + 2, sec.get("controls") or [], include_db, sec.get("format") == "List Form")
        sh.spacer(row)
        sh.spacer(row + 1)
        row += 2

    if spec["_buttons"]:
        row = _write_button_blocks(sh, row, spec["_buttons"], FORM_BUTTON_SLOTS)
    row = _write_conditional(sh, row, spec.get("conditional_visibility") or [], (3, 6), (7, band_end), band_end)
    _write_notes(sh, row, spec, band_end)


# ---------------------------------------------------------------------------
# Paginated Grid / Embedded Grid Modal — "Grid Page Template"
# ---------------------------------------------------------------------------
def write_grid(sh: Sheet, spec: dict) -> None:
    page_type = spec["page_type"]
    results = spec.get("results_area") or {}
    columns = results.get("columns") or []
    last_col = max(7, 2 + len(columns))   # results columns run C.. (starter: C..G)
    # Widen columns that results columns spill into (the starter's H and K are narrow spacers).
    for c in range(8, last_col + 1):
        letter = get_column_letter(c)
        sh.ws.column_dimensions[letter].width = max(sh.width(c), DEFAULT_WIDTH)

    # Header rows 2-4 (row 1 is the starter's 9pt spacer)
    sh.spacer(1, 9.0)
    sh.label(2, 2, "Page Type")
    sh.value(2, 3, page_type)
    sh.label(2, 4, spec.get("_feature_module_label") or DEFAULT_FEATURE_MODULE_LABEL)
    sh.value(2, 5, spec["_feature_module"])
    sh.label(2, 6, "Nav Tree Path")
    sh.value(2, 7, spec.get("nav_tree_path") or "")
    sh.label(3, 2, "Page Title")
    sh.value(3, 3, spec.get("page_title") or "", end_col=5)
    sh.label(3, 6, "Required Permission", end_row=4)
    sh.value(3, 7, spec.get("required_permission") or "", end_row=4)
    sh.label(4, 2, "Page Sub-title")
    sh.value(4, 3, spec["_sub_title"], end_col=5)
    if spec.get("route") or page_type == "Paginated Grid":
        # Framework-only: Route sits in the empty left area under the header.
        sh.label(5, 2, "Route")
        sh.value(5, 3, spec.get("route") or "", end_col=5)

    # Button blocks to the right, rows 2-7: I/J, L/M, O/P, ...
    for n, btn in enumerate(spec["_buttons"]):
        lc = 9 + 3 * n
        if lc + 1 > 14:
            for c in (lc, lc + 1):
                sh.ws.column_dimensions[get_column_letter(c)].width = max(sh.width(c), DEFAULT_WIDTH)
        _write_button(sh, 2, lc, lc + 1, None, btn)

    # Filters (starter row 9)
    row = 9
    filters = spec.get("search_filters")
    if page_type == "Paginated Grid" or filters:
        extras = [k for k in ("filters_on", "match_rule", "default") if any(f.get(k) not in (None, "") for f in (filters or []))]
        extra_titles = {"filters_on": "Filters On (Population Source)", "match_rule": "Match Rule", "default": "Default"}
        headers = [(2, None, "Filter Control Label"), (3, None, "Control Type"), (4, None, "Input Format"),
                   (5, None, "Min. Length"), (6, None, "Max. Length"), (7, None, "Mandatory"),
                   (8, 10, "Additional Functionality / Design Information")]
        extra_cols = {}
        for i, k in enumerate(extras):
            extra_cols[k] = 12 + i            # framework-only, right of H:J (skips the K spacer)
            headers.append((12 + i, None, extra_titles[k]))
        sh.header_row(row, headers)
        row += 1
        if filters:
            for f in filters:
                sh.value(row, 2, f.get("label"))
                sh.value(row, 3, f.get("control_type"), bold=False)
                sh.value(row, 4, f.get("input_format"), bold=False)
                sh.value(row, 5, f.get("min_length"), bold=False)
                sh.value(row, 6, f.get("max_length"), bold=False)
                sh.value(row, 7, f.get("mandatory"), bold=False)
                sh.value(row, 8, f.get("additional_functionality"), end_col=10, bold=False)
                for k, c in extra_cols.items():
                    sh.value(row, c, f.get(k), bold=False)
                row += 1
        else:
            sh.value(row, 2, "None (no on-page search or filters)", end_col=7, bold=False)
            sh.value(row, 8, None, end_col=10, bold=False)
            row += 1
        row += 1
    else:
        row = 9  # embedded grid without filters: results area moves up only if nothing else is there

    # Results Area (starter row 12) + transposed attribute rows
    sh.label(row, 2, "Results Area", fill=STEP_FILL)
    sh.value(row, 3, results.get("description") or "", end_col=last_col)
    row += 1
    attr_rows = [("Column Title", "title"), ("Population Source", "population_source"),
                 ("Display Format", "display_format"), ("Sortable?", "sortable"),
                 ("Additional Functionality", "additional_functionality")]
    for idx, (lbl, key) in enumerate(attr_rows):
        sh.label(row, 2, lbl, fill=HEADER_FILL if idx == 0 else ATTR_FILL)
        for c_idx, col in enumerate(columns):
            sh.value(row, 3 + c_idx, col.get(key), bold=(idx == 0))
        for c in range(3 + len(columns), last_col + 1):
            sh.value(row, c, None, bold=False)
        row += 1
    row += 1

    # Actions menu (starter row 19)
    sh.header_row(row, [(2, None, " Actions Menu Item"), (3, None, "Icon"), (4, None, "Req'd. Permission"),
                        (5, None, "Availability Logic"), (6, 10, "Action(s) on Click")])
    row += 1
    menu = spec.get("actions_menu") or []
    for item in menu:
        avail = item.get("availability_logic")
        if avail in (None, ""):
            avail = item.get("availability", "Always")
        sh.value(row, 2, item.get("item"))
        sh.value(row, 3, item.get("icon"), bold=False)
        sh.value(row, 4, item.get("required_permission"), bold=False)
        sh.value(row, 5, avail, bold=False)
        sh.value(row, 6, item.get("action_on_click"), end_col=10, bold=False)
        row += 1
    if not menu:
        sh.value(row, 2, "None", bold=False)
        for c in (3, 4, 5):
            sh.value(row, c, None, bold=False)
        sh.value(row, 6, None, end_col=10, bold=False)
        row += 1
    row += 1

    # Framework-only: pagination / results details
    pagination = spec.get("pagination") or {}
    pag_rows = [
        ("Results Visibility", results.get("visibility")),
        ("Page Size", pagination.get("page_size")),
        ("Page Size Options", pagination.get("page_size_options")),
        ("Paging", pagination.get("paging")),
        ("Default Sort", pagination.get("default_sort")),
        ("Paging Notes", pagination.get("notes")),
        ("Empty State", results.get("empty_state")),
    ]
    pag_rows = [(l, v) for l, v in pag_rows if v not in (None, "", [])]
    if pag_rows:
        for lbl, val in pag_rows:
            sh.label(row, 2, lbl, fill=ATTR_FILL)
            sh.value(row, 3, val, end_col=7, bold=False)
            row += 1
        row += 1

    _write_notes(sh, row, spec, 10)


# ---------------------------------------------------------------------------
# Import — "Import Template"
# ---------------------------------------------------------------------------
def write_import(sh: Sheet, spec: dict) -> None:
    imp = spec.get("import") or {}
    sh.spacer(1)
    sh.label(2, 2, "Page Type")
    sh.value(2, 3, spec["page_type"])
    sh.label(2, 4, "Parent Page(s)")
    sh.value(2, 5, _parents(spec), end_col=6)
    sh.label(2, 7, "Req'd. Permission")
    sh.value(2, 8, spec.get("required_permission") or "")
    sh.label(3, 2, "Page Title")
    sh.value(3, 3, spec.get("page_title") or "", end_col=8)
    sh.label(4, 2, "Page Sub-text")
    sh.value(4, 3, spec["_sub_title"], end_col=8)
    sh.spacer(5)

    download = dict(IMPORT_DEFAULT_DOWNLOAD)
    download.update({k: v for k, v in (imp.get("download_button") or {}).items() if v not in (None,)})
    download = _norm_button(download)
    _write_button(sh, 6, 6, 7, 8, download)
    sh.spacer(12)

    panel = dict(IMPORT_DEFAULT_PANEL)
    panel.update({k: v for k, v in (imp.get("panel") or {}).items() if v not in (None, "")})
    sh.label(13, 2, "Panel Description", fill=ATTR_FILL)
    sh.value(13, 3, panel["description"], end_col=8)
    sh.label(14, 2, "Panel Text", fill=ATTR_FILL)
    sh.value(14, 3, panel["text"], end_col=8, bold=False)
    sh.label(15, 2, "Functional Requirements", fill=ATTR_FILL)
    sh.value(15, 3, panel["functional_requirements"], end_col=8, bold=False)
    sh.spacer(16)

    buttons = spec["_buttons"] or [dict(b) for b in IMPORT_DEFAULT_BUTTONS]
    row = _write_button_blocks(sh, 17, buttons, [(2, 3, 3), (6, 7, 8)])
    # starter: buttons rows 17-22, 9pt spacer row 23, validation title row 24
    row = max(row - 1, 23)
    sh.spacer(row, 9.0)
    row += 1

    sh.label(row, 2, "Template Format & Upload Validation Logic", fill=SECTION_FILL, end_col=12, bold=True)
    row += 1
    sh.label(row, 2, "Validation Logic", fill=ATTR_FILL)
    sh.value(row, 3, imp.get("validation_logic") or "", end_col=12, bold=False)
    row += 1
    sh.header_row(row, [(2, 3, "Template Column Name"), (4, None, "Mandatory"), (5, 6, "Format"),
                        (7, None, "Min. Len / Value"), (8, None, "Max. Len / Value"),
                        (9, None, "Additional Validation Rules"), (10, None, "Service"),
                        (11, None, "Target DB Table"), (12, None, "Target DB Column")])
    row += 1
    for col in imp.get("template_columns") or []:
        sh.value(row, 2, col.get("name"), end_col=3)
        sh.value(row, 4, col.get("mandatory", "No"), bold=False)
        sh.value(row, 5, col.get("format"), end_col=6, bold=False)
        sh.value(row, 7, col.get("min_len_val"), bold=False)
        sh.value(row, 8, col.get("max_len_val"), bold=False)
        sh.value(row, 9, col.get("additional_validation_rules"), bold=False)
        sh.value(row, 10, col.get("service"), bold=False)
        sh.value(row, 11, col.get("target_db_table"), bold=False)
        sh.value(row, 12, col.get("target_db_column"), bold=False)
        row += 1
    row += 1
    row = _write_conditional(sh, row, spec.get("conditional_visibility") or [], (3, 6), (7, 12), 12)
    _write_notes(sh, row, spec, 12)


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------
def build_workbook(raw_spec: dict) -> Workbook:
    spec = normalise(raw_spec)
    page_type = spec.get("page_type") or ""
    if page_type not in SHEET_FOR_TYPE:
        raise ValueError(f"Unsupported page_type: {raw_spec.get('page_type')!r}")
    wb = Workbook()
    ws = wb.active
    title = spec.get("page_title") or spec.get("wizard_name") or "Page Spec"
    for ch in '\\/?*[]:':
        title = title.replace(ch, "-")
    ws.title = title[:31]
    ws.sheet_view.showGridLines = False
    widths = _reference_widths(SHEET_FOR_TYPE[page_type])
    _apply_widths(ws, widths)
    sh = Sheet(ws, widths)

    if page_type in ("Full-Page Wizard", "Wizard Modal"):
        write_wizard(sh, spec)
    elif page_type in ("Basic Form", "Form Modal"):
        write_form(sh, spec)
    elif page_type in ("Paginated Grid", "Embedded Grid Modal"):
        write_grid(sh, spec)
    else:
        write_import(sh, spec)
    sh.finish_heights()
    return wb


def load_spec(path: Path) -> dict:
    with path.open(encoding="utf-8-sig") as f:   # tolerate a BOM on input; never write one
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping (page spec object)")
    if not data.get("page_type"):
        raise ValueError("page_type is required")
    if not data.get("page_title") and not data.get("wizard_name"):
        raise ValueError("page_title or wizard_name is required")
    return data


# ---------------------------------------------------------------------------
# Validation (schemas/page-spec.schema.json)
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=None)
def _validator():
    try:
        import jsonschema
    except ImportError:
        return None
    return jsonschema.Draft202012Validator(_schema())


def format_error(err) -> str:
    """'sections[0].controls[1]: 'service' is a required property' style message."""
    path = ""
    for part in err.absolute_path:
        path += f"[{part}]" if isinstance(part, int) else (f".{part}" if path else str(part))
    msg = err.message
    if err.validator == "additionalProperties":
        msg = msg.replace("Additional properties are not allowed", "unknown field(s)")
    return f"{path or '(top level)'}: {msg}"


def validate_spec(spec: dict) -> list[str]:
    """Schema errors as readable strings (empty list = valid). Raises RuntimeError without jsonschema."""
    v = _validator()
    if v is None:
        raise RuntimeError("jsonschema is not installed: python -m pip install --user jsonschema "
                           "(or pass --no-validate for a draft)")
    data = {k: val for k, val in spec.items() if not k.startswith("_")}
    errs = sorted(v.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path])
    return [format_error(e) for e in errs]


def _resolve(node: dict) -> dict:
    ref = node.get("$ref") if isinstance(node, dict) else None
    if ref and ref.startswith("#/$defs/"):
        return _resolve(_schema()["$defs"][ref.split("/")[-1]])
    return node if isinstance(node, dict) else {}


def deprecated_fields(spec: dict) -> list[str]:
    """Paths of fields the schema marks deprecated (older names that still work)."""
    found: list[str] = []
    if spec.get("page_type") in PAGE_TYPE_ALIASES:
        found.append(f"page_type: {spec['page_type']} (use {PAGE_TYPE_ALIASES[spec['page_type']]})")

    def walk(schema: dict, data: Any, path: str) -> None:
        schema = _resolve(schema)
        if isinstance(data, dict):
            props = schema.get("properties") or {}
            for k, v in data.items():
                sub = _resolve(props.get(k) or {})
                here = f"{path}.{k}" if path else k
                if (props.get(k) or {}).get("deprecated") or sub.get("deprecated"):
                    found.append(here)
                if sub:
                    walk(sub, v, here)
        elif isinstance(data, list) and schema.get("items"):
            for i, item in enumerate(data):
                walk(schema["items"], item, f"{path}[{i}]")

    walk(_schema(), spec, "")
    return found


def workbook_bytes(wb: Workbook) -> bytes:
    """Serialise with fixed timestamps so identical input gives identical bytes."""
    raw = io.BytesIO()
    wb.save(raw)
    src = zipfile.ZipFile(io.BytesIO(raw.getvalue()))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                              rb"\g<1>" + FIXED_TIMESTAMP.encode() + rb"\g<2>", data)
            zi = zipfile.ZipInfo(info.filename, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            dst.writestr(zi, data)
    return out.getvalue()


# ---------------------------------------------------------------------------
# Project profile (project.profile in ai-framework.config.yaml; defaults in projects/_template/project.yaml)
# ---------------------------------------------------------------------------
DEFAULT_FEATURE_MODULE_LABEL = "Feature / Module"
SHARED_CONFIG = Path(__file__).resolve().parent.parent.parent / "ai-framework.config.yaml"


def load_profile(path: Path | None) -> dict:
    """Read the project profile from --profile, else from project.profile in the shared config."""
    if path is None and SHARED_CONFIG.is_file():
        cfg = yaml.safe_load(SHARED_CONFIG.read_text(encoding="utf-8")) or {}
        rel = ((cfg.get("project") or {}).get("profile") or "").strip()
        if rel:
            path = SHARED_CONFIG.parent / rel
    if path is None:
        return {}
    if not path.is_file():
        sys.stderr.write(f"note: profile {path} not found; using framework defaults\n")
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def feature_module_label(profile: dict) -> str:
    return ((profile.get("ui") or {}).get("feature_module_label") or DEFAULT_FEATURE_MODULE_LABEL)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate page-spec Excel from YAML in the layout of templates/excel/page-spec-templates.xlsx."
    )
    parser.add_argument("yaml_path", type=Path, help="Path to page spec YAML")
    parser.add_argument("-o", "--output", type=Path, help="Output .xlsx path (default: <yaml_stem>.xlsx beside input)")
    parser.add_argument("--no-validate", action="store_true",
                        help="Skip schema validation (rough drafts only; specs for hand-off must validate)")
    parser.add_argument(
        "--profile", type=Path,
        help="Project profile. Default: project.profile from ai-framework.config.yaml",
    )
    args = parser.parse_args(argv)

    if not args.yaml_path.is_file():
        sys.stderr.write(f"File not found: {args.yaml_path}\n")
        return 1

    try:
        spec = load_spec(args.yaml_path)
        if not args.no_validate:
            errors = validate_spec(spec)
            if errors:
                sys.stderr.write(f"Invalid spec {args.yaml_path} ({len(errors)} error(s)); nothing written:\n")
                for e in errors:
                    sys.stderr.write(f"  - {e}\n")
                sys.stderr.write("Fix the spec (schemas/page-spec.schema.json), or pass --no-validate for a draft.\n")
                return 1
        for path in deprecated_fields(spec):
            sys.stderr.write(f"note: deprecated field {path} (still supported)\n")
        spec["_feature_module_label"] = feature_module_label(load_profile(args.profile))
        data = workbook_bytes(build_workbook(spec))
    except (ValueError, RuntimeError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Error: {args.yaml_path}: {exc}\n")
        return 1
    out = args.output or args.yaml_path.with_suffix(".xlsx")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"Wrote {out}")
    if not REFERENCE_WORKBOOK.is_file():
        print(f"  (reference workbook not found at {REFERENCE_WORKBOOK}; built-in column widths used)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
