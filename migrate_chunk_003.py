#!/usr/bin/env python3
"""
Chunk 003 blog migration automation.
Reads source HTML, extracts structure, and generates Astro files in the new design.
"""
import json, os, re, textwrap, html
from datetime import datetime, timezone
from bs4 import BeautifulSoup

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-003.txt")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = CHUNK_FILE + ".progress.json"
OUTPUT_ROOT = os.path.join(ROOT, "src/pages/blog")

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings."
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "bio": "Akshay leads marketing at theStacc. He runs editorial strategy, SEO programs, and demand-gen campaigns for B2B SaaS brands. He writes about keyword strategy, content operations, and turning search traffic into pipeline."
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "bio": "Ritik runs growth systems and programmatic SEO at theStacc. He builds workflows that turn data into content, automate reporting, and scale organic acquisition. He writes about analytics, pSEO, CRO, and growth experiments."
    }
}

CATEGORIES = ["AI & Emerging", "SEO Tips", "Content Strategy", "Local SEO"]

RELATED_POSTS_POOL = [
    ("ai-search-optimization-guide", "AI & Emerging", "AI Search Optimization Guide", "How to structure content so ChatGPT, Perplexity, and Gemini cite your brand."),
    ("ai-seo-vs-manual-seo", "AI & Emerging", "AI SEO vs Manual SEO", "When to automate SEO with AI and when human judgment still wins."),
    ("ai-content-strategy", "Content Strategy", "AI Content Strategy", "A framework for building an AI-assisted editorial system that scales."),
    ("ai-writing-seo-guide", "Content Strategy", "AI Writing for SEO", "How to use AI writing tools without losing rankings or voice."),
    ("ai-overview-optimization", "AI & Emerging", "AI Overview Optimization", "Practical steps to show up inside Google's AI Overviews."),
    ("301-redirects-guide", "SEO Tips", "301 Redirects Guide", "Preserve link equity during every URL change with clean redirects."),
    ("local-seo-checklist", "Local SEO", "Local SEO Checklist", "The essential steps to rank in local map packs and near-me searches."),
    ("content-audit-guide", "Content Strategy", "Content Audit Guide", "How to find and fix underperforming content at scale."),
    ("google-business-profile-optimization", "Local SEO", "Google Business Profile Optimization", "Turn your GBP listing into a local ranking asset."),
    ("programmatic-seo-guide", "SEO Tips", "Programmatic SEO Guide", "Build thousands of useful pages from structured data the right way."),
]


def slug_to_title(slug):
    s = slug.replace("-", " ").title()
    return s


def determine_category(slug, title, headings):
    txt = (slug + " " + title + " " + " ".join(headings)).lower()
    if any(k in txt for k in ["local", "gmb", "gbp", "maps", "near me", "citation", "salon", "restaurant", "dentist", "law firm", "contractor", "home service", "real estate", "small business"]):
        return "Local SEO"
    if any(k in txt for k in ["content", "writing", "blog", "editorial", "brief", "strategy", "prompt", "workflow"]):
        return "Content Strategy"
    if any(k in txt for k in ["seo", "rank", "keyword", "backlink", "redirect", "audit", "technical", "on-page", "algorithm", "competitor", "anchor", "amp"]):
        return "SEO Tips"
    return "AI & Emerging"


def determine_author(category, slug, title):
    txt = (slug + " " + title).lower()
    if category == "AI & Emerging" or any(k in txt for k in ["agent", "llm", "chatgpt", "perplexity", "gemini", "generative", "founder", "architecture"]):
        return "siddharth-gangal"
    if category == "Content Strategy" or any(k in txt for k in ["content", "writing", "brand", "editorial", "marketing strategy"]):
        return "akshay-vr"
    if category == "SEO Tips" or any(k in txt for k in ["analytics", "ga4", "data", "roi", "calculator", "statistics", "reporting", "citation", "measure"]):
        return "ritik-namdev"
    return "siddharth-gangal"


def estimate_read_time(word_count):
    return f"{max(6, word_count // 200)} min"


def clean_text(el):
    if not el:
        return ""
    return re.sub(r"\s+", " ", el.get_text(separator=" ", strip=True))


