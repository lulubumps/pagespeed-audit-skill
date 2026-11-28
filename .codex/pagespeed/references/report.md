# Audit report

1. Lead with the weakest measured page or device and the fixes to start with. Keep the summary brief. Give the tested final URLs, devices, capture dates, report links or filenames and the categories available. Include additional categories shown by PSI, such as Agentic Browsing, and record if they were available only in the web report.
2. Show lab and CrUX metrics separately. Include lab score, FCP, LCP, TBT, CLS and Speed Index where available. Show CrUX p75 LCP, INP and CLS with page or origin scope and coverage. Mark unavailable metrics and invalid or blocked runs.
3. Inventory all evidenced issues across available PSI categories. Include notices or errors that limit coverage and distinguish manual checks from confirmed failures. When several audits describe the same cause, group them and retain every audit ID and affected URL/device. If evidence comes from the web interface and an ID is unavailable, preserve the visible audit name. Group only when a shared resource or mechanism is evidenced. Related symptoms with different causes keep independent actions. Use additional tables or an appendix for long inventories. A short summary never substitutes for this inventory.
4. For each confirmed issue or group, include category, audit ID, affected page/template and device, evidence, priority, proposed change and owner, verification and rollback where applicable. State observation and causal confidence independently. Use **confirmed** for directly evidenced causes, **probable** for a supported attribution that needs isolation or a retest, and **unverified** for an unresolved cause. Label platform signals separately. A timeout means the check failed to retrieve the resource in that run. It does not establish that the resource is invalid or globally unavailable. Label savings as estimates and never add overlapping estimates.

| Priority | Category and audit IDs | Evidence and affected scope | Change and owner | Verification and rollback |
| --- | --- | --- | --- | --- |
| High | Performance and matching LCP audits | Mobile product page, hero discovered late, identified resource | Change the matching theme media component | Retest LCP and discovery delay, check image rendering, revert the component change if needed |

If an LCP breakdown does not reconcile with the headline metric, preserve both labeled sources and flag the discrepancy. Do not sum, normalize or assign the missing time to a specific asset. A text LCP can coexist with large image savings. Treat image delivery as a separate opportunity unless evidence connects those assets to the text render path.

Match each recommendation to the user's known access (editor, theme source, or hosting). If access or the owning component is unknown, give a confirmation step before a product-specific change.

For before/after requests, show the observed delta, comparison caveats and functional checks separately. Report proposed, applied and verified changes with their actual status.
