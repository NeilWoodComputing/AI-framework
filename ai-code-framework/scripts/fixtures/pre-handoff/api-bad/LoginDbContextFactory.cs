public class LoginDbContextFactory
{
    public string Get(string? configured) => configured
        ?? "Host=localhost;Port=5432;Database=fixture;Username=fixture;Password=PLANTED-pw-0003";
}
