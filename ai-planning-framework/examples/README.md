# Examples

The framework's own samples use a neutral Library domain (`../templates/yaml/`, `../templates/out/`).
The canonical layout is the starter workbook `../templates/excel/page-spec-templates.xlsx`
(see `../templates/README.md`).

## Source attachments

The filled workbooks the starter was taken from, kept so a generated sheet can be compared with
its origin. They predate the starter's later additions (Required Permission, Req'd. Permission per
button and action), so follow the starter where they differ.

| File | Pattern | Framework page type |
|------|---------|---------------------|
| `Edit-Development-Details.xlsx` | Full-Page Wizard with Service / Target DB Table / Target DB Column | Full-Page Wizard |
| `Add-Edit-Appointment.xlsx` | Wizard Modal (original UI-focused; the YAML adds DB mappings) | Wizard Modal |
| `Manage-Contacts.xlsx` | Manage/list modal with Population Source (a second copy of this file, `Manage-Organisation-Contact.xlsx`, was byte-identical and was removed) | Embedded Grid Modal |
| `Organisation-Management.xlsx` | Routed list page with two buttons and a filter table | Paginated Grid (its bulk-import button opens an Import page) |
