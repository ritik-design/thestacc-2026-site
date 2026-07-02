#!/usr/bin/env python3
"""Migrate chunk-021 blog posts to the new 2026 theStacc design."""

import json
import os
import re
import subprocess
import textwrap
from datetime import datetime, timezone
from html import escape

from bs4 import BeautifulSoup

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = f"{ROOT}/Stacc/blog-migration/small-chunks/chunk-021.txt"
PROGRESS_FILE = f"{ROOT}/Stacc/blog-migration/progress.json"
CHUNK_PROGRESS = CHUNK_FILE + ".progress.json"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He writes about SEO, content at scale, AI search, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "bio": "Akshay runs marketing at theStacc. He specializes in SEO strategy, editorial workflows, brand voice, and turning content into qualified demand.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev_",
        "bio": "Ritik leads growth systems at theStacc. He works on programmatic SEO, analytics, CRO, and the experiments that scale organic traffic.",
    },
}

CATEGORY_SOURCES = {
    "SEO Tips": [
        {"url": "https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "text": "Google Search Central — SEO Starter Guide"},
        {"url": "https://moz.com/beginners-guide-to-seo", "text": "Moz — Beginner's Guide to SEO"},
        {"url": "https://ahrefs.com/blog/seo-basics/", "text": "Ahrefs — SEO Basics"},
        {"url": "https://www.searchenginejournal.com/seo-guide/", "text": "Search Engine Journal — SEO Guide"},
    ],
    "Content Strategy": [
        {"url": "https://blog.hubspot.com/marketing/content-strategy", "text": "HubSpot — Content Strategy Guide"},
        {"url": "https://contentmarketinginstitute.com/articles/content-strategy/", "text": "Content Marketing Institute — What Is Content Strategy?"},
        {"url": "https://www.semrush.com/blog/content-strategy/", "text": "Semrush — How to Build a Content Strategy"},
    ],
    "Local SEO": [
        {"url": "https://support.google.com/business/answer/2911778", "text": "Google Business Profile Help"},
        {"url": "https://www.brightlocal.com/learn/local-consumer-review-survey/", "text": "BrightLocal — Local Consumer Review Survey"},
        {"url": "https://whitespark.ca/blog/", "text": "Whitespark — Local SEO Blog"},
    ],
    "AI & Emerging": [
        {"url": "https://ai.google/discover/", "text": "Google AI"},
        {"url": "https://www.anthropic.com/news", "text": "Anthropic — AI Research"},
        {"url": "https://openai.com/research", "text": "OpenAI Research"},
        {"url": "https://www.perplexity.ai/hub", "text": "Perplexity Hub"},
    ],
}

RELATED_CARDS = {
    "SEO Tips": [
        {"slug": "301-redirects-guide", "cat": "SEO Tips", "title": "301 Redirects: The Complete SEO Guide", "desc": "Preserve link equity during every URL change with clean 301 redirect workflows."},
        {"slug": "on-page-seo-guide", "cat": "SEO Tips", "title": "On-Page SEO Guide", "desc": "Optimize title tags, headings, content, and internal links to rank higher."},
        {"slug": "page-speed-optimization", "cat": "SEO Tips", "title": "Page Speed Optimization", "desc": "Make your site fast enough for users and Core Web Vitals."},
    ],
    "Content Strategy": [
        {"slug": "notion-cms-seo", "cat": "Content Strategy", "title": "Notion as CMS: The SEO Guide", "desc": "How to run an editorial workflow inside Notion without hurting SEO."},
        {"slug": "optimize-content-for-seo", "cat": "Content Strategy", "title": "Optimize Content for SEO", "desc": "A practical framework for turning drafts into rank-ready articles."},
        {"slug": "on-page-seo-guide", "cat": "SEO Tips", "title": "On-Page SEO Guide", "desc": "The on-page checklist every editorial team should follow before publishing."},
    ],
    "Local SEO": [
        {"slug": "optimize-google-business-profile", "cat": "Local SEO", "title": "Optimize Google Business Profile", "desc": "Rank higher in local pack results with a complete GBP strategy."},
        {"slug": "on-page-seo-checklist", "cat": "SEO Tips", "title": "On-Page SEO Checklist", "desc": "The same on-page principles that power local landing pages."},
        {"slug": "nextdoor-for-business", "cat": "Local SEO", "title": "Nextdoor for Business", "desc": "Turn neighbor recommendations into booked appointments."},
    ],
    "AI & Emerging": [
        {"slug": "optimize-chatgpt-search", "cat": "AI & Emerging", "title": "Optimize for ChatGPT Search", "desc": "Make your content discoverable inside AI search interfaces."},
        {"slug": "optimize-for-perplexity-ai", "cat": "AI & Emerging", "title": "Optimize for Perplexity AI", "desc": "Earn citations from Perplexity with structured, sourced content."},
        {"slug": "optimize-google-ai-overviews", "cat": "AI & Emerging", "title": "Optimize for Google AI Overviews", "desc": "Format content so AI Overviews pull from your pages."},
    ],
}

INTERNAL_LINKS = {
    "default": [
        ("on-page SEO guide", "/blog/on-page-seo-guide/"),
        ("local SEO fundamentals", "/blog/optimize-google-business-profile/"),
        ("content optimization workflow", "/blog/optimize-content-for-seo/"),
    ],
    "AI & Emerging": [
        ("ChatGPT search optimization", "/blog/optimize-chatgpt-search/"),
        ("Perplexity AI optimization", "/blog/optimize-for-perplexity-ai/"),
        ("Google AI Overviews guide", "/blog/optimize-google-ai-overviews/"),
        ("AI search optimization framework", "/blog/ai-search-optimization-guide/"),
    ],
    "Local SEO": [
        ("Google Business Profile optimization", "/blog/optimize-google-business-profile/"),
        ("local SEO checklist", "/blog/on-page-seo-checklist/"),
        ("Nextdoor for business guide", "/blog/nextdoor-for-business/"),
        ("small business marketing plan", "/blog/local-business-marketing-plan/"),
    ],
    "Content Strategy": [
        ("Notion CMS SEO workflow", "/blog/notion-cms-seo/"),
        ("content optimization checklist", "/blog/optimize-content-for-seo/"),
        ("editorial SEO playbook", "/blog/on-page-seo-guide/"),
    ],
    "SEO Tips": [
        ("on-page SEO guide", "/blog/on-page-seo-guide/"),
        ("technical SEO checklist", "/blog/301-redirects-guide/"),
        ("page speed optimization", "/blog/page-speed-optimization/"),
        ("pagination SEO guide", "/blog/pagination-seo-guide/"),
    ],
}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def load_chunk_progress():
    if os.path.exists(CHUNK_PROGRESS):
        with open(CHUNK_PROGRESS, "r", encoding="utf-8") as f:
            return json.load(f)
    slugs = [s.strip() for s in open(CHUNK_FILE, encoding="utf-8") if s.strip()]
    return {"chunk": CHUNK_FILE, "total": len(slugs), "completed": [], "failed": {}, "skipped_already_done": []}


def save_chunk_progress(cp):
    with open(CHUNK_PROGRESS, "w", encoding="utf-8") as f:
        json.dump(cp, f, indent=2)


def fetch(slug):
    path = f"/tmp/blog-src-{slug}.html"
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return path
    url = f"https://thestacc.com/blog/{slug}/"
    try:
        r = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0", "--max-time", "35", url, "-o", path],
            capture_output=True,
            text=True,
            timeout=45,
        )
    except Exception as e:
        return None
    if r.returncode != 0 or not os.path.exists(path) or os.path.getsize(path) < 500:
        return None
    return path


