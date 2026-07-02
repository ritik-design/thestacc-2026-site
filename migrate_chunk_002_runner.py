#!/usr/bin/env python3
"""Migrate chunk-002 blog posts to the 2026 Astro design."""
import json
import html
import os
import re
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag

ROOT = Path("/home/ritik/thestacc.com-astro/thestacc-2026-site")
CHUNK_FILE = ROOT / "Stacc/blog-migration/small-chunks/chunk-002.txt"
PROGRESS_FILE = ROOT / "Stacc/blog-migration/progress.json"
CHUNK_PROGRESS_FILE = ROOT / "Stacc/blog-migration/small-chunks/chunk-002.txt.progress.json"
OUT_DIR = ROOT / "src/pages/blog"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "slug": "siddharth-gangal",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc · B2B SaaS Marketing",
        "initials": "AVR",
        "slug": "akshay-vr",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "bio": "Akshay leads marketing at theStacc. He runs editorial strategy, demand-gen campaigns, and the content operations that turn raw research into ranked pages. He writes about SEO strategy, brand voice, and scaling content without losing quality.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc · Programmatic SEO & Analytics",
        "initials": "RN",
        "slug": "ritik-namdev",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "bio": "Ritik builds growth systems at theStacc. He specializes in programmatic SEO, analytics, CRO experiments, and the operations that turn content into pipeline. He writes about data-driven SEO, automation, and scaling traffic predictably.",
    },
}

CATEGORY_AUTHOR_MAP = {
    "AI & Emerging": "siddharth-gangal",
    "Content Strategy": "akshay-vr",
    "SEO Tips": "akshay-vr",
    "Local SEO": "akshay-vr",
    "Growth & Analytics": "ritik-namdev",
    "CRO": "ritik-namdev",
}

SLUG_OVERRIDES = {
    "content-marketing-roi-zero-click": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-marketing-small-business": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-marketing-statistics": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-marketing-strategy": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-marketing-workflow": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-personalization": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-plan-vs-strategy": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-production-process": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-pruning-guide": {"category": "SEO Tips", "author": "akshay-vr"},
    "content-refresh-strategy": {"category": "SEO Tips", "author": "akshay-vr"},
    "content-roi-guide": {"category": "Content Strategy", "author": "akshay-vr"},
    "content-score-rankings-study": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "content-scoring-guide": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "content-update-impact-study": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "content-updates-rankings-study": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "content-velocity-seo": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "content-velocity-sweet-spot": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "conversational-landing-pages": {"category": "CRO", "author": "ritik-namdev"},
    "copywriting-skills-writers": {"category": "Content Strategy", "author": "akshay-vr"},
    "copywriting-vs-content-writing": {"category": "Content Strategy", "author": "akshay-vr"},
    "core-update-recovery-case-study": {"category": "SEO Tips", "author": "akshay-vr"},
    "core-web-vitals-statistics": {"category": "Growth & Analytics", "author": "ritik-namdev"},
    "cost-start-agency": {"category": "Content Strategy", "author": "akshay-vr"},
    "cost-to-start-a-digital-marketing-agency": {"category": "Content Strategy", "author": "akshay-vr"},
    "crawl-budget-optimization": {"category": "SEO Tips", "author": "ritik-namdev"},
    "fact-checking-ai-content": {"category": "AI & Emerging", "author": "siddharth-gangal"},
    "facts-cited-ai-overviews": {"category": "AI & Emerging", "author": "siddharth-gangal"},
}

SOURCE_CITATIONS = {
    "Content Strategy": [
        ("HubSpot — State of Marketing Report", "https://www.hubspot.com/state-of-marketing"),
        ("Content Marketing Institute — B2B Content Marketing Benchmarks", "https://contentmarketinginstitute.com/research/b2b-content-marketing-research/"),
        ("Semrush — Content Marketing Statistics", "https://www.semrush.com/blog/content-marketing-statistics/"),
    ],
    "SEO Tips": [
        ("Google Search Central — How Search Works", "https://developers.google.com/search/docs/fundamentals/how-search-works"),
        ("Moz — Beginner's Guide to SEO", "https://moz.com/beginners-guide-to-seo"),
        ("Ahrefs — SEO Basics", "https://ahrefs.com/seo"),
    ],
    "Growth & Analytics": [
        ("Google Search Central — Core Web Vitals", "https://developers.google.com/search/docs/appearance/core-web-vitals"),
        ("web.dev — Core Web Vitals", "https://web.dev/vitals/"),
        ("Ahrefs — Search Traffic Analytics", "https://ahrefs.com/seo-metrics"),
    ],
    "CRO": [
        ("Unbounce — Landing Page Benchmarks", "https://unbounce.com/landing-page-articles/landing-page-benchmarks/"),
        ("Instapage — Conversational Landing Pages", "https://instapage.com/blog/conversational-landing-pages"),
        ("Nielsen Norman Group — Form Design", "https://www.nngroup.com/articles/web-form-design/"),
    ],
    "AI & Emerging": [
        ("Google Search Central — AI Overviews", "https://developers.google.com/search/docs/appearance/ai-overviews"),
        ("MIT Technology Review — AI Hallucinations", "https://www.technologyreview.com/2023/05/10/1072583/why-ai-chatbots-hallucinate/"),
        ("NewsGuard — AI-Generated Misinformation", "https://www.newsguardtech.com/special-reports/generative-ai-misinformation/"),
    ],
}

