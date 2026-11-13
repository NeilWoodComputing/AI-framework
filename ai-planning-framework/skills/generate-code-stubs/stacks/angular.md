# Stack hint: angular

Read by `generate-code-stubs` only, when the project profile lists `angular` under `stacks`. Naming hints, not rules; stubs stay pseudocode.

- **Interfaces:** camelCase fields with a comment back to `Table.Column`; interface names PascalCase (`Book`).
- **Pages:** `pages/<PageTitle>.md` notes the route and the feature area (`feature_module`) the page belongs to.
- **Grids:** list results columns in spec order with Population Source, sortable flag and display format so a grid column definition can be derived later.
- Do not write Angular components, modules or services.
