# Ticket: T-BOOK-001 — Add | Edit Book (Form Modal)

| Field | Value |
|-------|--------|
| ID | T-BOOK-001 |
| Type | UI page |
| Feature | Catalogue |
| Priority | P1 |
| Specs | `templates/yaml/form-modal-sample.yaml`, `templates/out/form-modal-sample.xlsx` |
| Journey (optional) | — |

## User story

**As a** librarian  
**I want** to add or edit a book in a single Form Modal opened from Manage Books  
**So that** the catalogue holds correct book details and members can find and borrow it

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Title | Keyed Input | Catalogue | Book | Title |
| Author | Keyed Input | Catalogue | Book | Author |
| ISBN | Keyed Input | Catalogue | Book | Isbn |
| Genre | Single-Select Dropdown | Catalogue | Book | GenreCode |
| Published Year | Keyed Input | Catalogue | Book | PublishedYear |
| Available for Loan | Switch | Catalogue | Book | IsLoanable |

## Work to do

1. Render Form Modal sections **Book Details** and **Availability** per the Excel spec (enablement, editable, mandatory).
2. Wire Save/load through the **Catalogue** service to table **Book** for the columns above.
3. Enforce Title and Author required, ISBN check digit and uniqueness when provided, Genre from reference data, and Published Year not in the future.
4. Gate Save on `catalogue_write`; View mode is read-only.

## Acceptance criteria

### Scenario: S1 — Create book with required fields

```gherkin
Given I have catalogue_write
And I open Add Book from Manage Books
When I enter Title "The Lighthouse Keeper"
And I enter Author "M. Okafor"
And I choose Genre "Fiction"
And I leave optional fields blank
And I save the form
Then the modal closes and Manage Books refreshes
And the Catalogue service writes Book.Title = "The Lighthouse Keeper"
And the Catalogue service writes Book.Author = "M. Okafor"
And the Catalogue service writes Book.GenreCode for "Fiction"
And Book.Isbn and Book.PublishedYear are stored as empty or null
```

### Scenario: S2 — Title is mandatory

```gherkin
Given I open Add Book from Manage Books
When I clear Title and attempt to save
Then I see the validation message "Title is required"
And no row is written via the Catalogue service to Book
```

### Scenario: S3 — Duplicate ISBN is rejected

```gherkin
Given a Book with ISBN "9780000000002" already exists
And I open Add Book with Title, Author and Genre populated
When I enter ISBN "9780000000002"
And I attempt to save
Then I see the validation message "A book with this ISBN already exists"
And no row is written via the Catalogue service to Book
```

### Scenario: S4 — Published Year cannot be in the future

```gherkin
Given I open Add Book or Edit Book
When I enter a Published Year after the current year
And I attempt to save
Then I see the validation message "Published Year cannot be in the future"
And Book.PublishedYear is not updated via the Catalogue service
```

### Scenario: S5 — Edit persists changed fields

```gherkin
Given an existing Book is opened in Edit mode
When I change Author to "Mara Okafor"
And I turn Available for Loan off
And I save
Then the Catalogue service updates Book.Author = "Mara Okafor"
And the Catalogue service updates Book.IsLoanable = false
And unchanged columns on Book are left as they were
```

### Scenario: S6 — View mode is read-only

```gherkin
Given I open the book in View mode
When the form loads
Then every control has Editable = No
And Save is hidden
And Cancel / Close is available
And no writes are made via the Catalogue service to Book
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel control rows (enablement, mandatory, validation messages)
- [ ] Data read/written via `Catalogue` to `Book.<column>` as asserted in Then/And
- [ ] Implementation stays framework-agnostic unless the repo already standardises a stack

## Out of scope

- Manage Books grid / actions menu (separate Paginated Grid page and grid tickets)
- Book copies (Book Copies embedded grid modal) and bulk import

## Notes

- Spec source: `templates/yaml/form-modal-sample.yaml` → `templates/out/form-modal-sample.xlsx`
- Opened from Manage Books in Add, Edit or View mode
- Stable ID for tracker upsert: `T-BOOK-001`