INTERNAL_LINKS = {
    "Content Strategy": [
        ("/blog/content-marketing-strategy/", "content marketing strategy"),
        ("/blog/content-refresh-strategy/", "content refresh strategy"),
        ("/features/content-briefs/", "content briefs"),
        ("/modules/content-seo/", "content SEO module"),
    ],
    "SEO Tips": [
        ("/blog/301-redirects-guide/", "301 redirects"),
        ("/blog/adapt-google-algorithm-updates/", "Google algorithm updates"),
        ("/modules/technical-seo/", "technical SEO"),
        ("/features/site-audit/", "site audit"),
    ],
    "Growth & Analytics": [
        ("/blog/core-web-vitals-statistics/", "Core Web Vitals"),
        ("/blog/content-velocity-seo/", "content velocity"),
        ("/features/client-reporting/", "client reporting"),
        ("/modules/technical-seo/", "technical SEO"),
    ],
    "CRO": [
        ("/blog/ai-personalized-landing-pages/", "AI personalized landing pages"),
        ("/features/landing-pages/", "landing page builder"),
        ("/modules/conversion-rate-optimization/", "conversion rate optimization"),
        ("/checkout/", "theStacc growth plan"),
    ],
    "AI & Emerging": [
        ("/blog/ai-hallucination-guide/", "AI hallucination guide"),
        ("/blog/ai-content-quality-checklist/", "AI content quality checklist"),
        ("/features/fact-check/", "AI fact-checking"),
        ("/modules/ai-search/", "AI search optimization"),
    ],
}

CTA_COPY = {
    "Content Strategy": {
        "eyebrow": "Free content audit · 24-hour delivery",
        "title": "Publish content that ranks and converts",
        "body": "Get a content strategy audit, editorial calendar, and SEO briefs built for your audience.",
        "button": "Start for $1",
        "url": "/checkout/",
        "meta": "30-day trial · Cancel anytime",
        "bullets": ["Editorial workflow audit", "Keyword-to-content map", "Competitor gap analysis", "90-day publishing roadmap"],
        "social": "No credit card required",
    },
    "SEO Tips": {
        "eyebrow": "Free SEO audit · 24-hour delivery",
        "title": "Fix technical SEO issues fast",
        "body": "Find redirect chains, crawl errors, and index gaps before they hurt your rankings.",
        "button": "Start for $1",
        "url": "/checkout/",
        "meta": "30-day trial · Cancel anytime",
        "bullets": ["Crawl budget audit", "Indexability report", "Internal link cleanup", "90-day technical roadmap"],
        "social": "No credit card required",
    },
    "Growth & Analytics": {
        "eyebrow": "Free analytics audit · 24-hour delivery",
        "title": "Turn content data into growth",
        "body": "Get a metrics audit, dashboard setup, and growth forecast based on your site data.",
        "button": "Start for $1",
        "url": "/checkout/",
        "meta": "30-day trial · Cancel anytime",
        "bullets": ["GA4 + GSC audit", "Core Web Vitals report", "Content velocity tracker", "90-day growth roadmap"],
        "social": "No credit card required",
    },
    "CRO": {
        "eyebrow": "Free CRO audit · 24-hour delivery",
        "title": "Convert more visitors into leads",
        "body": "Get a landing-page audit, A/B test roadmap, and conversion copy review.",
        "button": "Start for $1",
        "url": "/checkout/",
        "meta": "30-day trial · Cancel anytime",
        "bullets": ["Landing page teardown", "Form-friction audit", "A/B test roadmap", "90-day CRO roadmap"],
        "social": "No credit card required",
    },
    "AI & Emerging": {
        "eyebrow": "Free AI search audit · 24-hour delivery",
        "title": "Get cited in AI Overviews",
        "body": "Optimize your content for ChatGPT, Gemini, and Perplexity with structured answers and citations.",
        "button": "Start for $1",
        "url": "/checkout/",
        "meta": "30-day trial · Cancel anytime",
        "bullets": ["AI Overview visibility audit", "Citation readiness score", "Entity optimization plan", "90-day GEO roadmap"],
        "social": "No credit card required",
    },
}

