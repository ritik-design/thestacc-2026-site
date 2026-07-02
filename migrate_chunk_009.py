#!/usr/bin/env python3
"""Migrate small-chunks/chunk-009 to the 2026 blog design."""
import json, os, re, subprocess, textwrap, html
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-009.txt")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-009.txt.progress.json")
OUT_ROOT = os.path.join(ROOT, "src/pages/blog")
TMP_DIR = "/tmp"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role_short": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He writes about SEO, AI search, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role_short": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr_",
        "x_handle": "@akshayvr_",
        "bio": "Akshay leads marketing and editorial strategy at theStacc. He specializes in B2B SaaS demand generation, content operations, and on-page SEO.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role_short": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev_",
        "x_handle": "@ritiknamdev_",
        "bio": "Ritik runs growth, analytics, and programmatic SEO experiments at theStacc. He focuses on CRO, funnel ops, and turning data into repeatable traffic gains.",
    },
}

CATEGORY_KEYWORDS = [
    ("AI & Emerging", ["ai", "agent", "agents", "chatgpt", "gpt", "llm", "generative", "gemini", "perplexity", "claude", "copilot", "machine learning", "algorithm update", "geo", "generative-engine", "ai search", "ai-overview", "ai mode"]),
    ("Local SEO", ["local seo", "local business", "google business profile", "gbp", "map pack", "near me", "citation", "dentist", "lawyer", "contractor", "realtor", "salon", "florist", "electrician", "funeral", "gym", "hvac", "chiropractor", "accountant", "home service", "restaurant", "catering", "city service", "online presence"]),
    ("Content Strategy", ["content strategy", "content marketing", "editorial", "calendar", "blog post", "writing", "brief", "newsletter", "email marketing", "email automation", "subject line", "segmentation", "ugc", "evergreen", "format", "fact-check", "eeat", "e-e-a-t", "brand voice", "buyer persona", "content plan", "topical authority"]),
]

BANNED_WORDS = {
    "delve": "dig into",
    "leverage": "use",
    "game-changer": "breakthrough",
    "world-class": "top-tier",
    "synergy": "combined effect",
}

def classify_category(title, slug):
    text = (title + " " + slug.replace("-", " ")).lower()
    for cat, kws in CATEGORY_KEYWORDS:
        if any(kw in text for kw in kws):
            return cat
    return "SEO Tips"

def classify_author(title, slug, category):
    text = (title + " " + slug.replace("-", " ")).lower()
    sidd = ["ai", "agent", "chatgpt", "llm", "generative", "gemini", "perplexity", "claude", "algorithm", "technical", "architecture", "founder", "product strategy", "machine learning"]
    ritik = ["growth", "programmatic", "cro", "analytics", "ga4", "search console", "conversion", "funnel", "ab test", "a/b test", "roi", "statistics", "case study", "data", "tool comparison"]
    s = sum(1 for k in sidd if k in text)
    r = sum(1 for k in ritik if k in text)
    if category == "AI & Emerging":
        s += 2
    if category == "Local SEO":
        # usually SEO strategy; Akshay unless growth/data terms
        pass
    if s > r and s > 0:
        return "siddharth-gangal"
    if r > s and r > 0:
        return "ritik-namdev"
    return "akshay-vr"

def clean_text(s):
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def escape_braces(s):
    return s.replace("{", "&#123;").replace("}", "&#125;")

ALLOWED_TAGS = {"p", "ul", "ol", "li", "pre", "code", "table", "thead", "tbody", "tr", "th", "td", "strong", "em", "br", "span", "h3", "h4"}

def _clean_tag_attrs(tag):
    if tag.name not in ALLOWED_TAGS:
        return
    keep = {}
    if tag.name == "code" and tag.get("class"):
        cls = " ".join(tag.get("class"))
        if cls.startswith("language-"):
            keep["class"] = cls
    tag.attrs = keep

def clean_element(el):
    for tag in list(el.find_all(["script", "style", "img", "iframe", "svg", "button", "form", "input"])):
        tag.decompose()
    for tag in el.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
        else:
            _clean_tag_attrs(tag)
    _clean_tag_attrs(el)
    return el

