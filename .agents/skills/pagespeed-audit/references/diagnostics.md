# Diagnostics and implementation

| PSI evidence | Where to investigate and what to change |
| --- | --- |
| LCP breakdown or render-blocking resources | Identify the LCP element per viewport. Match the fix to the measured subpart (TTFB, discovery delay, transfer or render delay). For a proven image discovery issue, expose the hero in initial HTML when viable and avoid lazy-loading it. Consider priority or preload only for the matching resource. For text LCP, check CSS and font dependencies. |
| Oversized images or layout shifts | Map examples to the shared template. Use responsive sizes and fitting compression. Reserve accurate dimensions or aspect ratio for images, embeds and dynamic slots. Verify crops and layout on relevant breakpoints. |
| TBT, long tasks, heavy third parties | Identify the script owner and call path. Reduce unused code, defer noncritical work or load an integration on demand where compatible with consent and critical interactions. Avoid treating estimated savings as measured gains. |
| High TTFB, long request chains or short static TTL | Inspect the measured document or resource. Distinguish DNS, server processing and cache symptoms when evidence permits. Use versioned static assets for long TTLs. Preserve bypasses for authenticated pages, forms with per-user tokens, checkout and personalized content. |
| Audit evidence overlaps | Combine actions addressing the same resource or cause. Avoid summing estimated milliseconds or bytes across overlapping audits. |

## Apply to the stack

- WordPress or other CMS: map the issue to the actual theme, builder, image pipeline, plugin, host or CDN. Start with one reversible setting and avoid overlapping asset transformations. Check navigation, forms, consent and editor-dependent behavior after a change.
- Ecommerce: work on a duplicate theme where available. Review storefront templates and app embeds. Validate cart and checkout behavior before promoting changes. Keep customer data, checkout sessions and account URLs out of PSI.
- SSR or SPA: inspect entry route, server-rendered markup, route chunks, hydration and data dependencies where PSI points to them. Keep public route caching compatible with authentication and personalization.
- Static site: find the component or build step generating the relevant asset. Check responsive markup, critical CSS and asset headers in the affected output before deployment.
- Unknown stack: name the universal change and what to inspect to locate its owner. Use conditional instructions for a plausible platform and label the assumption.