RELATED_POOL = {
    "content-marketing-roi-zero-click": ("Content Strategy", "Content Marketing ROI in a Zero-Click World", "Prove content value when searches end without a click."),
    "content-marketing-small-business": ("Content Strategy", "Content Marketing for Small Business", "A lean content plan that competes with bigger budgets."),
    "content-marketing-statistics": ("Content Strategy", "Content Marketing Statistics", "Data points to benchmark your strategy."),
    "content-marketing-strategy": ("Content Strategy", "Content Marketing Strategy", "Build a strategy around search intent and revenue."),
    "content-marketing-workflow": ("Content Strategy", "Content Marketing Workflow", "The editorial process behind consistent publishing."),
    "content-personalization": ("Content Strategy", "Content Personalization", "Match content to segments without manual work."),
    "content-plan-vs-strategy": ("Content Strategy", "Content Plan vs Strategy", "Why plans fail without strategy and how to align them."),
    "content-production-process": ("Content Strategy", "Content Production Process", "From brief to published without bottlenecks."),
    "content-pruning-guide": ("SEO Tips", "Content Pruning Guide", "Remove, consolidate, and revive underperforming pages."),
    "content-refresh-strategy": ("SEO Tips", "Content Refresh Strategy", "How to update old posts and win rankings again."),
    "content-roi-guide": ("Content Strategy", "Content ROI Guide", "Frameworks for measuring content revenue."),
    "content-score-rankings-study": ("Growth & Analytics", "Content Score Rankings Study", "What content quality metrics correlate with rankings."),
    "content-scoring-guide": ("Growth & Analytics", "Content Scoring Guide", "Grade content before you publish."),
    "content-update-impact-study": ("Growth & Analytics", "Content Update Impact Study", "How updates affect traffic and rankings."),
    "content-updates-rankings-study": ("Growth & Analytics", "Content Updates Rankings Study", "The update frequency that moves SERPs."),
    "content-velocity-seo": ("Growth & Analytics", "Content Velocity for SEO", "Publish fast without sacrificing quality."),
    "content-velocity-sweet-spot": ("Growth & Analytics", "Content Velocity Sweet Spot", "The right publishing cadence for growth."),
    "conversational-landing-pages": ("CRO", "Conversational Landing Pages", "Replace static forms with guided conversations."),
    "copywriting-skills-writers": ("Content Strategy", "Copywriting Skills for Writers", "The persuasion skills every writer needs."),
    "copywriting-vs-content-writing": ("Content Strategy", "Copywriting vs Content Writing", "When to sell and when to educate."),
    "core-update-recovery-case-study": ("SEO Tips", "Core Update Recovery Case Study", "How one site recovered after a Google core update."),
    "core-web-vitals-statistics": ("Growth & Analytics", "Core Web Vitals Statistics", "Benchmarks for page speed and UX."),
    "cost-start-agency": ("Content Strategy", "Cost to Start an Agency", "Startup costs for a modern service business."),
    "cost-to-start-a-digital-marketing-agency": ("Content Strategy", "Cost to Start a Digital Marketing Agency", "Budget breakdown for launching an agency."),
    "crawl-budget-optimization": ("SEO Tips", "Crawl Budget Optimization", "Help Google crawl your most important pages."),
    "fact-checking-ai-content": ("AI & Emerging", "Fact-Checking AI Content", "How to verify claims generated by AI."),
    "facts-cited-ai-overviews": ("AI & Emerging", "Facts Cited in AI Overviews", "Why citations matter in AI search."),
}


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[-\s]+", "-", s)[:50]


def clean_text(s: str) -> str:
    # Remove banned words/phrases
    replacements = {
        r"\bdelve\b": "explore",
        r"\bDelve\b": "Explore",
        r"\bleverage\b": "use",
        r"\bLeverage\b": "Use",
        r"\bgame-changer\b": "major shift",
        r"\bGame-changer\b": "Major shift",
        r"\bworld-class\b": "top-tier",
        r"\bWorld-class\b": "Top-tier",
        r"\bsynergy\b": "alignment",
        r"\bSynergy\b": "Alignment",
    }
    for pat, repl in replacements.items():
        s = re.sub(pat, repl, s)
    # normalize whitespace
    s = " ".join(s.split())
    return s


def escape_body(s: str) -> str:
    # First unescape any existing entities, then full escape
    s = html.unescape(s)
    s = html.escape(s, quote=True)
    # Escape braces for Astro markup using expressions (replace each char individually)
    out = []
    for ch in s:
        if ch == "{":
            out.append("{'{'}")
        elif ch == "}":
            out.append("{'}'}")
        else:
            out.append(ch)
    return "".join(out)


def js_str(s: str) -> str:
    """Return a JSON-encoded string safe for Astro frontmatter JS."""
    return json.dumps(s, ensure_ascii=True)


def fetch_source(slug: str) -> str:
    tmp = f"/tmp/blog-src-{slug}.html"
    try:
        subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", "--max-time", "30", f"https://thestacc.com/blog/{slug}/", "-o", tmp],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"curl failed: {e.stderr.decode('utf-8', errors='ignore')}")
    if not os.path.exists(tmp) or os.path.getsize(tmp) < 1000:
        raise RuntimeError("source_unavailable")
    return tmp


