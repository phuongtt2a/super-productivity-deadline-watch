# Deadline Watch architecture

The entire dashboard is in plugin/index.html. Host-side plugin.js is intentionally minimal. The iframe is populated from PluginAPI.getAppState() (tasks, projects and taskRepeatCfgs), with no external requests and no persistence.

**A task deadline** is either deadlineDay (all-day, YYYY-MM-DD) or deadlineWithTime (Unix timestamp in milliseconds). A scheduled date, dueDay or dueWithTime, is only when the user planned to work and must never silently turn into a deadline.

**A recurring-series end** comes from repeatUntilDay on a recurrence configuration, appears in the SAME sorted deadline timeline, and has a clear **Repeats until** tag plus a calendar-day countdown. Paused and past series are excluded. Actual task instances with repeatCfgId are still real tasks and may have their own deadline. Recurring templates or projections must not be fabricated into deadline entries.

The plugin's pure helpers live between BEGIN_CORE and END_CORE in the HTML script. Sorting uses the actual deadline instant and countdowns use local calendar-day differences. All-day deadlines remain due until local end-of-day. Timed deadlines use their exact timestamp; a deadline earlier today shows Overdue today. Calendar-day arithmetic avoids daylight-saving 23/25-hour errors.

Task names are rendered using textContent, never HTML injection. A task row calls selectTask(taskId). The UI does not re-render while a pointer press is in progress.

PluginAPI.getAppState() returns raw read-only application models. The current public PluginAPI TypeScript Task and PluginTaskRepeatCfg interfaces do not declare every deadline/recurrence field, although the app implementation defines them. Verify in an installed recent Super Productivity build; never manufacture dates if unavailable.

**Neo-brutalist design:** Keep Today+'s 1220px width, 41px green icon, transparent page and compact header. A one-line subtitle says “All your important dates, in one place.” Use flat opaque category backgrounds (coral overdue, gold today, mint soon, blue later, lilac recurring end); dark 2–3px borders; almost-square corners; hard zero-blur offset shadows; and an editorial hierarchy with the first three entries stepping down in scale. User-facing type tags read **Task** and **Repeats until**, not technical fields such as “Deadline” or “Series ends.” The narrowest viewport uses a two-row card so titles and days-left counts never collide. Avoid gradients and oversize hero sections.

Tests: Node core helper tests, Python packaging tests, and Playwright checks across nine viewport widths (320, 360, 390, 430, 480, 600, 768, 1024, 1200) with synthetic fixture data only.

## Release

On PRs, .github/workflows/check.yml validates and provides preview artifacts. On main, .github/workflows/release.yml rebuilds and publishes the ZIP; see [release instructions](RELEASING.md).
