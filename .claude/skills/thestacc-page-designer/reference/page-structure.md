# Page Structure — How to Assemble a Perfect Page

This guide explains the **shape** of a great page on theStacc — the order, the rhythm, the proportions, the polish moves. Use it after you've picked a recipe from `page-templates.md`.

## The 3-zone model

Every page divides into three zones — top, middle, bottom — and each zone has a job.

```
╔═══════════════════════════════════════════╗
║ TOP ZONE — 0–100vh                        ║   GOAL: Convert in 8 seconds.
║   • Hero (pitch + CTA pair)               ║   - The H1 says "I solve your problem."
║   • Trust strip (logos + 4.9★)            ║   - The CTA says "Start now."
║   • Hero video (the product)              ║   - The proof says "you're not the first."
╠═══════════════════════════════════════════╣
║ MIDDLE ZONE — explanation + proof         ║   GOAL: Earn the click.
║   • Stats / modules / problem→solution    ║   - Explain how, with shape & motion.
║   • How it works (3 steps)                ║   - Mix copy + visual + numbers.
║   • Benefits / integrations / verticals   ║   - Vary section width and direction.
║   • Case studies, testimonials, cost      ║   - Stack proof relentlessly.
╠═══════════════════════════════════════════╣
║ BOTTOM ZONE — close + safety net          ║   GOAL: Remove the last objection.
║   • Resources (educational off-ramp)      ║   - Show breadth of expertise.
║   • Guarantee (risk reversal)             ║   - Cancel any anxiety.
║   • Final CTA (the close)                 ║   - One simple action.
║   • Footer (long tail nav)                ║   - Recover the bouncing visitor.
╚═══════════════════════════════════════════╝
```

## Section spacing rhythm

| Position | Padding (vertical) | Visual change vs. previous |
|---|---|---|
| Hero | 80px top, 96px bottom | Light, full-bleed |
| Trust strip | 56px / 24px | Mono eyebrow → reset |
| Video | 48px / 96px | Frames a screenshot |
| Stats | none (touches neighbors) | Tight cells |
| Modules / Bento | 96px / 96px | Wash background |
| Problem | 96px / 96px | White background |
| Solution intro | 64px / 64px | Tight 2-col |
| How it works | 96px / 0 | Steps stack tightly |
| Benefits | 96px / 96px | Light background |
| Integrations | 96px / 96px | White |
| Case studies | 96px / 96px | Soft background |
| Testimonials | 96px / 96px | Dark band |
| Verticals | 96px / 96px | White |
| Cost | 96px / 96px | White |
| Resources | 96px / 96px | Soft background |
| Guarantee | 80px / 80px | Soft (right before final CTA) |
| Final CTA | 140px / 140px | Dark with dot-pattern |
| Footer | 80px top | Purple |

Why these aren't arbitrary: a page that flows well **alternates** white / soft / brand-wash / dark across sections. Three sections of the same background in a row reads as a wall.

## Background rotation rule

No more than **two consecutive sections** with the same background color.

✅ Good: white → soft → white → dark → white → soft
❌ Bad: white → white → white → soft → soft → white

## The 6 "rhythm beats" in a great commercial page

A perfect commercial page hits these six beats in order:

1. **Promise** — hero H1
2. **Proof** — trust logos, ratings, customer count
3. **Picture** — the video, the screenshots, the bento
4. **Pain** — problem section
5. **Pathway** — how-it-works
6. **Push** — guarantee + final CTA

Skip any one of these and conversion drops. A page that's all Promise + Push (modal-style "Sign up!") feels pushy. A page that's all Picture + Pathway (technical-deep tour) feels like a docs page.

## Content density rules

| Page goal | Density |
|---|---|
| Convert ($1 trial) | High — 12+ sections, motion, proof everywhere |
| Educate (blog, glossary) | Medium-low — 4–6 sections, mostly body copy, one CTA at the end |
| Build trust (about, case study) | Medium — narrative arc with 1–2 stats moments |
| Compare (review, alternative, vs) | High — tables, lists, FAQs, scannable |
| Capture leads (demo, contact) | Low — 3–4 sections, the form is the page |