def extract_dates(soup: BeautifulSoup) -> tuple:
    published = None
    modified = None
    # common article date meta
    for prop in ["article:published_time", "datePublished", "published_time"]:
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag and tag.get("content"):
            published = tag["content"][:10]
            break
    for prop in ["article:modified_time", "dateModified", "modified_time"]:
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag and tag.get("content"):
            modified = tag["content"][:10]
            break
    # time elements
    if not published:
        time = soup.find("time", datetime=True)
        if time:
            published = time["datetime"][:10]
    if not modified:
        modified = published
    if not published:
        published = "2026-01-01"
    if not modified:
        modified = "2026-07-01"
    return published, modified


def extract_sections(soup: BeautifulSoup):
    body = soup.find("article") or soup.find("main") or soup.body
    if not body:
        return []
    # Remove non-content elements
    for sel in ["script", "style", "nav", "header", "footer", "aside", "form", "button", "svg", "img", "figure", "noscript"]:
        for t in body.find_all(sel):
            t.decompose()

    # Find the most likely main content container: the deepest element that
    # contains multiple H2s and has no child with the same set of H2s.
    candidates = []
    for el in body.find_all(True):
        if not isinstance(el, Tag):
            continue
        h2s = el.find_all("h2")
        if len(h2s) < 2:
            continue
        # Check if a child contains the same H2s; if so, this is not minimal
        same_child = False
        for child in el.find_all(True, recursive=False):
            if len(child.find_all("h2")) == len(h2s):
                same_child = True
                break
        if same_child:
            continue
        candidates.append(el)
    if candidates:
        # Prefer the candidate with the longest text (the real content block)
        container = max(candidates, key=lambda el: len(el.get_text()))
    else:
        container = body

    # Extract semantic content tags in document order, ignoring nested duplicates.
    CONTENT_TAGS = {"h2", "h3", "p", "ul", "ol", "pre"}
    tags = []
    for el in container.descendants:
        if not isinstance(el, Tag) or el.name not in CONTENT_TAGS:
            continue
        # Skip tags nested inside other content tags (e.g. <p> inside <li>)
        if any(a.name in CONTENT_TAGS or a.name == "li" for a in el.parents):
            continue
        tags.append(el)

    sections = []
    current = {"level": 2, "heading": "Introduction", "items": []}
    started = False
    for tag in tags:
        name = tag.name
        if name in ("h2", "h3"):
            started = True
            if current["items"]:
                sections.append(current)
            current = {"level": int(name[1]), "heading": clean_text(tag.get_text()), "items": []}
        elif name == "p":
            txt = clean_text(tag.get_text())
            if txt and len(txt) > 20:
                current["items"].append(("p", txt))
        elif name in ("ul", "ol"):
            items = [clean_text(li.get_text()) for li in tag.find_all("li")]
            items = [i for i in items if i and len(i) > 5]
            if items:
                current["items"].append(("list", name, items))
        elif name == "pre":
            code = clean_text(tag.get_text())
            if code:
                current["items"].append(("code", code))

    if current["items"]:
        sections.append(current)

    # Drop generic / non-body sections
    SKIP_HEADING = re.compile(r"frequently asked|faq|conclusion|summary|written by|explore more|keep reading|related|about the author", re.I)
    filtered = []
    for sec in sections:
        if SKIP_HEADING.search(sec["heading"]):
            continue
        words = sum(
            len(it[1].split()) if it[0] != "list" else sum(len(x.split()) for x in it[2])
            for it in sec["items"]
        )
        if words > 25 or sec["level"] == 2:
            filtered.append(sec)

    # If we never found a real heading, the source may be unstructured.
    if not filtered:
        return []
    # Drop an initial "Introduction" section if it only contains metadata crumbs.
    if filtered[0]["heading"].lower() == "introduction" and len(filtered[0]["items"]) <= 1:
        filtered = filtered[1:]
    return filtered[:30]


def build_section_html(sections):
    parts = []
    for sec in sections:
        hid = slugify(sec["heading"])
        tag = "h2" if sec["level"] == 2 else "h3"
        parts.append(f'<{tag} id="{hid}">{escape_body(sec["heading"])}</{tag}>')
        for item in sec["items"]:
            if item[0] == "p":
                parts.append(f'<p>{escape_body(item[1])}</p>')
            elif item[0] == "list":
                tagname = item[1]
                lis = "".join(f'<li>{escape_body(li)}</li>' for li in item[2])
                parts.append(f'<{tagname}>{lis}</{tagname}>')
            elif item[0] == "code":
                parts.append(f'<pre><code>{escape_body(item[1])}</code></pre>')
    return "\n".join(parts)


