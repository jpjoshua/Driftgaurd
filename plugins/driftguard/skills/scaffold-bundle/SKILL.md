---
description: Scaffold a new OKF v0.2 bundle. index.md and log.md are optional per spec — only add them if the user wants them.
---

When the user runs this skill, create a new knowledge bundle folder (ask for a path/name if not given).

Per SPEC.md §8/§9, `index.md` and `log.md` are OPTIONAL at any directory level — do not force-create them. Ask the user:
- "Do you want an index.md (directory listing) and log.md (change log)? They're optional per spec, but useful for larger bundles."

If yes, create:
```
<bundle-name>/
  index.md
  log.md
  concepts/
```
**index.md** — freeform listing, no strict required format per §8.

**log.md** (§9 format — date-grouped, newest first, ISO 8601 headings):
```markdown
# Directory Update Log

## 2026-07-24
* **Creation**: Established the bundle.
```

If the user wants Driftguard's optional taxonomy convention (NOT part of OKF — see check-taxonomy), also create `_taxonomy.md`:
```markdown
# Type Taxonomy (Driftguard extension, not part of OKF)

OKF itself accepts any value in `type:` (§4.1) and requires tolerant parsing
of unknown types (§11). This file is an opt-in convention for teams who
want consistency across a bundle — skip it entirely for a spec-minimal setup.

- concept — a standing idea, term, or piece of domain knowledge
- decision — a choice that was made, with rationale
- person — info about a specific person relevant to the bundle
- process — a repeatable procedure or workflow
- artifact — a specific file, document, or deliverable being tracked
```

Every concept file must start with frontmatter declaring `type` (§4.1, the only always-required key):
```yaml
---
type: <any value>
---
```

Optionally mention the v0.2 lifecycle fields if the user wants them from the start: `status: draft|stable|deprecated`, `stale_after: YYYY-MM-DD`, `verified: { by: human:<id>, at: <datetime> }`.

After scaffolding, tell the user to run `/driftguard:check-compliance` any time to check spec compliance and staleness.
