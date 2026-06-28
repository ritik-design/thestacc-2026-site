# Sections Library

Every section pattern proved-out in the homepage at `src/pages/index.astro`. When you need a section, copy the markup from the homepage line range below, then customise the copy.

Each entry: **name** · **homepage line range (approx)** · **purpose** · **adapt for**.

## 1. Header with mega-menu
- Lines: ~1750–1830
- Three trigger items (Product, Solutions, Resources) each open a 3-column fixed-position mega-panel (centered on viewport, not on the trigger).
- Adapt: only the menu items themselves — leave the open/close JS, the caret rotation, and the fixed positioning untouched.

## 2. Scroll-progress bar
- Single `<div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>` above `<header>`.
- 3px brand-purple line tracking page scroll.
- Don't remove — adds polish to every page.

## 3. Hero (centered)
- Lines: ~1755–1810
- Pattern: pill → H1 → subhead → CTAs → meta (avatars + 4.9 stars).
- Adapt: H1, subhead, CTAs. Keep the avatar tile + star line — it's recognizable cross-page social proof.

## 4. Trust logos
- Lines: ~1790–1810
- 4.9 from 127 reviews + 10 customer logos in a 5×2 grayscale grid (color on hover).
- Use on: homepage, modules, pricing, about, demo, vertical landings, SEO-keyword landings.
- Skip on: blog posts, glossary terms, tools.

## 5. Hero video (browser-chrome wrapper)
- Lines: ~1812–1828
- Browser-chrome (mac dots + URL pill) wraps a muted-autoplay video.
- Adapt: only the video source. Use `/hero-demo.mp4` as fallback for any page.
- Skip on: text-heavy pages (glossary, terms, privacy).

## 6. Stats row (4-cell)
- 4 brand-stat cells with animated counters (92%, 47+, 3,000+, $40k+).
- Use as the proof beat between major sections.
- Adapt: numbers + labels per page narrative. Keep 4 cells.

## 7. Modules bento (3 cards)
- The "Three modules · One platform" bento — 2 cards top row, full-width Social Media card bottom.
- Adapt: when on `/modules/*` itself, make the current module the featured (top) card; demote the others to a smaller "also see" section.

## 8. Problem section (before / after)
- Two-column "Before theStacc" vs "With theStacc" — 5 numbered pain/win rows each, arrow divider.
- Use on: homepage, pricing, demo, comparison pages, any SEO-keyword landing where buyers are agency-disappointed.

## 9. Solution intro
- "One platform. **Three jobs.** Zero busywork." — the highlighted phrase animates a brand-purple sweep on scroll-into-view (`.hl-highlight`).
- Adapt: change "Three jobs." to a 1–2-word emphasis phrase per page; keep the highlight effect.

## 10. How it works (3 steps)
- 3 alternating L/R panels with brand-purple frosted-glass cards on a light grid background.
- Use on: homepage, demo, pricing, vertical landings.
- Adapt: the 3 step descriptions to match the buyer's journey for that page's audience.

## 11. Benefits cards (4 cells, 200ms stagger)
- 4 outcomes with stat + label. Staggered fade-up on enter viewport.
- Adapt: pick 4 outcomes from product.md's value list relevant to the page.

## 12. Integrations grid
- 8 logos in a 4×2 grid + "Custom CMS" as the 8th.
- Use on: any page where buyers worry about "will it work with my stack?" — modules, pricing, integrations landings.

## 13. Case studies carousel (70/30 infinite loop)
- 3 slides, first at 70% width, next at ~28% peek, auto-rotate every 4.5s, dot navigation.
- Use on: homepage, pricing, demo, vertical landings, case-studies index. On `/case-studies/{slug}/` itself, replace with a single full-bleed featured study.

## 14. Testimonials (dark grid, sticky left)
- Dark band with sticky left column (label + headline) and scrollable right column of 1 large featured case + 5 t-cards.
- Use on: homepage, modules, pricing, demo.
- Adapt: testimonials per page topic if you have them; reuse the homepage's if not.

## 15. Cost comparison table
- 4-column table (Vertical / Agency / Freelancer / theStacc), 3 example rows + the "You save $40,800/year" footer + 25px-padded footnote.
- Use on: pricing, alternatives, comparison, agency landings, white-label-* pages.

## 16. Verticals bento (4×2)
- 6 cards: 2 wide cards top row (SaaS + Local Businesses), 4 standard cards bottom row (one is brand-purple). Uniform 22px card headings.
- Use on: homepage, `/for/`, vertical landings (highlight that page's vertical as the brand-purple card).

## 17. Resources marquee (auto-scrolling)
- 9 cards: Blog, Tools, Glossary, Best, Reviews, Alternatives, Case studies, By vertical, Compare. Cloned for seamless 60s loop.
- Use on: homepage, blog index, glossary index, tools index.
- Skip on: blog posts and glossary terms (would be self-referential).

## 18. Guarantee strip (3 cards)
- 30-day money-back / Content stays forever / No contract.
- Use ABOVE the final CTA on every commercial page.

## 19. Final CTA (dot-pattern dark)
- Dark `--bg-dark` band with magicui-style dot-pattern radial-faded background.
- "Your competitors are publishing daily. / You're not." headline (two lines, balanced).
- Use on every commercial page.
- Adapt: swap the headline per page (always 2 short lines).

## 20. Footer (purple, 5 columns)
- Product / Solutions / Resources / Company / Connect — 35+ links, every link with the global up-right-arrow `::after`.
- Brand wordmark below the columns.
- Bottom bar: Privacy / Terms / Security + © year.

## Compositional rules

- **Section order** is usually: header → hero → trust → video → stats → modules → problem → solution → howitworks → benefits → integrations → case-studies → testimonials → verticals → cost → resources → guarantee → final-cta → footer.
- **Pick 5–10 sections** for any given page. Not every page needs all 20.
- **Group sections in pairs** that share a tonal beat (e.g. problem + solution always together; guarantee + final-cta always together).
- **Always end commercial pages** with guarantee → final-cta → footer.
- **Always end content pages** (blog, glossary, tools) with "Related X" → final-cta lite (smaller variant) → footer.
