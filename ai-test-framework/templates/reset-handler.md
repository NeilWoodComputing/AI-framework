# Template — test-data module (API.Framework): guards, seed units, master and batch resets, personas

Skeletons for the implementing agent, per `skills/add-test-data-reset/SKILL.md`. Names follow API.Framework's layout (`Api.Framework.Services/{Area}/`, `Api.Framework/Controllers/{Area}/...`); routes have no version segment (T-RENAME-001), so copy the route attributes from an existing controller such as `AnimalController`, and adjust to the real types (`User`, `PermissionGroup`, the password hasher the login service uses). Verify the EF Core metadata calls against EF Core 10 / Npgsql 10 when implementing. **Not added to any codebase.**

## 1. Options and registration (`Api.Framework.Services/TestData/`)

```csharp
public sealed class TestDataOptions
{
    public bool Enabled { get; set; }                        // default false; absent from appsettings.json
    public bool AllowMasterReset { get; set; }               // default false; true only in the Test environment
    public string[] AllowedEnvironments { get; set; } = [];  // ["Test"] (or ["E2E"])
    public string RequiredDatabase { get; set; } = "";       // "<api_framework_test>"
    public string KeyEnvVar { get; set; } = "E2E_TEST_DATA_KEY";   // env var NAME, never the value
    public string PersonaEmailDomain { get; set; } = "";     // "<e2e.test>"
    public Guid TestTenantId { get; set; }                   // fixed GUID of "<e2e-test-tenant>"
}

public static class TestDataRegistration
{
    public static bool IsEnabled(TestDataOptions o, IHostEnvironment env)
    {
        if (!o.Enabled) return false;
        if (env.IsProduction())
            throw new InvalidOperationException("TestData must never be enabled in Production.");
        if (!o.AllowedEnvironments.Contains(env.EnvironmentName, StringComparer.OrdinalIgnoreCase)) return false;
        return !string.IsNullOrEmpty(Environment.GetEnvironmentVariable(o.KeyEnvVar));
    }

    public static IServiceCollection AddTestData(this IServiceCollection services, IConfiguration config)
    {
        services.Configure<TestDataOptions>(config.GetSection("TestData"));
        services.AddScoped<TestDataGuard>();
        services.AddScoped<TestDataAccessFilter>();
        services.AddScoped<ITestDataService, TestDataService>();

        // Seed units: baseline first, then one persona unit and N batch units per feature.
        services.AddScoped<ITestSeedUnit, MigrationSeedUnit>();          // baseline.migration-seed
        services.AddScoped<ITestSeedUnit, TestTenantUnit>();             // baseline.test-tenant
        services.AddScoped<ITestSeedUnit, TestDataAdminPersonasUnit>();  // personas.testdata
        services.AddScoped<ITestSeedUnit, AnimalsPersonasUnit>();        // personas.animals
        services.AddScoped<ITestSeedUnit, AnimalsFormBatch>();           // animals.form (one line per batch)
        return services;
    }
}

public sealed class RemoveTestDataController : IApplicationFeatureProvider<ControllerFeature>
{
    public void PopulateFeature(IEnumerable<ApplicationPart> parts, ControllerFeature feature) =>
        feature.Controllers.Remove(typeof(TestDataController).GetTypeInfo());
}
```

`Program.cs` (the runtime test API runs with `InitialisationSettings:MigrateDatabase=false`; migrations are applied with a separate owner connection):

```csharp
var testDataOptions = builder.Configuration.GetSection("TestData").Get<TestDataOptions>() ?? new();
var testDataOn = TestDataRegistration.IsEnabled(testDataOptions, builder.Environment);
builder.Services.AddControllers()
    .ConfigureApplicationPartManager(m => { if (!testDataOn) m.FeatureProviders.Add(new RemoveTestDataController()); });
if (testDataOn) builder.Services.AddTestData(builder.Configuration);
// ... var app = builder.Build(); existing Migrate() block (off in Test) ...
if (testDataOn)
{
    using var scope = app.Services.CreateScope();
    await scope.ServiceProvider.GetRequiredService<ITestDataService>().StartupSeedAsync(CancellationToken.None);
}
```

## 2. Guards

