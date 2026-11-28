# PageSpeed Audit for Codex

For PageSpeed Insights audits in this project, load the shared pagespeed-audit skill for the baseline workflow. In Codex, use the following extensions when the user asks for a full audit, CMS-specific recommendations or deployment verification.

- Use the [chat and PDF delivery guide](.codex/pagespeed/references/pdf-delivery.md) to provide a chat summary and the downloadable full audit with clickable source and credits.
- When comparing audits, follow the [finding follow-up workflow](.codex/pagespeed/references/follow-up.md) to preserve finding identity, assign evidence-based statuses, and report unknowns.
- Follow the [complete report format](.codex/pagespeed/references/report.md). Deliver a short prioritized summary followed by all evidenced findings across all categories supplied by PSI, including interface-only categories when shown. Keep audit IDs or visible audit names when combining findings. Separate observed findings from causal confidence and mark manual checks, errors and coverage gaps.
- Use `python3 .codex/pagespeed/scripts/psi.py fetch URL --strategy both --out psi-reports` to request all four categories. Reuse supplied evidence first and use the same script with `summarize` or `compare` for existing reports. See the [measurement rules](.codex/pagespeed/references/measurement.md).
- Use the [Codex role workflow](.codex/pagespeed/references/roles.md) and [platform diagnostics](.codex/pagespeed/references/diagnostics.md). Activate `psi-scope`, `psi-cms`, `psi-third-party` and `psi-regression` when relevant. The coordinator reconciles the inventory against PSI evidence and supplies any findings beyond the scope of a specialist summary.