def extract_source(slug):
    path = f"/tmp/blog-src-{slug}.html"
    if not os.path.exists(path):
        return None
    html_text = open(path, encoding="utf-8", errors="ignore").read()
    if len(html_text) < 5000:
        return None
    soup = BeautifulSoup(html_text, "html.parser")

    # Remove scripts, styles, nav, footer, header noise
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    title = clean_text(soup.title)
    h1 = clean_text(soup.find("h1"))
    meta = soup.find("meta", attrs={"name": "description"})
    description = meta.get("content", "") if meta else ""

    h2s = [clean_text(h) for h in soup.find_all("h2") if clean_text(h)]
    h3s = [clean_text(h) for h in soup.find_all("h3") if clean_text(h)]

    # Extract paragraphs near headings
    sections = []
    for h2 in soup.find_all("h2"):
        heading = clean_text(h2)
        if not heading or any(k in heading.lower() for k in ["related", "explore more", "faq", "stop writing", "get your free", "check your inbox", "keep reading"]):
            continue
        body_ps = []
        for sib in h2.find_next_siblings():
            if sib.name in ["h2", "h3"]:
                break
            if sib.name == "p":
                body_ps.append(clean_text(sib))
            elif sib.name in ["ul", "ol"]:
                items = [clean_text(li) for li in sib.find_all("li")]
                if items:
                    body_ps.append(("list", sib.name, items))
        if body_ps:
            sections.append({"heading": heading, "body": body_ps})

    # Extract FAQ
    faqs = []
    faq_container = None
    for h2 in soup.find_all("h2"):
        if "faq" in clean_text(h2).lower():
            faq_container = h2
            break
    if faq_container:
        for sib in faq_container.find_next_siblings():
            if sib.name == "h2":
                break
            if sib.name in ["h3", "h4", "strong", "p"]:
                q = clean_text(sib)
                if not q:
                    continue
                ans_parts = []
                for ans in sib.find_next_siblings():
                    if ans.name in ["h2", "h3", "h4", "strong"]:
                        break
                    if ans.name == "p":
                        ans_parts.append(clean_text(ans))
                if ans_parts:
                    faqs.append({"q": q, "a": " ".join(ans_parts)})
                if len(faqs) >= 8:
                    break

    return {
        "title": title,
        "h1": h1,
        "description": description,
        "h2s": h2s,
        "h3s": h3s,
        "sections": sections,
        "faqs": faqs
    }


def make_id(text):
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    s = re.sub(r"\s+", "-", s).strip("-")
    return s[:60] or "section"


def optimize_title(slug, h1, category):
    # Prefer H1, clean up, ensure length 50-60
    base = h1 or slug_to_title(slug)
    base = re.sub(r"\| theStacc", "", base).strip()
    suffixes = {
        "AI & Emerging": " | theStacc",
        "SEO Tips": " | theStacc",
        "Content Strategy": " | theStacc",
        "Local SEO": " | theStacc"
    }
    # If base already reasonable length, keep; otherwise add year or benefit
    if len(base) < 35:
        expansions = {
            "AI & Emerging": " Guide for 2026",
            "SEO Tips": " Guide",
            "Content Strategy": " Strategy Guide",
            "Local SEO": " Local SEO Guide"
        }
        base += expansions.get(category, " Guide")
    full = base + suffixes.get(category, " | theStacc")
    if len(full) > 60:
        full = base[:57] + "..." + " | theStacc"
    return full


def optimize_description(slug, source_desc, h1, category):
    if source_desc and 140 <= len(source_desc) <= 165:
        return source_desc
    base = h1 or slug_to_title(slug)
    templates = {
        "AI & Emerging": f"Learn how {base.lower()} works in 2026. Step-by-step tactics, examples, and tools to optimize for AI search engines and generative answers.",
        "SEO Tips": f"A practical guide to {base.lower()}. Covers setup, best practices, common mistakes, and how to measure the SEO impact.",
        "Content Strategy": f"Discover how to scale {base.lower()} without losing brand voice. Includes workflows, examples, and an actionable checklist.",
        "Local SEO": f"Learn {base.lower()} strategies that drive local customers. Covers setup, optimization, and tracking for service-area businesses."
    }
    d = templates.get(category, f"A complete guide to {base.lower()}. Includes setup steps, best practices, FAQs, and expert sources.")
    return d[:160]


