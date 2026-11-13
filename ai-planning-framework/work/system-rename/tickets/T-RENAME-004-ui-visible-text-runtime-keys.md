# Ticket: T-RENAME-004 — UI.NextJs.Framework: visible text and runtime storage keys / events

| Field | Value |
|-------|--------|
| ID | T-RENAME-004 |
| Type | UI page text + runtime keys |
| Feature | system-rename |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** a user of the Next.js UI  
**I want** the screens and browser storage to use System instead of Unity  
**So that** the product name is consistent

## Full-stack scope

Visible text: `src/features/auth/sign-in/SignInForm.tsx:50` (`Unity Login`), `src/app/auth/sign-in/page.tsx:10` (`Sign in with your Unity credentials.`), `src/app/layout.tsx:7` (title `Unity UI Next`), the `Unity API returned …` errors in the fetch helper. Keys: `unity-auth-session` (`src/framework/auth/constants/auth-cookies.ts:5`, `e2e/helpers/authentication.ts:9`), `unity-theme` (`ThemeProvider.tsx:16, 29`, inline script `layout.tsx:17`), events `unity-auth-cleared` / `unity-auth-refreshed`.

## Work to do

1. Visible text → `System Login`, `Sign in with your System credentials.`, title `System UI Next`, `System API returned …`.
2. Keys and events → `system-auth-session`, `system-theme`, `system-auth-cleared`, `system-auth-refreshed`, in both the dispatcher and every listener. The inline theme script and `ThemeProvider` must use the same key.
3. `e2e/helpers/authentication.ts` (Dev Bot scaffolding) uses `system-auth-session`. The comment in `e2e/features/common/auth.steps.ts:12` belongs to Test Bot (T-RENAME-008).
4. No migration code for old keys: a one-time logout and theme reset are accepted.
5. D10: comments naming the real Unity UI origin and the DesignSystemShowcase text stay as they are.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-004/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Sign-in page says System

```gherkin
Given I am signed out
When I open /auth/sign-in
Then the heading reads "System Login", the intro reads "Sign in with your System credentials." and the browser title is "System UI Next"
```

### Scenario: S2 — Session uses the new key

```gherkin
Given I sign in with a valid Test user
When I inspect sessionStorage
Then the session is stored under "system-auth-session" and nothing is written under "unity-auth-session"
```

### Scenario: S3 — Theme uses the new key with no flash

```gherkin
Given I choose the dark theme
When I reload the page
Then localStorage "system-theme" is "dark", the page renders dark before hydration, and "unity-theme" is not written
```

### Scenario: S4 — Auth events still work in the same tab

```gherkin
Given I am signed in, with the session stored under "system-auth-session"
When I sign out in that tab
Then the "system-auth-cleared" event fires, "system-auth-session" is removed and the same tab shows the signed-out state
```

### Scenario: S5 — Token refresh still notifies

```gherkin
Given my access token is about to expire
When the refresh succeeds
Then the "system-auth-refreshed" event fires and I stay signed in
```

### Scenario: S6 — Old storage is ignored once

```gherkin
Given a browser that still has "unity-auth-session" and "unity-theme" from before the change
When I open the UI
Then I am asked to sign in once and the theme is the default, with no error
```

Checklist (derived from scenarios):

- [ ] 4 visible texts changed
- [ ] 4 keys / events changed everywhere, including the inline script
- [ ] e2e helper uses the new session key
- [ ] No stray `unity-` key

## Out of scope

- Comments naming the real Unity UI (D10)
- e2e scenario steps (T-RENAME-008)
- Cross-tab sign-out is out of scope: the app never had it, and the rename changes no behaviour (plan-bot 2026-10-09, after Test Bot's question)

## Notes

- Stable ID for DevOps upsert: `T-RENAME-004`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
