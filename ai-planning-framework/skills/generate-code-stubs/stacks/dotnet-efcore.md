# Stack hint: dotnet-efcore

Read by `generate-code-stubs` only, when the project profile lists `dotnet-efcore` under `stacks`. Naming hints, not rules; stubs stay pseudocode.

- **Models:** one `models/<Table>.md` per `target_db_table`, named as the EF entity (PascalCase singular, e.g. `Book`, `BookCopy`). Fields keep the `target_db_column` name in PascalCase (`Title`, `Isbn`).
- **Services:** one `services/<Service>.md` per `service`; list operations as `GetAsync`, `ListAsync(query)`, `CreateAsync`, `UpdateAsync`, `DeleteAsync` where the spec needs them.
- **Query DTOs** (grids): `<Entity>ListQuery` with paging (`Page`, `PageSize`), sort and the filter fields from `search_filters`; result rows named `<Entity>ListItem`.
- **Conventions:** note the profile's `conventions` (soft delete flag, audit columns, tenant filter) on each model stub rather than repeating them per field.
- Do not write migrations, DbContext code or controllers.
