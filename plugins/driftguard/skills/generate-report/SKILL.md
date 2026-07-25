---
description: Turn a check-compliance run into a written test report — same structure every time, for re-validation after spec changes or before posting results publicly.
---

Run this after `/driftguard:check-compliance` to turn raw output into a shareable report. Use this fixed structure every time so reports are comparable across runs and spec versions:

```markdown
# Driftguard `check-compliance` — Test Report

**Date:** <today, ISO 8601>
**Tool tested:** `plugins/driftguard/scripts/okf_lint.py`
**Spec tested against:** OKF <version — read from spec_version_tested.txt or ask the user>, SPEC.md §<sections actually exercised>

## What was tested
<list the bundles/files run through check-compliance, and why — real reference bundles vs. synthetic edge cases>

## Results: real bundles
<table: bundle | files checked | conformant | degraded | reserved-file failures | stale | deprecated>
State plainly whether zero false positives held. If any bundle failed, do not soften it — say what failed and whether it's a tool bug or a genuine bundle non-conformance.

## Results: synthetic edge cases (if run)
<table: file | defect injected | expected detection | result (caught/missed)>

## What this proves
<only claim what the results actually support>

## What this does not prove
<explicitly list untested spec sections/behaviors — pull this from the tool's known coverage gaps, don't guess>

## Recommendation
<one line: safe to post publicly as-is, or what needs fixing first>
```

Rules:
- Never inflate a claim beyond what the run actually showed. "Zero false positives across N files" only if that's literally true of this run.
- If this report is being generated because a spec version change was detected (see the spec-drift check), open with a note: "Re-validation triggered by spec version change: v<old> → v<new>" and highlight any results that differ from the last report on file.
- Save the report as `driftguard-test-report-<date>.md` so re-validation reports don't overwrite each other — the history of reports is itself useful evidence the tool keeps pace with the spec.
- Offer to update `spec_version_tested.txt` to the new version once the report confirms the tool still passes.
