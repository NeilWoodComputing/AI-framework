# Plan: Add | Edit Contact

## Summary

Organisation administrators need to add, view, and edit contacts against an organisation from Manage Contacts, with each field persisted through the Contacts service to the Contact table (and related Organisation linkage). This feature delivers a Manage Contacts list modal plus a Basic Form for Add | Edit | View Contact — full-stack, not UI-only.

## Actors & permissions

| Actor | Permissions |
|-------|-------------|
| Organisation administrator | Open Manage Contacts for an organisation; Add / Edit / View / soft-delete contacts |
| Read-only user (optional) | View Contact only; Save hidden |

## Pages / surfaces

| Page | Type | Opens from | Notes |
|------|------|------------|-------|
| Manage Contacts | Modal (manage/list) | Organisation context | Results grid + actions; primary action "+ Add Contact" |
| Add \| Edit Contact | Basic Form | Manage Contacts (Add / Edit / View) | Sections: Contact Details, Status; Service/Table/Column on every control |

## Domain entities

| Entity / table | Owning service | Notes |
|----------------|----------------|-------|
| Contact | Contacts | Primary persist target for the Basic Form |
| Organisation | Contacts (ref) | Parent context; OrganisationId on Contact; not edited on the form |

Cross-cutting: soft delete on Contact; LastAmendedOn / LastAmendedBy on list; at most one PrimaryContact per Organisation.

## Field inventory (draft)

| UI label | Service | Table | Column | Notes |
|----------|---------|-------|--------|-------|
| Name | Contacts | Contact | Name | Mandatory; trim |
| Job Title / Department | Contacts | Contact | JobTitleDepartment | Optional |
| Email Address | Contacts | Contact | EmailAddress | Optional; email format when set |
| Telephone | Contacts | Contact | Telephone | Optional |
| Organisation | Contacts | Contact | OrganisationId | Pre-populated from parent; not editable |
| Primary Contact | Contacts | Contact | PrimaryContact | Switch; clears previous primary for org |
| Active | Contacts | Contact | IsActive | Switch |
| Last Amended (list only) | Contacts | Contact | LastAmendedOn & LastAmendedBy | Population source on manage grid |

## Integrations

- Parent organisation context when opening Manage Contacts / Add Contact
- No external identity provider in scope for this slice

## Open questions

1. Default values for Primary Contact and Active on Add — assume Active = true, Primary = false unless product says otherwise.
2. Soft-delete confirmation copy and whether deleted rows remain filterable on Manage Contacts.
3. Whether Job Title / Department is free text only or may later become a lookup (spec treats as Keyed Input).

## Suggested delivery slices

1. **Contact schema + Contacts service read/write** for Contact columns above (including OrganisationId, PrimaryContact uniqueness rule).
2. **Manage Contacts modal** — list Population Sources + actions that open the Basic Form; soft delete.
3. **Add \| Edit Contact Basic Form** — sections, validation, View mode read-only; Save wired to Contacts → Contact.
