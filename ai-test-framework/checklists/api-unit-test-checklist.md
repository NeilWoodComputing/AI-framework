# Checklist — API unit tests

Rules: `skills/write-api-unit-tests/SKILL.md` and the active API's own test rule.

- [ ] U1 Test project is the codebase's own: `Unity.API.Tests`, or `Api.Framework.Tests` (approved by Neil 08/10/2026; created by the implementing agent, not the testing agent); no other new test projects
- [ ] U2 Folder mirrors the code under test (`Controllers/V2/...`, `Mapping`, `Validation`, `Authorization`, or the API.Framework area)
- [ ] U3 One behaviour per `[Fact]` (or `[Theory]` row); name `{Action}_{Condition}_{Expected}`
- [ ] U4 `[Trait("Ticket", "T-<DOMAIN>-NNN")]` and `[Trait("Scenario", "T-<DOMAIN>-NNN/S<n>")]` on every scenario test
- [ ] U5 Every spec validation rule has a test asserting the **exact** message and that nothing was written
- [ ] U6 Uniqueness: scope (organisation / tenant or global per the plan), trim and case rules, soft-deleted rows ignored, DB unique-violation path mapped
- [ ] U7 Soft delete: flag set, row kept, audit set, excluded from list, not found afterwards
- [ ] U8 Permissions: policy registered with the right claim; every endpoint carries it; other permissions rejected
- [ ] U9 Mappers: every property, plus fallbacks
- [ ] U10 Mocks only at boundaries (downstream clients, clock, current user, senders); no mocking of the class under test, validators, mappers or `DbContext`
- [ ] U11 Unity.API: `CancellationToken` in Moq setups; create-request shape tests include every property; no `WebApplicationFactory` for a normal BFF action
- [ ] U12 Assertions check outcomes (status, message text, persisted values), not just "no exception"
- [ ] U13 No secrets, real connection strings or personal data in test code
- [ ] U14 API.Framework: PostgreSQL-only behaviour (filtered unique indexes, `jsonb`, `PostgresException` unique violations) is not faked on SQLite / InMemory; it is covered by API e2e on the test database