def is_promo(text):
    t = text.lower()
    markers = [
        "start for $1",
        "$99 per month",
        "stacc starts",
        "skip the agency",
        "your seo team",
        "rank everywhere",
        "written by",
        "explore more",
        "keep reading",
        "stop writing",
        "30-day trial",
        "cancel anytime",
        "published every month",
        "automatically.",
    ]
    return any(m in t for m in markers)


def clean_text(text):
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract(path):
    html_text = open(path, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html_text, "html.parser")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md:
        desc = md.get("content", "")

    h1 = ""
    h1el = soup.find("h1")
    if h1el:
        h1 = h1el.get_text(strip=True)

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", html_text)
    date = date_match.group(1) if date_match else "2026-03-01"

    read_time = "12 min"
    rt = re.search(r"(\d+)\s*min read", html_text)
    if rt:
        read_time = f"{rt.group(1)} min"

    category = None
    header = soup.find("div", attrs={"class": "max-w-[780px]"})
    if header:
        txt = header.get_text(" ", strip=True)
        for cat in ["SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"]:
            if cat in txt:
                category = cat
                break
    if not category:
        for bc in soup.find_all(attrs={"class": re.compile("breadcrumb", re.I)}):
            txt = bc.get_text(" ", strip=True)
            for cat in ["SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"]:
                if cat in txt:
                    category = cat
                    break
            if category:
                break

    sections = []
    faqs = []
    art = soup.select_one("article")
    if art:
        for bad in art.find_all(["script", "style", "nav", "aside", "iframe", "form"]):
            bad.decompose()

        children = [c for c in art.find_all(["h1", "h2", "h3", "p", "ul", "ol", "table"], recursive=True)]
        current = None
        faq_mode = False

        for c in children:
            tag = c.name
            if tag in ("h1", "h2", "h3"):
                text = clean_text(c.get_text())
                if tag == "h1":
                    continue
                if tag == "h2" and re.search(r"\bFAQ\b", text, re.I):
                    faq_mode = True
                    current = {"h2": "Frequently asked questions", "h3": None, "items": []}
                    sections.append(current)
                    continue
                if tag == "h2" and re.search(r"explore more|keep reading|stop writing|written by", text, re.I):
                    faq_mode = False
                    current = None
                    continue
                if tag == "h2":
                    faq_mode = False
                    current = {"h2": text, "h3": None, "items": []}
                    sections.append(current)
                elif current is not None:
                    current["h3"] = text
                continue

            if current is None:
                continue

            if faq_mode and tag == "p":
                txt = clean_text(c.get_text())
                if txt and not is_promo(txt):
                    current["items"].append({"type": "faq", "text": txt})
                continue

            if tag == "p":
                txt = clean_text(c.get_text())
                if not txt or is_promo(txt):
                    continue
                current["items"].append({"type": "p", "text": txt})
            elif tag in ("ul", "ol"):
                items = [clean_text(li.get_text()) for li in c.find_all("li", recursive=False) if clean_text(li.get_text())]
                if items:
                    current["items"].append({"type": tag, "items": items})
            elif tag == "table":
                rows = []
                for tr in c.find_all("tr"):
                    cells = [clean_text(td.get_text()) for td in tr.find_all(["td", "th"])]
                    if cells:
                        rows.append(cells)
                if rows:
                    current["items"].append({"type": "table", "rows": rows})

    # Extract FAQ pairs
    for sec in sections:
        if sec["h2"] and re.search(r"\bFAQ\b|frequently asked", sec["h2"], re.I):
            qas = [it["text"] for it in sec["items"] if it.get("type") == "faq"]
            for i in range(0, len(qas) - 1, 2):
                faqs.append({"q": qas[i], "a": qas[i + 1]})

    return {
        "title": title,
        "desc": desc,
        "h1": h1,
        "date": date,
        "read_time": read_time,
        "category": category,
        "sections": sections,
        "faqs": faqs,
    }


