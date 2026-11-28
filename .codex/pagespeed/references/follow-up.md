# Follow up on audit findings

Use this workflow when a user supplies a baseline and follow-up or asks to validate proposed changes. It supports a dry run with existing reports or fixtures. Do not deploy changes to a site as part of the comparison.

1. **Pair comparable measurements.** Match final URL (including meaningful query parameters), device, evidence type and audit coverage. Inspect Lighthouse version, throttling, environment and blocked or redirected runs. Use the median of comparable repeated lab runs when available and disclose the sample size. Do not substitute origin-level CrUX for URL-level CrUX. Label the two rolling windows and whether they overlap.
2. **Carry forward finding identity.** Match by final URL, device, category and audit ID. When a report only supplies a visible name, use it and mark the weaker match. If one audit has several independent issues, add a stable resource or component identifier. Group shared causes while retaining the original IDs. Never merge mobile with desktop or infer a match from a similar title alone.
3. **Assign a status with evidence.**
   - Resolved: the comparable follow-up explicitly passes the same check or has positive evidence that the observed condition no longer occurs.
   - Improved: the condition is still present but the comparable evidence shows improvement.
   - Unchanged: the condition persists and the evidence shows no clear change.
   - Regressed: the comparable evidence worsens for the same finding.
   - New: the follow-up shows the issue and comparable baseline evidence shows it was absent.
   - Unverified: a category or audit is missing, the run is blocked, the finding cannot be matched reliably, or the relevant interaction remains untested. A missing audit or item in a filtered summary is not a pass.
4. **Explain what changed.** Give the status, baseline and follow-up evidence, source links, device, sample size and caveats. Separate metric deltas, finding status, and confidence that a particular change caused the result. When runs differ in material ways, report them separately and request comparable evidence rather than asserting a trend.
5. **Deliver the result.** In chat highlight resolved or improved findings, regressions and unverified checks. In the downloadable audit PDF include the full finding inventory, suggested next actions and both sets of sources, following the PDF footer and source rules. Never label a synthetic fixture as a real measurement.

### Regression checks for this workflow

- Comparable mobile fixtures: verify the known score delta, identify the affected metrics and mark individual audit statuses only when both source audits support them.
- Blocked follow-up or different device: no resolved or improved claim.
- Missing audit under otherwise comparable conditions: unverified, unless the raw follow-up explicitly passes that same check.