```csharp
public sealed class TestDataGuard(LoginDbContext db, IOptions<TestDataOptions> options)
{
    public void EnsureTestDatabase()
    {
        if (db.Database.ProviderName != "Npgsql.EntityFrameworkCore.PostgreSQL")
            throw new InvalidOperationException("TestData refused: not PostgreSQL.");
        var name = db.Database.GetDbConnection().Database;
        if (!string.Equals(name, options.Value.RequiredDatabase, StringComparison.Ordinal))
            throw new InvalidOperationException("TestData refused: not the named test database.");
    }
}

/// Both checks: the secret key header AND a signed-in test persona (master: testdata-admin only).
public sealed class TestDataAccessFilter(IOptions<TestDataOptions> options, IEnumerable<ITestSeedUnit> units)
    : IAuthorizationFilter
{
    public void OnAuthorization(AuthorizationFilterContext context)
    {
        var o = options.Value;
        var expected = Environment.GetEnvironmentVariable(o.KeyEnvVar);
        var given = context.HttpContext.Request.Headers["X-Test-Data-Key"].ToString();
        if (string.IsNullOrEmpty(expected) ||
            !CryptographicOperations.FixedTimeEquals(Encoding.UTF8.GetBytes(given), Encoding.UTF8.GetBytes(expected)))
        {
            context.Result = new StatusCodeResult(StatusCodes.Status403Forbidden);    // never echo or log the key
            return;
        }

        var user = context.HttpContext.User;
        if (user.Identity?.IsAuthenticated != true) { context.Result = new UnauthorizedResult(); return; }
        if (!Guid.TryParse(user.FindFirstValue("sub"), out var userId)) { context.Result = new ForbidResult(); return; }

        var all = units.OfType<PersonasUnit>().SelectMany(p => p.Personas).ToList();
        var persona = all.SingleOrDefault(p => p.UserId == userId);
        var isMaster = context.RouteData.Values["action"] as string == nameof(TestDataController.ResetMaster);
        if (persona is null || (isMaster && persona.UserId != TestDataAdminPersonasUnit.AdminUserId))
            context.Result = new ForbidResult();
    }
}
```

## 3. Controller

```csharp
[ApiController]
[Route("TestData")]
[Authorize]                                    // a valid JWT is required; the filter checks it is a test persona
[ServiceFilter(typeof(TestDataAccessFilter))]
public sealed class TestDataController(ITestDataService service) : ControllerBase
{
    [HttpPost("Reset/master")]                 // literal segment wins over {scenarioKey}
    public async Task<IActionResult> ResetMaster(CancellationToken cancellationToken) =>
        Ok(await service.ResetMasterAsync(cancellationToken));

    [HttpPost("Reset/{scenarioKey}")]
    public async Task<IActionResult> Reset(string scenarioKey, CancellationToken cancellationToken)
    {
        var result = await service.ResetBatchAsync(scenarioKey, cancellationToken);
        return result is null ? NotFound() : Ok(result);
    }
}
```

## 4. Seed units and the service

