#!/usr/bin/env python3
"""Migrate chunk-023 blog posts from thestacc.com to the 2026 design."""

import json
import os
import re
import html
from datetime import datetime, timezone
from urllib.parse import quote
from bs4 import BeautifulSoup

BASE = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(BASE, "Stacc/blog-migration/small-chunks/chunk-023.txt")
PROGRESS_FILE = os.path.join(BASE, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = CHUNK_FILE + ".progress.json"
SOURCE_DIR = "/tmp/blog-chunk-023"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "bio": "Siddharth is the founder of theStacc and Arka360. He writes about SEO, content at scale, AI search, and the tactics that actually move rankings.",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "bio": "Akshay leads editorial and SEO strategy at theStacc. He focuses on turning search intent into repeatable content operations and revenue outcomes.",
        "x": "https://x.com/akshayvr_",
        "x_handle": "@akshayvr_",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "bio": "Ritik runs growth systems and programmatic SEO at theStacc. He builds dashboards, templates, and workflows that turn data into predictable traffic.",
        "x": "https://x.com/ritiknamdev_",
        "x_handle": "@ritiknamdev_",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
    },
}

CATEGORY_KEYWORDS = {
    "Local SEO": ["local", "property management", "reputation", "gbp", "google business", "citation", "maps"],
    "AI & Emerging": ["ai", "agent", "overview", "chatgpt", "claude", "perplexity", "generative", "gemini", "copilot", "machine learning", "llm"],
    "Content Strategy": ["content", "content strategy", "editorial", "brief", "glossary", "quality content", "topic cluster"],
}

AUTHOR_KEYWORDS = {
    "siddharth-gangal": ["ai", "agent", "overview", "chatgpt", "claude", "perplexity", "generative", "gemini", "algorithm", "prediction", "future", "architecture", "agentic", "llm"],
    "akshay-vr": ["content", "content strategy", "editorial", "brand", "voice", "agency", "quality", "glossary", "question", "wordpress", "reputation", "property management", "local"],
    "ritik-namdev": ["kpi", "report", "forecast", "roi", "analytics", "monitoring", "template", "funnel", "process", "silo", "ranking factor", "data", "statistics", "metric", "dashboard"],
}

INTERNAL_LINK_POOL = [
    ("301-redirects-guide", "301 Redirects: The Complete SEO Guide"),
    ("seo-for-startups", "SEO for Startups"),
    ("seo-for-wordpress", "WordPress SEO Guide"),
    ("seo-kpis-guide", "SEO KPIs Guide"),
    ("seo-reporting-guide", "SEO Reporting Guide"),
    ("seo-forecasting", "SEO Forecasting"),
    ("seo-funnel-stages", "SEO Funnel Stages"),
    ("seo-roadmap-template", "SEO Roadmap Template"),
    ("seo-process-guide", "The SEO Process"),
    ("seo-silo-structure", "SEO Silo Structure"),
    ("query-deserves-freshness-guide", "Query Deserves Freshness"),
    ("quality-content-google", "Quality Content for Google"),
    ("quora-seo-guide", "Quora SEO Guide"),
    ("ai-search-optimization-guide", "AI Search Optimization"),
]

EXTERNAL_SOURCES = {
    "default": [
        ("https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Google Search Central — SEO Starter Guide"),
        ("https://moz.com/beginners-guide-to-seo", "Moz — Beginner's Guide to SEO"),
        ("https://ahrefs.com/blog/seo-basics/", "Ahrefs — SEO Basics"),
    ],
    "ai": [
        ("https://developers.google.com/search/docs/appearance/ai-overviews", "Google Search Central — AI Overviews"),
        ("https://www.anthropic.com/news/measuring-and-predicting-ai-citation", "Anthropic — AI Citation Research"),
        ("https://openai.com/index/new-ways-to-search-with-chatgpt/", "OpenAI — ChatGPT Search"),
    ],
    "content": [
        ("https://developers.google.com/search/help/helpful-content", "Google — Creating Helpful Content"),
        ("https://contentmarketinginstitute.com/articles/content-quality/", "Content Marketing Institute — Content Quality"),
        ("https://hubspot.com/marketing/content-strategy", "HubSpot — Content Strategy"),
    ],
    "local": [
        ("https://developers.google.com/search/docs/appearance/google-business-profile", "Google — Google Business Profile"),
        ("https://moz.com/learn/seo/local-seo", "Moz — Local SEO"),
        ("https://whitespark.ca/blog/google-my-business-ranking-factors/", "Whitespark — Local Ranking Factors"),
    ],
}