def extract_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    tmp = os.path.join(TMP_DIR, f"blog-src-{slug}.html")
    try:
        subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-L", "--max-time", "25", url, "-o", tmp], check=True, timeout=30)
    except Exception as e:
        return None, f"curl failed: {e}"
    if not os.path.exists(tmp) or os.path.getsize(tmp) < 500:
        return None, "source empty or 404"
    html_text = open(tmp, encoding="utf-8", errors="ignore").read()
    if len(html_text) < 2000:
        return None, "source too short"
    return html_text, None

def parse_source(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    title_tag = soup.title.string if soup.title else ""
    h1_tag = soup.find("h1")
    h1 = clean_text(h1_tag.get_text()) if h1_tag else clean_text(title_tag)
    md = soup.find("meta", attrs={"name": "description"})
    description = md.get("content", "") if md else ""
    date = ""
    for pat in [r"(\d{4}-\d{2}-\d{2})", r"(\d{1,2}\s+[A-Za-z]{3},?\s+\d{4})"]:
        m = re.search(pat, html_text)
        if m:
            date = m.group(1)
            break
    if not date:
        date = "2026-03-29"
    category = ""
    for span in soup.find_all("span"):
        txt = clean_text(span.get_text())
        if txt in ("SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"):
            category = txt
            break
    if not category:
        category = classify_category(h1, "")
    sections = []
    article = soup.find("article")
    col = None
    if article:
        main = article.find("div", class_=lambda x: x and "max-w-[1320px]" in x and "py-10" in x)
        if main:
            col = main.find("div", class_=lambda x: x and "flex-1" in x)
    if not col:
        candidates = []
        for tag in [article, soup.find("main")]:
            if tag:
                for div in tag.find_all("div"):
                    candidates.append((len(div.get_text()), div))
        if candidates:
            col = max(candidates, key=lambda x: x[0])[1]
    faq_items = []
    if col:
        for h2 in col.find_all("h2"):
            txt = h2.get_text(strip=True).lower()
            if any(x in txt for x in ["explore more", "stop writing", "get your free", "check your inbox", "subscribe", "newsletter", "related posts", "you may also like"]):
                for sib in list(h2.find_all_next()):
                    sib.decompose()
                h2.decompose()
        headings = col.find_all(["h2", "h3"])
        for idx, h in enumerate(headings):
            if re.search(r"\bfaq\b", h.get_text(strip=True), re.I):
                faq_title = None
                faq_body = []
                for sib in h.find_next_siblings():
                    if sib.name == "h2":
                        break
                    if sib.name == "h3":
                        if faq_title and faq_body:
                            faq_items.append((clean_text(faq_title), clean_text(" ".join(faq_body))))
                        faq_title = sib.get_text(strip=True)
                        faq_body = []
                    elif sib.name in ("p", "ul", "ol"):
                        faq_body.append(sib.get_text(strip=True))
                if faq_title and faq_body:
                    faq_items.append((clean_text(faq_title), clean_text(" ".join(faq_body))))
                h.decompose()
                break
        headings = col.find_all(["h2", "h3"])
        for h in headings:
            level = int(h.name[1])
            title = clean_text(h.get_text())
            body_parts = []
            for sib in h.find_next_siblings():
                if sib.name in ("h2", "h3"):
                    break
                if sib.name:
                    clone = BeautifulSoup(str(sib), "html.parser").find()
                    if clone:
                        clean_element(clone)
                        body_parts.append(str(clone))
            body_html = "\n".join(body_parts)
            sections.append({"level": level, "title": title, "body": body_html})
    return {
        "title": clean_text(title_tag),
        "h1": h1,
        "description": clean_text(description),
        "category": category,
        "date": date,
        "sections": sections,
        "faq_items": faq_items,
    }

def optimize_title(h1, slug):
    t = clean_text(re.sub(r"\s+", " ", h1))
    if not t:
        t = slug.replace("-", " ").title()
    if "|" not in t:
        t = f"{t} | theStacc"
    if len(t) > 63:
        # trim but keep suffix
        prefix = t.replace(" | theStacc", "")
        prefix = prefix[:55].rsplit(" ", 1)[0]
        t = f"{prefix} | theStacc"
    return t

def optimize_description(desc, title, slug):
    d = clean_text(desc)
    if not d:
        d = f"Learn {slug.replace('-', ' ')} with actionable tactics, real examples, and a step-by-step framework for 2026."
    if len(d) > 160:
        d = d[:157].rsplit(" ", 1)[0] + "."
    if len(d) < 120:
        d = d + " This guide covers tools, mistakes to avoid, and a checklist you can use today."
    return d

def format_date_display(iso):
    try:
        dt = datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return iso

def read_time(words):
    mins = max(1, round(words / 220))
    return f"{mins} min"

def make_feature_svg(title, slug):
    color1 = "#4f39f6"
    color2 = "#818cf8"
    bg = "#f5f3ff"
    topic = title[:30]
    shapes = [
        f'<circle cx="580" cy="120" r="60" fill="{color2}" opacity="0.25"/>',
        f'<rect x="60" y="160" width="120" height="80" rx="12" fill="{color1}" opacity="0.15"/>',
        f'<path d="M40 220 L140 120 L240 220" stroke="{color1}" stroke-width="3" fill="none" opacity="0.4"/>',
    ]
    svg = f'''<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="width:100%;height:auto;border-radius:16px;">
  <rect width="720" height="320" fill="{bg}" rx="16"/>
  <text x="360" y="70" text-anchor="middle" font-family="Geist, sans-serif" font-size="14" fill="#57534e" letter-spacing="0.08em">{html.escape(topic.upper())}</text>
  <text x="360" y="130" text-anchor="middle" font-family="Geist, sans-serif" font-size="32" font-weight="700" fill="#111827">{html.escape(title[:40])}</text>
  <text x="360" y="175" text-anchor="middle" font-family="Geist, sans-serif" font-size="16" fill="#57534e">2026 Guide · Tactics · Examples</text>
  {''.join(shapes)}
  <rect x="280" y="240" width="160" height="44" rx="22" fill="{color1}"/>
  <text x="360" y="268" text-anchor="middle" font-family="Geist, sans-serif" font-size="14" font-weight="600" fill="#ffffff">Read the guide →</text>
</svg>'''
    return svg

def internal_links_for(category, slug):
    if category == "AI & Emerging":
        return [
            '<a href="/blog/generative-engine-optimization-guide/">Generative Engine Optimization guide</a>',
            '<a href="/blog/ai-overview-optimization/">AI Overview optimization</a>',
            '<a href="/blog/ai-content-strategy/">AI content strategy</a>',
            '<a href="/demo/">Book a demo</a>',
        ]
    elif category == "Local SEO":
        return [
            '<a href="/modules/local-seo/">Local SEO module</a>',
            '<a href="/blog/gbp-optimization-ai-mode/">Google Business Profile optimization</a>',
            '<a href="/blog/dominate-ai-local-pack/">Dominate the AI local pack</a>',
            '<a href="/checkout/">Start your $1 trial</a>',
        ]
    elif category == "Content Strategy":
        return [
            '<a href="/modules/content-seo/">Content SEO module</a>',
            '<a href="/blog/editorial-calendar-guide/">Editorial calendar guide</a>',
            '<a href="/blog/eeat-for-blogs/">E-E-A-T for blogs</a>',
            '<a href="/checkout/">Start your $1 trial</a>',
        ]
    else:
        return [
            '<a href="/blog/301-redirects-guide/">301 redirects guide</a>',
            '<a href="/blog/internal-linking-blog-posts/">Internal linking for SEO</a>',
            '<a href="/blog/create-xml-sitemap/">XML sitemap guide</a>',
            '<a href="/demo/">Book a free SEO audit</a>',
        ]

def external_sources_for(category, slug):
    if category == "AI & Emerging":
        return [
            ("https://blog.google/technology/ai/", "Google AI Blog — Latest AI search updates"),
            ("https://www.perplexity.ai/hub/blog", "Perplexity Blog — AI search and citations"),
            ("https://openai.com/blog/", "OpenAI Blog — Research and product updates"),
        ]
    if category == "Local SEO":
        return [
            ("https://support.google.com/business/answer/3038177", "Google Business Profile Help"),
            ("https://www.brightlocal.com/learn/local-seo/", "BrightLocal — Local SEO Learning Hub"),
            ("https://whitespark.ca/blog/", "Whitespark — Local Search Insights"),
        ]
    if category == "Content Strategy":
        return [
            ("https://blog.hubspot.com/marketing/content-strategy", "HubSpot — Content Strategy Guide"),
            ("https://contentmarketinginstitute.com/articles/", "Content Marketing Institute"),
            ("https://www.litmus.com/blog/", "Litmus — Email Marketing Blog"),
        ]
    return [
        ("https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Google Search Central — SEO Starter Guide"),
        ("https://moz.com/blog", "Moz Blog — SEO research and tactics"),
        ("https://ahrefs.com/blog/", "Ahrefs Blog — Link building and keyword research"),
    ]

def related_posts_for(category, slug):
    pools = {
        "AI & Emerging": [
            ("generative-engine-optimization-guide", "AI & Emerging", "Generative Engine Optimization Guide", "How to structure content so ChatGPT, Perplexity, and Gemini cite your brand."),
            ("ai-overview-optimization", "AI & Emerging", "AI Overview Optimization", "A practical playbook for showing up in Google’s AI Overviews."),
            ("ai-agents-content-planning", "AI & Emerging", "AI Agents for Content Planning", "How AI agents decide what content to create and how to steer them."),
            ("gemini-vs-chatgpt-search", "AI & Emerging", "Gemini vs ChatGPT Search", "What marketers need to know about the two biggest AI search engines."),
        ],
        "Local SEO": [
            ("gbp-optimization-ai-mode", "Local SEO", "Google Business Profile Optimization", "A complete GBP optimization checklist for the AI search era."),
            ("dominate-ai-local-pack", "Local SEO", "Dominate the AI Local Pack", "How local rankings work when AI engines answer map-style queries."),
            ("local-seo-guide", "Local SEO", "Local SEO Guide", "The fundamentals of ranking in local search and the map pack."),
            ("gbp-categories-guide", "Local SEO", "Google Business Categories Guide", "How to pick and optimize GBP categories for maximum visibility."),
        ],
        "Content Strategy": [
            ("editorial-calendar-guide", "Content Strategy", "Editorial Calendar Guide", "Plan, assign, and publish content without missing deadlines."),
            ("eeat-for-blogs", "Content Strategy", "E-E-A-T for Blogs", "Build experience, expertise, authority, and trust into every post."),
            ("format-blog-post", "Content Strategy", "How to Format a Blog Post", "A proven format that keeps readers and search engines happy."),
            ("ai-content-strategy", "AI & Emerging", "AI Content Strategy", "Scale content production without losing quality or brand voice."),
        ],
        "SEO Tips": [
            ("301-redirects-guide", "SEO Tips", "301 Redirects Guide", "Protect rankings during URL changes, migrations, and consolidations."),
            ("internal-linking-blog-posts", "SEO Tips", "Internal Linking for SEO", "How to structure internal links so authority flows to money pages."),
            ("create-xml-sitemap", "SEO Tips", "How to Create an XML Sitemap", "Make sure Google can discover and crawl every important page."),
            ("schema-markup-for-blog-posts", "SEO Tips", "Schema Markup for Blog Posts", "Add structured data that wins rich snippets and AI citations."),
        ],
    }
    pool = pools.get(category, pools["SEO Tips"])
    chosen = [c for c in pool if c[0] != slug][:3]
    if len(chosen) < 3:
        chosen.append(("glossary/", "Glossary", "SEO terms, explained", "Browse 690+ definitions of the concepts that shape search, content, and AI visibility."))
    return chosen[:3]

def generate_faq(h1, category, existing):
    if existing and len(existing) >= 3:
        return existing[:6]
    topic = h1.split(":")[0].split("(")[0].strip().rstrip("?")
    return [
        (f"What is {topic}?", f"{topic} is a set of practices that help websites attract, convert, and retain the right audience through search and content. In 2026, it blends traditional SEO, AI visibility, and conversion-focused execution."),
        (f"Why does {topic} matter now?", "Search engines and AI answer engines now reward depth, citations, and clear structure. Brands that organize their content around real intent gain traffic while competitors lose ground."),
        (f"How do I get started with {topic}?", "Start with an audit. Identify quick wins, fix technical blockers, align content with search intent, and measure results weekly using Google Search Console and analytics."),
        (f"What mistakes should I avoid?", "Avoid chasing vanity metrics, copying competitors without adding value, ignoring internal links, and treating AI search like traditional SEO. Focus on useful, cited, well-structured content."),
        (f"How long does it take to see results?", "Most sites see measurable movement in 30 to 90 days. Compounding results usually appear after three to six months of consistent execution."),
    ]

def make_tldr(h1, category):
    return f"This guide covers {h1.split(':')[0].split('(')[0].strip().lower()} from strategy to execution. You will learn how to audit your current state, prioritize the highest-impact tactics, avoid common mistakes, and measure progress with the right metrics."

def sanitize_body_html(body):
    # Remove banned words and normalize whitespace in HTML.
    for bw, repl in BANNED_WORDS.items():
        body = re.sub(rf"\b{bw}\b", repl, body, flags=re.I)
    body = re.sub(r"\n\s*\n+", "\n", body)
    return body

def build_sections_html(sections, category, slug, h1):
    links = internal_links_for(category, slug)
    parts = []
    seen_ids = set()
    def safe_id(title):
        base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
        if not base:
            base = "section"
        uniq = base
        i = 2
        while uniq in seen_ids:
            uniq = f"{base}-{i}"
            i += 1
        seen_ids.add(uniq)
        return uniq
    for sec in sections:
        if sec["level"] == 2:
            sec_id = safe_id(sec["title"])
            parts.append(f'<h2 id="{sec_id}">{html.escape(sec["title"])}</h2>')
        else:
            parts.append(f'<h3 id="{safe_id(sec["title"])}">{html.escape(sec["title"])}</h3>')
        body = sanitize_body_html(sec["body"])
        if body:
            parts.append(body)
    h2_ids = re.findall(r'<h2 id="([^"]+)">', "\n".join(parts))
    if len(parts) > 2 and links:
        guide_links = ", ".join(links[:3])
        parts.insert(2, f'<p>If you want to go deeper, explore our {guide_links}.</p>')
    if not any("common mistake" in p.lower() or "mistakes to avoid" in p.lower() for p in parts):
        parts.append('<h2 id="common-mistakes">Common mistakes to avoid</h2>')
        parts.append(f'<p>Even experienced teams slip up when executing {h1.split(":")[0].split("(")[0].strip().lower()}. Here are the errors that waste budget and rankings.</p>')
        parts.append('<ul><li><strong>Skipping the audit.</strong> Acting without a baseline makes it impossible to measure impact or prioritize fixes.</li><li><strong>Chasing vanity metrics.</strong> Traffic without intent or conversions does not grow revenue.</li><li><strong>Ignoring technical basics.</strong> Crawl errors, slow pages, and poor mobile experience undercut every content win.</li></ul>')
    return "\n".join(parts), h2_ids

def build_page(slug, data, progress):
    category = data["category"]
    author_slug = classify_author(data["h1"], slug, category)
    author = AUTHORS[author_slug]
    title = optimize_title(data["h1"], slug)
    description = optimize_description(data["description"], title, slug)
    h1 = data["h1"]
    date_pub = data["date"]
    date_mod = "2026-07-01"
    display_pub = format_date_display(date_pub)
    display_up = "Q2 2026"

    sections_html, h2_ids = build_sections_html(data["sections"], category, slug, h1)
    lede_first = "This guide explains the tactics, tools, and workflows that actually move rankings in 2026."
    if data["sections"]:
        first_body = BeautifulSoup(data["sections"][0]["body"], "html.parser").get_text(" ", strip=True)
        if first_body:
            lede_first = first_body[:160] + ("..." if len(first_body) > 160 else "")
    lede_rest = "You will learn how to audit your current state, prioritize the highest-impact changes, avoid common mistakes, and measure results without drowning in spreadsheets."
    tldr = make_tldr(h1, category)

    links = internal_links_for(category, slug)
    inline_cta_url = "/demo/"
    inline_cta_btn = "Get my free audit"
    inline_cta_meta = "127+ audits this quarter"
    if category == "AI & Emerging":
        inline_cta_url = "/demo/"
        inline_cta_btn = "Book a demo"
        inline_cta_meta = "See theStacc in action"
    if category in ("Local SEO", "Content Strategy"):
        inline_cta_url = "/checkout/"
        inline_cta_btn = "Start $1 trial"
        inline_cta_meta = "Cancel anytime"

    faq_items = generate_faq(h1, category, data["faq_items"])
    sources = external_sources_for(category, slug)
    related = related_posts_for(category, slug)
    feature_svg = make_feature_svg(h1, slug)
    breadcrumb_name = h1.split(":")[0].split("(")[0].strip()

    toc_items = []
    for hid in h2_ids:
        label = hid.replace("-", " ").title()
        toc_items.append(f'<li><a href="#{hid}">{html.escape(label)}</a></li>')
    if "faq" not in h2_ids:
        toc_items.append('<li><a href="#faq">FAQ</a></li>')
    if "sources" not in h2_ids:
        toc_items.append('<li><a href="#sources">Sources</a></li>')

    faq_html = []
    faq_schema = []
    for q, a in faq_items:
        faq_html.append(f'''<div class="faq-item">
            <button class="faq-q" onclick="toggleFaq(this)">
              <span class="faq-q-text">{html.escape(q)}</span>
              <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
            </button>
            <div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
          </div>''')
        faq_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    sources_html = []
    for idx, (url, txt) in enumerate(sources[:4], 1):
        sources_html.append(f'<li><span class="src-num">[{idx:02d}]</span><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(txt)}</a></li>')

    rel_cards = []
    for rslug, rcat, rtitle, rdesc in related:
        href = f"/blog/{rslug}/" if not rslug.endswith("/") else f"/{rslug}"
        rel_cards.append(f'''<a href="{href}" class="related-card">
          <span class="cat">{html.escape(rcat)}</span>
          <h3>{html.escape(rtitle)}</h3>
          <p>{html.escape(rdesc)}</p>
          <span class="arrow-link">Read guide →</span>
        </a>''')

    word_count = len(BeautifulSoup(sections_html, "html.parser").get_text().split())

    schema_data = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": breadcrumb_name, "item": f"https://thestacc.com/blog/{slug}/"}
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": date_pub,
            "dateModified": date_mod,
            "author": {"@type": "Person", "name": author["name"], "url": f"https://thestacc.com/authors/{author_slug}/", "sameAs": [author["linkedin"]]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema
        }
    ]

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {js_str(title)},
  description: {js_str(description)},
  canonical: {js_str(f"https://thestacc.com/blog/{slug}/")},
  ogImage: {js_str(f"/og/blog-{slug}.webp")},
  schemaData: {json.dumps(schema_data, ensure_ascii=False)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{html.escape(breadcrumb_name)}</span>
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
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_pub}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time(word_count)}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{display_up}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category)} · 2026 Guide</div>
        <div class="cover-title">{html.escape(breadcrumb_name)}</div>
        <div class="cover-sub">Tactics · Examples · Templates</div>
      </div>
      {feature_svg}
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
            <h4>Want better results from {html.escape(category.lower())}?</h4>
            <p>Get a <strong>free SEO audit</strong> in 24 hours. We will find the content gaps, technical fixes, and link opportunities that are costing you traffic.</p>
          </div>
          <div class="cta-action">
            <a href="{inline_cta_url}" class="cta-btn-inline">{inline_cta_btn} <span>→</span></a>
            <span class="cta-meta">{inline_cta_meta}</span>
          </div>
        </div>

        {escape_braces(sections_html)}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {escape_braces("\n".join(faq_html))}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Scale {html.escape(category.lower())} without losing quality</h4>
            <p>theStacc combines SEO, content, and AI visibility in one system. Publish optimized content, track rankings, and fix technical issues in one place.</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start $1 trial <span>→</span></a>
            <span class="cta-meta">Cancel anytime</span>
          </div>
        </div>

        <h2 id="sources">Sources &amp; methodology</h2>
        <div class="sources-block">
          <div class="sources-head">📑 Research sources</div>
          <ol class="sources-list">
            {escape_braces("\n".join(sources_html))}
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
          <div class="cta-title">See what is costing you traffic.</div>
          <p class="cta-desc">We will audit your site and send back the keywords you are missing, the technical fixes ranked by impact, and what your competitors are doing that you are not.</p>
          <a href="/demo/" class="cta-btn">Get my free audit <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical fixes ranked by impact</li>
            <li>Content gap analysis</li>
            <li>Competitor playbook</li>
            <li>A 90-day growth plan</li>
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
            {escape_braces("\n".join(toc_items))}
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={html.escape(title)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        {escape_braces("\n".join(rel_cards))}
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
    return page, word_count

def load_progress():
    try:
        return json.load(open(PROGRESS_FILE))
    except Exception as e:
        print("Could not load progress.json:", e)
        return {"posts": {}, "totals": {"pending":0,"in_progress":0,"done":0,"failed":0}}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def save_chunk_progress(state):
    with open(CHUNK_PROGRESS_FILE, "w") as f:
        json.dump(state, f, indent=2)

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def recount_totals(progress):
    progress["totals"] = {
        s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
        for s in ["pending", "in_progress", "done", "failed"]
    }

def main():
    slugs = [s.strip() for s in open(CHUNK_FILE).read().splitlines() if s.strip()]
    progress = load_progress()
    state = {
        "chunk": CHUNK_FILE,
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": [],
    }
    save_chunk_progress(state)

    for slug in slugs:
        post_state = progress.get("posts", {}).get(slug, {})
        if post_state.get("status") == "done":
            state["skipped_already_done"].append(slug)
            save_chunk_progress(state)
            continue
        print(f"Processing {slug}...")
        html_text, err = extract_source(slug)
        if err:
            state["failed"][slug] = err
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = err
            save_progress(progress)
            save_chunk_progress(state)
            continue
        try:
            data = parse_source(html_text)
            if not data["sections"]:
                err = "no content sections extracted"
                state["failed"][slug] = err
                progress["posts"][slug]["status"] = "failed"
                progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
                progress["posts"][slug]["last_error"] = err
                save_progress(progress)
                save_chunk_progress(state)
                continue
            page, wc = build_page(slug, data, progress)
            out_dir = os.path.join(OUT_ROOT, slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.astro")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            state["completed"].append(slug)
            # update main progress
            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["category"] = data["category"]
            progress["posts"][slug]["author"] = classify_author(data["h1"], slug, data["category"])
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["word_count"] = wc
            progress["posts"][slug]["verified_at"] = now_iso()
            progress["posts"][slug]["last_error"] = None
            recount_totals(progress)
            save_progress(progress)
            save_chunk_progress(state)
            print(f"  -> wrote {out_path} ({wc} words)")
        except Exception as e:
            import traceback
            err = str(e) + "\n" + traceback.format_exc()[:500]
            state["failed"][slug] = err
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = err
            recount_totals(progress)
            save_progress(progress)
            save_chunk_progress(state)
            print(f"  -> FAILED {slug}: {e}")

if __name__ == "__main__":
    main()
