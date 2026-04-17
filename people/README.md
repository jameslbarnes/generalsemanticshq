# People (CRM)

This folder is a lightweight CRM for General Semantics HQ. Each markdown file represents a contact, with structured frontmatter and notes.

## How it works

- Each person gets a `firstname-lastname.md` file
- Frontmatter contains structured data (role, org, contact info, tags)
- The "Related Issues" section links to GitHub issues using `person:name` labels
- To find all tasks related to someone: filter issues by their `person:` label

## Labels

Issues are tagged with `person:name` labels to connect tasks to people:

- `person:nouriel` — Nouriel
- `person:vita-david` — Vita and David
- `person:wayne-ashley` — Wayne Ashley
- `person:gonzalo-gelso` — Gonzalo Gelso
- `person:james-disguise` — James (Disguise)

Category labels:
- `venue` — venue/space related
- `event` — event/salon/show
- `partnership` — partnership/collaboration
- `followup` — needs follow-up

## Adding a new person

1. Create `firstname-lastname.md` using the template below
2. Create a `person:firstname-lastname` label on the repo
3. Tag relevant issues with the label

## Template

```yaml
---
name: Full Name
org: Organization
role: Role/Title
email:
phone:
telegram:
github:
tags: [tag1, tag2]
label: person:firstname-lastname
---
```
