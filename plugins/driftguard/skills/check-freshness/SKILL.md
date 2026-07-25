---
description: Freshness audit — spec-native staleness (stale_after, status) plus git-history cross-check for bundles that don't use lifecycle fields yet. Opt-in, complements check-compliance.
---

Run `/driftguard:check-compliance` first — it already reports spec-native staleness (§5.5 `stale_after`) and lifecycle status (§5.4 `status: deprecated`) for any bundle that uses those fields. This skill is for the gap beyond that:

1. **If the bundle already uses `stale_after`/`status`**: just point the user to the check-compliance output, nothing more to do here.

2. **If the bundle does NOT use lifecycle fields** (older/simpler bundles, or teams who haven't adopted them yet): fall back to a git-history heuristic, clearly labeled as a heuristic, not a spec check:
   - For each concept file, get its last commit date via `git log -1 --format=%ai -- <file>`.
   - If the bundle sits next to a codebase, check whether files the bundle references (paths, module names mentioned in the content) have been modified in git more recently than the bundle file itself.
   - Suggest the user adopt `stale_after`/`status` going forward instead of relying on this heuristic — it's more reliable and matches the spec's own intended mechanism (§5.5).

3. **Index coverage** (only relevant if `index.md` exists — it's optional per §8): confirm every content file appears as a row/entry in `index.md`. Flag orphans and dangling entries.

4. **Log completeness** (only relevant if `log.md` exists — optional per §9): spot-check that recent git commits touching bundle files have a corresponding entry. Flag commits with no log entry.

5. Present a single summary. Do not auto-fix — ask the user which items to address, and offer to draft the corrected frontmatter (adding `stale_after`/`status`) or index/log entries for approval.