```csharp
public interface ITestSeedUnit
{
    string Key { get; }                              // "baseline.migration-seed", "personas.animals", "animals.form"
    IReadOnlyCollection<string> DependsOn { get; }
    IReadOnlyCollection<string> States => [];        // batch units only: ["empty", "bessie-exists", …]
    string? DefaultState => null;                    // batch units only: the state the master reset seeds
    Task ClearAsync(LoginDbContext db, CancellationToken ct) => Task.CompletedTask;    // own rows only
    Task<IReadOnlyDictionary<string, Guid>> SeedAsync(LoginDbContext db, string? state, CancellationToken ct); // upsert
}

public static class SeedOrder
{
    /// Dependency order, ties broken by key, so every run uses the same order. Throws on a cycle or a missing dependency.
    public static IReadOnlyList<ITestSeedUnit> Sort(IEnumerable<ITestSeedUnit> units)
    {
        var byKey = units.ToDictionary(u => u.Key);
        var done = new List<ITestSeedUnit>(); var state = new Dictionary<string, int>();
        void Visit(ITestSeedUnit u)
        {
            if (state.TryGetValue(u.Key, out var s)) { if (s == 1) throw new InvalidOperationException($"Seed cycle at {u.Key}"); return; }
            state[u.Key] = 1;
            foreach (var d in u.DependsOn.Order()) Visit(byKey.TryGetValue(d, out var dep) ? dep
                : throw new InvalidOperationException($"{u.Key} depends on missing unit {d}"));
            state[u.Key] = 2; done.Add(u);
        }
        foreach (var u in byKey.Values.OrderBy(u => u.Key, StringComparer.Ordinal)) Visit(u);
        return done;
    }
}

public sealed class TestDataService(
    LoginDbContext db, TestDataGuard guard, IEnumerable<ITestSeedUnit> units,
    IOptions<TestDataOptions> options, ILogger<TestDataService> logger) : ITestDataService
{
    private IReadOnlyList<ITestSeedUnit> Ordered => SeedOrder.Sort(units);

    /// API start in Test: tenant + personas only (upserts), so testdata-admin can sign in. No truncate.
    public async Task StartupSeedAsync(CancellationToken ct)
    {
        guard.EnsureTestDatabase();
        foreach (var u in Ordered.Where(u => u.Key == "baseline.test-tenant" || u.Key.StartsWith("personas.")))
            await u.SeedAsync(db, null, ct);
    }

    public async Task<object> ResetMasterAsync(CancellationToken ct)
    {
        if (!options.Value.AllowMasterReset) throw new InvalidOperationException("Master reset is off.");
        guard.EnsureTestDatabase();
        if ((await db.Database.GetPendingMigrationsAsync(ct)).Any())
            throw new InvalidOperationException("Test database schema is behind: apply migrations first.");

        // Every table in the EF model (auth + creatures). The history table is not in the model, so it is never touched.
        var tables = db.Model.GetEntityTypes()
            .Where(e => e.GetTableName() is not null && e.GetViewName() is null)
            .Select(e => $"\"{e.GetSchema() ?? LoginDbContext.Schema}\".\"{e.GetTableName()}\"")
            .Distinct().Order().ToList();

        await using var tx = await db.Database.BeginTransactionAsync(ct);
        await db.Database.ExecuteSqlRawAsync($"TRUNCATE TABLE {string.Join(", ", tables)} RESTART IDENTITY CASCADE", ct); // identifiers from the model only
        var ran = new List<string>();
        foreach (var u in Ordered)
        {
            await u.SeedAsync(db, u.DefaultState, ct);                                  // baseline → tenant → personas → batch defaults
            ran.Add(u.DefaultState is null ? u.Key : $"{u.Key}.{u.DefaultState}");
        }
        var seedRows = db.Model.GetEntityTypes()                                       // HasData rows per table, as recreated
            .Where(e => e.GetTableName() is not null && e.GetSeedData().Any())
            .ToDictionary(e => e.GetTableName()!, e => e.GetSeedData().Count());
        await tx.CommitAsync(ct);
        logger.LogWarning("TestData master reset: {Tables} tables truncated; units {Units}", tables.Count, ran);
        return new { scenario = "master", truncatedTables = tables.Count, units = ran, seedRows };
    }

    public async Task<object?> ResetBatchAsync(string key, CancellationToken ct)
    {
        var dot = key.LastIndexOf('.');
        if (dot <= 0) return null;
        var (batchKey, stateName) = (key[..dot], key[(dot + 1)..]);
        var batch = units.SingleOrDefault(u => u.Key == batchKey && u.States.Contains(stateName));
        if (batch is null) return null;

        guard.EnsureTestDatabase();
        if (!await db.Tenants.AnyAsync(t => t.Id == options.Value.TestTenantId, ct))
            throw new TestDataConflictException("Baseline missing: run the master reset.");   // → 409

        await using var tx = await db.Database.BeginTransactionAsync(ct);
        await batch.ClearAsync(db, ct);                                                  // footprint only
        foreach (var dep in batch.DependsOn)                                             // e.g. personas.animals (re-assert)
            await units.Single(u => u.Key == dep).SeedAsync(db, null, ct);
        var ids = await batch.SeedAsync(db, stateName, ct);
        await tx.CommitAsync(ct);
        logger.LogInformation("TestData reset {Key}", key);
        return new { scenario = key, ids };
    }
}
```