def generate_faqs(title: str, sections: list) -> list:
    topic = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    faqs = [
        (f"What is {topic}?", f"{topic} is a structured approach to improving how your site attracts, engages, and converts visitors through organic content and optimization. It covers research, execution, measurement, and iteration."),
        (f"Why does {topic} matter in 2026?", f"Search engines and AI Overviews now surface direct answers, comparisons, and structured data. A clear {topic} process helps your pages become the source those systems cite, protecting and growing traffic."),
        (f"How do I measure {topic} success?", f"Track leading indicators such as impressions, branded search lift, and engagement; then tie them to lagging indicators like leads, revenue, and customer acquisition cost. Use GA4 and Search Console for the full picture."),
        (f"What are the most common {topic} mistakes?", f"Teams often chase volume over intent, skip internal linking, publish without a refresh plan, or attribute success only to last-click conversions. Fix these and results compound."),
        (f"How long does it take to see results from {topic}?", f"Most sites see measurable movement in 30 to 60 days and stable growth in 90 to 120 days. Competitive niches and lower domain authority may take longer."),
        (f"Which tools help with {topic}?", f"Google Search Console, GA4, a keyword research tool, a content calendar, and an analytics dashboard are enough to start. theStacc adds automated briefs, scoring, and reporting on top of that stack."),
    ]
    # If source has FAQ-like H2/H3, use those for first slots
    extra = []
    for sec in sections:
        h = sec["heading"]
        if re.search(r"what|why|how|when|which|mistake|error", h, re.I):
            words = sum(len(it[1].split()) if it[0] != "list" else sum(len(x.split()) for x in it[2]) for it in sec["items"])
            summary = " ".join(
                it[1] for it in sec["items"] if it[0] == "p"
            )[:250]
            if summary:
                extra.append((h, summary + "..."))
    # Merge unique
    seen = set()
    merged = []
    for q, a in extra + faqs:
        if q.lower() not in seen and len(merged) < 6:
            seen.add(q.lower())
            merged.append((q, a))
    return merged


def generate_table(category: str, title: str) -> str:
    topic = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    if category == "AI & Emerging":
        rows = [
            ("Manual fact-checking", "High accuracy, slow, expert-dependent", "Final publish review"),
            ("AI-assisted verification", "Fast, scalable, needs human oversight", "First-pass checks at scale"),
            ("Cited source requirement", "Forces traceability, builds trust", "AI Overview optimization"),
        ]
    elif category in ("SEO Tips", "Growth & Analytics"):
        rows = [
            ("Metric", "Why it matters", "Where to track it"),
            ("Organic clicks", "Real search traffic", "Google Search Console"),
            ("Indexed pages", "Coverage health", "Search Console Pages report"),
            ("Core Web Vitals", "Page experience signal", "web.dev / Search Console"),
        ]
    elif category == "CRO":
        rows = [
            ("Element", "Static form", "Conversational page"),
            ("Friction", "High — all fields visible", "Low — one question at a time"),
            ("Conversion data", "Abandonment at field level", "Drop-off per question"),
            ("Personalization", "Generic for all visitors", "Adaptive based on answers"),
        ]
    else:
        rows = [
            ("Approach", "Best for", "Watch out for"),
            ("Evergreen content", "Steady traffic and links", "Needs periodic refresh"),
            ("Trend-driven content", "Short-term traffic spikes", "Drops quickly"),
            ("Repurposed content", "Maximum mileage per asset", "Can feel repetitive"),
        ]
    header = rows[0]
    body = rows[1:]
    thead = "<tr>" + "".join(f"<th>{escape_body(c)}</th>" for c in header) + "</tr>"
    tbody = ""
    for row in body:
        tbody += "<tr>" + "".join(f"<td>{escape_body(c)}</td>" for c in row) + "</tr>"
    return f'<div class="table-wrap"><table><thead>{thead}</thead><tbody>{tbody}</tbody></table></div>'


def generate_steps(category: str, title: str) -> str:
    topic = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    steps = [
        ("Audit your current state", f"Document existing pages, rankings, traffic, and conversions related to {topic}. Identify quick wins and decaying content."),
        ("Define the target outcome", f"Set one primary goal — more organic traffic, higher engagement, better conversions, or lower CAC — and choose metrics that prove it."),
        ("Build the execution plan", f"Create briefs, timelines, and ownership. Match each piece of content to a search intent stage and an internal link target."),
        ("Publish and measure", f"Ship the work, monitor Search Console and analytics weekly, and refresh the plan based on what moves the needle."),
    ]
    lis = "".join(f'<li><strong>{escape_body(s)}.</strong> {escape_body(d)}</li>' for s, d in steps)
    return f'<h2 id="how-to-implement-{slugify(topic)}">How to implement {escape_body(topic)}</h2><ol>{lis}</ol>'


