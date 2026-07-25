#!/usr/bin/env python3
"""
okf-lint — spec-accurate compliance + staleness checker for Open Knowledge
Format (OKF) v0.2 bundles.

Implements the conformance rules verbatim from SPEC.md §11:
  1. Every non-reserved .md file has a parseable YAML frontmatter block.
  2. Every frontmatter block has a non-empty `type` field.
  3. Reserved filenames (index.md, log.md) follow §8/§9 structure WHEN PRESENT
     (they are optional, not required).

Also implements spec-native staleness/lifecycle checks from §5.4-5.5:
  - status: draft | stable | deprecated (absent -> stable)
  - stale_after: a concept is stale when today >= stale_after

This tool has no opinion beyond what SPEC.md states. It does not require
index.md or log.md to exist, does not flag unknown `type` values, and does
not reject unrecognized frontmatter keys — all explicitly prohibited by §11.
"""
import sys
import os
import re
import datetime
import yaml
from pathlib import Path

RESERVED_NAMES = {"index.md", "log.md"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def read_frontmatter(path: Path):
    """Return (frontmatter_dict, error) for a markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"could not read file: {e}"

    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, "no YAML frontmatter block found (missing leading/closing ---)"

    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, f"frontmatter is not valid YAML: {e}"

    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, "frontmatter did not parse to a mapping"

    return data, None


def check_log_md(path: Path):
    """§9: date-grouped entries, newest first, ISO 8601 date headings."""
    issues = []
    text = path.read_text(encoding="utf-8")
    date_headings = re.findall(r"^##\s+(\S+)", text, re.MULTILINE)
    if not date_headings:
        issues.append("log.md has no '## YYYY-MM-DD' date headings")
        return issues
    for d in date_headings:
        try:
            datetime.date.fromisoformat(d)
        except ValueError:
            issues.append(f"log.md heading '{d}' is not ISO 8601 (YYYY-MM-DD)")
    dates = []
    for d in date_headings:
        try:
            dates.append(datetime.date.fromisoformat(d))
        except ValueError:
            pass
    if dates != sorted(dates, reverse=True):
        issues.append("log.md date headings are not newest-first")
    return issues


def lint_bundle(bundle_path: Path):
    report = {
        "pass": [],
        "degraded": [],       # non-reserved files missing frontmatter/type -> generic doc per spec, not fatal
        "reserved_failures": [],  # index.md/log.md present but malformed -> fails §11.3
        "stale": [],
        "deprecated": [],
        "trust": {"unverified": 0, "machine-confirmed": 0, "human-reviewed": 0},
    }
    today = datetime.date.today()

    md_files = sorted(bundle_path.rglob("*.md"))
    for f in md_files:
        rel = f.relative_to(bundle_path)
        name = f.name

        if name in RESERVED_NAMES:
            # Reserved files: only checked IF PRESENT (§8/§9 say MAY appear)
            if name == "log.md":
                issues = check_log_md(f)
                if issues:
                    report["reserved_failures"].append((str(rel), issues))
                else:
                    report["pass"].append(str(rel))
            else:  # index.md
                # §8 doesn't mandate a strict machine format beyond being a listing;
                # minimal check: file is non-empty markdown.
                if f.stat().st_size == 0:
                    report["reserved_failures"].append((str(rel), ["index.md is empty"]))
                else:
                    report["pass"].append(str(rel))
            continue

        # Non-reserved -> concept document
        data, err = read_frontmatter(f)
        if err:
            report["degraded"].append((str(rel), err))
            continue
        if not data.get("type"):
            report["degraded"].append((str(rel), "missing required 'type' field"))
            continue

        report["pass"].append(str(rel))

        # --- spec-native lifecycle checks (§5.4 / §5.5), informational ---
        status = data.get("status", "stable")
        if status == "deprecated":
            report["deprecated"].append(str(rel))

        stale_after = data.get("stale_after")
        if stale_after:
            try:
                sa = stale_after if isinstance(stale_after, datetime.date) else datetime.date.fromisoformat(str(stale_after))
                if today >= sa:
                    report["stale"].append((str(rel), str(sa)))
            except ValueError:
                report["degraded"].append((str(rel), f"stale_after '{stale_after}' is not a valid date"))

        # --- trust tier (§5.3), informational ---
        verified = data.get("verified")
        if not verified:
            report["trust"]["unverified"] += 1
        else:
            entries = verified if isinstance(verified, list) else [verified]
            is_human = any(
                isinstance(e, dict) and str(e.get("by", "")).startswith("human:")
                for e in entries
            )
            report["trust"]["human-reviewed" if is_human else "machine-confirmed"] += 1

    return report


def print_report(name, report):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    print(f"PASS: {len(report['pass'])} files fully conformant")

    if report["degraded"]:
        print(f"\nDEGRADED ({len(report['degraded'])}) — per §11, these are NOT bundle-fatal, "
              f"they just downgrade to a generic/unrouted document:")
        for rel, reason in report["degraded"]:
            print(f"  - {rel}: {reason}")

    if report["reserved_failures"]:
        print(f"\nRESERVED FILE FAILURES ({len(report['reserved_failures'])}) — index.md/log.md "
              f"present but malformed, fails §11.3:")
        for rel, issues in report["reserved_failures"]:
            for i in issues:
                print(f"  - {rel}: {i}")
    else:
        print("\nRESERVED FILE FAILURES: none")

    if report["stale"]:
        print(f"\nSTALE (§5.5, stale_after has passed) — {len(report['stale'])}:")
        for rel, sa in report["stale"]:
            print(f"  - {rel}: stale_after={sa}")

    if report["deprecated"]:
        print(f"\nDEPRECATED (§5.4 status: deprecated) — {len(report['deprecated'])}:")
        for rel in report["deprecated"]:
            print(f"  - {rel}")

    t = report["trust"]
    print(f"\nTRUST TIERS (§5.3): unverified={t['unverified']}, "
          f"machine-confirmed={t['machine-confirmed']}, human-reviewed={t['human-reviewed']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: okf_lint.py <bundle_path> [bundle_path ...]")
        sys.exit(1)
    for p in sys.argv[1:]:
        bp = Path(p)
        report = lint_bundle(bp)
        print_report(bp.name, report)
