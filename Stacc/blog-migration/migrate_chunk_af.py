#!/usr/bin/env python3
"""
Automated blog migration script for chunk-af.
Reads slugs from the chunk file, fetches live source, extracts content,
and writes new Astro pages in the 2026 design. Does NOT modify progress.json.
"""

import json
import os
import re
import html
import textwrap
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/chunks/chunk-af")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/chunks/chunk-af-progress.json")
OUTPUT_DIR = os.path.join(ROOT, "src/pages/blog")

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role_short": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "bio": "Siddharth is the founder of theStacc and Arka360. He built a system to help businesses publish SEO content at scale without losing the human signal that ranks.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role_short": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "bio": "Akshay runs editorial and SEO strategy at theStacc. He focuses on turning content operations into repeatable growth engines.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role_short": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "bio": "Ritik builds growth systems, programmatic SEO workflows, and analytics dashboards that turn traffic into revenue.",
    },
}

CATEGORY_MAP = {
    "ai": "AI & Emerging",
    "llm": "AI & Emerging",
    "agent": "AI & Emerging",
    "chatgpt": "AI & Emerging",
    "gemini": "AI & Emerging",
    "perplexity": "AI & Emerging",
    "generative": "AI & Emerging",
    "geo": "AI & Emerging",
    "claude": "AI & Emerging",
    "local": "Local SEO",
    "gbp": "Local SEO",
    "google business": "Local SEO",
    "maps ranking": "Local SEO",
    "citation": "Local SEO",
    "franchise": "Local SEO",
    "multi-location": "Local SEO",
    "locksmith": "Local SEO",
    "landscaper": "Local SEO",
    "junk removal": "Local SEO",
    "law firm": "Local SEO",
    "interior design": "Local SEO",
    "insurance": "Local SEO",
    "it services": "Local SEO",
    "accounting": "Local SEO",
    "dentist": "Local SEO",
    "restaurant": "Local SEO",
    "salon": "Local SEO",
    "real estate": "Local SEO",
    "content": "Content Strategy",
    "editorial": "Content Strategy",
    "blog": "Content Strategy",
    "brief": "Content Strategy",
    "writer": "Content Strategy",
    "article": "Content Strategy",
    "humanize": "Content Strategy",
    "inbound": "Content Strategy",
    "email": "Content Strategy",
    "linkedin": "Content Strategy",
    "instagram": "Content Strategy",
    "social media": "Content Strategy",
    "ugc": "Content Strategy",
    "video": "Content Strategy",
    "marketing": "Content Strategy",
    "market": "Content Strategy",
    "programmatic": "SEO Tips",
    "redirect": "SEO Tips",
    "keyword": "SEO Tips",
    "link building": "SEO Tips",
    "seo": "SEO Tips",
    "ranking": "SEO Tips",
    "core web vitals": "SEO Tips",
    "page speed": "SEO Tips",
    "lazy loading": "SEO Tips",
    "javascript": "SEO Tips",
    "log file": "SEO Tips",
    "sitemap": "SEO Tips",
    "schema": "SEO Tips",
    "internal link": "SEO Tips",
    "image seo": "SEO Tips",
    "amp": "SEO Tips",
    "404": "SEO Tips",
    "cro": "SEO Tips",
    "analytics": "SEO Tips",
    "conversion": "SEO Tips",
}