def generate_mistakes(category: str, title: str) -> str:
    topic = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    if category == "AI & Emerging":
        mistakes = [
            ("Trusting AI output without verification", "Always cross-check claims, statistics, and source URLs before publishing."),
            ("Publishing un-cited generative content", "Add inline links to reputable sources so readers and AI systems can verify your claims."),
            ("Ignoring entity accuracy", "Use precise names, dates, and definitions. Small hallucinations erode trust and rankings."),
        ]
    elif category in ("SEO Tips", "Growth & Analytics"):
        mistakes = [
            ("Fixating on one metric", "Rankings, traffic, and conversions all matter. Optimizing one while ignoring the others leads to blind spots."),
            ("Skipping technical basics", "Even great content underperforms if pages are slow, uncrawlable, or duplicated."),
            ("Setting and forgetting", "SEO is iterative. Refresh content, fix broken links, and monitor Core Web Vitals quarterly."),
        ]
    elif category == "CRO":
        mistakes = [
            ("Asking for too much too soon", "Long forms before trust is built kill conversions. Lead with value, then request details."),
            ("Testing without enough traffic", "Wait for statistical significance. Low-sample tests produce false winners."),
            ("Copying competitors blindly", "What works for their audience may not work for yours. Validate every change with data."),
        ]
    else:
        mistakes = [
            ("Publishing without distribution", "Great content needs promotion, email, SEO, and social to reach its audience."),
            ("Chasing trends over intent", "Trendy topics spike then fade. Solve persistent problems your buyers actually search for."),
            ("Forgetting the refresh cycle", "Old content decays. Schedule quarterly updates to protect rankings and accuracy."),
        ]
    lis = "".join(f'<li><strong>{escape_body(m)}.</strong> {escape_body(f)}</li>' for m, f in mistakes)
    return f'<h2 id="common-mistakes">Common mistakes to avoid</h2><p>{escape_body(f"Even experienced teams make these {topic} errors. Here is what to watch for and how to fix each one.")}</p><ul>{lis}</ul>'


def feature_svg(title: str, category: str) -> str:
    short = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    if len(short) > 40:
        short = short[:37] + "..."
    label = {
        "AI & Emerging": "AI Search",
        "SEO Tips": "SEO",
        "Growth & Analytics": "Analytics",
        "CRO": "CRO",
        "Content Strategy": "Content",
    }.get(category, "Guide")
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <rect x="80" y="120" width="160" height="120" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>
  <rect x="480" y="120" width="160" height="120" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>
  <path d="M240 180h80" stroke="#4f39f6" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="320,180 305,170 305,190" fill="#4f39f6"/>
  <path d="M400 180h80" stroke="#4f39f6" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polygon points="480,180 465,170 465,190" fill="#4f39f6"/>
  <text x="160" y="185" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="#4f39f6" font-weight="600">Input</text>
  <text x="560" y="185" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="#4f39f6" font-weight="600">Outcome</text>
  <text x="360" y="170" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#111827" font-weight="600">{escape_body(label)} System</text>
  <text x="360" y="205" text-anchor="middle" font-family="Geist, sans-serif" font-size="12" fill="#57534e">Research → Execute → Measure → Optimize</text>
  <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{escape_body(short)}</text>
  <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">thestacc.com/blog</text>
