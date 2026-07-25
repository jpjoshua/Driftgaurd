---
description: Run OKF v0.2's own binary compliance checks plus spec-native staleness/lifecycle checks against a bundle. CI-ready, zero opinions beyond SPEC.md.
---

This implements the actual Open Knowledge Format conformance rules from SPEC.md §11 (OKF v0.2, GoogleCloudPlatform/knowledge-catalog), plus the spec-native lifecycle fields from §5.4-5.5. It is not Driftguard's opinion — every check traces to a specific spec section, and the script comments cite the section.

When the user runs this skill against a bundle folder, run the bundled script:

```
python3 <plugin_dir>/scripts/okf_lint.py <bundle_path> [<bundle_path> ...]
```

The script checks, per §11:
1. Every non-reserved `.md` file has a parseable YAML frontmatter block.
2. Every frontmatter block has a non-empty `type` field (any value — unknown types are explicitly tolerated by spec, never flag the value itself).
3. Reserved files (`index.md`, `log.md`) — which are OPTIONAL per §8/§9, not required — follow their defined structure ONLY WHEN PRESENT. Do not fail a bundle for lacking them.

It also reports, informationally (not pass/fail — these are lifecycle signals, not conformance failures):
- **Stale concepts** (§5.5): any concept where `stale_after` has passed (`today >= stale_after`).
- **Deprecated concepts** (§5.4): any concept with `status: deprecated`.
- **Trust tiers** (§5.3): unverified / machine-confirmed / human-reviewed, derived from the `verified` field.

Present the script's output directly. Do not editorialize about files in the DEGRADED section — per §11 these are explicitly non-fatal, they just downgrade to generic documents. Only RESERVED FILE FAILURES represent an actual conformance failure.

Offer to save the output as `okf-lint-report.md` if the user wants something to commit or attach to a PR.

Note: this repo has an automated weekly GitHub Action (`.github/workflows/spec-drift-check.yml`) that checks whether the live OKF spec version has changed since `spec_version_tested.txt` was last updated, and if so, re-runs this same check against fresh reference bundles and opens an issue. If the user is running this manually because they suspect the spec changed, also run `python3 <plugin_dir>/scripts/check_spec_version.py` to confirm.
