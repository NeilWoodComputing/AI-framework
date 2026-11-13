export function passwordFor(envVar: string, env: Record<string, string | undefined>): string | undefined {
  const password = env[envVar];
  return password;
}