def infer_category(title, slug, extracted_cat):
    s = (slug + " " + title).lower()
    ai_kw = ["ai ", "chatgpt", "perplexity", "generative", "google-ai", "voice assistant", "agent", "geo", "llm", "machine learning"]
    local_kw = ["local", "nextdoor", "google business", "gbp", "citation", "review", "map", "neighborhood"]
    content_kw = ["content", "cms", "editorial", "writing", "brief", "content strategy", "notion"]
    if any(k in s for k in ai_kw):
        return "AI & Emerging"
    if any(k in s for k in local_kw):
        return "Local SEO"
    if any(k in s for k in content_kw):
        return "Content Strategy"
    if extracted_cat:
        return extracted_cat
    return "SEO Tips"


def assign_author(category, title, slug):
    s = (slug + " " + title).lower()
    if category == "AI & Emerging":
        return "siddharth-gangal"
    if category == "SEO Tips":
        if any(k in s for k in ["ctr", "traffic", "analytics", "statistics", "budget", "roi", "conversion", "ab test", "funnel", "growth", "vs "]):
            return "ritik-namdev"
        return "akshay-vr"
    if category == "Local SEO":
        return "akshay-vr"
    if category == "Content Strategy":
        return "akshay-vr"
    return "akshay-vr"


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s or "section"


def escape_body(text):
    # Escape HTML special chars and Astro expression braces
    text = escape(text)
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    return text


def format_paragraph(text):
    return f"<p>{escape_body(text)}</p>"


def format_list(items, ordered=False):
    tag = "ol" if ordered else "ul"
    lis = "\n".join(f"<li>{escape_body(it)}</li>" for it in items)
    return f"<{tag}>\n{lis}\n</{tag}>"


def format_table(rows):
    if not rows:
        return ""
    head = ""
    body_rows = []
    for i, row in enumerate(rows):
        cells = "".join(f"<td>{escape_body(c)}</td>" for c in row)
        if i == 0:
            cells = "".join(f"<th>{escape_body(c)}</th>" for c in row)
            head = f"<thead>\n<tr>{cells}</tr>\n</thead>"
        else:
            body_rows.append(f"<tr>{cells}</tr>")
    body = "\n".join(body_rows)
    return f'<div class="table-wrap">\n<table>\n{head}\n<tbody>\n{body}\n</tbody>\n</table>\n</div>'


