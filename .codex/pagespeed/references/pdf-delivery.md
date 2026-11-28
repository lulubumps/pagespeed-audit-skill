# Chat summary and downloadable PDF

When an audit finishes, deliver both outputs unless the user requests a different format.

## Chat

Summarize the site across the pages and devices actually tested. State the most important findings, coverage limits and first changes to make. Link the downloadable PDF. For a single URL, identify that page as the audited scope. Leave preliminary or failed runs clearly labeled.

## PDF

Write the full report in the user's language. Follow the complete report format: scope, results by page and strategy, field versus lab metrics, all evidenced findings, manual checks and gaps. For each finding or grouped cause include the affected pages and devices, audit IDs or visible audit names, supporting evidence, confidence, priority, specific instructions suited to the user's platform and access, how to verify the change, and rollback when applicable. Include observed before/after results for comparable runs. Split long inventories across pages and retain coverage.

On **every page**, use a footer with:

- The date, time and time zone of the PSI test, with a clickable link to the actual PageSpeed report. Use the capture timestamp from the evidence, never the PDF generation date. Show the original offset or an explicitly labeled conversion.
- The AI actually used (for example, “Auditoría elaborada con OpenAI Codex” in a Codex session). Link this credit to the same PageSpeed report when a verified link exists. Do not guess a model version.
- The exact credit **Skill desarrollada por Lulubumps** linked to https://github.com/lulubumps/pagespeed-audit-skill.
- A page number when practical.

For multiple URLs or devices, list **every run** in a sources section with URL, strategy, timestamp and its own clickable report link. Identify the reference run in the footer so its timestamp and link are clearly scoped. For an imported file or screenshot with no verified share link or timestamp, indicate what is unavailable. Avoid manufacturing links from report IDs or replacing missing capture times with the current time. Keep PDF links limited to verified sources and never include API keys or private URLs.

Use available PDF tooling. If ReportLab is available and the language fits its built-in fonts, use `python3 scripts/render_report_pdf.py report.json report.pdf` from the skill directory (in the repository use `python3 .codex/pagespeed/scripts/render_report_pdf.py report.json report.pdf`). The renderer takes a report written from the evidence. It does not perform audits or write recommendations automatically. See its module docstring for the input format. For other scripts or languages, use tooling with suitable embedded fonts and the same footer contract.

Before delivering, verify the PDF opens, the text is complete and readable, and footer links on every page point to the actual report and repository. Use the workspace's supported file delivery mechanism; persist the PDF when available. If the current environment cannot produce a PDF, still deliver the summary and say what prevented the download.
