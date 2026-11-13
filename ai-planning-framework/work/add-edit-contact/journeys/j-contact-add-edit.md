# Journey: J-CONTACT-001 — Add and edit a contact for an organisation

| Field | Value |
|-------|--------|
| Actor | Organisation administrator |
| Goal | Create or update a contact so details persist against the organisation |
| Trigger | User opens Manage Contacts for an organisation, then Add or Edit Contact |
| Primary pages | Manage Contacts; Add \| Edit Contact |
| Source specs | `specs/manage-contacts.yaml`, `specs/add-edit-contact.yaml` |

## Happy path

1. **Open Manage Contacts** — Page: Manage Contacts
   - UI: Results grid (Name, Job Title / Department, Primary Contact, Active, Last Amended); "+ Add Contact"
   - Data: Service `Contacts` → Contact rows for the parent Organisation (Population Source per column)
   - Outcome: Non-deleted contacts for the organisation are listed

2. **Add Contact** — Page: Add \| Edit Contact / Add mode
   - UI: Sections Contact Details + Status; Organisation pre-populated read-only
   - Data: On Save, Contacts → `Contact.Name`, `JobTitleDepartment`, `EmailAddress`, `Telephone`, `OrganisationId`, `PrimaryContact`, `IsActive`
   - Outcome: Form closes; new row appears on Manage Contacts

3. **Edit Contact** — Page: Add \| Edit Contact / Edit mode (from actions menu)
   - UI: Same Basic Form; fields loaded from Contact
   - Data: Contacts updates only changed columns on Contact
   - Outcome: List refreshes with updated values / Last Amended

4. **View Contact (optional)** — Page: Add \| Edit Contact / View mode
   - UI: All controls Editable = No; Save hidden
   - Data: Read-only via Contacts → Contact; no writes
   - Outcome: User closes without persistence

## Alternate paths

- **Validation failure:** Name required → "Name is required"; invalid email → "Enter a valid email address"; no write to Contact
- **Cancel / close:** Form closes; no Contacts writes
- **Primary Contact conflict:** Setting Primary clears previous PrimaryContact for the same OrganisationId
- **Authorisation denied:** User without edit rights cannot Save (View-only or action hidden)

## Done when

- [ ] Add and Edit persist all mapped columns via Contacts to Contact
- [ ] Manage Contacts grid Population Sources match the Excel manage spec
- [ ] Persisted fields match Target DB Column / Population Source in the Excel specs