## Above-the-fold hierarchy (the 8-second test)

Within 8 seconds of landing on the page, a visitor must see:

1. **Who it's for** (a name they recognise — "for dentists", "for SaaS")
2. **What it does** (a verb-led promise)
3. **Why now / why this** (a number — `$1`, `30/mo`, `92%`)
4. **The action** (the CTA)
5. **The reassurance** (trust line + 4.9★)

That's 5 elements that must compress into the hero zone. The H1 carries the first 3; the CTAs carry the 4th; the trust strip carries the 5th. The rest of the page elaborates.

## Width and column shapes

Vary visual width across sections so the page doesn't feel like a single column extending forever.

| Section type | Width pattern |
|---|---|
| Hero, trust, video | Full bleed (with internal max-width 1180px) |
| Stats | Full bleed (cells touch viewport edges) |
| Modules bento, verticals bento | 1180px max, 2-col grid |
| Problem section | 1180px max, 2-col split |
| How it works | Full bleed (alternates L/R) |
| Cases, testimonials | 1180px max |
| Cost table | 1080px max |
| Resources marquee | Full bleed (mask-fade on edges) |
| Guarantee, final CTA | 720–900px centered |
| Footer | 1180px max |

## Decorative moves we use sparingly

These polish the page when used 1–2× per page. More than that = visual noise.

1. **Brand-purple background wash** (e.g. modules featured card, vertical-brand card) — once per page max
2. **Dark band** — once per page (the testimonials section is the canonical use; final CTA is the second)
3. **Frosted-glass card** (e.g. how-it-works step cards) — only on brand-purple or dark surfaces
4. **Dot pattern overlay** (final CTA) — never more than once
5. **Scroll-spy nav active state** — passive, always-on
6. **Magnetic CTA** — only on the hero primary CTA and the final CTA
7. **Tilt parallax** — only on the hero video
8. **Counter animation** — only on the main stats row
9. **Sweep highlight** (`.hl-highlight`) — once per page max
10. **Marquee** — once per page max

## Mobile behavior (1180 → 540px)

Every section needs an explicit mobile rule. Defaults:

- **Multi-column grids** → 1 column
- **Bento spans 2x1 / 2x2** → 1x1 each
- **Carousels** → still carousels, each slide 92% width
- **Mega-menu** → collapses into a hamburger sheet
- **Sticky CTA** → smaller (40px height) with reduced padding
- **Hero H1** → drops to mobile clamp lower bound
- **Cost table** → horizontal scroll inside fixed-height container

If you don't write a mobile media query for a custom section, it's broken on mobile by default.

## Accessibility floor

- Color contrast minimum 4.5:1 for body, 3:1 for large text. Dark-purple text on brand-softer bg passes; light-gray on white usually fails — double-check.
- Every section gets a heading (visually or with `aria-label`).
- Every interactive thing keyboard-focusable + has a visible focus ring (the project default focus ring uses 2px brand purple).
- Reduced-motion variant exists for every animation (the global media query covers most).
- Alt text on every image, captions on video.
- All form fields have associated labels.

## Polish — the last 5%

These are the moves that separate a 90% page from a 100% page. Apply at the end of every build:

1. **Optical balance** the hero — if H1 ends with a tall character (`!`, `?`), nudge it left 4px. If the subhead has a long single word that wraps awkwardly, add `text-wrap: balance`.
2. **Tighten letter-spacing on big headlines** — `-0.025em` to `-0.045em` depending on size. Display-size text always wants negative tracking.
3. **Audit the CTA copy** — read each button aloud. If you'd never say it in conversation, rewrite it.
4. **Look at the page at 1440 / 1100 / 900 / 540 widths.** Fix any cramping, gaps, or weird wraps at each.
5. **Hide the cursor and tab through.** Every CTA must be reachable, every link must focus.
6. **Throttle network to "Fast 3G"** in DevTools. The above-the-fold must still render in under 3s.
7. **Confirm no console errors.** Even silent JS errors block the magnetic CTA, the carousel, and the mega-menu.