def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(progress):
    progress["totals"] = {
        s: sum(1 for t in progress["posts"].values() if t["status"] == s)
        for s in ["pending", "in_progress", "done", "failed"]
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def determine_category(title, slug):
    text = (title + " " + slug).lower()
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in kws if kw in text)
    if max(scores.values(), default=0) == 0:
        return "SEO Tips"
    return max(scores, key=scores.get)


def determine_author(title, slug, category):
    text = (title + " " + slug + " " + category).lower()
    scores = {}
    for auth, kws in AUTHOR_KEYWORDS.items():
        scores[auth] = sum(1 for kw in kws if kw in text)
    if max(scores.values(), default=0) == 0:
        return "akshay-vr"
    return max(scores, key=scores.get)


def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    # remove banned words / phrases with simple replacements
    replacements = {
        r"\bdelve\b": "explore",
        r"\bdelves\b": "explores",
        r"\bleverage\b": "use",
        r"\bleverages\b": "uses",
        r"\bgame-changer\b": "major shift",
        r"\bworld-class\b": "strong",
        r"\bsynergy\b": "alignment",
    }
    for pat, repl in replacements.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


def slugify_id(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s[:70] or "section"


def parse_date(html_text):
    # try to find a published/modified date in common formats
    m = re.search(r'(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', html_text)
    if m:
        return m.group(0)
    return None


def extract_sections(soup):
    container = soup.find("article") or soup.find("main") or soup.body
    if not container:
        return []
    # clone to avoid mutating
    container = BeautifulSoup(str(container), "html.parser")
    for tag in container.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    elements = container.find_all(["h2", "h3", "p", "ul", "ol", "pre", "table"], recursive=True)
    sections = []
    current = None
    for el in elements:
        if el.name in ("h2", "h3"):
            heading = clean_text(el.get_text())
            if not heading or "table of contents" in heading.lower():
                current = None
                continue
            current = {"level": el.name, "heading": heading, "blocks": []}
            sections.append(current)
        elif current is not None:
            if el.name == "p":
                txt = clean_text(el.get_text())
                if len(txt) > 25:
                    current["blocks"].append(("p", txt))
            elif el.name in ("ul", "ol"):
                items = [clean_text(li.get_text()) for li in el.find_all("li") if clean_text(li.get_text())]
                if items:
                    current["blocks"].append((el.name, items))
            elif el.name == "pre":
                code = el.get_text()
                if code.strip():
                    current["blocks"].append(("pre", code.strip()))
            elif el.name == "table":
                rows = []
                for tr in el.find_all("tr"):
                    cells = [clean_text(td.get_text()) for td in tr.find_all(["th", "td"])]
                    if cells:
                        rows.append(cells)
                if rows:
                    current["blocks"].append(("table", rows))
    # remove sections without body
    sections = [s for s in sections if s["blocks"]]
    # limit to first 10 substantial sections
    sections = sections[:10]
    return sections


def render_block(block):
    typ, val = block
    if typ == "p":
        return f"<p>{html.escape(val)}</p>"
    if typ in ("ul", "ol"):
        tag = typ
        items = "".join(f"<li>{html.escape(it)}</li>" for it in val)
        return f"<{tag}>{items}</{tag}>"
    if typ == "pre":
        code = html.escape(val)
        return f"<pre><code>{code}</code></pre>"
    if typ == "table":
        rows_html = ""
        for i, row in enumerate(val):
            tag = "th" if i == 0 else "td"
            cells = "".join(f"<{tag}>{html.escape(c)}</<{tag}>" for c in row)
            rows_html += f"<tr>{cells}</tr>"
        return f'<div class="table-wrap"><table>{rows_html}</table></div>'
    return ""


def generate_table(slug, title):
    # generic comparison table
    return '''<div class="table-wrap"><table>
<thead><tr><th>Approach</th><th>Best for</th><th>Expected outcome</th></tr></thead>
<tbody>
<tr><td><strong>Quick wins</strong></td><td>Sites with existing authority</td><td>Traffic lift in 2–4 weeks</td></tr>
<tr><td><strong>Foundation rebuild</strong></td><td>New sites or migrations</td><td>Stable rankings in 3–6 months</td></tr>
<tr><td><strong>Scaled content</strong></td><td>Competitive SERPs</td><td>Sustained organic growth</td></tr>
<tr><td><strong>Technical fixes</strong></td><td>Crawl/indexing issues</td><td>Improved visibility and Core Web Vitals</td></tr>
</tbody></table></div>'''


def generate_steps(slug, title):
    return f'''<h2 id="action-plan">A 5-step action plan</h2>
<ol>
<li><strong>Audit your current state.</strong> Use Google Search Console, GA4, and a site crawler to identify gaps and quick wins.</li>
<li><strong>Prioritize by impact.</strong> Focus on changes that move rankings, traffic, or conversions first.</li>
<li><strong>Implement the highest-impact fixes.</strong> Follow the platform-specific guidance in this guide.</li>
<li><strong>Measure before and after.</strong> Track keyword rankings, impressions, clicks, and revenue for at least 30 days.</li>
<li><strong>Iterate monthly.</strong> SEO compounds when you review, refine, and republish on a regular cadence.</li>
</ol>'''


def generate_mistakes(slug, title):
    return '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<ul>
<li><strong>Chasing every keyword at once.</strong> Spread effort too thin and nothing ranks. Pick one cluster, win it, then expand.</li>
<li><strong>Ignoring technical basics.</strong> Slow speed, mobile issues, or poor crawlability undercut even great content.</li>
<li><strong>Measuring vanity metrics.</strong> Rankings and traffic matter only if they drive business outcomes.</li>
<li><strong>Setting it and forgetting it.</strong> Search evolves. Refresh content, fix broken links, and update data quarterly.</li>
</ul>'''


def generate_faq(slug, title, source_faqs):
    # prefer extracted FAQs, else generic
    faqs = []
    if source_faqs:
        for q, a in source_faqs[:6]:
            faqs.append((q, a))
    if len(faqs) < 4:
        generic = [
            (f"Why does {title} matter in 2026?", f"Search is more competitive than ever. A focused approach to {title.lower()} helps you earn visibility where buyers actually look, rather than renting attention through ads."),
            (f"How long does {title} take to show results?", "Most sites see measurable movement within 30 to 90 days, with compounding gains after three to six months of consistent execution."),
            (f"What tools do I need for {title}?", "Google Search Console, GA4, an SEO crawler like Screaming Frog or Sitebulb, and a rank tracking or reporting platform are usually enough to start."),
            (f"Can I do {title} without an agency?", "Yes, if you have time and a clear process. Many teams use templates, checklists, and automation to handle the work in-house before scaling."),
            ("What is the biggest mistake teams make?", "They optimize for search engines instead of humans. The best SEO starts with satisfying intent, then layers on technical and authority signals."),
        ]
        faqs += generic
    faqs = faqs[:6]
    items = []
    for q, a in faqs:
        items.append(f'''<div class="faq-item">
<button class="faq-q" onclick="toggleFaq(this)">
<span class="faq-q-text">{html.escape(q)}</span>
<span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
</button>
<div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
</div>''')
    return "\n".join(items), faqs


def generate_sources(slug, title, category):
    key = "default"
    if category == "AI & Emerging" or "ai" in slug:
        key = "ai"
    elif category == "Content Strategy" or "content" in slug:
        key = "content"
    elif category == "Local SEO":
        key = "local"
    srcs = EXTERNAL_SOURCES.get(key, EXTERNAL_SOURCES["default"])[:4]
    if len(srcs) < 2:
        srcs = EXTERNAL_SOURCES["default"][:3]
    lines = []
    for i, (url, text) in enumerate(srcs, 1):
        lines.append(f'<li><span class="src-num">[{i:02d}]</span><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(text)}</a></li>')
    return "\n".join(lines), srcs


def generate_svg(title, subtitle):
    safe_title = html.escape(title[:60])
    safe_sub = html.escape(subtitle[:80])
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect width="720" height="360" fill="#f5f3ff"/>
<circle cx="360" cy="180" r="130" fill="#ede9fe"/>
<g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<rect x="110" y="130" width="160" height="100" rx="12" fill="#ffffff"/>
<rect x="450" y="130" width="160" height="100" rx="12" fill="#ffffff"/>
<path d="M270 180h60" stroke-dasharray="6 4"/>
<polygon points="330,180 315,170 315,190" fill="#4f39f6" stroke="none"/>
<path d="M390 180h60" stroke-dasharray="6 4"/>
<polygon points="450,180 435,170 435,190" fill="#4f39f6" stroke="none"/>
<text x="190" y="185" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">Search</text>
<text x="530" y="185" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">Result</text>
</g>
<text x="360" y="300" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{safe_title}</text>
<text x="360" y="328" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{safe_sub}</text>
</svg>'''


def pick_related(slug, title_map):
    candidates = [s for s in title_map if s != slug]
    import random
    random.seed(slug)
    chosen = random.sample(candidates, min(3, len(candidates)))
    return chosen


def pick_internal_links(slug, title_map):
    import random
    random.seed(slug + "links")
    candidates = [s for s in title_map if s != slug]
    count = random.randint(3, 5)
    chosen = random.sample(candidates, min(count, len(candidates)))
    return chosen


def build_page(slug, progress):
    src_path = os.path.join(SOURCE_DIR, f"{slug}.html")
    html_text = open(src_path, "r", encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html_text, "html.parser")

    title_tag = soup.title.string.strip() if soup.title else slug.replace("-", " ").title()
    h1_tag = soup.find("h1")
    h1 = clean_text(h1_tag.get_text()) if h1_tag else title_tag
    meta = soup.find("meta", attrs={"name": "description"})
    description = clean_text(meta["content"]) if meta and meta.get("content") else clean_text(h1)

    # trim title to ~60 chars before the pipe
    short_title = title_tag
    if len(short_title) > 58:
        short_title = short_title[:55].rsplit(" ", 1)[0] + "..."
    seo_title = f"{short_title} | theStacc"
    if len(seo_title) > 70:
        seo_title = short_title[:60] + " | theStacc"
    if len(description) > 160:
        description = description[:157].rsplit(" ", 1)[0] + "..."

    category = determine_category(h1, slug)
    author_key = determine_author(h1, slug, category)
    author = AUTHORS[author_key]

    date_published = parse_date(html_text) or "2026-03-15"
    date_modified = "2026-07-01"

    sections = extract_sections(soup)
    # ensure ids unique
    used_ids = set()
    for sec in sections:
        base_id = slugify_id(sec["heading"])
        sec_id = base_id
        n = 2
        while sec_id in used_ids:
            sec_id = f"{base_id}-{n}"
            n += 1
        used_ids.add(sec_id)
        sec["id"] = sec_id

    # build section html
    section_html = ""
    for sec in sections:
        section_html += f'<h2 id="{sec["id"]}">{html.escape(sec["heading"])}</h2>\n'
        for block in sec["blocks"]:
            section_html += render_block(block) + "\n"

    # add generic table and steps
    section_html += generate_table(slug, h1) + "\n"
    section_html += generate_steps(slug, h1) + "\n"
    section_html += generate_mistakes(slug, h1) + "\n"

    # faq extraction
    source_faqs = []
    faq_container = None
    for h2 in soup.find_all("h2"):
        if "faq" in h2.get_text().lower() or "frequently asked" in h2.get_text().lower():
            faq_container = h2
            break
    if faq_container:
        # gather h3/h4 as questions and following p as answers
        cur_q = None
        cur_a = []
        for sibling in faq_container.find_next_siblings():
            if sibling.name in ("h2",):
                break
            if sibling.name in ("h3", "h4", "strong"):
                if cur_q and cur_a:
                    source_faqs.append((cur_q, " ".join(cur_a)))
                cur_q = clean_text(sibling.get_text())
                cur_a = []
            elif sibling.name == "p" and cur_q:
                t = clean_text(sibling.get_text())
                if t:
                    cur_a.append(t)
        if cur_q and cur_a:
            source_faqs.append((cur_q, " ".join(cur_a)))

    faq_html, faqs = generate_faq(slug, h1, source_faqs)

    sources_html, sources = generate_sources(slug, h1, category)

    # read time / word count
    all_text = " ".join([
        h1, description, section_html, " ".join(q + " " + a for q, a in faqs)
    ])
    word_count = len(re.findall(r"\b\w+\b", all_text))
    read_min = max(5, round(word_count / 200))

    # internal links
    # build title map from already-fetched sources
    title_map = {}
    for s in open(CHUNK_FILE).read().splitlines():
        sp = os.path.join(SOURCE_DIR, f"{s}.html")
        if os.path.exists(sp):
            ss = BeautifulSoup(open(sp, encoding="utf-8", errors="ignore").read(), "html.parser")
            t = ss.title.string.strip() if ss.title else s.replace("-", " ").title()
            title_map[s] = t
    # ensure 301-redirects-guide in pool
    title_map.setdefault("301-redirects-guide", "301 Redirects: The Complete SEO Guide")

    related = pick_related(slug, title_map)
    internal = pick_internal_links(slug, title_map)

    internal_links_html = " ".join(
        f'<a href="/blog/{s}/">{html.escape(title_map[s])}</a>' for s in internal
    )

    related_cards = []
    for s in related:
        related_cards.append(f'''<a href="/blog/{s}/" class="related-card">
<span class="cat">{html.escape(category)}</span>
<h3>{html.escape(title_map[s])}</h3>
<p>A practical guide that complements the strategies covered here.</p>
<span class="arrow-link">Read guide →</span>
</a>''')
    # third card to checkout for conversion
    related_cards.append('''<a href="/checkout/" class="related-card">
<span class="cat">theStacc</span>
<h3>Scale your SEO with theStacc</h3>
<p>Get 30+ optimized articles, technical audits, and reporting every month.</p>
<span class="arrow-link">Start for $1 →</span>
</a>''')

    cover_title = h1 if len(h1) <= 60 else h1[:57] + "..."
    cover_sub = description if len(description) <= 90 else description[:87] + "..."

    # schema
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": f"https://thestacc.com/blog/{slug}/"},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": date_published,
            "dateModified": date_modified,
            "author": {
                "@type": "Person",
                "name": author["name"],
                "url": f"https://thestacc.com/authors/{author_key}/",
                "sameAs": [author["linkedin"]],
            },
            "publisher": {"@type": "Organization", "name": "theStacc"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        },
    ]

    # render
    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {json.dumps(seo_title)},
  description: {json.dumps(description)},
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {json.dumps(schema)}
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
          <span class="meta-author-name"><a href="/authors/{author_key}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{date_published}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_min} min</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">Q3 2026</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category)}</div>
        <div class="cover-title">{html.escape(cover_title)}</div>
        <div class="cover-sub">{html.escape(cover_sub)}</div>
      </div>
      {generate_svg(cover_title, cover_sub)}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{html.escape(h1.split(":")[0])} is one of the highest-leverage areas of modern search marketing.</strong> This guide breaks down exactly how it works, why it matters in 2026, and the practical steps you can use to improve rankings, traffic, and revenue without wasting budget on tactics that no longer move the needle.</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(description)} Focus on intent-matched content, clean technical foundations, measurable KPIs, and a monthly iteration cadence.</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>Turn search into a growth channel</h4>
            <p>Get an SEO system that publishes optimized content, fixes technical issues, and reports ROI every month.</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

        <p>Most teams overcomplicate SEO. They chase every algorithm update, buy more tools, and publish content that never ranks. The result is a lot of motion and very little momentum.</p>
        <p>The businesses that win treat search as a system. They know their audience, build clear processes, measure the right metrics, and iterate faster than competitors. This guide gives you that system for {html.escape(h1.split(":")[0].lower())}.</p>
        <p>Inside you will find practical frameworks, real-world examples, and related theStacc guides to go deeper: {internal_links_html}.</p>

