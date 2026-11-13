public sealed class Personas
{
    public const string PasswordEnvVar = "E2E_ANIMALS_TESTER_PASSWORD";
    public const string PasswordSetting = "DefaultUser:Password";
    public string? Password { get; set; }

    public void Load(Record record, Persona persona)
    {
        Password = Environment.GetEnvironmentVariable(persona.PasswordEnvVar);
        Password = record.Password;
        var connection = $"Host={host};Password={password}";
        var reason = active ? "invalid_password" : "inactive";
    }

    private const string InvalidRefreshToken = "The refresh token is invalid or has expired.";
    private void Unused()
    {
    }
}
