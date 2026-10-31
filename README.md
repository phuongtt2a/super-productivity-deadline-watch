# Deadline Watch

**Know what's coming. Act in time.**

Deadline Watch is an independent, read-only dashboard for [Super Productivity](https://app.super-productivity.com/). It helps you notice upcoming deadlines instead of managing another checklist. This is separate from [Today+](https://github.com/phuongtt2a/super-productivity-today-plus) and [Five](https://github.com/phuongtt2a/super-productivity-five).

## What you see

- **One unified date timeline:** Every task deadline and upcoming recurring-series end date is shown together, nearest first.
- **Gradual visual emphasis:** The first, second and third items progressively decrease in font size and accent intensity, while overdue items have a warmer warning palette. Every entry still shows its precise date and days remaining.
- Calendar-day countdowns: overdue, due today, tomorrow, or days left. Exact deadline times are shown when set.
- Project names and a direct click to open an individual task in Super Productivity.
- Recurring series **Ends on** dates appear inline with a clear **Repeats until** label, last repeat date, and days left. Normal deadlines carry a **Task** label.
- **Quiet summary:** Overdue, near-term, and total date counts in a compact line under the header, without unnecessary marketing headings.
- **Neo-brutalist, but readable:** Solid coral, golden yellow, mint, blue and lilac; crisp 2–3px outlines; square tags; bold editorial type; and hard offset shadows that step down through the list. The plugin retains the existing header proportions and a transparent page background. A short subtitle reads “All your important dates, in one place.” Browser checks cover 320px to 1200px.

**Scheduled work dates are not deadlines.** Planned dates are excluded unless the task also has an actual deadline. Completed tasks and paused or already-ended recurring series are hidden.

## Install

Download the installable **deadline-watch-super-productivity.zip** from the [latest Release](https://github.com/phuongtt2a/super-productivity-deadline-watch/releases/latest). In Super Productivity open **Settings → Plugins**, choose **Choose Plugin File**, and import the ZIP without extracting it.

The ZIP contains exactly four files at its root: manifest.json, plugin.js, index.html, and icon.svg. Do not install the GitHub-generated source-code archive.

The CI workflow makes preview ZIPs and phone/desktop screenshots available as downloadable workflow artifacts for review. After an approved PR is merged, GitHub Actions automatically refreshes the existing v1.0.0 Release asset without requiring a manual upload or version bump.

## Recurring tasks and date meaning

The recurring series setting **Ends on** is stored as repeatUntilDay. It marks the last date an occurrence can be scheduled; it is **not** a deadline to finish a particular task. We therefore label it **Repeats until**.

Actual instances of a recurring task can also have their own deadline, and such instances appear as ordinary deadline entries with a recurring symbol. We do not invent or count projected future instances. An actual instance with a deadline and a series end date can appear separately, because they represent different dates and responsibilities.

Technical compatibility caveat: the app's internal models include deadlineDay, deadlineWithTime, and repeatUntilDay, but the current published PluginAPI TypeScript interfaces do not declare all of these fields. We read the actual read-only getAppState() snapshot and do not substitute scheduled dates if a field is missing. Verify support with the user's installed Super Productivity version before relying on recurring-series end dates.

## Development

Track user-reported bugs using [GitHub Issues](https://github.com/phuongtt2a/super-productivity-deadline-watch/issues). New standalone features may be developed directly in a feature branch and PR. See [CONTRIBUTING.md](CONTRIBUTING.md), [developer notes](docs/DEVELOPMENT.md), and [release instructions](docs/RELEASING.md).

Run checks:

    node tests/deadline-core.test.js
    python -m unittest discover -s tests -p 'test_*.py' -v
    python tests/browser_check.py

Browser tests require Python Playwright and Chromium. Package using:

    python scripts/package.py --tag v1.0.0

The plugin uses no external accounts, services, or network requests and does not store a separate copy of personal data.

MIT licensed. This is a community plugin, not an official Super Productivity feature.