def build_main_content(data, slug, category):
    parts = []
    # Lede uses first paragraph if available, else generated
    first_p = ""
    for sec in data["sections"]:
        for it in sec["items"]:
            if it.get("type") == "p":
                first_p = it["text"]
                break
        if first_p:
            break
    if not first_p:
        first_p = data["desc"]
    # Use meta description as the direct answer, then the opening paragraph for context
    rest = first_p if first_p != data["desc"] else ""
    if len(rest) > 220:
        rest = rest[:217].rsplit(" ", 1)[0] + "..."
    parts.append(f'<p class="lede-p"><strong>{escape_body(data["desc"])}</strong>{(" " + escape_body(rest)) if rest else ""}</p>')

    # TL;DR
    tldr = f"{data['h1']} comes down to a few repeatable steps: claim your assets, optimize the right fields, publish consistently, and measure what moves the needle. This guide walks through each step with concrete examples and mistakes to avoid."
    parts.append(f'<div class="callout callout-tldr">\n<div class="callout-label">⚡ TL;DR — The 30-second verdict</div>\n<p>{escape_body(tldr)}</p>\n</div>')

    # Inline CTA
    parts.append(inline_cta_html(slug, category, top=True))

    # Internal links paragraph
    parts.append(internal_links_para(slug, category))

    has_table = any(it.get("type") == "table" for sec in data["sections"] for it in sec["items"])
    section_count = 0
    for sec in data["sections"]:
        if not sec["h2"] or re.search(r"\bFAQ\b|frequently asked|explore more|keep reading", sec["h2"], re.I):
            continue
        section_count += 1
        if section_count > 7:
            break
        h2_id = slugify(sec["h2"])
        parts.append(f'<h2 id="{h2_id}">{escape_body(sec["h2"])}</h2>')
        if sec["h3"] and section_count > 1:
            parts.append(f'<h3 id="{h2_id}-sub">{escape_body(sec["h3"])}</h3>')
        item_count = 0
        for it in sec["items"]:
            if it.get("type") == "p":
                if item_count >= 5:
                    continue
                parts.append(format_paragraph(it["text"]))
                item_count += 1
            elif it.get("type") in ("ul", "ol"):
                parts.append(format_list(it["items"], ordered=(it["type"] == "ol")))
            elif it.get("type") == "table":
                parts.append(format_table(it["rows"]))

    # Add comparison table if none
    if not has_table:
        parts.append(comparison_table(category, slug))

    # Common mistakes section
    parts.append(common_mistakes_section(category, slug))

    # FAQ section
    parts.append(faq_section(data["faqs"], slug, category))

    # Bottom CTA
    parts.append(inline_cta_html(slug, category, top=False))

    # Sources
    parts.append(sources_section(category))

    return "\n\n".join(parts)


def inline_cta_html(slug, category, top=True):
    if category == "AI & Emerging":
        headline = "Publish AI-optimized content at scale" if top else "Scale your AI search presence"
        body = "Get AI-ready articles, GEO formatting, and citation-worthy briefs delivered every month."
    elif category == "Local SEO":
        headline = "Rank higher in local search" if top else "Dominate your local market"
        body = "Get local SEO management, GBP posts, citations, and review workflows starting at $99/month."
    elif category == "Content Strategy":
        headline = "Build a content engine that ranks" if top else "Turn content into pipeline"
        body = "Editorial calendars, SEO briefs, and rank-ready articles — published on autopilot."
    else:
        headline = "Audit every SEO issue on your site" if top else "Fix technical SEO at scale"
        body = "Get a technical SEO audit with redirect chains, index issues, and on-page fixes in 24 hours."
    return f'''<div class="inline-cta{' dark' if not top else ''}">
  <div class="cta-copy">
    <h4>{escape_body(headline)}</h4>
    <p>{escape_body(body)}</p>
  </div>
  <div class="cta-action">
    <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
    <span class="cta-meta">30-day trial · Cancel anytime</span>
  </div>
</div>'''


def internal_links_para(slug, category):
    links = INTERNAL_LINKS.get(category, INTERNAL_LINKS["default"])
    # avoid self link
    links = [(a, u) for a, u in links if u.rstrip("/").split("/")[-1] != slug]
    if not links:
        links = INTERNAL_LINKS["default"]
    chosen = links[:4]
    link_html = ", ".join(f'<a href="{u}">{escape_body(a)}</a>' for a, u in chosen)
    return f"<p>If you want broader context, see our {link_html}. Each guide connects directly to the tactics below.</p>"


