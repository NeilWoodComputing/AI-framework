# Ticket: T-CONTACT-001 — Add | Edit Contact (Basic Form)

| Field | Value |
|-------|--------|
| ID | T-CONTACT-001 |
| Type | UI page |
| Feature | Contacts |
| Priority | P1 |
| Specs | `specs/add-edit-contact.yaml`, `excel/add-edit-contact.xlsx` |
| Journey (optional) | J-CONTACT-001 |

## User story

**As a** organisation administrator  
**I want** to add or edit a contact on a single Basic Form  
**So that** contact details are stored correctly against the organisation and available from Manage Contacts

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input | Contacts | Contact | Name |
| Job Title / Department | Keyed Input | Contacts | Contact | JobTitleDepartment |
| Email Address | Keyed Input | Contacts | Contact | EmailAddress |
| Telephone | Keyed Input | Contacts | Contact | Telephone |
| Organisation | Single-select Dropdown (searchable) | Contacts | Contact | OrganisationId |
| Primary Contact | Switch | Contacts | Contact | PrimaryContact |
| Active | Switch | Contacts | Contact | IsActive |

## Work to do

1. Render Basic Form sections **Contact Details** and **Status** per the Excel spec (enablement, editable, mandatory).
2. Wire Save/load through the **Contacts** service to table **Contact** for the columns above.
3. Enforce Name required, email format when provided, Organisation pre-populated and read-only, and single Primary Contact per organisation.

## Acceptance criteria

### Scenario: Create contact with required fields

```gherkin
Given I open Add Contact from Manage Contacts for an organisation
And the Organisation field is pre-populated and not editable
When I enter Name "Alex Rivera"
And I leave optional fields blank
And I save the form
Then the form closes successfully
And the Contacts service writes Contact.Name = "Alex Rivera"
And the Contacts service writes Contact.OrganisationId for the parent organisation
And Contact.JobTitleDepartment, EmailAddress, and Telephone are stored as empty or null
And Contact.PrimaryContact and Contact.IsActive follow the switch defaults from the form
```

### Scenario: Name is mandatory

```gherkin
Given I open Add Contact from Manage Contacts
When I clear Name and attempt to save
Then I see the validation message "Name is required"
And no row is written via the Contacts service to Contact
```

### Scenario: Invalid email is rejected

```gherkin
Given I open Add Contact or Edit Contact
And Name is populated
When I enter Email Address "not-an-email"
And I attempt to save
Then I see the validation message "Enter a valid email address"
And Contact.EmailAddress is not updated via the Contacts service
```

### Scenario: Edit persists changed fields

```gherkin
Given an existing Contact is opened in Edit mode
When I change Job Title / Department to "Operations"
And I change Telephone to "020 7946 0000"
And I save
Then the Contacts service updates Contact.JobTitleDepartment = "Operations"
And the Contacts service updates Contact.Telephone = "020 7946 0000"
And unchanged columns on Contact are left as they were
```

### Scenario: Setting Primary Contact clears the previous primary

```gherkin
Given organisation O1 already has a contact marked PrimaryContact = true
And I open another contact for O1 in Edit mode
When I set Primary Contact to on and save
Then the Contacts service sets Contact.PrimaryContact = true for the edited contact
And the Contacts service sets Contact.PrimaryContact = false for the previous primary of O1
```

### Scenario: View mode is read-only

```gherkin
Given I open the contact in View mode
When the form loads
Then every control has Editable = No
And Save is hidden
And Cancel / Close is available
And no writes are made via the Contacts service to Contact
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel control rows (enablement, mandatory, validation messages)
- [ ] Data read/written via `Contacts` to `Contact.<column>` as asserted in Then/And
- [ ] Implementation stays framework-agnostic unless the repo already standardises a stack

## Out of scope

- Manage Contacts grid / actions menu (separate manage-list ticket)
- Soft delete / audit columns not listed in the Basic Form spec

## Notes

- Spec source: `specs/add-edit-contact.yaml` → `excel/add-edit-contact.xlsx`
- Organisation is pre-populated from Manage Contacts parent context
