# Thresholds

Use these bands to label values. Source: web.dev Core Web Vitals and the Lighthouse scoring guides; re-check them if PSI starts showing different bands.

## Field (CrUX, p75, from real visits)

| Metric | Good | Needs improvement | Poor |
| --- | --- | --- | --- |
| LCP | <= 2.5 s | 2.5-4.0 s | > 4.0 s |
| INP | <= 200 ms | 200-500 ms | > 500 ms |
| CLS | <= 0.1 | 0.1-0.25 | > 0.25 |
| FCP (diagnostic) | <= 1.8 s | 1.8-3.0 s | > 3.0 s |
| TTFB (diagnostic) | <= 0.8 s | 0.8-1.8 s | > 1.8 s |

A page passes Core Web Vitals only when LCP, INP and CLS are all Good at p75. If any of the three is missing, do not claim a pass.

## Lab (Lighthouse, one simulated run)

| Metric | Good | Needs improvement | Poor |
| --- | --- | --- | --- |
| Performance score | 90-100 | 50-89 | 0-49 |
| FCP | <= 1.8 s | 1.8-3.0 s | > 3.0 s |
| LCP | <= 2.5 s | 2.5-4.0 s | > 4.0 s |
| TBT | <= 200 ms | 200-600 ms | > 600 ms |
| CLS | <= 0.1 | 0.1-0.25 | > 0.25 |
| Speed Index | <= 3.4 s | 3.4-5.8 s | > 5.8 s |

Lab and field answer different questions. A good lab score does not offset poor field data, and TBT is a lab proxy for responsiveness, not INP.

## LCP subparts

Compare the four phases (TTFB, resource load delay, resource load duration, element render delay) before choosing a fix. The largest phase points to the work: slow TTFB to server and cache, large load delay to discovery (lazy-loading, late injection, priority), long load duration to image weight and delivery, long render delay to blocking CSS, fonts or scripts. As a rough guide from web.dev, a healthy LCP spends about 40% in TTFB, under 10% in load delay, about 40% in load duration and under 10% in render delay. Large deviations from that split show where to look first.
