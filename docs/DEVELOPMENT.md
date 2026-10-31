# Deadline Watch architecture

The entire dashboard is in plugin/index.html. Host-side plugin.js is intentionally minimal. The iframe is populated from PluginAPI.getAppState() (tasks, projects and taskRepeatCfgs), with no external requests and no persistence.

**A task deadline** is either deadlineDay (all-day, YYYY-MM-DD) or deadlineWithTime (Unix timestamp in milliseconds). A scheduled date, dueDay or dueWithTime, is only when the user planned to work and must never silently turn into a deadline.

**A recurring-series end** comes from repeatUntilDay on a recurrence configuration, is displayed as its own informational event, and has a different label. Paused and past series are excluded. Actual task instances with repeatCfgId are still real tasks and may have their own deadline. Recurring templates or projections must not be fabricated into deadline entries.

The plugin's pure helpers live between BEGIN_CORE and END_CORE in the HTML script. Sorting uses the actual deadline instant and countdowns use local calendar-day differences. All-day deadlines remain due until local end-of-day. Timed deadlines use their exact timestamp; a deadline earlier today shows Overdue today. Calendar-day arithmetic avoids daylight-saving 23/25-hour errors.

Task names are rendered using textContent, never HTML injection. A task row calls selectTask(taskId). The UI does not re-render while a pointer press is in progress.

PluginAPI.getAppState() returns raw read-only application models. The current public PluginAPI TypeScript Task and PluginTaskRepeatCfg interfaces do not declare every deadline/recurrence field, although the app implementation defines them. Verify in an installed recent Super Productivity build; never manufacture dates if unavailable.

Tests: Node core helper tests, Python packaging tests, and optional Playwright desktop/mobile tests with synthetic fixture data only.

## Release

On PRs, .github/workflows/check.yml validates and provides preview artifacts. On main, .github/workflows/release.yml rebuilds and publishes the ZIP; see [release instructions](RELEASING.md).
