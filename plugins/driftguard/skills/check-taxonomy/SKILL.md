---
description: Opt-in team convention check — flag type values that fall outside a bundle's shared taxonomy (NOT an OKF spec requirement; use check-compliance for spec compliance)
---

This is Driftguard's opinionated add-on, not part of OKF. The spec itself deliberately makes `type` free-form and requires tolerant parsing of any value — that's a resilience feature, not a gap. This skill is for teams who want more consistency than the spec requires. If the user just wants spec compliance, point them to `/driftguard:check-compliance` instead.

When the user runs this skill against a bundle folder:

1. Read `_taxonomy.md` in the bundle root. If it doesn't exist, tell the user this is optional — ask whether they want one generated now (inferred from existing `type:` values) or whether they'd rather skip taxonomy enforcement entirely and just use check-compliance.

2. Walk every markdown file in the bundle (skip the OKF reserved files `index.md` and `log.md`, and Driftguard's own `_taxonomy.md`). For each file, read its frontmatter `type:` value.

3. Build a report with three sections:
   - **Missing type**: files with no `type:` field at all.
   - **Unregistered type**: files whose `type:` value isn't listed in `_taxonomy.md` — valid per OKF, but outside this bundle's chosen convention. For each, suggest the closest existing taxonomy value if one is a reasonable match, or suggest adding it to the taxonomy if it represents a genuinely new category.
   - **Consistent**: a short count of files that pass.

4. Do not silently rewrite files. Present the report and ask the user which fixes to apply (add to taxonomy vs. correct the file's type) before making any changes.

5. If the user approves fixes, update the file's frontmatter and/or append the new type to `_taxonomy.md`, and add a row to `log.md` noting the correction.
