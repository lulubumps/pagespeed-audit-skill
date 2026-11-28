# Diagnostics and implementation

| PSI evidence | Where to investigate and what to change |
| --- | --- |
| LCP breakdown or render-blocking resources | Identify the LCP element per viewport. Match the fix to the measured subpart (TTFB, discovery delay, transfer or render delay). For a proven image discovery issue, expose the hero in initial HTML when viable and avoid lazy-loading it. Consider priority or preload only for the matching resource. For text LCP, check CSS and font dependencies. |
| Oversized images or layout shifts | Map examples to the shared template. Use responsive sizes and fitting compression. Reserve accurate dimensions or aspect ratio for images, embeds and dynamic slots. Verify crops and layout on relevant breakpoints. |
| TBT, long tasks, heavy third parties | Identify the script owner and call path. Reduce unused code, defer noncritical work or load an integration on demand where compatible with consent and critical interactions. Avoid treating estimated savings as measured gains. |
| High TTFB, long request chains or short static TTL | Inspect the measured document or resource. Distinguish DNS, server processing and cache symptoms when evidence permits. Use versioned static assets for long TTLs. Preserve bypasses for authenticated pages, forms with per-user tokens, checkout and personalized content. |
| Fonts or render-blocking CSS delaying text LCP and FCP | Identify the font files and stylesheets in the critical path. Self-host the fonts actually used, subset them where possible, use `font-display: swap` or `optional` and preload only the one or two files used above the fold. Inline or split critical CSS only through the build or optimization layer already in place. |
| Audit evidence overlaps | Combine actions addressing the same resource or cause. Avoid summing estimated milliseconds or bytes across overlapping audits. |

## Apply to the stack

- WordPress or other CMS: map the issue to the actual theme, builder, image pipeline, plugin, host or CDN. Start with one reversible setting and avoid overlapping asset transformations. Check navigation, forms, consent and editor-dependent behavior after a change.
- Ecommerce: work on a duplicate theme where available. Review storefront templates and app embeds. Validate cart and checkout behavior before promoting changes. Keep customer data, checkout sessions and account URLs out of PSI.
- SSR or SPA: inspect entry route, server-rendered markup, route chunks, hydration and data dependencies where PSI points to them. Keep public route caching compatible with authentication and personalization.
- Static site: find the component or build step generating the relevant asset. Check responsive markup, critical CSS and asset headers in the affected output before deployment.
- Unknown stack: name the universal change and what to inspect to locate its owner. Use conditional instructions for a plausible platform and label the assumption.

## WordPress and WooCommerce specifics

Apply only after confirming the theme, builder, cache layer and host. Change one layer at a time and retest, because stacking optimizers is the usual cause of regressions.

- **Page cache and TTFB:** confirm which layer caches (host, LiteSpeed, WP Rocket, W3 Total Cache, CDN) before touching settings. Check `cache-control` and cache-hit headers on the measured document. Add a persistent object cache (Redis or Memcached) only when TTFB stays high on cached-miss pages and the host supports it. Always exclude cart, checkout, my-account and any page with per-user tokens.
- **LCP image:** find the element PSI reports and confirm it is not lazy-loaded. Recent WordPress versions already add `fetchpriority="high"` to the first content image, but builders, sliders and lazy-load plugins can override it, so check the final HTML. Background images set in CSS or by a slider are discovered late; prefer a real `<img>` for the hero.
- **Elementor and other builders:** look for the builder's own switches for optimized asset loading, optimized DOM output, local Google Fonts and lazy-loaded backgrounds. Remove unused widgets and global kits' unused fonts. Do not combine these with a second plugin that minifies or delays the same assets without testing.
- **JavaScript delay or defer:** "delay until interaction" options can break consent banners, menus, sliders and checkout. Exclude critical scripts and verify navigation, forms, consent and payment after the change.
- **WooCommerce cart fragments:** if `wc-ajax=get_refreshed_fragments` runs on non-shop pages, disable it there only after checking the mini-cart still updates where it is shown. Keep cart, checkout and account URLs out of PSI.
- **Plugins and third parties:** map long tasks to the owning plugin or tag (chat widgets, analytics, pixels, maps, reviews). Query Monitor on staging shows which plugin owns slow queries and enqueued assets. Load heavy embeds on interaction where consent and function allow.
- **Images:** serve responsive `srcset` and modern formats (WebP or AVIF) through one image pipeline only, regenerate thumbnails after changing sizes, and set explicit width and height to prevent layout shift.
- **Safe rollout:** use a staging copy or one reversible setting at a time, record the previous value for rollback, then retest the same URL and device.