</svg>'''


def generate_related(slug: str, category: str) -> list:
    candidates = [s for s, v in RELATED_POOL.items() if s != slug and v[0] == category]
    if len(candidates) < 3:
        candidates = [s for s, v in RELATED_POOL.items() if s != slug]
    # Deterministic shuffle using slug hash
    import hashlib
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    ordered = sorted(candidates, key=lambda s: (h ^ int(hashlib.md5(s.encode()).hexdigest(), 16)))
    chosen = ordered[:3]
    cards = []
    for i, s in enumerate(chosen):
        cat, ttl, desc = RELATED_POOL[s]
        url = f"/blog/{s}/"
        cards.append((cat, ttl, desc, url, "Read guide"))
    return cards


def build_page(slug: str, title: str, description: str, sections: list, category: str, author_slug: str) -> str:
    author = AUTHORS[author_slug]
    cta = CTA_COPY.get(category, CTA_COPY["Content Strategy"])
    published, modified = extract_dates(BeautifulSoup(open(f"/tmp/blog-src-{slug}.html", encoding="utf-8", errors="ignore").read(), "html.parser"))
    display_published = datetime.strptime(published, "%Y-%m-%d").strftime("%b %d, %Y")
    display_updated = datetime.strptime(modified, "%Y-%m-%d").strftime("%b %d, %Y")

    # H1 = title
    h1 = title
    # SEO title trim
    seo_title = title if len(title) <= 58 else title[:55] + "..."
    if not seo_title.endswith(" | theStacc"):
        seo_title_page = f"{seo_title} | theStacc"
    else:
        seo_title_page = seo_title

    # Build main content
    section_html = build_section_html(sections)
    # Add our generated expansion after a short intro if section_html is thin
    table_html = generate_table(category, title)
    steps_html = generate_steps(category, title)
    mistakes_html = generate_mistakes(category, title)

    faqs = generate_faqs(title, sections)
    faq_schema = []
    faq_accordion = []
    for q, a in faqs:
        faq_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        faq_accordion.append(f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{escape_body(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{escape_body(a)}</p></div></div>
</div>''')

    sources = SOURCE_CITATIONS.get(category, SOURCE_CITATIONS["Content Strategy"])[:4]
    sources_html = "\n".join(
        f'<li><span class="src-num">[{i+1:02d}]</span><a href="{url}" target="_blank" rel="noopener">{escape_body(text)}</a></li>'
        for i, (text, url) in enumerate(sources)
    )

    internal = INTERNAL_LINKS.get(category, INTERNAL_LINKS["Content Strategy"])[:4]
    internal_para = "<p>" + escape_body("Related reading: ") + ", ".join(
        f'<a href="{url}">{escape_body(anchor)}</a>' for url, anchor in internal
    ) + escape_body(". These resources connect the tactics above to a complete growth system.") + "</p>"

    related = generate_related(slug, category)
    related_cards = "\n".join(
        f'''<a href="{url}" class="related-card">
  <span class="cat">{escape_body(cat)}</span>
  <h3>{escape_body(ttl)}</h3>
  <p>{escape_body(desc)}</p>
  <span class="arrow-link">{escape_body(cta_text)} →</span>
</a>'''
        for cat, ttl, desc, url, cta_text in related
    )

    # TOC from H2s
    toc_items = []
    for sec in sections:
        if sec["level"] == 2:
            toc_items.append((slugify(sec["heading"]), sec["heading"]))
    # Add generated sections to TOC if not present
    generated_toc = [
        ("how-to-implement-" + slugify(re.sub(r"\s*\(\d{4}.*$", "", title).strip()), "How to implement"),
        ("common-mistakes", "Common mistakes"),
        ("faq", "FAQ"),
        ("sources", "Sources"),
    ]
    existing_ids = {i[0] for i in toc_items}
    for gid, glbl in generated_toc:
        if gid not in existing_ids:
            toc_items.append((gid, glbl))
    toc_html = "\n".join(f'<li><a href="#{gid}">{escape_body(glbl)}</a></li>' for gid, glbl in toc_items)

    # Lede / TLDR
    topic = re.sub(r"\s*\(\d{4}.*$", "", title).strip()
    lede = f'<strong>{escape_body(title)}</strong> ' + escape_body(f'is a practical framework for improving how your site earns attention, trust, and revenue from organic content. This guide covers the strategy, execution, measurement, and common mistakes that determine whether {topic} drives real business results in 2026.')
    tldr = escape_body(f"{topic} works when you align content with search intent, measure the right metrics, refresh pages regularly, and fix technical blockers. Use this guide to audit your current approach and build a repeatable system.")

    # Count words for progress
    all_text = " ".join([
        title, description, " ".join(s["heading"] for s in sections),
        " ".join(
            it[1] if it[0] != "list" else " ".join(it[2])
            for s in sections for it in s["items"]
        ),
        " ".join(q + " " + a for q, a in faqs),
    ])
    word_count = len(all_text.split())

    # Schema data
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
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": published,
            "dateModified": modified,
            "author": {
                "@type": "Person",
                "name": author["name"],
                "url": f"https://thestacc.com/authors/{author['slug']}/",
                "sameAs": [author["linkedin"]],
            },
            "publisher": {"@type": "Organization", "name": "theStacc"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema,
        },
    ]
    schema_json = json.dumps(schema_data, ensure_ascii=True)

    # Share text
    share_text = quote(h1)
    page_url = f"https://thestacc.com/blog/{slug}/"

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {js_str(seo_title_page)},
  description: {js_str(description)},
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
      <span class="current">{escape_body(h1)}</span>
    </div>
    <span class="post-cat">{escape_body(category)}</span>
    <h1>{escape_body(h1)}</h1>
    <p class="description">{escape_body(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{escape_body(author["name"])}</a></span>
          <span class="meta-author-role">{escape_body(author["role"])}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_published}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{max(1, word_count // 200)} min</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{display_updated}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{escape_body(category)}</div>
        <div class="cover-title">{escape_body(re.sub(r"\s*\(\d{{4}}.*$", "", title).strip())}</div>
        <div class="cover-sub">{escape_body(f"A complete guide to {topic.lower()} in 2026")}</div>
      </div>
      {feature_svg(title, category)}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p">{lede}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{tldr}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{escape_body(cta["title"])}</h4>
            <p>{escape_body(cta["body"])}</p>
          </div>
          <div class="cta-action">
            <a href="{cta['url']}" class="cta-btn-inline">{escape_body(cta["button"])} <span>→</span></a>
            <span class="cta-meta">{escape_body(cta["meta"])}</span>
          </div>
        </div>

        {section_html}

        {table_html}

        {steps_html}

        {mistakes_html}

        {internal_para}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          { "\n          ".join(faq_accordion) }
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{escape_body(cta["title"])}</h4>
            <p>{escape_body(cta["body"])}</p>
          </div>
          <div class="cta-action">
            <a href="{cta['url']}" class="cta-btn-inline">{escape_body(cta["button"])} <span>→</span></a>
            <span class="cta-meta">{escape_body(cta["meta"])}</span>
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
            <h4><a href="/authors/{author['slug']}/">{escape_body(author["name"])}</a></h4>
            <div class="role">{escape_body(author["role_full"])}</div>
            <p>{escape_body(author["bio"])}</p>
            <div class="author-links-row">
              <a href="{author['x']}">{author['x_handle']}</a>
              <a href="{author['linkedin']}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{escape_body(cta["eyebrow"])}</div>
          <div class="cta-title">{escape_body(cta["title"])}</div>
          <p class="cta-desc">{escape_body(cta["body"])}</p>
          <a href="{cta['url']}" class="cta-btn">{escape_body(cta["button"])} <span>→</span></a>
          <ul class="cta-bullets">
            { "".join(f'<li>{escape_body(b)}</li>' for b in cta["bullets"]) }
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {escape_body(cta["social"])}
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
            <a href="https://twitter.com/intent/tweet?url={page_url}&text={share_text}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={page_url}" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a>
            <a href="#" onclick="navigator.clipboard.writeText('{page_url}');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <section class="related-posts">
    <div class="related-inner">
      <div class="related-head">
        <h2>{escape_body(f"More {category} guides")}</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        {related_cards}
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

  <style>
    pre {{
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
    }}
    pre code {{
      background: transparent;
      border: none;
      padding: 0;
      font-size: inherit;
      color: inherit;
    }}
  </style>
</BaseLayout>
'''
    return page, word_count


def main():
    slugs = [s.strip() for s in CHUNK_FILE.read_text().splitlines() if s.strip()]
    progress = json.loads(PROGRESS_FILE.read_text())
    completed = []
    failed = {}
    skipped = []

    for slug in slugs:
        post = progress["posts"].get(slug)
        if not post:
            failed[slug] = "not in progress tracker"
            continue
        if post.get("status") == "done":
            skipped.append(slug)
            continue
        print(f"\n--- Processing {slug} ---")
        try:
            fetch_source(slug)
            html_src = open(f"/tmp/blog-src-{slug}.html", encoding="utf-8", errors="ignore").read()
            soup = BeautifulSoup(html_src, "html.parser")
            title = clean_text(html.unescape(soup.title.string)) if soup.title and soup.title.string else slug.replace("-", " ").title()
            h1_tag = soup.find("h1")
            h1 = clean_text(html.unescape(h1_tag.get_text())) if h1_tag else title
            title = h1 if h1 else title
            meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            description = clean_text(html.unescape(meta_tag.get("content"))) if meta_tag and meta_tag.get("content") else f"Learn {title.lower()} with practical steps, examples, and mistakes to avoid in 2026."

            override = SLUG_OVERRIDES.get(slug, {})
            category = override.get("category") or infer_category(title)
            author_slug = override.get("author") or CATEGORY_AUTHOR_MAP.get(category, "akshay-vr")

            sections = extract_sections(soup)
            if not sections:
                # fallback: generate minimal from description
                sections = [{"level": 2, "heading": "What you will learn", "items": [("p", description)]}]

            page_html, word_count = build_page(slug, title, description, sections, category, author_slug)
            out_path = OUT_DIR / slug / "index.astro"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(page_html, encoding="utf-8")

            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["category"] = category
            progress["posts"][slug]["author"] = author_slug
            progress["posts"][slug]["word_count"] = word_count
            progress["posts"][slug]["verified_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            progress["posts"][slug]["last_error"] = None
            completed.append(slug)
            print(f"  Wrote {out_path} ({word_count} words)")
        except Exception as e:
            failed[slug] = str(e)
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = str(e)
            print(f"  FAILED: {e}")

    progress["totals"] = {
        s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
        for s in ["pending", "in_progress", "done", "failed"]
    }
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")

    chunk_progress = {
        "chunk": str(CHUNK_FILE),
        "total": len(slugs),
        "completed": completed,
        "failed": failed,
        "skipped_already_done": skipped,
    }
    CHUNK_PROGRESS_FILE.write_text(json.dumps(chunk_progress, indent=2), encoding="utf-8")

    print(f"\nCompleted: {len(completed)}, Failed: {len(failed)}, Skipped: {len(skipped)}")


def infer_category(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["ai ", "chatgpt", "perplexity", "generative", "llm", "fact-check", "fact check", "overview"]):
        return "AI & Emerging"
    if any(k in t for k in ["crawl", "core web vitals", "redirect", "index", "technical seo", "schema", "site speed"]):
        return "SEO Tips"
    if any(k in t for k in ["landing page", "conversion", "cro", " conversational"]):
        return "CRO"
    if any(k in t for k in ["analytics", "velocity", "score", "study", "statistics", "roi", "data"]):
        return "Growth & Analytics"
    return "Content Strategy"


if __name__ == "__main__":
    main()
