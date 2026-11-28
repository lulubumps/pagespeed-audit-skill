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

## CMS and commerce platforms

Confirm the platform and identify the owner of the issue before giving instructions. Choose one reversible change at a time, keep sensitive routes out of PSI, and preserve checkout, personalization, consent and cache bypasses. The paths below are places to investigate, subject to the installed version, theme and permissions.

| Platform | Where to investigate | Regression checks |
| --- | --- | --- |
| Shopify | Liquid sections and snippets, product and collection templates, theme app embeds, storefront assets and responsive image markup. Use a duplicate theme when available. | Product variants, media gallery, cart drawer, checkout handoff and pixels or consent behavior. |
| WordPress and WooCommerce | Theme or block templates, builder, plugin ownership, image pipeline and host/CDN layers. Preserve cart, checkout and account cache bypasses. | Navigation, forms, mini-cart updates, payment handoff and consent. |
| Drupal | Twig templates, asset libraries, image styles and responsive images, render cache, Dynamic Page Cache and CDN. Preserve cache contexts for personalized output. | Anonymous and authenticated behavior, forms and language variants. |
| Joomla | Template overrides, extensions, media and caching configuration. Isolate the extension or template that owns the resource. | Menus, modules, forms and multilingual routes. |
| Wix or Squarespace | Editor sections, image and video settings, built-in fonts and integrations, custom code and embeds. Describe managed-host constraints and available editor controls. | Responsive layout, navigation, booking or forms, storefront and checkout where relevant. |
| Webflow | Designer components, publishing settings, custom code, animations, image sizing and third-party embeds. Verify changes on the intended published site. | Breakpoints, interactions, CMS templates and forms. |
| Adobe Commerce / Magento or PrestaShop | Storefront theme, modules, image presets, static asset pipeline and full-page cache where supported. Keep customer-specific routes and state out of shared caches. | Product variants, cart state, checkout and logged-in behavior. |
| Headless CMS | Trace the finding to the storefront framework, CMS asset delivery, image CDN or build pipeline. Separate editorial changes from code changes. | Published route data, hydration, previews and image rendering. |

## Other PSI categories

- **Accessibility:** map each failed audit to the element and template. Suggest the appropriate semantic, contrast, accessible name or focus fix. Use a manual check when PSI cannot validate the interaction or experience.
- **Best practices:** tie recommendations to the cited audit and evidence. Prefer defensive fixes for affected configuration or dependencies. Automated PSI checks alone provide limited security coverage.
- **SEO:** inspect the template or settings serving the tested final page for the evidenced issue (for example metadata, crawlability, canonical links or anchor labeling). Verify the rendered page and keep intentionally private routes private.
- **Third-party assets:** distinguish the vendor domain, the actual integration owner and resource-attributed evidence. Avoid assuming every request from a vendor is responsible for a long task. Retest critical events and consent behavior before any rollout.