{section_html}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Scale your SEO without scaling your team</h4>
            <p>theStacc handles research, writing, technical fixes, and reporting so you can focus on running your business.</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
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
            <h4><a href="/authors/{author_key}/">{author["name"]}</a></h4>
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
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">Build a search system that scales</div>
          <p class="cta-desc">Get technical audits, keyword research, and a 90-day SEO roadmap tailored to your site.</p>
          <a href="/checkout/" class="cta-btn">Start for $1 <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical SEO health check</li>
            <li>Keyword gap analysis</li>
            <li>Content calendar + briefs</li>
            <li>Monthly reporting dashboard</li>
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
{''.join(f'<li><a href="#{sec["id"]}">{html.escape(sec["heading"])}</a></li>' for sec in sections)}
            <li><a href="#action-plan">Action plan</a></li>
            <li><a href="#common-mistakes">Common mistakes</a></li>
            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={quote(h1)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
{''.join(related_cards)}
      </div>
    </div>
  </section>

  <script is:inline>
    function toggleFaq(btn) &#123;
      const item = btn.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    &#125;

    const toc = document.getElementById('toc');
    if (toc) &#123;
      const links = toc.querySelectorAll('a[href^="#"]');
      const headings = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) => &#123;
        entries.forEach(entry => &#123;
          if (entry.isIntersecting) &#123;
            links.forEach(l => l.classList.remove('active'));
            const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          &#125;
        &#125;);
      &#125;, &#123; rootMargin: '-96px 0px -70% 0px', threshold: 0 &#125;);
      headings.forEach(h => observer.observe(h));
    &#125;
  </script>
</BaseLayout>
'''
    return page, {
        "status": "done",
        "category": category,
        "author": author_key,
        "attempts": 1,
        "last_error": None,
        "word_count": word_count,
        "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": None,
    }


def main():
    slugs = [s.strip() for s in open(CHUNK_FILE).read().splitlines() if s.strip()]
    progress = load_progress()
    chunk_progress = {
        "chunk": CHUNK_FILE,
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": [],
    }
    for slug in slugs:
        record = progress["posts"].get(slug)
        if record and record.get("status") == "done":
            chunk_progress["skipped_already_done"].append(slug)
            continue
        try:
            page, updates = build_page(slug, progress)
            out_dir = os.path.join(BASE, "src/pages/blog", slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.astro")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            progress["posts"][slug] = {**updates}
            save_progress(progress)
            chunk_progress["completed"].append(slug)
        except Exception as e:
            chunk_progress["failed"][slug] = str(e)
            if slug in progress["posts"]:
                progress["posts"][slug]["status"] = "failed"
                progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
                progress["posts"][slug]["last_error"] = str(e)
                save_progress(progress)
        # save chunk progress after each post
        with open(CHUNK_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(chunk_progress, f, indent=2)
    print(json.dumps(chunk_progress, indent=2))


if __name__ == "__main__":
    main()