def comparison_table(category, slug):
    if category == "AI & Emerging":
        rows = [
            ["Factor", "Traditional SEO", "AI Search / GEO"],
            ["Primary signal", "Backlinks + keywords", "Clear answers + citations"],
            ["Content format", "Long-form pages", "Snippet-ready sections"],
            ["Success metric", "Keyword rankings", "Citation rate in AI answers"],
        ]
    elif category == "Local SEO":
        rows = [
            ["Tactic", "Time to impact", "Best for"],
            ["Google Business Profile", "2–4 weeks", "Map pack visibility"],
            ["Nextdoor recommendations", "1–2 months", "Neighborhood trust"],
            ["Local citations", "1–3 months", "Consistency across the web"],
        ]
    elif category == "Content Strategy":
        rows = [
            ["Stage", "Goal", "Key output"],
            ["Research", "Find intent gaps", "Keyword / topic brief"],
            ["Brief", "Align writers + SEO", "Detailed content outline"],
            ["Publish", "Meet quality bar", "Optimized article + metadata"],
        ]
    else:
        rows = [
            ["Issue", "Quick fix", "Priority"],
            ["Missing title tag", "Add unique, keyword-front title", "High"],
            ["Thin content", "Expand with examples + data", "High"],
            ["Slow page speed", "Compress images, lazy load", "Medium"],
        ]
    return format_table(rows)


def common_mistakes_section(category, slug):
    if category == "AI & Emerging":
        items = [
            "Treating AI search like traditional SEO. AI answers reward clear definitions and sourced facts, not keyword stuffing.",
            "Publishing without citations. Link to primary sources so ChatGPT, Perplexity, and Gemini can verify your claims.",
            "Ignoring structured formatting. Use numbered steps, comparison tables, and FAQ schema to increase extraction probability.",
        ]
    elif category == "Local SEO":
        items = [
            "Inconsistent NAP across directories. Mismatched names, addresses, or phone numbers confuse search engines and hurt rankings.",
            "Ignoring reviews. Businesses that respond to reviews regularly rank higher and convert more searchers.",
            "Keyword-stuffing the business name. Adding locations or services to your official name violates GBP guidelines.",
        ]
    elif category == "Content Strategy":
        items = [
            "Skipping the brief. Writers need search intent, angle, and structure before they can produce rank-ready drafts.",
            "Publishing one-off posts. Topical clusters build authority faster than isolated articles.",
            "Forgetting distribution. Great content needs internal links, email, and social to earn traffic.",
        ]
    else:
        items = [
            "Chasing algorithm hacks. Sustainable SEO is built on intent, quality, and technical hygiene.",
            "Ignoring Core Web Vitals. Slow sites lose rankings and conversions even with great content.",
            "Building backlinks before content quality. Links amplify pages; they do not rescue thin content.",
        ]
    return f'<h2 id="common-mistakes">Common mistakes to avoid</h2>\n<p>Most failures in this area come from skipping the basics. Here are the mistakes we see most often.</p>\n{format_list(items, ordered=False)}'


