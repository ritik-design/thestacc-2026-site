# CTA Library

Every CTA on the site comes from this library. If you're tempted to write a new CTA, check here first — there's almost certainly one that fits.

## Primary CTAs (the ones that drive money)

| CTA copy | URL | Use on |
|---|---|---|
| **Start your $1 trial →** | `/checkout/` | Default homepage CTA, every commercial page primary CTA |
| **Start for $1 →** | `/checkout/` | Header nav button (shorter form, fits the nav height) |
| **Get started — $1** | `/checkout/` | Pricing card buttons |
| **Try theStacc — $1** | `/checkout/` | End-of-article CTAs in blog/glossary/reviews |
| **Start publishing today** | `/checkout/` | Landing pages for content-focused buyers |

## Secondary CTAs (sales-led / education)

| CTA copy | URL | Use on |
|---|---|---|
| **Book a 15-min demo** | `/demo/` | Always paired with the primary $1 trial CTA |
| **Watch 60-sec demo** | `#video` (in-page anchor) | When the video is on the same page |
| **See how it works** | `#howitworks` (in-page anchor) | On vertical landings |
| **See pricing →** | `/pricing/` | Mega-menu, footer, mid-article |
| **Run free SEO audit** | `/audit/` | Mid-page, when audience is in research mode |
| **Talk to sales** | `/contact/` | Agency / multi-location landings |
| **Get a custom proposal** | `/contact/?type=enterprise` | Enterprise / multi-location footer CTA |

## Tertiary CTAs (content / education)

| CTA copy | URL | Use on |
|---|---|---|
| **Read the playbook** | `/blog/` | Resource cards |
| **Browse 690+ glossary terms** | `/glossary/` | Resource cards |
| **Use the free tool** | `/tools/{tool}/` | Tool index, blog mid-article |
| **See all 22 reviews** | `/reviews/` | Resource cards |
| **Compare alternatives** | `/alternatives/` | Resource cards |
| **Explore the case studies** | `/case-studies/` | Resource cards, footer |
| **View all 118 best-of lists** | `/best/` | Resource cards |

## Module-specific CTAs

| CTA copy | URL | Use on |
|---|---|---|
| **Explore Content SEO →** | `/modules/content-seo/` | Bento card, in-line within homepage |
| **Explore Local SEO →** | `/modules/local-seo/` | Bento card, vertical landings |
| **Explore Social Media →** | `/modules/social-media/` | Bento card, ecommerce / DTC pages |

## CTA pairing rules

1. **Always offer a Primary + Secondary** as the hero CTA pair. Primary on the left/first, secondary on the right.
2. Default pair across the site: **Start your $1 trial → / Book a 15-min demo**.
3. On pages where buyers are early in research (glossary, blog), invert: **Run free SEO audit / Read the playbook**, then surface $1 trial in the final CTA only.
4. On vertical landings: pair the $1 trial with a vertical-specific demo CTA — `Book a demo for dentists`, `Talk to our agency team`.
5. Never show three or more CTAs in a hero. Maximum two.

## Button class mapping

```html
<!-- Primary (dark) -->
<a href="/checkout/" class="btn btn-primary">
  <span>Start your $1 trial <span class="arrow">→</span></span>
</a>

<!-- Secondary (outlined, dark border) -->
<a href="/demo/" class="btn btn-secondary">Book a 15-min demo</a>

<!-- Ghost (text only) — for header sign-in -->
<a href="/sign-in/" class="btn btn-ghost">Sign in</a>

<!-- Inline link CTA (text + animated arrow) -->
<a href="/blog/" class="tab-link">
  Read the playbook <span class="arrow">→</span>
</a>

<!-- Final CTA (large pill, on the dot-pattern dark band) -->
<a href="/checkout/" class="final-cta-btn">
  Start your $1 trial <span class="arrow">→</span>
</a>

<!-- Sticky floating CTA -->
<div class="sticky-cta" id="stickyCta" aria-hidden="true">
  <a href="/checkout/">
    <span class="price-pill">$1</span>
    Start your trial <span class="arrow">→</span>
  </a>
</div>
```

## CTA placement on the page

Standard commercial-page rhythm:

1. **Above the fold** — Primary + Secondary in hero
2. **After modules** — Inline `Explore {module} →` per card
3. **After pricing/comparison** — Primary `Start $1 trial`
4. **After case studies** — Secondary `Book a demo`
5. **Sticky bottom-right** — appears after 200px scroll (auto, no markup change needed if BaseLayout includes it)
6. **Final CTA section** — Primary `Start $1 trial` on the dark dot-pattern band

That's 6 CTA touchpoints on a fully-loaded commercial page. Don't add more.

## Microcopy below the primary CTA

Always include 1 of these trust-strip lines under the hero primary CTA — pick the one that fits the audience:

- "$1 trial · Cancel anytime · Content stays forever"
- "$1 trial · No credit card for the first 14 days"  *(if applicable to the plan)*
- "First article live in 24 hours · No agency lock-in"
- "30-day money-back · No contract"
- "Trusted by 127+ businesses · 4.9★ on G2"

If the page is a vertical landing, prepend the vertical: "Trusted by 18 dental practices · 4.9★ on G2".
