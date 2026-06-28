# Design Tokens — theStacc 2026

The complete design vocabulary. Every value here is already declared in `src/pages/index.astro`'s `:root` and global styles — never re-derive.

## Color

```css
:root {
  /* Brand */
  --brand:         #4f39f6;        /* primary purple — buttons, links, accents */
  --brand-bright:  #6d5ef8;        /* hover state */
  --brand-deep:    #3a28b5;        /* footer background, deep emphasis */
  --brand-soft:    #ede9fe;        /* light-purple background tint */
  --brand-softer:  #f5f3ff;        /* lighter still — section washes */
  --brand-glow:    rgba(79, 57, 246, 0.4);  /* drop-shadows, focus rings */

  /* Neutral */
  --bg:            #ffffff;
  --bg-soft:       #fafaf9;        /* secondary section bg */
  --bg-dark:       #0a0a0f;        /* final CTA dark surface */
  --text-1:        #292524;        /* headings */
  --text-2:        #57534e;        /* body */
  --text-3:        #79716b;        /* muted */
  --border:        #e7e5e4;        /* subtle */
  --border-strong: #a8a29e;        /* visible dividers */

  /* Status */
  --accent-emerald: #10b981;       /* success */
  --accent-cyan:    #06b6d4;       /* info */
}
```

**Rules**
- Brand purple `#4f39f6` is the only primary. Never introduce a new purple.
- Hover always `#615fff` (`--brand-bright`).
- Footer + final-CTA dark band use `--brand-deep` and `--bg-dark` respectively. The footer is purple, the final CTA is near-black.
- Dot-pattern overlays (magicui-style) on dark backgrounds use `rgba(255,255,255,0.18)` for dots and a radial-gradient mask for the fade.

## Typography

| Class | Font | Size | Weight | Line | Use |
|---|---|---|---|---|---|
| `.h-display` | Geist | `clamp(44px, 6.4vw, 92px)` | 700 | 0.95 | Hero H1 only |
| `.h-lg` | Geist | `clamp(36px, 4.5vw, 64px)` | 600 | 1.02 | Every section H2 |
| `.h-md` | Geist | `clamp(28px, 3vw, 40px)` | 600 | 1.1 | Section sub-headings |
| `.h-sm` | Geist | `22px` | 600 | 1.2 | Card titles |
| Body | Geist | `15–17px` | 400–500 | 1.5–1.65 | Paragraphs |
| Mono | Geist Mono | `10–12px` | 600 | 1.4 | Eyebrow labels, stat suffixes, code-feel meta |

**Rules**
- Use ONE H1 per page.
- Every section H2 uses `.h-lg`. No mixing sizes between sections.
- Brand wordmark "theStacc" uses the **Doto** font (head + footer logo), provided by `public/button.flex.svg`.

## Spacing

Sections breathe with `padding: 96px 32px` (top/bottom 96, sides 32). Cards use 24–36px padding. Inline gaps use 8/12/16/24/32px multiples — never odd values.

## Radius

```css
*, *::before, *::after { border-radius: 0 !important; clip-path: none !important; }
```

The universal reset. Sharp corners everywhere except:
- Avatar circles (explicitly `border-radius: 50% !important`)
- Pill buttons / pill labels (`border-radius: 100px !important`)
- The browser-chrome URL pill on the hero video (`border-radius: 100px !important`)

## Shadow

```css
/* card lift on hover */
box-shadow: 0 18px 36px -14px rgba(79,57,246,0.18);

/* large hero / final card */
box-shadow: 0 24px 60px -16px rgba(15,15,30,0.35);

/* subtle row separation */
box-shadow: 0 1px 2px rgba(0,0,0,0.04);
```

Never use blurry "elevation 0–24" Material-style shadows. Always brand-purple-tinged or clean blue-black.

## Motion

| Effect | Duration | Easing | Where |
|---|---|---|---|
| Hover lift on cards | 250ms | `cubic-bezier(.2,.8,.2,1)` | Modules bento, verticals bento, resource marquee cards |
| Mega-menu open/close | 220ms | `cubic-bezier(.2,.8,.2,1)` | Header mega panels |
| Scroll-reveal fade-up | 550–700ms | `cubic-bezier(.2,.8,.2,1)` | All section content |
| Stat counters | 1.3s | `easeOutCubic` (custom) | Stats row only |
| Hero entrance stagger | 700ms each, 80ms gap | `cubic-bezier(.2,.8,.2,1)` | Pill → H1 → sub → CTAs → meta |
| Carousel slide | 720ms | `cubic-bezier(.2,.8,.2,1)` | Case-studies infinite loop |
| Marquee | 60s linear | infinite | Resources marquee |
| Tilt parallax (hero video) | 180–500ms | `cubic-bezier(.2,.8,.2,1)` | Hero video shell on mousemove |
| Magnetic CTA button | 180ms | `cubic-bezier(.2,.8,.2,1)` | Hero primary, final CTA |

All motion respects `@media (prefers-reduced-motion: reduce)` — every animation no-ops for that audience.

## Scroll Progress + Sticky CTA

- **Scroll progress bar**: 3px brand-purple bar at top, fixed, z-index 200, `transform: scaleX(0→1)` driven by `window.scrollY / scrollHeight`.
- **Sticky CTA**: appears after `scrollY > 200`, bottom-right `right: 24px; bottom: 24px;` — dark pill button with the brand-purple `$1` price chip prefix.

## Components inventory

These class names are stable. Reuse them — never rename.

```
.btn, .btn-primary, .btn-secondary, .btn-ghost, .btn-cta-nav
.hero-section, .hero-pill, .hero-ctas, .hero-meta, .hero-avatars
.trust-section, .trust-label, .trust-rating, .trust-logos, .trust-logo
.video-section, .video-shell, .browser-chrome, .browser-dots, .browser-url
.stats-row, .stat-cell, .stat-num, .stat-label
.modules-bento, .bento-grid, .bento-card, .bento-feature, .bento-num, .bento-icon
.problem-section, .ba-grid, .ba-col, .ba-list, .ba-divider
.solution-section, .solution-grid, .hl-highlight   /* "Three jobs." sweep */
.howitworks-section, .step-block, .step-grid, .step-card-1, .step-card-2, .step-card-3
.benefits-section, .benefit-cell, .b-stagger
.integrations-section, .integrations-grid, .integration-cell
.verticals-bento, .vb-card, .vb-feature, .vb-wide, .vb-brand
.cases-section, .cases-carousel, .cases-track, .case-slide
.testimonials-section, .testimonials-grid, .testimonials-left, .testimonials-right
.cost-section, .cost-table, .cost-row, .cost-savings, .cost-footnote
.resources-section, .resources-marquee, .resources-track, .resource-card
.guarantee-section, .guarantee-card
.final-section, .final-headline, .final-cta-btn, .final-trust, .final-ps, .dot-pattern
header .nav-item, .nav-trigger, .mega-panel, .mega-grid, .mega-col, .mega-link, .mega-cta
footer .footer-top, .footer-col, .footer-brand-block
.sticky-cta
.scroll-progress
```

## Universal rules

1. `border-radius: 0 !important` everywhere except explicit overrides.
2. Brand purple `#4f39f6` is the only primary.
3. All section H2s use `.h-lg`.
4. Stat number suffix (e.g. `+`, `k`, `%`, `×`) inside `.accent` uses **the same `font-weight: 700`** as its parent number.
5. Every footer link gets the up-right arrow icon (global `::after` mask).
6. Mega-menu is `position: fixed; left: 50%` — always centered on viewport, never on trigger.
7. The page-wide `prefers-reduced-motion` guard wraps every animation.
