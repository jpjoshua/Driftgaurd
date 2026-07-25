# Driftguard `check-compliance` — Test Report

**Date:** 2026-07-24
**Tool tested:** `plugins/driftguard/scripts/okf_lint.py`
**Spec tested against:** Open Knowledge Format v0.2, `SPEC.md` §4, §5, §8, §9, §11 ([GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog))

## What was tested

Two test sets, run twice each for reproducibility:

1. **Real bundles** — all four official reference bundles shipped in the spec repo (`okf/bundles/`): `ga4`, `stackoverflow`, `crypto_bitcoin`, `acme_retail`. These are Google's own conformant examples, so the correct outcome is zero conformance failures.
2. **Synthetic edge cases** — a hand-built test bundle designed to trigger every failure and detection path the tool implements: missing frontmatter, missing `type`, an out-of-order `log.md`, and a passed `stale_after` date.

## Results: real bundles

| Bundle | Files checked | Conformant | Degraded | Reserved-file failures | Stale | Deprecated |
|---|---|---|---|---|---|---|
| `ga4` | 14 | 14 | 0 | 0 | 0 | 0 |
| `stackoverflow` | 32 | 32 | 0 | 0 | 0 | 1 |
| `crypto_bitcoin` | 15 | 15 | 0 | 0 | 0 | 0 |
| `acme_retail` | 17 | 17 | 0 | 0 | 0 | 1 |

**Zero false positives across 78 files in Google's own reference bundles.** This is the core claim the tool needs to be trustworthy, and it holds.

The two flagged items are real, correct signal, not errors:
- `stackoverflow/tables/stackoverflow_posts.md` — carries `status: deprecated` (§5.4); the tool correctly surfaces this rather than treating it as a failure.
- `acme_retail/metrics/gross-margin-legacy.md` — same, correctly reported as deprecated, not broken.

Trust-tier reporting (§5.3, derived from `verified`) also worked as expected: `acme_retail` is the only bundle using `verified` at scale (1 unverified, 8 human-reviewed), which the tool reflects accurately — the other three bundles report all-unverified, matching their actual content.

No bundle currently has a concept past its `stale_after` date, so the staleness path reported nothing on real data — confirmed separately below on synthetic data.

## Results: synthetic edge cases

A purpose-built bundle (`test_bundle/`) with four deliberately broken files:

| File | Defect injected | Expected detection | Result |
|---|---|---|---|
| `concepts/broken.md` | No frontmatter at all | DEGRADED — missing frontmatter | ✅ caught |
| `concepts/no_type.md` | Frontmatter present, no `type` key | DEGRADED — missing `type` | ✅ caught |
| `concepts/old_metric.md` | `stale_after: 2026-01-01` (past) | STALE | ✅ caught |
| `log.md` | Date headings out of order | RESERVED FILE FAILURE | ✅ caught |

All four detection paths fired correctly. No false negatives, no crashes on malformed input.

## What this proves

- The linter implements §11 conformance accurately enough to run clean against the spec authors' own examples — the strongest available correctness signal short of a formal test suite from Google itself.
- It correctly distinguishes spec-compliant-but-noteworthy content (deprecated, stale) from actual conformance failures, matching §11's explicit instruction not to reject bundles for lifecycle status.
- Every failure and detection path in the tool has been exercised at least once and behaves as documented.

## What this does not prove

- Coverage of every SPEC.md clause — notably, the tool does not yet validate `sources`, `generated`, `computation`/`Attested Computation` fields (§5.1, §5.2, §10), or cross-link resolution (§6). These are unchecked, not incorrectly checked.
- Behavior on adversarial or very large bundles (performance, deeply nested directories, non-UTF-8 files) is untested.
- No external user has run this against their own bundle yet — this is a self-test, not field validation.

## Recommendation

Safe to post publicly as "tested against all four official reference bundles, zero false positives" — that claim is accurate and verifiable by anyone who clones the repo and runs the same command. Do not claim broader spec coverage than what's listed above until the untested sections are addressed.
