#!/usr/bin/env python3
"""
check_spec_version.py — compares the OKF spec version this repo was last
tested against (spec_version_tested.txt) to the version currently live at
GoogleCloudPlatform/knowledge-catalog's SPEC.md.

Exit codes:
  0 — versions match, nothing to do.
  1 — spec version changed since last test. Prints old/new for the
      calling workflow to act on (re-run tests, open an issue).
  2 — could not determine either version (network/parse failure).
"""
import re
import sys
import urllib.request

SPEC_RAW_URL = "https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md"
VERSION_FILE = "spec_version_tested.txt"
VERSION_RE = re.compile(r"\*\*Version\s+([0-9]+\.[0-9]+)\*\*")


def get_live_version() -> str | None:
    try:
        with urllib.request.urlopen(SPEC_RAW_URL, timeout=15) as resp:
            text = resp.read(4000).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR: could not fetch live SPEC.md: {e}", file=sys.stderr)
        return None
    m = VERSION_RE.search(text)
    if not m:
        print("ERROR: could not find a version string in live SPEC.md", file=sys.stderr)
        return None
    return m.group(1)


def get_tested_version() -> str | None:
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: {VERSION_FILE} not found", file=sys.stderr)
        return None


if __name__ == "__main__":
    live = get_live_version()
    tested = get_tested_version()

    if live is None or tested is None:
        sys.exit(2)

    if live == tested:
        print(f"OK: spec version unchanged (v{tested})")
        sys.exit(0)

    print(f"DRIFT: spec version changed v{tested} -> v{live}")
    # Machine-readable line for the workflow to parse into env vars.
    print(f"OLD_VERSION={tested}")
    print(f"NEW_VERSION={live}")
    sys.exit(1)