## 5. The units

```csharp
/// baseline.migration-seed — recreates every HasData row from the current EF model (the source the migrations'
/// InsertData came from), principals before dependants. ON CONFLICT DO NOTHING keeps it idempotent.
public sealed class MigrationSeedUnit : ITestSeedUnit
{
    public string Key => "baseline.migration-seed";
    public IReadOnlyCollection<string> DependsOn => [];

    public async Task<IReadOnlyDictionary<string, Guid>> SeedAsync(LoginDbContext db, string? state, CancellationToken ct)
    {
        foreach (var entity in ByForeignKeys(db.Model.GetEntityTypes()))
        {
            var table = StoreObjectIdentifier.Table(entity.GetTableName()!, entity.GetSchema() ?? LoginDbContext.Schema);
            foreach (var row in entity.GetSeedData(providerValues: true))
            {
                var props = row.Keys.Select(k => entity.FindProperty(k)!).ToList();
                var columns = string.Join(", ", props.Select(p => $"\"{p.GetColumnName(table)}\""));
                var values = string.Join(", ", props.Select((_, i) => $"@p{i}"));
                var parameters = props.Select((p, i) => new NpgsqlParameter($"p{i}", row[p.Name] ?? DBNull.Value)
                    { DataTypeName = p.GetColumnType() }).ToArray();                       // jsonb, uuid, timestamptz …
                await db.Database.ExecuteSqlRawAsync(
                    $"INSERT INTO \"{table.Schema}\".\"{table.Name}\" ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING",
                    parameters, ct);
            }
        }
        return new Dictionary<string, Guid>();
    }

    private static IEnumerable<IEntityType> ByForeignKeys(IEnumerable<IEntityType> all)
    {
        var list = all.Where(e => e.GetTableName() is not null).OrderBy(e => e.Name).ToList();
        var done = new HashSet<IEntityType>();
        while (done.Count < list.Count)
        {
            var next = list.First(e => !done.Contains(e) && e.GetForeignKeys()
                .All(fk => fk.PrincipalEntityType == e || done.Contains(fk.PrincipalEntityType)));
            done.Add(next);
            yield return next;
        }
    }
}

/// baseline.test-tenant — the test tenant (fixed GUID), upsert.
public sealed class TestTenantUnit : ITestSeedUnit
{
    public string Key => "baseline.test-tenant";
    public IReadOnlyCollection<string> DependsOn => ["baseline.migration-seed"];
    public Task<IReadOnlyDictionary<string, Guid>> SeedAsync(LoginDbContext db, string? state, CancellationToken ct) =>
        throw new NotImplementedException("Upsert Tenant { Id = TestTenantId, Name = \"<e2e-test-tenant>\" } and its features as needed.");
}

public sealed record TestPersona(string Feature, string Role, Guid UserId, string? DisplayName, string[] Permissions)
{
    public string Name => $"{Feature}-{Role}";                                         // animals-tester
    public string PasswordEnvVar => $"E2E_{Feature}_{Role}_PASSWORD".ToUpperInvariant().Replace('-', '_');
}

/// personas.<feature> — upsert each persona: user (fixed id, email "<name>@<PersonaEmailDomain>", DisplayName,
/// password hashed from its env var with the login service's hasher, tenant = TestTenantId), its own group
/// "<name>" in the test tenant with exactly its permissions (looked up by name), and its only membership.
/// A missing password env var skips that persona and logs its NAME (never a value).
public abstract class PersonasUnit(string feature, IReadOnlyList<TestPersona> personas) : ITestSeedUnit
{
    public string Key => $"personas.{feature}";
    public IReadOnlyCollection<string> DependsOn => ["baseline.test-tenant"];
    public IReadOnlyList<TestPersona> Personas => personas;
    public Task<IReadOnlyDictionary<string, Guid>> SeedAsync(LoginDbContext db, string? state, CancellationToken ct) =>
        throw new NotImplementedException("Upsert users, groups and memberships as described above.");
}

public sealed class TestDataAdminPersonasUnit() : PersonasUnit("testdata",
    [new("testdata", "admin", AdminUserId, "Test Data Admin", [])])                   // no product permissions
{
    public static readonly Guid AdminUserId = Guid.Parse("<fixed guid>");
}

public sealed class AnimalsPersonasUnit() : PersonasUnit("animals",
[
    new("animals", "tester", Guid.Parse("<fixed guid>"), "Animals Tester", ["animals_write"]),
    new("animals", "tester-emailonly", Guid.Parse("<fixed guid>"), null, ["animals_write"]),     // no DisplayName → Email fallback
    new("animals", "viewer", Guid.Parse("<fixed guid>"), "Animals Viewer", []),
    new("animals", "usermanager", Guid.Parse("<fixed guid>"), "Animals User Manager",
        ["user_management_read", "user_management_write"]),
]);

/// animals.form — one batch = one feature file. Clears only its footprint, then seeds one state.
public sealed class AnimalsFormBatch : ITestSeedUnit
{
    public string Key => "animals.form";
    public IReadOnlyCollection<string> DependsOn => ["personas.animals"];
    public IReadOnlyCollection<string> States => ["empty", "bessie-exists", "bessie-soft-deleted"];
    public string? DefaultState => "empty";

    private static readonly Guid Bessie = Guid.Parse("<fixed guid>");
    private static readonly string[] Names = ["BESSIE"];                     // NormalizedName values this batch creates
    private static readonly Guid[] FeaturePersonaIds = [/* AnimalsPersonasUnit ids */];

    public Task ClearAsync(LoginDbContext db, CancellationToken ct) =>
        db.Animals
          .Where(a => a.Id == Bessie || (Names.Contains(a.NormalizedName) && FeaturePersonaIds.Contains(a.UpdatedBy)))
          .ExecuteDeleteAsync(ct);                                           // footprint only; never the whole table

    public async Task<IReadOnlyDictionary<string, Guid>> SeedAsync(LoginDbContext db, string? state, CancellationToken ct)
    {
        if (state is null or "empty") return new Dictionary<string, Guid>();
        // Upsert with the real Animal model and the service's normalisation; UpdatedBy = animals-tester.
        // Animal { Id = Bessie, Name = "Bessie", DateBorn = 2020-01-01, IsDeleted = state == "bessie-soft-deleted", ... }
        await db.SaveChangesAsync(ct);
        return new Dictionary<string, Guid> { ["bessie"] = Bessie };
    }
}
```