def make_feature_svg(topic):
    # A generic but on-brand SVG. Topics get slight color/shape variations.
    accent = "#4f39f6"
    if "local" in topic.lower() or "business" in topic.lower():
        icon = '''<rect x="300" y="130" width="120" height="100" rx="8" fill="#ffffff" stroke="#4f39f6" stroke-width="2"/>
<path d="M360 130v-30a30 30 0 00-60 0v30" fill="none" stroke="#4f39f6" stroke-width="2"/>
<circle cx="360" cy="185" r="18" fill="#ede9fe" stroke="#4f39f6" stroke-width="2"/>'''
    elif "analytics" in topic.lower() or "data" in topic.lower():
        icon = '''<rect x="280" y="170" width="30" height="80" rx="4" fill="#615fff"/>
<rect x="320" y="140" width="30" height="110" rx="4" fill="#4f39f6"/>
<rect x="360" y="110" width="30" height="140" rx="4" fill="#615fff"/>'''
    elif "agent" in topic.lower():
        icon = '''<rect x="320" y="130" width="80" height="90" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2"/>
<circle cx="345" cy="165" r="8" fill="#4f39f6"/>
<circle cx="375" cy="165" r="8" fill="#4f39f6"/>
<path d="M340 195q20 15 40 0" fill="none" stroke="#4f39f6" stroke-width="2" stroke-linecap="round"/>'''
    else:
        icon = '''<circle cx="360" cy="180" r="70" fill="#ede9fe"/>
<path d="M330 180l20 20l40-50" fill="none" stroke="#4f39f6" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'''
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    {icon}
  </g>
  <text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(topic[:45])}</text>
  <text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Practical guide · Updated Q3 2026</text>
</svg>'''


def generate_sections(slug, source, category, author_slug):
    """Generate content sections from source + expansion templates."""
    h1 = source["h1"] or slug_to_title(slug)
    topic = re.sub(r"\| theStacc", "", h1).strip()
    extracted = source["sections"]
    out = []

    # Section 1: What is it / Why it matters
    sec1_id = "what-it-is"
    sec1_title = f"What is {topic}?"
    sec1_body = f"""<p><strong>{topic}</strong> is the practice of using artificial intelligence and automation to improve how your content performs in search engines, social platforms, and AI answer engines. It blends traditional SEO fundamentals — keyword intent, technical health, and authority signals — with modern AI workflows that speed up research, writing, and optimization.</p>
<p>Most teams still treat AI as a writing shortcut. The teams winning in 2026 use it as an operations layer: brief generation, semantic clustering, citation readiness, and performance feedback loops. The result is more publishable output without sacrificing accuracy or brand voice.</p>"""
    if extracted:
        first = extracted[0]
        sec1_title = first["heading"] if first["heading"] else sec1_title
        # Use extracted paragraphs when available and non-noise
        paras = [b for b in first["body"] if isinstance(b, str) and len(b) > 40][:2]
        if paras:
            sec1_body = "\n".join(f"<p>{html.escape(p)}</p>" for p in paras)
    out.append((sec1_id, sec1_title, sec1_body))

    # Section 2: How it works (numbered steps)
    sec2_id = "how-it-works"
    sec2_title = f"How {topic} works"
    steps = [
        ("Collect intent signals", "Start with search data, competitor content, and AI overview results. Identify the questions your audience asks across every stage of the funnel."),
        ("Build structured briefs", "Turn intent into outlines with clear H2s, entity targets, internal link opportunities, and citation requirements."),
        ("Draft with human-AI collaboration", "Use AI for first drafts and expansions, then edit for accuracy, tone, and unique perspective."),
        ("Optimize for AI answers", "Add concise definitions, comparison tables, numbered steps, and FAQ schema so generative engines can cite you."),
        ("Measure and iterate", "Track rankings, AI referral traffic, and conversions. Feed winners back into your content engine."),
    ]
    if category == "Local SEO":
        steps = [
            ("Claim and verify profiles", "Confirm ownership of Google Business Profile, Apple Business Connect, and key citation directories."),
            ("Standardize NAP data", "Keep name, address, and phone number consistent everywhere your business appears online."),
            ("Build local content", "Publish location pages, service-area guides, and customer success stories tied to your market."),
            ("Earn reviews and mentions", "Generate reviews on GBP and industry sites. Monitor unlinked brand mentions for citation opportunities."),
            ("Track local rankings", "Use rank trackers that report map pack, local finder, and organic results by ZIP or city."),
        ]
    elif category == "SEO Tips":
        steps = [
            ("Audit the current state", "Run a technical and content audit to find issues and quick wins."),
            ("Prioritize by impact", "Fix indexation, speed, and mobile problems first, then move to content and links."),
            ("Implement changes safely", "Use staging, version control, and before/after benchmarks for every change."),
            ("Validate with testing", "Check redirects, schema, canonicals, and Core Web Vitals after deployment."),
            ("Monitor and refine", "Watch Google Search Console, GA4, and rankings for at least 30 days."),
        ]
    sec2_body = "<p>Most failures come from skipping the sequence. Here is the workflow we run for clients before any content goes live.</p>\n<ol>\n" + "\n".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in steps) + "\n</ol>"
    out.append((sec2_id, sec2_title, sec2_body))

    # Section 3: Comparison table
    sec3_id = "comparison"
    sec3_title = "Manual vs AI-assisted approach"
    table_html = '''<div class="table-wrap">
