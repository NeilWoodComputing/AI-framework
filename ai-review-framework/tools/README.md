# tools/

## check.py

One command that verifies this framework. Exit code 0 and `RESULT: PASS` mean every check passed.

```bash
python3 tools/check.py          # Windows: py tools/check.py   (from ai-review-framework/)
```

Needs Python 3.10+. It only reads.

| Check | Fails when |
|-------|------------|
| `files` | an API checklist or the report template is missing, the template has lost a section the loop requires, or `api-checklist.md` does not point at both API checklists |
| `paths` | a doc still sends features to the old per-project work folder |
| `terms` | a project name, a person's name, a hardcoded agent id or a project feature name appears outside the stack checklists (`api-csharp-checklist.md`, `api-framework-checklist.md`, `security-checklist.md`) |
| `tests` | the unit run is optional again, or a blocked test run is allowed to approve |