## 6. Unit tests the module needs (`Api.Framework.Tests/TestData/`)

- `IsEnabled_FlagOff_ReturnsFalse`; `IsEnabled_ProductionWithFlagOn_Throws`; `IsEnabled_EnvironmentNotAllowed_ReturnsFalse`; `IsEnabled_KeyEnvVarMissing_ReturnsFalse`
- `EnsureTestDatabase_OtherDatabaseName_Throws`; `EnsureTestDatabase_NotNpgsql_Throws`
- `OnAuthorization_WrongKey_Returns403`; `OnAuthorization_NotSignedIn_Returns401`; `OnAuthorization_NonPersonaUser_Returns403`; `OnAuthorization_MasterAsAnimalsTester_Returns403`; `OnAuthorization_MasterAsTestDataAdmin_Allows`
- `SeedOrder_Sort_PutsDependenciesFirstAndIsStable`; `SeedOrder_Sort_Cycle_Throws`; `SeedOrder_Sort_MissingDependency_Throws`
- `MigrationSeedUnit_InsertsExactlyTheModelSeedRows` (row count per table equals `GetSeedData()` count, and matches `seedRows`); `MigrationSeedUnit_ByForeignKeys_PrincipalsFirst`
- `ResetMaster_AllowMasterResetOff_Throws`; `ResetMaster_TruncateList_IsModelTablesOnly` (no `__ef_migrations_history`); `ResetBatch_UnknownKey_ReturnsNull`
- `AnimalsFormBatch_Clear_KeepsRowsOutsideFootprint`; `AnimalsFormBatch_SeedTwice_LeavesSameState`
- `TestPersona_PasswordEnvVar_FollowsPattern` (`animals-tester` → `E2E_ANIMALS_TESTER_PASSWORD`)

The truncate itself and the end-to-end master run are exercised by the e2e global setup on the test database (InMemory has no `TRUNCATE`).
