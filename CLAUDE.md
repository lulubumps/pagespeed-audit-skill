# PageSpeed Audit for Claude Code

For PageSpeed Insights audits in this project, load the shared pagespeed-audit skill for the baseline workflow. In Claude Code, use the following extensions when the user asks for a full audit, CMS-specific recommendations or deployment verification.

- Follow the [complete report format](.claude/pagespeed/references/report.md). Deliver a short prioritized summary followed by all evidenced findings across the available performance, accessibility, best practices and SEO categories. Keep audit IDs when combining findings and mark manual checks, errors and coverage gaps.
- Use `python3 .claude/pagespeed/scripts/psi.py fetch URL --strategy both --out psi-reports` to request all four categories. Reuse supplied evidence first and use the same script with `summarize` or `compare` for existing reports. See the [measurement rules](.claude/pagespeed/references/measurement.md).
- Use the [Claude Code role workflow](.claude/pagespeed/references/roles.md) and [platform diagnostics](.claude/pagespeed/references/diagnostics.md). Activate `psi-scope`, `psi-cms`, `psi-third-party` and `psi-regression` when relevant. The coordinator reconciles the inventory against PSI evidence and supplies any findings beyond the scope of a specialist summary.
