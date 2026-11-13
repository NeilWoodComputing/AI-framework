# Stack hint: nextjs

Read by `generate-code-stubs` only, when the project profile lists `nextjs` under `stacks`. Naming hints, not rules; stubs stay pseudocode.

- **Interfaces:** camelCase fields (`title`, `isbn`) with a comment back to `Table.Column`; interface names PascalCase (`Book`).
- **Pages:** `pages/<PageTitle>.md` notes the `route` for Paginated Grid pages (e.g. `/books`) and which modals open over it.
- **Forms:** list controls in spec order with their mandatory / format / validation messages so a form schema can be derived later.
- Do not write React components, hooks or API routes.