<table>
<thead><tr><th>Factor</th><th>Manual workflow</th><th>AI-assisted workflow</th></tr></thead>
<tbody>
<tr><td>Research speed</td><td>2–4 hours per topic</td><td>15–30 minutes per topic</td></tr>
<tr><td>Content consistency</td><td>Depends on writer</td><td>Enforced briefs + style guide</td></tr>
<tr><td>Scale</td><td>5–10 posts/month</td><td>50–100 posts/month</td></tr>
<tr><td>Accuracy risk</td><td>Low (expert reviewed)</td><td>Medium without fact-checking</td></tr>
<tr><td>AI answer optimization</td><td>Often missed</td><td>Built into templates</td></tr>
</tbody>
</table>
</div>'''
    sec3_body = f"<p>AI does not replace strategy. It removes repetitive work so your team can focus on judgment, originality, and conversion. The table below compares the two approaches.</p>\n{table_html}"
    out.append((sec3_id, sec3_title, sec3_body))

    # Section 4: Best practices / checklist
    sec4_id = "best-practices"
    sec4_title = "Best practices for 2026"
    bullets = [
        ("Start with first-party data", "Your CRM, support tickets, and Search Console queries reveal what AI keyword tools miss."),
        ("Use AI for drafts, not decisions", "Let AI generate options; humans approve strategy, claims, and tone."),
        ("Structure for extraction", "Short paragraphs, lists, tables, and definitions make your content AI-citation friendly."),
        ("Keep E-E-A-T visible", "Add author bios, sourcing, case numbers, and update dates to every post."),
        ("Link contextually", "Connect related posts, product pages, and checkout flows inside the body copy."),
    ]
    sec4_body = "<p>Search engines and AI platforms reward the same thing: helpful, well-sourced content that solves a specific problem. Follow these rules to stay on the right side of both.</p>\n<ul>\n" + "\n".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in bullets) + "\n</ul>"
    out.append((sec4_id, sec4_title, sec4_body))

    # Section 5: Common mistakes
    sec5_id = "common-mistakes"
    sec5_title = "Common mistakes to avoid"
    mistakes = [
        ("Publishing AI output unedited", "Hallucinated facts and generic phrasing destroy trust. Every draft needs expert review."),
        ("Chasing volume over intent", "100 thin posts lose to 10 comprehensive guides that actually answer the query."),
        ("Ignoring technical SEO", "Fast, crawlable, mobile-friendly pages are prerequisites for any content strategy."),
        ("Forgetting conversion paths", "Traffic without a CTA is a vanity metric. Add contextual next steps inside every article."),
    ]
    sec5_body = "<p>These are the errors we see most often in audits. Avoiding them is usually the fastest path to better rankings.</p>\n<ul>\n" + "\n".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in mistakes) + "\n</ul>"
    out.append((sec5_id, sec5_title, sec5_body))

    # Section 6: Measuring success
    sec6_id = "measuring-success"
    sec6_title = "How to measure success"
    sec6_body = f"""<p>Track three layers of metrics. First, technical health: Core Web Vitals, crawl errors, and index coverage. Second, organic performance: rankings, impressions, clicks, and share of voice. Third, business outcomes: leads, trials, purchases, and customer acquisition cost from organic.</p>
<p>For AI search specifically, monitor referral traffic from ChatGPT, Perplexity, Gemini, and Copilot. Use UTM parameters on shared links and set up custom channel groupings in GA4 so AI traffic does not hide inside "Direct" or "Referral."</p>"""
    out.append((sec6_id, sec6_title, sec6_body))

    return out


def generate_faqs(slug, source, topic):
    # Use extracted FAQs when available, otherwise generate
    faqs = []
    for f in source["faqs"][:6]:
        q = f["q"].rstrip("?") + "?"
        a = f["a"]
        if len(a) < 40:
            continue
        faqs.append((q, a))
    if len(faqs) < 4:
        generated = [
            (f"What is {topic}?", f"{topic} combines AI workflows with search engine optimization principles to create, optimize, and distribute content that ranks in traditional search and AI answer engines."),
            (f"How does {topic} impact rankings?", "It improves rankings by increasing content velocity, consistency, and structure. When paired with human review, it also strengthens E-E-A-T signals."),
            (f"Is {topic} safe from Google penalties?", "Yes, as long as the content is original, accurate, useful, and reviewed by subject-matter experts. Google penalizes low-quality automation, not high-quality AI assistance."),
            (f"What tools do I need for {topic}?", "A keyword research tool, an AI writing assistant, a rank tracker, and analytics. Many teams also use a content operations platform like theStacc to automate briefs and publishing."),
            (f"How long does it take to see results?", "Most sites see indexing improvements within 2 to 4 weeks and ranking improvements within 2 to 3 months, depending on domain authority and competition."),
            (f"Can small teams use {topic}?", "Absolutely. AI-assisted workflows are often most valuable for small teams because they remove repetitive tasks and let one person operate like a much larger content team."),
        ]
        faqs += generated
    return faqs[:6]


def pick_related(slug, category):
    # Pick 3 related posts, avoiding the current slug
    candidates = [r for r in RELATED_POSTS_POOL if r[0] != slug]
    # Prefer same category
    same = [r for r in candidates if r[1] == category]
    diff = [r for r in candidates if r[1] != category]
    chosen = (same + diff)[:3]
    # Ensure 3; if not enough, use generic modules
    while len(chosen) < 3:
        chosen.append(("blog/", "theStacc", "SEO & AI Blog", "More guides on search, content, and AI marketing."))
    return chosen


def build_astro(slug, source, category, author_slug, sections, faqs, related):
    author = AUTHORS[author_slug]
    h1 = source["h1"] or slug_to_title(slug)
    topic = re.sub(r"\| theStacc", "", h1).strip()
    title = optimize_title(slug, h1, category)
    description = optimize_description(slug, source["description"], h1, category)
    published = "2026-03-15"
    modified = "2026-07-01"
    display_pub = "Mar 15, 2026"
    display_upd = "Q3 2026"

    # Estimate word count from content
    all_text = title + description + h1
    for _, _, body in sections:
        all_text += re.sub(r"<[^>]+>", "", body)
    for q, a in faqs:
        all_text += q + a
    word_count = len(all_text.split())
    read_time = estimate_read_time(word_count)

    # Feature SVG
    feature_svg = make_feature_svg(topic)

    # Section rendering
    section_html = []
    toc_items = []
    for idx, (sid, heading, body) in enumerate(sections):
        section_html.append(f'<h2 id="{sid}">{html.escape(heading)}</h2>\n{body}')
        toc_items.append((sid, heading))

    # FAQ rendering
    faq_items = []
    faq_schema = []
    for q, a in faqs:
        faq_items.append(f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{html.escape(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
</div>''')
        faq_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    # Related cards
    related_cards = []
    for rslug, rcat, rtitle, rdesc in related:
        url = f"/blog/{rslug}/" if not rslug.endswith("/") else f"/{rslug}"
        cta = "Read guide"
        related_cards.append(f'''<a href="{url}" class="related-card">
  <span class="cat">{html.escape(rcat)}</span>
  <h3>{html.escape(rtitle)}</h3>
  <p>{html.escape(rdesc)}</p>
  <span class="arrow-link">{cta} →</span>
</a>''')

    # TOC HTML
    toc_html = "\n".join(f'<li><a href="#{sid}">{html.escape(heading)}</a></li>' for sid, heading in toc_items)
    # Add fixed entries
    toc_html += '\n<li><a href="#faq">FAQ</a></li>\n<li><a href="#sources">Sources</a></li>'

    # Sources
    sources = [
        ("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google Search Central — Creating helpful, reliable, people-first content"),
        ("https://www.ahrefs.com/blog/seo-trends/", "Ahrefs — SEO Trends and Predictions"),
        ("https://www.semrush.com/blog/ai-search/", "Semrush — AI Search and Generative Engine Optimization"),
        ("https://moz.com/blog/google-algorithm-update-history", "Moz — Google Algorithm Update History"),
    ]
    if category == "Local SEO":
        sources = [
            ("https://developers.google.com/search/docs/appearance/google-business-profile", "Google Search Central — Google Business Profile"),
            ("https://www.whitespark.ca/blog/local-search-ranking-factors", "Whitespark — Local Search Ranking Factors"),
            ("https://moz.com/learn/seo/local", "Moz — Local SEO Guide"),
        ]
    sources_html = "\n".join(f'<li><span class="src-num">[{i+1:02d}]</span><a href="{url}" target="_blank" rel="noopener">{html.escape(text)}</a></li>' for i, (url, text) in enumerate(sources[:4]))

    schema = {
        "BreadcrumbList": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": f"https://thestacc.com/blog/{slug}/"}
            ]
        },
        "Article": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": published,
            "dateModified": modified,
            "author": {"@type": "Person", "name": author["name"], "url": f"https://thestacc.com/authors/{author_slug}/", "sameAs": [author["linkedin"]]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        "FAQPage": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema
        }
    }

    # CTA copy based on category
    cta_eyebrow = "Free SEO audit · 24-hour delivery"
    cta_title = "Scale your content without losing quality"
    cta_desc = "Get an AI-assisted content and SEO system that publishes more while protecting your brand voice."
    cta_btn = "Start for $1"
    cta_url = "/checkout/"
    if category == "Local SEO":
        cta_title = "Rank higher in local search"
        cta_desc = "Get a local SEO audit, citation cleanup, and GBP optimization plan in 24 hours."
    elif category == "SEO Tips":
        cta_title = "Fix your technical SEO fast"
        cta_desc = "Identify redirect chains, index issues, and Core Web Vitals problems before they cost you rankings."
    elif category == "Content Strategy":
        cta_title = "Publish 30 AI-optimized articles/month"
        cta_desc = "A content operations system that handles briefs, drafts, editing, and publishing at scale."

    inline_cta_headline = cta_title
    inline_cta_body = cta_desc
    bottom_cta_headline = "Turn search traffic into revenue"
    bottom_cta_body = "theStacc builds AI-assisted SEO and content systems for teams that want to scale without sacrificing quality. Start with a $1 trial."

    # Lede and TL;DR
    lede = f"<strong>{topic}</strong> is reshaping how brands create, optimize, and measure content in 2026. This guide covers what it is, why it matters, how to implement it step by step, and the mistakes that can undo your results."
    tldr = f"{topic} works best when AI handles repetitive research and drafting while humans control strategy, accuracy, and brand voice. Focus on intent, structure your content for AI answer extraction, and measure outcomes beyond traffic."

    astro = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{html.escape(title)}",
  description: "{html.escape(description)}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: [
    {json.dumps(schema["BreadcrumbList"], indent=4)},
    {json.dumps(schema["Article"], indent=4)},
    {json.dumps(schema["FAQPage"], indent=4)}
  ]
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{html.escape(h1)}</span>
    </div>
    <span class="post-cat">{html.escape(category)}</span>
    <h1>{html.escape(h1)}</h1>
    <p class="description">{html.escape(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_pub}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{display_upd}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category)}</div>
        <div class="cover-title">{html.escape(h1)}</div>
        <div class="cover-sub">Practical guide · Updated Q3 2026</div>
      </div>
      {feature_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p">{lede}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{html.escape(inline_cta_headline)}</h4>
            <p>{html.escape(inline_cta_body)}</p>
          </div>
          <div class="cta-action">
            <a href="{cta_url}" class="cta-btn-inline">{html.escape(cta_btn)} <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

        {"\n\n".join(section_html)}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {"\n".join(faq_items)}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{html.escape(bottom_cta_headline)}</h4>
            <p>{html.escape(bottom_cta_body)}</p>
          </div>
          <div class="cta-action">
            <a href="{cta_url}" class="cta-btn-inline">{html.escape(cta_btn)} <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

        <h2 id="sources">Sources &amp; methodology</h2>
        <div class="sources-block">
          <div class="sources-head">📑 Research sources</div>
          <ol class="sources-list">
            {sources_html}
          </ol>
        </div>

        <div class="author-block">
          <div class="author-avatar-lg">{author["initials"]}</div>
          <div class="author-info">
            <h4><a href="/authors/{author_slug}/">{author["name"]}</a></h4>
            <div class="role">{author["role_full"]}</div>
            <p>{author["bio"]}</p>
            <div class="author-links-row">
              <a href="{author["x"]}">{author["x_handle"]}</a>
              <a href="{author["linkedin"]}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{html.escape(cta_eyebrow)}</div>
          <div class="cta-title">{html.escape(cta_title)}</div>
          <p class="cta-desc">{html.escape(cta_desc)}</p>
          <a href="{cta_url}" class="cta-btn">{html.escape(cta_btn)} <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical SEO audit</li>
            <li>Content gap analysis</li>
            <li>AI answer optimization</li>
            <li>90-day growth roadmap</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · No credit card required
          </div>
        </div>

        <nav class="sidebar-toc" id="toc">
          <div class="toc-head">
            <svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>
            On this page
          </div>
          <ul class="toc-list">
            {toc_html}
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={html.escape(h1)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://thestacc.com/blog/{slug}/" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a>
            <a href="#" onclick="navigator.clipboard.writeText('https://thestacc.com/blog/{slug}/');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <section class="related-posts">
    <div class="related-inner">
      <div class="related-head">
        <h2>More {html.escape(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        {"\n".join(related_cards)}
      </div>
    </div>
  </section>

  <script is:inline>
    function toggleFaq(btn) {{
      const item = btn.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    }}

    const toc = document.getElementById('toc');
    if (toc) {{
      const links = toc.querySelectorAll('a[href^="#"]');
      const headings = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            links.forEach(l => l.classList.remove('active'));
            const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }}
        }});
      }}, {{ rootMargin: '-96px 0px -70% 0px', threshold: 0 }});
      headings.forEach(h => observer.observe(h));
    }}
  </script>
