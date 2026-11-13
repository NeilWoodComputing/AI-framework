export function ok() {
  return process.env.E2E_ANIMALS_TESTER_PASSWORD ? "set" : "unset";
}
