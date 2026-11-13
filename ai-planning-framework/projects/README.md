# projects/

Framework defaults only. This folder holds no project and no domain name.

```
projects/
  _template/project.yaml     # copy these values into the active profile
```

Features for every project go to `ai-planning-framework/work/`.

## The active profile

`ai-framework.config.yaml` (one level above this framework) names it:

```yaml
project:
  active: <project>
  profile: project.yaml                # beside the config, outside this framework
  work_dir: ai-planning-framework/work
```

Agents read that file after the config and before any skill. If `project` is missing, use
`projects/_template/project.yaml`.

## Starting a new project

1. Copy `projects/_template/project.yaml` over the active profile and fill it in.
2. Point `project.profile` in `ai-framework.config.yaml` at that file (`work_dir` stays `ai-planning-framework/work`).
3. Leave any rule you want in `rules:` set to `true` (the default); set it to `false` to switch it off.

## What a profile controls

| Key | Used by |
|-----|---------|
| `framework_version` | the `VERSION` (major.minor) the profile was written for; `tools/check.py` warns on a mismatch |
| `ui.feature_module_label` | grid header label for `feature_module` (generator; default `Feature / Module`) |
| `services`, `glossary` | plan-feature, generate-ui-spec (service names, domain terms) |
| `permissions.pattern` | generate-ui-spec (permission keys, e.g. `{entity}_{action}`) |
| `database.*`, `conventions.*` | generate-ui-spec, generate-code-stubs (naming, tenancy, soft delete, audit) |
| `rules.*` | framework rules a project may switch off (see DECISIONS.md) |
| `tickets.*` | generate-tickets, publish-tickets (ID prefixes, tracker) |
| `stacks` | generate-code-stubs (hint files in `skills/generate-code-stubs/stacks/`) |
| `work_dir` | where new features are written |

`tools/check.py` validates `projects/*/project.yaml` and the active profile against `../schemas/project-profile.schema.json` (unknown keys are errors). Specs in groups with `cross_check: true` in `tests/manifest.yaml` are compared with their profile: a service not in `services`, or a permission that does not fit `permissions.pattern`, is a warning.