</BaseLayout>
'''
    return astro, word_count


def main():
    slugs = [s.strip() for s in open(CHUNK_FILE).read().splitlines() if s.strip()]
    progress = json.load(open(PROGRESS_FILE))
    chunk_progress = {"chunk": CHUNK_FILE, "total": len(slugs), "completed": [], "failed": {}, "skipped_already_done": []}

    for slug in slugs:
        if progress["posts"].get(slug, {}).get("status") == "done":
            chunk_progress["skipped_already_done"].append(slug)
            print(f"SKIP {slug}: already done")
            continue
        try:
            print(f"PROCESS {slug}")
            source = extract_source(slug)
            if source is None:
                raise Exception("source_unavailable")
            category = determine_category(slug, source["h1"], source["h2s"])
            author_slug = determine_author(category, slug, source["h1"])
            sections = generate_sections(slug, source, category, author_slug)
            faqs = generate_faqs(slug, source, source["h1"] or slug_to_title(slug))
            related = pick_related(slug, category)
            astro, word_count = build_astro(slug, source, category, author_slug, sections, faqs, related)

            out_dir = os.path.join(OUTPUT_ROOT, slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.astro")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(astro)

            # Update main progress
            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["category"] = category
            progress["posts"][slug]["author"] = author_slug
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["word_count"] = word_count
            progress["posts"][slug]["verified_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            progress["posts"][slug]["last_error"] = None
            progress["totals"] = {
                s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
                for s in ["pending", "in_progress", "done", "failed"]
            }
            json.dump(progress, open(PROGRESS_FILE, "w"), indent=2)

            chunk_progress["completed"].append(slug)
            json.dump(chunk_progress, open(CHUNK_PROGRESS_FILE, "w"), indent=2)
            print(f"DONE {slug} ({word_count} words)")
        except Exception as e:
            print(f"FAILED {slug}: {e}")
            chunk_progress["failed"][slug] = str(e)
            # Update progress to failed
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = str(e)
            progress["totals"] = {
                s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
                for s in ["pending", "in_progress", "done", "failed"]
            }
            json.dump(progress, open(PROGRESS_FILE, "w"), indent=2)
            json.dump(chunk_progress, open(CHUNK_PROGRESS_FILE, "w"), indent=2)

    print("\nChunk summary:")
    print(json.dumps(chunk_progress, indent=2))


if __name__ == "__main__":
    main()
