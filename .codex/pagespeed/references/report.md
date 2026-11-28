# Audit report

1. Lead with the weakest measured page or device and the fixes to start with. Keep the summary brief. Give the tested final URLs, devices, capture dates, report links or filenames and the categories available.
2. Show lab and CrUX metrics separately. Include lab score, FCP, LCP, TBT, CLS and Speed Index where available. Show CrUX p75 LCP, INP and CLS with page or origin scope and coverage. Mark unavailable metrics and invalid or blocked runs.
3. Inventory all evidenced issues across available PSI categories. Include notices or errors that limit coverage and distinguish manual checks from confirmed failures. When several audits describe the same cause, group them and retain every audit ID and affected URL/device. Use additional tables or an appendix for long inventories. A short summary never substitutes for this inventory.
4. For each confirmed issue or group, include category, audit ID, affected page/template and device, evidence, priority, proposed change and owner, verification and rollback where applicable. Mark hypotheses and missing evidence. Label savings as estimates and never add overlapping estimates.

| Priority | Category and audit IDs | Evidence and affected scope | Change and owner | Verification and rollback |
| --- | --- | --- | --- | --- |
| High | Performance and matching LCP audits | Mobile product page, hero discovered late, identified resource | Change the matching theme media component | Retest LCP and discovery delay, check image rendering, revert the component change if needed |

For before/after requests, show the observed delta, comparison caveats and functional checks separately. Report proposed, applied and verified changes with their actual status.