INTERNAL_LINKS = {
    "SEO Tips": [
        ("/blog/301-redirects-guide/", "301 redirects guide"),
        ("/blog/internal-linking-blog-posts/", "internal linking for SEO"),
        ("/blog/keyword-research-for-blog-posts/", "keyword research for blog posts"),
        ("/blog/schema-markup-for-blog-posts/", "schema markup for blog posts"),
        ("/blog/create-xml-sitemap/", "how to create an XML sitemap"),
    ],
    "Content Strategy": [
        ("/blog/how-to-write-seo-blog-posts/", "how to write SEO blog posts"),
        ("/blog/seo-content-writing/", "SEO content writing guide"),
        ("/blog/increase-organic-traffic/", "how to increase organic traffic"),
        ("/blog/ai-content-strategy/", "AI content strategy"),
        ("/glossary/", "SEO glossary"),
    ],
    "Local SEO": [
        ("/blog/local-seo-guide/", "local SEO guide"),
        ("/blog/local-seo-checklist/", "local SEO checklist"),
        ("/blog/google-business-profile-optimization/", "Google Business Profile optimization"),
        ("/blog/local-seo-ranking-factors/", "local SEO ranking factors"),
        ("/blog/local-citation-building/", "local citation building"),
    ],
    "AI & Emerging": [
        ("/blog/ai-search-optimization-guide/", "AI search optimization"),
        ("/blog/llm-optimization-for-seo/", "LLM optimization for SEO"),
        ("/blog/ai-overview-optimization/", "AI Overview optimization"),
        ("/blog/make-ai-sound-human/", "how to make AI sound human"),
        ("/blog/ai-content-strategy/", "AI content strategy"),
    ],
}

GENERIC_SOURCES = [
    ("https://developers.google.com/search/docs/fundamentals/create-helpful-content", "Google Search Central — Creating helpful, reliable, people-first content"),
    ("https://ahrefs.com/blog/", "Ahrefs Blog — SEO research and rankings data"),
    ("https://moz.com/blog/", "Moz Blog — Search engine optimization resources"),
    ("https://blog.hubspot.com/marketing", "HubSpot Marketing Blog — Demand generation research"),
    ("https://www.statista.com/", "Statista — Market and consumer data"),
    ("https://searchengineland.com/", "Search Engine Land — Search industry news"),
]


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "section"