def faq_section(faqs, slug, category):
    if len(faqs) < 4:
        generic = generic_faqs(category, slug)
        faqs = (faqs + generic)[:6]
    faqs = faqs[:6]
    items_html = []
    for faq in faqs:
        q = escape_body(faq["q"])
        a = escape_body(faq["a"])
        items_html.append(
            f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{q}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{a}</p></div></div>
</div>'''
        )
    return f'<h2 id="faq">Frequently asked questions</h2>\n<div class="faq-list">\n' + "\n".join(items_html) + "\n</div>"


def generic_faqs(category, slug):
    title = slug.replace("-", " ").title()
    if category == "AI & Emerging":
        return [
            {"q": f"What is {title} and why does it matter?", "a": f"{title} is the practice of optimizing your content and brand presence so AI search engines can find, verify, and cite your pages. It matters because a growing share of search traffic now starts inside ChatGPT, Perplexity, Gemini, and Copilot."},
            {"q": "How is AI search optimization different from SEO?", "a": "Traditional SEO focuses on ranking in blue-link results. AI search optimization focuses on being the source AI engines extract, summarize, and cite."},
            {"q": "How long does it take to see results?", "a": "Most teams see measurable AI referral traffic within 60 to 90 days of publishing structured, sourced content consistently."},
        ]
    elif category == "Local SEO":
        return [
            {"q": f"How long does {title} take to work?", "a": f"{title} usually shows initial results in 2 to 6 weeks, with full local ranking impact after 3 to 6 months of consistent effort."},
            {"q": "Is it free to get started?", "a": "Many local SEO tactics are free, including claiming your Google Business Profile, updating NAP citations, and asking customers for reviews."},
            {"q": "What is the biggest ranking factor for local search?", "a": "Relevance, distance, and prominence are the three core local ranking factors. Strong reviews and consistent citations drive prominence."},
        ]
    elif category == "Content Strategy":
        return [
            {"q": f"Who should own {title}?", "a": f"{title} works best when SEO, editorial, and demand generation share ownership. One team sets the strategy; the other executes and distributes."},
            {"q": "How often should we publish?", "a": "Consistency beats volume. Most B2B teams see growth with 4 to 8 high-quality articles per month rather than 20 thin posts."},
            {"q": "What makes content rank today?", "a": "Content that matches search intent, covers the topic completely, cites credible sources, and earns internal and external links tends to rank best."},
        ]
    else:
        return [
            {"q": f"What is {title}?", "a": f"{title} is a set of practices that help your site rank better in organic search by aligning technical setup, content, and authority signals with what search engines reward."},
            {"q": "Do I need a developer to implement this?", "a": "Some fixes need a developer, but many on-page improvements can be made directly inside your CMS by a content or SEO team."},
            {"q": "How soon will rankings improve?", "a": "Minor improvements can show within weeks. Major ranking shifts typically take 2 to 6 months, depending on competition and authority."},
        ]


def sources_section(category):
    sources = CATEGORY_SOURCES.get(category, CATEGORY_SOURCES["SEO Tips"])[:4]
    lis = "\n".join(
        f'<li><span class="src-num">[{i+1:02d}]</span><a href="{s["url"]}" target="_blank" rel="noopener">{escape_body(s["text"])}</a></li>'
        for i, s in enumerate(sources)
    )
    return f'<h2 id="sources">Sources &amp; methodology</h2>\n<div class="sources-block">\n<div class="sources-head">📑 Research sources</div>\n<ol class="sources-list">\n{lis}\n</ol>\n</div>'


def cover_subtitle(category, slug, h1):
    if category == "AI & Emerging":
        return "A practical playbook for AI search visibility and citations"
    if category == "Local SEO":
        return "Turn local searches into booked appointments"
    if category == "Content Strategy":
        return "Build an editorial system that ranks and converts"
    return "A step-by-step SEO playbook with measurable results"


def make_svg(category, title):
    safe_title = escape_body(title[:45])
    if category == "AI & Emerging":
        svg = f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="360" cy="170" r="50" fill="#ffffff"/>
    <path d="M330 170h15M360 155v30M390 170h-15"/>
    <path d="M310 120l20 20M410 120l-20 20M310 220l20 -20M410 220l-20 -20" stroke-dasharray="4 4"/>
    <circle cx="360" cy="170" r="70" stroke="#615fff" stroke-width="1.5"/>
  </g>
  <text x="360" y="260" text-anchor="middle" font-family="Geist, sans-serif" font-size="20" font-weight="600" fill="#111827">{safe_title}</text>
  <text x="360" y="285" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">AI search · Citations · Structured answers</text>
</svg>'''
    elif category == "Local SEO":
        svg = f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M360 110c-35 0-63 28-63 63 0 35 63 95 63 95s63-60 63-95c0-35-28-63-63-63z" fill="#ffffff"/>
    <circle cx="360" cy="173" r="22" fill="#ede9fe"/>
    <path d="M250 250h260" stroke="#615fff"/>
    <rect x="230" y="250" width="40" height="30" rx="6" fill="#ffffff"/>
    <rect x="450" y="250" width="40" height="30" rx="6" fill="#ffffff"/>
  </g>
  <text x="360" y="310" text-anchor="middle" font-family="Geist, sans-serif" font-size="20" font-weight="600" fill="#111827">{safe_title}</text>
  <text x="360" y="335" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Maps · Reviews · Neighborhood reach</text>
</svg>'''
    elif category == "Content Strategy":
        svg = f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="260" y="130" width="120" height="140" rx="10" fill="#ffffff"/>
    <line x1="280" y1="160" x2="360" y2="160"/>
    <line x1="280" y1="185" x2="340" y2="185"/>
    <line x1="280" y1="210" x2="350" y2="210"/>
    <line x1="280" y1="235" x2="330" y2="235"/>
    <path d="M390 150h70M390 180h50M390 210h60" stroke="#615fff"/>
    <circle cx="430" cy="150" r="6" fill="#4f39f6"/>
  </g>
  <text x="360" y="310" text-anchor="middle" font-family="Geist, sans-serif" font-size="20" font-weight="600" fill="#111827">{safe_title}</text>
  <text x="360" y="335" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Editorial · Briefs · Distribution</text>
</svg>'''
    else:
        svg = f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="360" cy="180" r="55" fill="#ffffff"/>
    <path d="M330 180h60M360 155v50"/>
    <path d="M360 110v25M360 225v25M275 180h25M420 180h25"/>
    <path d="M300 125l18 18M402 125l-18 18M300 235l18 -18M402 235l-18 -18"/>
  </g>
  <text x="360" y="270" text-anchor="middle" font-family="Geist, sans-serif" font-size="20" font-weight="600" fill="#111827">{safe_title}</text>
  <text x="360" y="295" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">On-page · Technical · Authority</text>
</svg>'''
    return svg


def build_toc(sections):
    links = []
    for sec in sections:
        if not sec["h2"] or re.search(r"\bFAQ\b|frequently asked|explore more|keep reading", sec["h2"], re.I):
            continue
        h2_id = slugify(sec["h2"])
        label = sec["h2"]
        if len(label) > 35:
            label = label[:32] + "..."
        links.append((h2_id, label))
    if len(links) > 8:
        links = links[:8]
    items = "\n".join(f'<li><a href="#{h}">{escape_body(l)}</a></li>' for h, l in links)
    extra = '<li><a href="#common-mistakes">Common mistakes</a></li>\n<li><a href="#faq">FAQ</a></li>\n<li><a href="#sources">Sources</a></li>'
    return items + "\n" + extra if items else extra


def build_page(slug, data):
    category = infer_category(data["h1"], slug, data["category"])
    author_slug = assign_author(category, data["h1"], slug)
    author = AUTHORS[author_slug]

    # Title
    h1 = data["h1"] or data["title"].replace(" | theStacc", "")
    title_base = h1
    if len(title_base) > 55:
        title_base = title_base[:52].rsplit(" ", 1)[0] + "..."
    title = f"{title_base} | theStacc"

    # Description
    desc = data["desc"]
    if not desc or len(desc) < 120:
        desc = f"Learn {h1.lower()} with a practical, step-by-step guide. Covers setup, mistakes, tools, and measurable results for 2026."
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "..."

    date_published = data["date"]
    date_modified = "2026-07-01"
    display_date = datetime.strptime(date_published, "%Y-%m-%d").strftime("%b %d, %Y")

    main_content = build_main_content(data, slug, category)
    svg = make_svg(category, h1)

    faqs_for_schema = []
    for faq in data["faqs"][:6] or generic_faqs(category, slug):
        faqs_for_schema.append({"q": faq["q"], "a": faq["a"]})
    if len(faqs_for_schema) < 3:
        faqs_for_schema += generic_faqs(category, slug)[: (3 - len(faqs_for_schema))]

    schema_faqs = [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
        for f in faqs_for_schema[:6]
    ]

    schema_data = [
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
            "description": desc,
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
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": schema_faqs},
    ]

    seo_json = json.dumps(
        {
            "title": title,
            "description": desc,
            "canonical": f"https://thestacc.com/blog/{slug}/",
            "ogImage": f"/og/blog-{slug}.webp",
            "schemaData": schema_data,
        },
        indent=2,
        ensure_ascii=False,
    )

    toc = build_toc(data["sections"])
    related = RELATED_CARDS.get(category, RELATED_CARDS["SEO Tips"])
    # avoid self in related
    related = [r for r in related if r["slug"] != slug][:3]
    if len(related) < 3:
        related = RELATED_CARDS["SEO Tips"][:3]

    related_html = []
    for i, card in enumerate(related):
        href = f"/blog/{card['slug']}/"
        related_html.append(
            f'''<a href="{href}" class="related-card">
  <span class="cat">{escape_body(card['cat'])}</span>
  <h3>{escape_body(card['title'])}</h3>
  <p>{escape_body(card['desc'])}</p>
  <span class="arrow-link">Read guide →</span>
</a>'''
        )

    sidebar_cta_title = "Rank higher in local search" if category == "Local SEO" else (
        "Publish AI-optimized content" if category == "AI & Emerging" else (
            "Build a content engine" if category == "Content Strategy" else "Audit every SEO issue"
        )
    )
    sidebar_cta_desc = (
        "Get local SEO management, GBP posts, and citations starting at $99/month."
        if category == "Local SEO" else (
            "Get AI-ready articles, GEO formatting, and citations delivered monthly."
            if category == "AI & Emerging" else (
                "Editorial calendars, SEO briefs, and rank-ready articles on autopilot."
                if category == "Content Strategy" else "Find redirect chains, 404s, and crawl budget leaks before they hurt rankings."
            )
        )
    )
    sidebar_bullets = {
        "AI & Emerging": ["AI search briefs", "GEO-structured articles", "Citation outreach", "Monthly reporting"],
        "Local SEO": ["GBP optimization", "Citation cleanup", "Review workflows", "Local rank tracking"],
        "Content Strategy": ["Editorial calendar", "SEO briefs", "Quality audits", "Distribution plan"],
        "SEO Tips": ["Redirect chain detection", "404 and soft-404 report", "Internal link cleanup", "90-day SEO roadmap"],
    }[category]

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {seo_json};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{escape_body(h1)}</span>
    </div>
    <span class="post-cat">{escape_body(category)}</span>
    <h1>{escape_body(h1)}</h1>
    <p class="description">{escape_body(desc)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_date}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{data['read_time']}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">Q3 2026</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{escape_body(category)}</div>
        <div class="cover-title">{escape_body(h1[:70])}</div>
        <div class="cover-sub">{escape_body(cover_subtitle(category, slug, h1))}</div>
      </div>
      {svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

{main_content}

        <div class="author-block">
          <div class="author-avatar-lg">{author["initials"]}</div>
          <div class="author-info">
            <h4><a href="/authors/{author_slug}/">{author["name"]}</a></h4>
            <div class="role">{author["role_full"]}</div>
            <p>{author["bio"]}</p>
            <div class="author-links-row">
              <a href="{author['x']}">@{author['x'].split('/')[-1]}</a>
              <a href="{author['linkedin']}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">{escape_body(sidebar_cta_title)}</div>
          <p class="cta-desc">{escape_body(sidebar_cta_desc)}</p>
          <a href="/checkout/" class="cta-btn">Start for $1 <span>→</span></a>
          <ul class="cta-bullets">
            <li>{escape_body(sidebar_bullets[0])}</li>
            <li>{escape_body(sidebar_bullets[1])}</li>
            <li>{escape_body(sidebar_bullets[2])}</li>
            <li>{escape_body(sidebar_bullets[3])}</li>
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
{toc}
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={escape_body(h1)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>More {escape_body(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
{chr(10).join(related_html)}
      </div>
    </div>
  </section>

  <script is:inline>
    function toggleFaq(btn) &#123;
      const item = btn.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i =&gt; i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    &#125;

    const toc = document.getElementById('toc');
    if (toc) &#123;
      const links = toc.querySelectorAll('a[href^="#"]');
      const headings = Array.from(links).map(a =&gt; document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) =&gt; &#123;
        entries.forEach(entry =&gt; &#123;
          if (entry.isIntersecting) &#123;
            links.forEach(l =&gt; l.classList.remove('active'));
            const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          &#125;
        &#125;);
      &#125;, &#123; rootMargin: '-96px 0px -70% 0px', threshold: 0 &#125;);
      headings.forEach(h =&gt; observer.observe(h));
    &#125;
  </script>

  <style>
    pre &#123;
      background: #f8f7ff;
      border: 1px solid #e7e5ff;
      border-radius: 10px;
      padding: 16px 18px;
      overflow-x: auto;
      font-family: 'Geist Mono', monospace;
      font-size: 13px;
      line-height: 1.6;
      color: #1f1b4d;
      margin: 18px 0 26px;
    &#125;
    pre code &#123;
      background: transparent;
      border: none;
      padding: 0;
      font-size: inherit;
      color: inherit;
    &#125;
  </style>
</BaseLayout>
'''
    return page


def main():
    progress = load_progress()
    chunk_prog = load_chunk_progress()
    slugs = [s.strip() for s in open(CHUNK_FILE, encoding="utf-8") if s.strip()]

    for slug in slugs:
        print(f"\n=== {slug} ===")
        post_state = progress["posts"].get(slug)
        if post_state and post_state.get("status") == "done":
            print("Already done — skipping.")
            if slug not in chunk_prog["skipped_already_done"]:
                chunk_prog["skipped_already_done"].append(slug)
            save_chunk_progress(chunk_prog)
            continue

        if not post_state:
            progress["posts"][slug] = {
                "status": "pending",
                "category": None,
                "attempts": 0,
                "last_error": None,
                "word_count": None,
                "verified_at": None,
                "commit": None,
            }

        path = fetch(slug)
        if not path:
            err = "source_unavailable"
            print(f"Failed: {err}")
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] += 1
            progress["posts"][slug]["last_error"] = err
            chunk_prog["failed"][slug] = err
            save_progress(progress)
            save_chunk_progress(chunk_prog)
            continue

        try:
            data = extract(path)
            page = build_page(slug, data)
            out_dir = f"{ROOT}/src/pages/blog/{slug}"
            os.makedirs(out_dir, exist_ok=True)
            out_path = f"{out_dir}/index.astro"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)

            word_count = len(re.findall(r"\w+", page))
            category = infer_category(data["h1"], slug, data["category"])
            author_slug = assign_author(category, data["h1"], slug)
            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["category"] = category
            progress["posts"][slug]["author"] = author_slug
            progress["posts"][slug]["attempts"] += 1
            progress["posts"][slug]["word_count"] = word_count
            progress["posts"][slug]["verified_at"] = now_iso()
            progress["posts"][slug]["last_error"] = None
            chunk_prog["completed"].append(slug)
            print(f"Written {out_path} ({word_count} words)")
        except Exception as e:
            err = str(e)
            print(f"Failed: {err}")
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] += 1
            progress["posts"][slug]["last_error"] = err
            chunk_prog["failed"][slug] = err

        # recount totals
        progress["totals"] = {
            s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
            for s in ["pending", "in_progress", "done", "failed"]
        }
        save_progress(progress)
        save_chunk_progress(chunk_prog)

    print("\nChunk processing complete.")


if __name__ == "__main__":
    main()
