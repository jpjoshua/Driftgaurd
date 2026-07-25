# Driftguard

**A checker that tells you if your AI knowledge base is set up correctly — and flags what's gone stale.**

## What is this, in plain terms?

In June 2026, Google published a new open standard called **Open Knowledge Format (OKF)**. The idea is simple: instead of every AI tool inventing its own way to store "memory" or reference documentation, you organize your knowledge as a folder of plain markdown files — the kind you'd write in any text editor — with a small structured header on each file. Any AI agent that understands the format can then read that folder and use it as context, without needing a database, an API key, or any special software.

It's a good idea, and it's catching on fast (the spec's GitHub repo went from ~3,000 stars to over 7,500 in about six weeks). But the rules for what makes a file "valid" are spelled out in a fairly dense technical spec document, and nothing automatically checks whether you've actually followed them. If you get something wrong — a typo in a required field, a missing marker — nothing tells you. Your AI agent might quietly treat that file as generic and ignore the useful parts of it, and you'd never know.

**Driftguard is that missing check.** Point it at your folder of knowledge files and it tells you:
- Which files are set up correctly and which aren't (and exactly what's wrong, in plain language)
- Which pieces of content are marked as outdated or past their "good until" date
- Which files have been reviewed/verified by a person versus never checked

It's the kind of thing a spell-checker is to a document, or a linter is to code — except for this new AI-knowledge-file format.

## Why trust it

The checker was tested against Google's own official example files (the ones that ship with the spec itself) and produced zero incorrect flags. It was also tested against deliberately broken example files to confirm it actually catches real problems. Full results are in `driftguard-test-report-2026-07-24.md`.

## What's included

- **`scaffold-bundle`** — sets up a new knowledge folder for you, following the format's rules.
- **`check-compliance`** — the main checker. Tells you exactly what's valid, what's broken, what's outdated, and what's been verified. This is the one that's been tested against Google's official examples.
- **`check-taxonomy`** — an optional add-on for teams who want to keep their file categories consistent (the spec itself doesn't require this, but some teams like the extra structure).
- **`check-freshness`** — an optional add-on that estimates staleness by looking at your file history, for folders that haven't adopted the built-in "good until" dates yet.
- **`generate-report`** — turns a check-compliance run into a clean, shareable written report.

## How to use it

This ships as a Claude Code plugin, and the core checker also runs standalone with just Python — no Claude Code required.

**Install as a Claude Code plugin:**
```
claude plugin marketplace add ./driftguard
claude plugin install driftguard@driftguard
```

**Or just run the checker directly:**
```
python3 plugins/driftguard/scripts/okf_lint.py /path/to/your/knowledge/folder
```

## Staying current

The underlying spec is new and still evolving — it already moved from version 0.1 to 0.2 within its first six weeks. To make sure this tool doesn't quietly fall out of date:

- A scheduled check runs automatically every Monday, comparing this tool's rules against the live, current version of the spec.
- If the spec has changed, it automatically re-tests against fresh official examples and opens a note here so it gets looked at.
- You can also run this check manually any time: `python3 plugins/driftguard/scripts/check_spec_version.py`
