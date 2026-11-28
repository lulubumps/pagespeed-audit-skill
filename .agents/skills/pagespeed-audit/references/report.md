# Quick report

Keep the default report to roughly one screen for a single URL. Use more detail only when the number of URLs or the user's request calls for it.

1. State the weakest measured device/route, dominant evidenced issue, and first action in one or two sentences. When the audit failed, lead with the missing evidence and why.
2. Give the capture date, tested final URL and PSI links or input filenames. Provide compact metrics per device. Use separate lab and field rows or tables. Lab includes score, FCP, LCP, TBT, CLS and Speed Index where available. Field includes p75 LCP, INP and CLS, page/origin scope and coverage. Use “unavailable” for missing values and give the reason when evidenced. Do not synthesize a score across templates.
3. Use the following table for up to three priority changes. Describe impact as qualitative unless measured. Flag hypotheses as such.

| Priority | Evidence and affected template | Change and where to make it | Verify and revert |
| --- | --- | --- | --- |
| 1 | Device, audit/metric, resource or selector when available | One concrete action with the owner or settings area | Retest the specific metric and feature, name the rollback when relevant |

4. If changes were applied, list their observed results and unverified checks. If evidence is incomplete, specify the next requested report, missing device or template. Don't invent a recommendation to fill the table.

## Example (shortened)

> **Mobile is the weak spot: LCP is 5.6 s because the hero image loads late (2.4 s load delay). Fix its discovery first.**
> Captured 2026-11-20, final URL https://example.com/, PSI report links attached.
> Lab mobile: score 42, FCP 3.1 s, LCP 5.6 s, TBT 780 ms, CLS 0.08, SI 6.2 s. Field: origin fallback only (page has no CrUX data), LCP 3.9 s (poor), INP 240 ms, CLS 0.07.
>
> | Priority | Evidence and affected template | Change and where to make it | Verify and revert |
> | --- | --- | --- | --- |
> | 1 | Mobile, LCP element `div.hero > img.wp-post-image`, load delay 2.4 s, image has `loading="lazy"` | Remove lazy-loading from the hero image in the theme template | Retest mobile LCP and phases (median of 3). Revert by restoring the attribute |
