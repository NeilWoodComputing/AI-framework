# Ticket: T-CONTACT-002 — Manage Contacts (list modal)

| Field | Value |
|-------|--------|
| ID | T-CONTACT-002 |
| Type | Manage list |
| Feature | Contacts |
| Priority | P1 |
| Specs | `specs/manage-contacts.yaml`, `excel/manage-contacts.xlsx` |
| Journey (optional) | J-CONTACT-001 |

## User story

**As a** organisation administrator  
**I want** a Manage Contacts list for an organisation with Add and row actions  
**So that** I can find contacts and open Add | Edit | View or soft-delete them

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Results column | Contacts | Contact | Contact.Name |
| Job Title / Department | Results column | Contacts | Contact | Contact.JobTitleDepartment |
| Primary Contact | Results column (Switch) | Contacts | Contact | Contact.PrimaryContact |
| Active | Results column (Switch) | Contacts | Contact | Contact.IsActive |
| Last Amended | Results column | Contacts | Contact | Contact.LastAmendedOn & LastAmendedBy |
| + Add Contact | Primary action | Contacts | Contact | Opens Add \| Edit Contact in Add mode |
| View / Edit / Delete | Actions menu | Contacts | Contact | View/Edit open Basic Form; Delete soft-deletes |

## Work to do

1. Render Manage Contacts modal for the parent organisation with paginated results per Excel columns.
2. Populate grid via Contacts service using Population Sources above (exclude soft-deleted).
3. Wire "+ Add Contact" and View / Edit / Delete actions to Add \| Edit Contact modes and soft-delete confirmation.

## Acceptance criteria

### Scenario: List shows organisation contacts

```gherkin
Given I open Manage Contacts for organisation O1
When the results area loads
Then each visible row is a non-deleted Contact for O1 via the Contacts service
And Name, Job Title / Department, Primary Contact, Active, and Last Amended match Contact Population Sources
```

### Scenario: Add opens Basic Form

```gherkin
Given Manage Contacts is open for organisation O1
When I click "+ Add Contact"
Then Add | Edit Contact opens in Add mode
And Organisation is pre-populated for O1 and not editable
```

### Scenario: Edit opens Basic Form with existing data

```gherkin
Given a Contact row is shown on Manage Contacts
When I choose Edit Contact from the actions menu
Then Add | Edit Contact opens in Edit mode
And fields are loaded via the Contacts service from Contact for that row
```

### Scenario: Soft delete removes row from the list

```gherkin
Given a Contact row is shown on Manage Contacts
When I choose Delete Contact and confirm
Then the Contacts service soft-deletes that Contact
And the row no longer appears in the non-deleted results list
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel manage-list rows (columns, actions, primary action)
- [ ] Data read via `Contacts` from `Contact.<column>` as asserted in Then/And
- [ ] Implementation stays framework-agnostic unless the repo already standardises a stack

## Out of scope

- Basic Form field validation (see T-CONTACT-001)
- Creating organisations

## Notes

- Spec source: `specs/manage-contacts.yaml` → `excel/manage-contacts.xlsx`
- Primary Contact uniqueness is enforced on Save of the Basic Form (T-CONTACT-001)