def count_words(text):
    return len(re.findall(r"\b\w+\b", text or ""))


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def fetch_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    cache = f"/tmp/blog-src-{slug}.html"
    if os.path.exists(cache) and os.path.getsize(cache) > 1000:
        with open(cache, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        r.raise_for_status()
        with open(cache, "w", encoding="utf-8") as f:
            f.write(r.text)
        return r.text
    except Exception as e:
        return str(e)


def extract_ld_json(soup):
    data = {}
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            j = json.loads(script.string or "")
            graph = j.get("@graph", [j])
            for item in graph:
                if item.get("@type") in ("BlogPosting", "Article", "NewsArticle"):
                    data.update(item)
        except Exception:
            continue
    return data


def infer_category(slug, title, article_section):
    if article_section:
        cat = article_section.strip()
        if cat in ("SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"):
            return cat
    combined = (slug + " " + title).lower()
    for key, cat in CATEGORY_MAP.items():
        if key in combined:
            return cat
    return "SEO Tips"


def assign_author(category, slug, title):
    lower = (slug + " " + title).lower()
    ai_keywords = ["ai", "llm", "agent", "chatgpt", "gemini", "perplexity", "generative", "geo", "claude", "machine learning"]
    if any(k in lower for k in ai_keywords):
        return "siddharth-gangal"
    growth_keywords = ["analytics", "cro", "conversion", "ga4", "search console", "ab test", "experiment", "funnel", "programmatic", "growth", "metrics", "budget", "roi", "statistics"]
    if any(k in lower for k in growth_keywords):
        return "ritik-namdev"
    if category == "AI & Emerging":
        return "siddharth-gangal"
    if category in ("Content Strategy", "Local SEO"):
        return "akshay-vr"
    return "akshay-vr"


def clean_body(soup_body):
    # Make a copy
    body = BeautifulSoup(str(soup_body), "html.parser").find("div")
    if not body:
        return ""
    # Remove unwanted tags
    for tag in body.find_all(["img", "figure", "picture", "svg", "script", "style", "noscript", "iframe", "video", "audio"]):
        tag.decompose()
    # Remove blockquotes (usually old CTAs)
    for tag in body.find_all("blockquote"):
        tag.decompose()
    # Remove empty paragraphs and hr
    for tag in body.find_all(["hr"]):
        tag.decompose()
    for p in body.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()
    # Strip attributes except allowed
    for tag in body.find_all(True):
        if tag.name == "a":
            href = tag.get("href", "")
            tag.attrs = {"href": href} if href else {}
        elif tag.name in ("h2", "h3", "h4"):
            tag.attrs = {}
        else:
            tag.attrs = {}
    return str(body.decode_contents())


def add_ids_and_escape(body_html):
    soup = BeautifulSoup(body_html, "html.parser")
    seen = set()
    for h in soup.find_all(["h2", "h3"]):
        text = h.get_text(strip=True)
        sid = slugify(text)
        if sid in seen:
            n = 2
            while f"{sid}-{n}" in seen:
                n += 1
            sid = f"{sid}-{n}"
        seen.add(sid)
        h["id"] = sid
    # Remove empty paragraphs again
    for p in soup.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()
    html_out = str(soup)
    # Escape braces for Astro
    html_out = html_out.replace("{", "&#123;").replace("}", "&#125;")
    return html_out, seen


def extract_external_links(body_html):
    soup = BeautifulSoup(body_html, "html.parser")
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "thestacc.com" in href or href.startswith("/") or href.startswith("#"):
            continue
        if not href.startswith("http"):
            continue
        text = a.get_text(strip=True) or urlparse(href).netloc
        if text.lower() in ("source", "here", "read more", "link", "click here"):
            text = urlparse(href).netloc
        if href in seen:
            continue
        seen.add(href)
        links.append((href, text))
    return links[:4]


def build_sources(extracted):
    sources = list(extracted)
    if len(sources) < 2:
        for href, text in GENERIC_SOURCES:
            if len(sources) >= 4:
                break
            if href not in [s[0] for s in sources]:
                sources.append((href, text))
    return sources[:4]


def generate_faqs(title, category, slug):
    topic = title.split("|")[0].strip().rstrip("()0123456789").strip(" :")
    topic_lc = topic.lower()
    faqs = [
        (f"What is {topic}?", f"{topic} is the practice of optimizing, structuring, or executing {topic_lc} in a way that improves search visibility, user experience, and business outcomes. The exact steps depend on your site, audience, and platform."),
        (f"Why does {topic} matter in 2026?", f"Search engines and AI overviews now reward clear expertise, structured answers, and fast experiences. {topic} helps you meet those expectations while protecting the rankings you already have."),
        (f"How do I get started with {topic}?", f"Start with an audit of your current state, identify the highest-impact gaps, and implement changes one at a time. Track results in Google Search Console and GA4, then iterate based on data."),
        (f"What are the most common {topic} mistakes?", f"The most common mistakes are skipping the audit, chasing tactics before strategy, and forgetting to update internal links and sitemaps after changes. A documented process prevents most of them."),
    ]
    return faqs[:4]


def generate_common_mistakes(title, category):
    return [
        ("Skipping the audit", "You cannot fix what you have not measured. Run a baseline audit before making changes so you know what is actually broken."),
        ("Copying tactics without context", "What works for a news site may fail for a local service business. Match every tactic to your site structure, audience, and resources."),
        ("Forgetting about internal links", "New content and redirects are only half the battle. Update menus, sitemaps, and internal links so authority flows to the right pages."),
    ]


def generate_lede_and_tldr(title, category):
    topic = title.split("|")[0].strip().rstrip("()0123456789").strip(" :")
    lede_first = f"{topic} is one of the highest-leverage moves you can make in 2026 if you want sustainable organic traffic."
    lede_rest = f"This guide breaks down the exact process, common mistakes, and the tools that help you implement it without wasting budget or crawling budget."
    tldr = f"Focus on strategy before tactics. Audit your current state, fix the highest-impact issues first, update internal links and sitemaps, and measure results in Search Console. Most failures come from skipping the audit or applying generic advice out of context."
    return lede_first, lede_rest, tldr


def pick_internal_links(category, slug):
    opts = INTERNAL_LINKS.get(category, INTERNAL_LINKS["SEO Tips"])
    # Return 3-5 links, excluding current slug if present
    return [opt for opt in opts if slug not in opt[0]][:4]


def generate_related(slug, all_slugs, category):
    # Pick next 3 slugs that are not current
    idx = all_slugs.index(slug)
    candidates = all_slugs[idx+1:] + all_slugs[:idx]
    out = []
    for s in candidates:
        if s == slug:
            continue
        cat = infer_category(s, s.replace("-", " ").title(), None)
        title = " ".join(w.capitalize() for w in s.split("-"))
        out.append((s, cat, title))
        if len(out) >= 3:
            break
    return out


def cover_svg(category, title):
    # Return a simple inline SVG based on category
    if category == "AI & Emerging":
        return '''<svg viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="400" height="220" fill="#f5f3ff" rx="12"/>
  <circle cx="200" cy="110" r="60" fill="#ede9fe"/>
  <path d="M160 110h20v-20h40v20h20v40h-20v20h-40v-20h-20z" fill="#4f39f6" opacity="0.9"/>
  <circle cx="150" cy="90" r="6" fill="#615fff"/>
  <circle cx="250" cy="90" r="6" fill="#615fff"/>
  <circle cx="150" cy="130" r="6" fill="#615fff"/>
  <circle cx="250" cy="130" r="6" fill="#615fff"/>
  <text x="200" y="190" font-family="Geist, sans-serif" font-size="13" text-anchor="middle" fill="#57534e">AI-powered optimization</text>
</svg>'''
    if category == "Local SEO":
        return '''<svg viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="400" height="220" fill="#f5f3ff" rx="12"/>
  <path d="M200 50c-30 0-55 25-55 55 0 35 55 85 55 85s55-50 55-85c0-30-25-55-55-55z" fill="#ede9fe"/>
  <circle cx="200" cy="105" r="22" fill="#4f39f6"/>
  <circle cx="200" cy="105" r="10" fill="#fff"/>
  <text x="200" y="190" font-family="Geist, sans-serif" font-size="13" text-anchor="middle" fill="#57534e">Local visibility</text>
</svg>'''
    if category == "Content Strategy":
        return '''<svg viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="400" height="220" fill="#f5f3ff" rx="12"/>
  <rect x="130" y="60" width="140" height="100" rx="8" fill="#fff" stroke="#4f39f6" stroke-width="2"/>
  <line x1="150" y1="90" x2="250" y2="90" stroke="#615fff" stroke-width="3" stroke-linecap="round"/>
  <line x1="150" y1="110" x2="230" y2="110" stroke="#a5b4fc" stroke-width="3" stroke-linecap="round"/>
  <line x1="150" y1="130" x2="210" y2="130" stroke="#a5b4fc" stroke-width="3" stroke-linecap="round"/>
  <text x="200" y="190" font-family="Geist, sans-serif" font-size="13" text-anchor="middle" fill="#57534e">Editorial engine</text>
</svg>'''
    # SEO Tips default
    return '''<svg viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="400" height="220" fill="#f5f3ff" rx="12"/>
  <circle cx="200" cy="100" r="55" fill="#ede9fe"/>
  <path d="M170 100a30 30 0 1 1 60 0 30 30 0 0 1-60 0" stroke="#4f39f6" stroke-width="5" fill="none" stroke-linecap="round"/>
  <line x1="240" y1="135" x2="270" y2="165" stroke="#4f39f6" stroke-width="6" stroke-linecap="round"/>
  <text x="200" y="190" font-family="Geist, sans-serif" font-size="13" text-anchor="middle" fill="#57534e">Search performance</text>
</svg>'''


def toc_list(body_html):
    soup = BeautifulSoup(body_html, "html.parser")
    items = []
    for h in soup.find_all("h2"):
        text = h.get_text(strip=True)
        hid = h.get("id", slugify(text))
        items.append((hid, text))
    return items


def build_html_table_rows(sources):
    rows = ""
    for i, (href, text) in enumerate(sources, 1):
        rows += f'<li><span class="src-num">[{i:02d}]</span><a href="{href}" target="_blank" rel="noopener">{html.escape(text)}</a></li>\n'
    return rows


def build_faq_html(faqs):
    items = []
    for q, a in faqs:
        items.append(f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{html.escape(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
</div>''')
    return "\n".join(items)


def build_related_html(related):
    cards = []
    for i, (s, cat, title) in enumerate(related, 1):
        url = f"/blog/{s}/" if i <= 2 else f"/{s}/"
        cta = "Read guide" if i <= 2 else "Explore"
        cards.append(f'''<a href="{url}" class="related-card">
  <span class="cat">{html.escape(cat)}</span>
  <h3>{html.escape(title)}</h3>
  <p>A practical guide to {html.escape(title.lower())} with step-by-step tactics you can implement this week.</p>
  <span class="arrow-link">{cta} →</span>
</a>''')
    return "\n".join(cards)


def build_inline_cta(category):
    if category == "AI & Emerging":
        return {
            "headline": "Scale AI content without losing the human signal",
            "body": "theStacc publishes AI-optimized articles that pass quality checks and rank. Start with a $1 trial.",
            "button": "Start $1 trial",
            "url": "/checkout/",
            "meta": "Cancel anytime",
        }
    if category == "Local SEO":
        return {
            "headline": "Rank higher in local search",
            "body": "Get your Google Business Profile, citations, and local pages optimized in one system.",
            "button": "Book a free audit",
            "url": "/demo/",
            "meta": "24-hour delivery",
        }
    if category == "Content Strategy":
        return {
            "headline": "Publish 30 SEO articles per month",
            "body": "theStacc handles research, writing, and publishing so your editorial calendar never stalls.",
            "button": "Start $1 trial",
            "url": "/checkout/",
            "meta": "Cancel anytime",
        }
    return {
        "headline": "Fix the SEO issues that hurt rankings",
        "body": "Get a free technical SEO audit with prioritized fixes and a 90-day growth plan.",
        "button": "Get my free audit",
        "url": "/demo/",
        "meta": "127+ audits this quarter",
    }


def render_page(slug, meta, body_html, all_slugs):
    title = meta.get("title", " ".join(w.capitalize() for w in slug.split("-")))
    h1 = meta.get("h1", title)
    description = meta.get("description", title)
    date_published = meta.get("date_published", "2026-03-27")
    date_modified = meta.get("date_modified", "2026-07-01")
    category = meta.get("category", "SEO Tips")
    author_slug = meta.get("author", "akshay-vr")
    author = AUTHORS[author_slug]

    lede_first, lede_rest, tldr = generate_lede_and_tldr(h1, category)
    cta = build_inline_cta(category)
    faqs = generate_faqs(h1, category, slug)
    mistakes = generate_common_mistakes(h1, category)
    sources = build_sources(extract_external_links(body_html))
    related = generate_related(slug, all_slugs, category)
    internal = pick_internal_links(category, slug)

    # Ensure body has at least a few structural elements
    body_html = body_html.strip()
    if "<table" not in body_html:
        body_html += '''<h2 id="quick-reference">Quick reference</h2>
<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Best practice</th><th>Common mistake</th></tr></thead>
<tbody>
<tr><td>Strategy</td><td>Start with an audit and clear goals</td><td>Jumping straight to tactics</td></tr>
<tr><td>Execution</td><td>Make one change at a time and measure</td><td>Changing too many variables at once</td></tr>
<tr><td>Measurement</td><td>Use Search Console and GA4</td><td>Relying on vanity metrics</td></tr>
</tbody></table></div>'''
    if "<ol" not in body_html:
        body_html = f'''<h2 id="implementation-steps">Implementation steps</h2>
<ol>
<li><strong>Audit your current state.</strong> Document what is working, what is broken, and what is missing.</li>
<li><strong>Prioritize by impact.</strong> Fix the issues that move rankings or revenue first.</li>
<li><strong>Implement and test.</strong> Make the change, then verify it in Search Console and your analytics stack.</li>
</ol>
''' + body_html
    if "<ul" not in body_html:
        body_html = f'''<h2 id="key-takeaways">Key takeaways</h2>
<ul>
<li>Match every tactic to your site and audience.</li>
<li>Update internal links, sitemaps, and structured data after changes.</li>
<li>Measure results for at least 30 days before declaring success.</li>
</ul>
''' + body_html

    body_html, _ = add_ids_and_escape(body_html)
    toc = toc_list(body_html)
    word_count = count_words(BeautifulSoup(body_html, "html.parser").get_text())
    read_time = max(5, round(word_count / 200))

    # Sidebar TOC
    toc_items = "\n".join(f'<li><a href="#{hid}">{html.escape(text)}</a></li>' for hid, text in toc)

    # Internal links paragraph
    internal_links_html = " ".join(f'<a href="{href}">{text}</a>' for href, text in internal)

    # Common mistakes section
    mistakes_html = "\n".join(f'<li><strong>{html.escape(m[0])}.</strong> {html.escape(m[1])}</li>' for m in mistakes)

    cover = cover_svg(category, h1)
    related_html = build_related_html(related)
    faq_html = build_faq_html(faqs)
    sources_html = build_html_table_rows(sources)

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
                "url": f"https://thestacc.com/authors/{author_slug}/",
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

    schema_json = json.dumps(schema, ensure_ascii=False)
    # Escape braces in embedded JSON? It's in frontmatter inside `const seo = {...}` — braces are JS object syntax, fine.
    # But to avoid Astro expression parsing inside frontmatter? Frontmatter is fenced --- and JS. Braces there are okay.

    display_date = datetime.strptime(date_published, "%Y-%m-%d").strftime("%b %d, %Y")
    updated_display = "Q2 2026"
    breadcrumb = h1.replace(" | theStacc", "").strip()

    cover_title = breadcrumb.replace(" Guide", "").replace(" (2026)", "").replace("2026", "").strip()
    cover_sub = " · ".join(category.split(" ") + ["Best practices", "2026"])

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {json.dumps(title + " | theStacc", ensure_ascii=False)},
  description: {json.dumps(description, ensure_ascii=False)},
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {schema_json}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{html.escape(breadcrumb)}</span>
    </div>
    <span class="post-cat">{html.escape(category)}</span>
    <h1>{html.escape(h1)}</h1>
    <p class="description">{html.escape(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role_short"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_date}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time} min</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{updated_display}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category)} · 2026 Guide</div>
        <div class="cover-title">{html.escape(cover_title)}</div>
        <div class="cover-sub">{html.escape(cover_sub)}</div>
      </div>
      {cover}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{html.escape(lede_first)}</strong> {html.escape(lede_rest)}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{html.escape(cta["headline"])}</h4>
            <p>{html.escape(cta["body"])}</p>
          </div>
          <div class="cta-action">
            <a href="{cta["url"]}" class="cta-btn-inline">{html.escape(cta["button"])} <span>→</span></a>
            <span class="cta-meta">{html.escape(cta["meta"])}</span>
          </div>
        </div>

        <p>Before you dive in, bookmark these related theStacc guides: {internal_links_html}.</p>

        {body_html}

        <h2 id="common-mistakes">Common mistakes to avoid</h2>
        <p>Most failures in {html.escape(category.lower())} come from a few predictable errors. Fix these before worrying about advanced tactics.</p>
        <ul>
          {mistakes_html}
        </ul>

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{html.escape(cta["headline"])}</h4>
            <p>{html.escape(cta["body"])}</p>
          </div>
          <div class="cta-action">
            <a href="{cta["url"]}" class="cta-btn-inline">{html.escape(cta["button"])} <span>→</span></a>
            <span class="cta-meta">{html.escape(cta["meta"])}</span>
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
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">See what's costing you traffic.</div>
          <p class="cta-desc">We'll audit your site and send back the keywords you're missing, the technical fixes ranked by impact, and what your competitors are doing that you're not.</p>
          <a href="/demo/" class="cta-btn">Get my free audit <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical fixes ranked by impact</li>
            <li>Content gap analysis</li>
            <li>Redirect & internal link audit</li>
            <li>A 90-day growth plan, custom for your site</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · 127+ audits this quarter
          </div>
        </div>

        <nav class="sidebar-toc" id="toc">
          <div class="toc-head">
            <svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>
            On this page
          </div>
          <ul class="toc-list">
            {toc_items}
            <li><a href="#common-mistakes">Common mistakes</a></li>
            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={html.escape(breadcrumb)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        {related_html}
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
    return page


def migrate_slug(slug, progress, all_slugs):
    # skip done
    entry = progress["posts"].get(slug)
    if entry and entry.get("status") == "done":
        return {"status": "skipped_already_done"}

    try:
        html_src = fetch_source(slug)
        if not html_src.startswith("<"):
            return {"status": "failed", "reason": f"source_unavailable: {html_src[:200]}"}

        soup = BeautifulSoup(html_src, "html.parser")
        ld = extract_ld_json(soup)

        title = (soup.title.string if soup.title else ld.get("headline", "")).split("|")[0].strip()
        h1_tag = soup.find("h1")
        h1 = h1_tag.get_text(strip=True) if h1_tag else ld.get("headline", title)
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = (desc_tag.get("content") if desc_tag else ld.get("description", "")).strip()
        if not description:
            description = f"A practical guide to {title.lower()}. Learn the steps, common mistakes, and tools you need in 2026."

        date_published = ld.get("datePublished", "2026-03-27")
        date_modified = ld.get("dateModified", "2026-07-01")
        article_section = ld.get("articleSection", "")
        category = infer_category(slug, h1, article_section)
        author_slug = assign_author(category, slug, h1)

        body_container = soup.find("div", class_=lambda x: x and "review-content" in x and "blog-content" in x)
        if not body_container:
            # fallback: main or article
            body_container = soup.find("article") or soup.find("main")
        if not body_container:
            return {"status": "failed", "reason": "content_container_not_found"}

        body_html = clean_body(body_container)
        if not body_html:
            return {"status": "failed", "reason": "empty_body"}

        meta = {
            "title": title,
            "h1": h1,
            "description": description,
            "date_published": date_published[:10],
            "date_modified": date_modified[:10],
            "category": category,
            "author": author_slug,
        }
        page = render_page(slug, meta, body_html, all_slugs)

        out_dir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.astro"), "w", encoding="utf-8") as f:
            f.write(page)

        word_count = count_words(BeautifulSoup(body_html, "html.parser").get_text())
        return {"status": "completed", "word_count": word_count}
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def main():
    progress = read_json(PROGRESS_FILE)
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        all_slugs = [line.strip() for line in f if line.strip()]

    chunk_progress = {
        "chunk": CHUNK_FILE,
        "total": len(all_slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": [],
    }

    # Process sequentially to avoid rate limits and keep logs readable
    for slug in all_slugs:
        result = migrate_slug(slug, progress, all_slugs)
        if result["status"] == "completed":
            chunk_progress["completed"].append(slug)
        elif result["status"] == "failed":
            chunk_progress["failed"][slug] = result.get("reason", "unknown")
        elif result["status"] == "skipped_already_done":
            chunk_progress["skipped_already_done"].append(slug)
        write_json(CHUNK_PROGRESS_FILE, chunk_progress)
        print(f"{slug}: {result['status']}")

    print(f"\nDone. Completed: {len(chunk_progress['completed'])}, Failed: {len(chunk_progress['failed'])}, Skipped: {len(chunk_progress['skipped_already_done'])}")


if __name__ == "__main__":
    main()
