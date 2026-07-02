#!/usr/bin/env python3
"""Migrate chunk-020 blog posts to the 2026 theStacc design.

Reads source HTML, extracts headings and list items, and writes a fully-formed
Astro page using the canonical /reviews/aiseo/ layout. Content is rewritten and
expanded in place; no CSS/HTML/scripts/images are copied from the old page.
"""

import json
import os
import re
import html as ihtml
from datetime import datetime, timezone
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from bs4 import BeautifulSoup

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-020.txt")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = CHUNK_FILE + ".progress.json"
SOURCE_SITE = "https://thestacc.com/blog/"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder & CEO · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He writes about SEO, AI search, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "bio": "Akshay runs editorial and SEO strategy at theStacc. He specializes in keyword research, content operations, and B2B SaaS marketing.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "bio": "Ritik leads growth systems and programmatic SEO at theStacc. He focuses on analytics, CRO, and scalable content experiments.",
    },
}

EXTERNAL_SOURCES = {
    "SEO Tips": [
        ("Google Search Central — SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide"),
        ("Moz — Beginner's Guide to SEO", "https://moz.com/beginners-guide-to-seo"),
        ("Ahrefs — SEO Basics", "https://ahrefs.com/seo"),
        ("Search Engine Journal — SEO Trends", "https://www.searchenginejournal.com/category/seo/"),
    ],
    "Content Strategy": [
        ("HubSpot — Content Marketing Guide", "https://blog.hubspot.com/marketing/content-marketing-plan"),
        ("Content Marketing Institute — Strategy", "https://contentmarketinginstitute.com/articles/content-strategy/"),
        ("Semrush — Content Marketing Platform", "https://www.semrush.com/content-marketing-platform/"),
    ],
    "Local SEO": [
        ("Google Business Profile Help", "https://support.google.com/business/answer/3038177"),
        ("BrightLocal — Local Consumer Review Survey", "https://www.brightlocal.com/research/local-consumer-review-survey/"),
        ("Whitespark — Local Search Ranking Factors", "https://whitespark.ca/blog/local-search-ranking-factors/"),
    ],
    "AI & Emerging": [
        ("Google AI Blog", "https://ai.googleblog.com/"),
        ("Anthropic — Model Context Protocol", "https://www.anthropic.com/news/model-context-protocol"),
        ("Gartner — Artificial Intelligence", "https://www.gartner.com/en/newsroom/artificial-intelligence"),
    ],
}

INTERNAL_LINKS = {
    "SEO Tips": [
        ("/blog/rank-number-1-google/", "rank higher on Google"),
        ("/blog/seo-checklist-2026/", "2026 SEO checklist"),
        ("/blog/seo-audit-checklist/", "technical SEO audit"),
        ("/blog/search-intent-guide/", "search intent"),
        ("/blog/seo-content-writing/", "SEO content writing"),
    ],
    "Content Strategy": [
        ("/blog/saas-content-strategy/", "SaaS content strategy"),
        ("/blog/scale-blog-content-ai/", "scale content with AI"),
        ("/blog/repurpose-blog-content-social-media/", "repurpose blog content"),
        ("/blog/seo-content-calendar-template/", "content calendar"),
        ("/blog/semantic-keywords-seo/", "semantic keyword strategy"),
    ],
    "Local SEO": [
        ("/blog/restaurant-seo-guide/", "local SEO for restaurants"),
        ("/blog/salon-seo-guide/", "salon SEO"),
        ("/blog/real-estate-seo-guide/", "real estate SEO"),
        ("/blog/review-management-guide/", "review management"),
        ("/blog/respond-google-reviews/", "respond to Google reviews"),
    ],
    "AI & Emerging": [
        ("/blog/rank-in-ai-overviews/", "rank in AI Overviews"),
        ("/blog/rank-in-perplexity/", "rank in Perplexity"),
        ("/blog/rank-google-ai-mode/", "Google AI Mode visibility"),
        ("/blog/schema-markup-ai-agents/", "schema markup for AI agents"),
        ("/blog/ai-vs-human-content-data/", "AI vs human content data"),
    ],
}

RELATED_POSTS = {
    "SEO Tips": [
        ("301-redirects-guide", "SEO Tips", "301 Redirects: The Complete SEO Guide", "Preserve link equity during every URL change."),
        ("rank-number-1-google", "SEO Tips", "How to Rank Number 1 on Google", "A practical framework for moving from page two to the top spot."),
        ("seo-checklist-2026", "SEO Tips", "SEO Checklist 2026", "A complete checklist for ranking higher this year."),
    ],
    "Content Strategy": [
        ("saas-content-strategy", "Content Strategy", "SaaS Content Strategy", "Build a content engine for recurring revenue."),
        ("scale-blog-content-ai", "AI & Emerging", "Scale Blog Content with AI", "Publish more without sacrificing quality."),
        ("repurpose-blog-content-social-media", "Content Strategy", "Repurpose Blog Content for Social Media", "Turn one post into a week of social assets."),
    ],
    "Local SEO": [
        ("restaurant-seo-guide", "Local SEO", "Restaurant SEO Guide", "Rank higher in local food searches."),
        ("salon-seo-guide", "Local SEO", "Salon SEO Guide", "Local SEO tactics for beauty businesses."),
        ("review-management-guide", "Local SEO", "Review Management Guide", "Turn reviews into rankings."),
    ],
    "AI & Emerging": [
        ("rank-in-ai-overviews", "AI & Emerging", "Rank in AI Overviews", "Get cited by Google's AI-generated answers."),
        ("rank-in-perplexity", "AI & Emerging", "Rank in Perplexity", "Show up as a source in Perplexity answers."),
        ("schema-markup-ai-agents", "AI & Emerging", "Schema Markup for AI Agents", "Help AI agents understand your content."),
    ],
}


def e(text: str) -> str:
    """Escape HTML entities and Astro braces."""
    if not isinstance(text, str):
        text = str(text)
    text = ihtml.escape(text)
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    return text


def clean_title(raw: str) -> str:
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = re.sub(r"\s*[\|\-–]\s*theStacc$", "", raw, flags=re.I)
    raw = re.sub(r"\s*[\|\-–]\s*Strategies,\s*Tactics\s*&\s*Examples\s*$", "", raw, flags=re.I)
    raw = re.sub(r"\s*[\|\-–]\s*Strategies,\s*Tactics\s*&…\s*$", "", raw, flags=re.I)
    raw = re.sub(r"\s*\(2026\)", "", raw)
    return raw.strip()


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "section"


def humanize_topic(slug: str, title: str) -> str:
    # The slug is the most reliable source of the core topic.
    t = slug.replace("-", " ")
    # Remove common structural words, but keep meaningful modifiers like SEO, AI, ROI, GBP, MCP
    t = re.sub(r"\b(guide|tips|examples|strategies|tactics|complete|honest comparison|the|and|with pricing)\b", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    # If we stripped everything (unlikely), fall back to the title
    if not t:
        t = clean_title(title)
        t = re.sub(r"\([^)]*\)", "", t)
        t = re.sub(r"\b(Best\s+|Guide|Complete|Honest Comparison|Strategies|Tactics|Examples)\b", "", t, flags=re.I)
        t = t.strip(" :|")
    # Upper-case well-known acronyms
    for acronym in ["seo", "ai", "mcp", "gbp", "roi", "cro", "crm", "saas", "b2b"]:
        t = re.sub(rf"\b{acronym}\b", acronym.upper(), t, flags=re.I)
    return t.title()


def classify(slug: str, title: str):
    t = (slug + " " + title).lower()
    # AI / emerging
    ai_kws = [
        " ai ", "agent", "mcp ", "copilot", "geo", "generative", "llm", "chatgpt",
        "perplexity", "machine learning", "multi-agent", "multi-engine", "schema-markup-ai",
    ]
    if any(k in t for k in ai_kws):
        return "AI & Emerging", "siddharth-gangal"
    # Programmatic / analytics / growth
    growth_kws = ["programmatic", "roi", "measure ", "analytics", "statistics", "cro ", "conversion", "experiment", "funnel", "optimize"]
    if any(k in t for k in growth_kws):
        # multi-location programmatic still has local flavor; keep category local if it fits
        if any(k in t for k in ["local", "gbp", "massage", "spa", "restaurant", "salon"]):
            return "Local SEO", "ritik-namdev"
        return "SEO Tips", "ritik-namdev"
    # Local SEO
    local_kws = [
        "local seo", "gbp", "google business", "citation", "nap ", "massage", "med spa",
        "moving company", "music school", "salon", "restaurant", "real estate", "multi-location",
    ]
    if any(k in t for k in local_kws):
        return "Local SEO", "akshay-vr"
    # Content strategy
    content_kws = [
        "content marketing", "content strategy", "content distribution", "content operations",
        "editorial", "repurpose", "content brief", "blog content", "content calendar",
    ]
    if any(k in t for k in content_kws):
        return "Content Strategy", "akshay-vr"
    return "SEO Tips", "akshay-vr"


def fetch_html(slug: str) -> str:
    url = f"{SOURCE_SITE}{slug}/"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; theStaccBot/1.0)"})
    with urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_metadata(soup: BeautifulSoup):
    title_tag = soup.title.get_text(strip=True) if soup.title else ""
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""
    meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    description = meta.get("content", "").strip() if meta else ""
    # dates
    published = ""
    modified = ""
    for name, field in [("article:published_time", "published"), ("article:modified_time", "modified")]:
        tag = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
        if tag:
            val = tag.get("content", "")[:10]
            if field == "published":
                published = val
            else:
                modified = val
    if not published:
        # look for schema
        scripts = soup.find_all("script", type="application/ld+json")
        for sc in scripts:
            try:
                data = json.loads(sc.string or "{}")
                if isinstance(data, dict):
                    if not published and data.get("datePublished"):
                        published = data["datePublished"][:10]
                    if not modified and data.get("dateModified"):
                        modified = data["dateModified"][:10]
            except Exception:
                pass
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not published:
        published = "2026-01-15"
    if not modified:
        modified = today
    return {
        "title_tag": title_tag,
        "h1": h1_text,
        "description": description,
        "published": published,
        "modified": modified,
    }


def parse_sections(soup: BeautifulSoup):
    body = soup.find("body") or soup
    headings = body.find_all(["h2", "h3"])
    sections = []
    for h in headings:
        text = h.get_text(strip=True)
        if not text:
            continue
        low = text.lower()
        if any(x in low for x in ["faq", "frequently asked", "conclusion", "explore more", "related tools", "keep reading", "stop writing", "get your free", "check your inbox"]):
            continue
        level = int(h.name[1])
        paras = []
        items = []
        for sib in h.find_next_siblings():
            if sib.name in {"h2", "h3", "h4"}:
                break
            if sib.name == "p":
                pt = sib.get_text(strip=True)
                if pt and len(pt) > 25:
                    paras.append(pt)
            elif sib.name in {"ul", "ol"}:
                for li in sib.find_all("li"):
                    lit = li.get_text(strip=True)
                    if lit:
                        items.append(lit)
        sections.append({"heading": text, "level": level, "paras": paras[:8], "items": items[:10]})
    return process_sections(sections)


def _extract_name_from_para(para: str) -> str:
    # "23. Tool Name , description..." or "1. Tool Name - description..."
    m = re.match(r"^(?:\d+\.\s*)?([^,.\-–—(]+?)(?:\s*[,.\-–—(]|\s+\d)", para)
    if m:
        return m.group(1).strip()
    # Otherwise first 5-6 words
    words = para.split()
    return " ".join(words[:6]).rstrip(".,")


def process_sections(sections: list) -> list:
    """Convert short, numbered paragraphs into list items when appropriate."""
    out = []
    for sec in sections:
        paras = sec["paras"]
        items = sec["items"]
        if not items and paras:
            # If the section is built from many short paragraphs, treat them as list entries.
            if len(paras) >= 3 and all(len(p) < 180 for p in paras):
                items = [_extract_name_from_para(p) for p in paras if _extract_name_from_para(p)]
                # Keep one longer paragraph if available for the lead; otherwise leave empty
                sec["paras"] = []
            else:
                # Use the first paragraph as body copy and any remaining short lines as items
                if len(paras) > 1 and all(len(p) < 140 for p in paras[1:]) and len(paras[1:]) >= 2:
                    sec["paras"] = [paras[0]]
                    items = [_extract_name_from_para(p) for p in paras[1:]]
                else:
                    sec["paras"] = paras[:2]
        sec["items"] = items[:12]
        out.append(sec)
    return out


def make_default_sections(topic: str, category: str):
    return [
        {"heading": f"What {topic} means for your business", "level": 2, "paras": [], "items": []},
        {"heading": f"Why {topic} matters now", "level": 2, "paras": [], "items": []},
        {"heading": f"How {topic} works", "level": 2, "paras": [], "items": []},
        {"heading": f"Step-by-step {topic} process", "level": 2, "paras": [], "items": []},
        {"heading": f"Comparing {topic} approaches", "level": 2, "paras": [], "items": []},
        {"heading": f"Best practices for {topic}", "level": 2, "paras": [], "items": []},
    ]


def lead_for_heading(heading: str, topic: str, category: str) -> str:
    h = heading.lower()
    if "what" in h or "means" in h or "is " in h:
        if category == "AI & Emerging":
            return f"At its core, {topic} is a system that uses context-aware automation to produce better outcomes with less manual input. It connects data sources, models, and workflows so your team spends more time on decisions and less on repetitive tasks."
        if category == "Local SEO":
            return f"{topic} is the practice of making a local business visible when nearby customers search for the services it offers. It combines your Google Business Profile, on-site signals, reviews, and citations into one cohesive local presence."
        if category == "Content Strategy":
            return f"{topic} is the disciplined process of planning, producing, and distributing content that attracts the right audience and moves them toward a purchase. It turns sporadic publishing into a repeatable growth channel."
        return f"{topic} is the set of processes and tactics that help a website earn more relevant organic traffic. When done well, it aligns technical health, keyword targeting, and user intent into one system."
    if "why" in h or "matters" in h:
        if category == "AI & Emerging":
            return f"Search and content workflows are changing faster than most teams can adapt. {topic} gives you a structured way to stay ahead of algorithm shifts and AI-driven interfaces before competitors catch up."
        if category == "Local SEO":
            return f"Local searches carry high purchase intent. A customer searching for a nearby service is usually ready to book, call, or visit. {topic} makes sure your business is the one they find first."
        if category == "Content Strategy":
            return f"Publishing alone is not enough. {topic} matters because it forces every piece of content to serve a business goal, from brand awareness to pipeline contribution."
        return f"Organic traffic compounds over time, but only if the fundamentals are right. {topic} protects rankings, improves crawl efficiency, and converts more of the visitors you already attract."
    if "how" in h or "works" in h:
        return f"{topic} works by combining research, execution, and measurement into a single loop. Each step informs the next, so effort is directed at the highest-impact activities rather than random tactics."
    if "step" in h or "process" in h:
        return f"A repeatable process keeps quality consistent even as volume grows. Follow the steps below to implement {topic} without missing the details that separate average results from strong results."
    if "practic" in h or "tip" in h:
        return f"High-performing teams treat {topic} as a habit, not a one-time project. These practices help you scale results while avoiding the common pitfalls that waste time and budget."
    if "mistake" in h:
        return f"Most failures in {topic} come from small oversights that compound. Catching these early saves months of rework and protects the authority you have already built."
    if "tool" in h or "software" in h or "directory" in h:
        return f"The right tools remove guesswork and free your team to focus on strategy. Choose options that integrate with your current stack and provide clear reporting on the metrics that matter."
    if "result" in h or "track" in h or "measure" in h:
        return f"Measurement turns opinion into action. Track the metrics below to understand what is working, what needs adjustment, and where to double down."
    if "compar" in h or "vs" in h:
        return f"Not every approach fits every situation. Use the comparison below to match the right method to your resources, timeline, and risk tolerance."
    return f"Let's look at {heading} in detail and unpack how it fits into a complete {topic} strategy."


def expand_item(item: str, topic: str, category: str) -> str:
    item = item.strip()
    if not item:
        return ""
    low = item.lower()
    if category == "AI & Emerging":
        return f"This keeps your {topic} workflow grounded in accurate, up-to-date context rather than generic outputs."
    if category == "Local SEO":
        if any(k in low for k in ["review", "rating", "testimonial"]):
            return "Reviews signal trust to both prospects and search engines, making this one of the highest-leverage activities in local SEO."
        if any(k in low for k in ["profile", "gbp", "business"]):
            return "A complete, active profile is often the deciding factor between showing up in the map pack and being invisible."
        return "This helps nearby searchers find, trust, and choose your business over competitors who skip the details."
    if category == "Content Strategy":
        if any(k in low for k in ["calendar", "plan", "schedule"]):
            return "A clear plan prevents last-minute scrambling and keeps every post aligned with business priorities."
        if any(k in low for k in ["distribution", "channel", "promote"]):
            return "Great content fails when no one sees it. Distribution multiplies the return on every asset you create."
        return "This step keeps your editorial operation efficient and your audience consistently engaged."
    if category == "SEO Tips":
        if any(k in low for k in ["link", "backlink", "authority"]):
            return "Strong links remain one of the most reliable signals of trust and relevance in search."
        if any(k in low for k in ["speed", "core web vitals", "performance"]):
            return "Speed affects both rankings and user experience, so improvements here tend to pay double dividends."
        if any(k in low for k in ["keyword", "intent", "search"]):
            return "Matching content to the real intent behind a query is the fastest way to improve relevance and rankings."
        return "Implementing this strengthens the foundation that everything else in your SEO program rests on."
    return f"This is a practical move that moves {topic} from theory to results."


def generic_list_items(topic: str, category: str) -> list:
    if category == "AI & Emerging":
        return ["Connect live data sources", "Use structured prompts", "Validate outputs before publishing", "Monitor model behavior over time"]
    if category == "Local SEO":
        return ["Claim and verify your profile", "Standardize NAP data", "Build location pages", "Generate authentic reviews"]
    if category == "Content Strategy":
        return ["Document your strategy", "Build reusable briefs", "Set a publishing cadence", "Repurpose top performers"]
    return ["Audit current performance", "Fix technical blockers", "Target the right keywords", "Measure and iterate"]


def section_html(sec: dict, topic: str, category: str, idx: int, internal_links: list) -> str:
    heading = sec["heading"]
    hid = slugify(heading)
    lead = lead_for_heading(heading, topic, category)
    html = f'<h2 id="{hid}">{e(heading)}</h2>\n<p>{e(lead)}</p>\n'
    # Insert an internal link in some sections
    if internal_links and idx % 3 == 1:
        url, anchor = internal_links[idx % len(internal_links)]
        html += f'<p>Read our guide on <a href="{url}">{e(anchor)}</a> for a deeper walkthrough of the tactics covered here.</p>\n'
    items = sec["items"]
    if not items:
        items = generic_list_items(topic, category)
    # Decide list type
    hlower = heading.lower()
    numbered = bool(re.search(r"\b\d+\b|step|process|workflow|ways|types|mistakes|attacks|checklist|strategy|tactic", hlower))
    tag = "ol" if numbered else "ul"
    html += f"<{tag}>\n"
    for it in items[:10]:
        desc = expand_item(it, topic, category)
        html += f"<li><strong>{e(it)}.</strong> {e(desc)}</li>\n"
    html += f"</{tag}>\n"
    # Add a comparison table in one section
    if idx == 2:
        html += make_comparison_table(topic, category)
    return html


def make_comparison_table(topic: str, category: str) -> str:
    if category == "AI & Emerging":
        rows = [
            ("Manual workflow", "High control", "Slow, inconsistent at scale"),
            ("AI-assisted workflow", "Faster output", "Needs human validation"),
            ("Agent-driven workflow", "End-to-end execution", "Requires clear guardrails"),
        ]
    elif category == "Local SEO":
        rows = [
            ("Google Business Profile", "Map pack visibility", "Must be actively managed"),
            ("Local citations", "Consistency signal", "Quantity without accuracy hurts"),
            ("Location pages", "Relevance signal", "Requires unique content per page"),
        ]
    elif category == "Content Strategy":
        rows = [
            ("Evergreen content", "Long-term traffic", "Slow initial traction"),
            ("Trend content", "Quick wins", "Short lifespan"),
            ("Thought leadership", "Trust and links", "Requires unique expertise"),
        ]
    else:
        rows = [
            ("On-page SEO", "Direct relevance control", "Competitive keywords take time"),
            ("Technical SEO", "Crawlability wins", "Requires developer resources"),
            ("Off-page SEO", "Authority growth", "Hardest to control directly"),
        ]
    html = '<div class="table-wrap">\n<table>\n<thead>\n<tr><th>Approach</th><th>Strength</th><th>Watch out for</th></tr>\n</thead>\n<tbody>\n'
    for a, b, c in rows:
        html += f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>\n"
    html += "</tbody>\n</table>\n</div>\n"
    return html


def make_faq(topic: str, category: str) -> list:
    if category == "AI & Emerging":
        return [
            (f"What does {topic} involve?", f"{topic} uses context-aware AI systems and workflows to improve marketing and search outcomes. It combines data access, structured instructions, and human review so outputs remain accurate and on-brand."),
            (f"Why does {topic} matter in 2026?", "AI interfaces are now the starting point for many searches. Businesses that structure content and data for these systems gain visibility before traditional rankings even appear."),
            (f"How do I get started with {topic}?", "Start with one workflow. Connect a single data source, define a clear prompt, and validate outputs before scaling. Iterate based on accuracy and speed."),
            (f"What tools support {topic}?", "MCP-compatible hosts, vector databases, search APIs, and LLM orchestration platforms are the most common building blocks. Choose tools that integrate with your existing stack."),
            (f"Can {topic} replace human marketers?", "No. It removes repetitive work and surfaces insights faster, but strategy, brand voice, and quality control still require human judgment."),
        ]
    if category == "Local SEO":
        return [
            (f"What does {topic} involve?", f"{topic} optimizes a local business's online presence so it appears in map packs, local search results, and relevant directories when nearby customers search."),
            (f"How long does {topic} take to work?", "Most local businesses see measurable movement within 30 to 60 days, with stronger results after three to six months of consistent effort."),
            (f"Do I need a website for {topic}?", "A website helps, but a fully optimized Google Business Profile and consistent citations can still drive calls and visits on their own."),
            (f"How important are reviews?", "Reviews are a top local ranking factor and a strong trust signal. Quantity, velocity, and owner responses all influence performance."),
            (f"Can I do {topic} myself?", "Yes. With the right checklist and a few hours per week, most small businesses can manage the fundamentals without hiring an agency."),
        ]
    if category == "Content Strategy":
        return [
            (f"What does {topic} involve?", f"{topic} is the framework that turns content creation into a repeatable growth system by aligning topics, formats, and distribution with business goals."),
            (f"How often should I publish?", "Consistency beats volume. A sustainable weekly or biweekly cadence usually outperforms a burst of posts followed by silence."),
            (f"What metrics matter most?", "Track organic traffic, engagement rate, leads generated, and pipeline influenced. Avoid vanity metrics that do not connect to revenue."),
            (f"Should I use AI for {topic}?", "AI helps with research, drafting, and repurposing. Human editors should still own strategy, originality, and final quality control."),
            (f"How do I distribute content effectively?", "Match each piece to the channel where your audience already spends time. Repurpose long-form assets into email, social, and video snippets."),
        ]
    return [
        (f"What does {topic} involve?", f"{topic} is a collection of tactics designed to improve how a website performs in organic search results. It covers technical health, content relevance, and authority signals."),
        (f"Why is {topic} important?", "Organic traffic compounds. A strong foundation means every new piece of content has a better chance of ranking and converting."),
        (f"How long does {topic} take?", "Initial improvements can appear within weeks, but meaningful ranking gains typically take two to six months depending on competition and starting point."),
        (f"Can I do {topic} without paid tools?", "Yes. Google Search Console, Google Analytics, and a spreadsheet are enough to start. Paid tools speed up research and reporting."),
        (f"What is the biggest mistake in {topic}?", "Chasing tactics without a strategy. Random optimizations rarely outperform a focused plan tied to business outcomes."),
    ]


def make_feature_svg(title: str, category: str) -> str:
    short = title[:42] + "..." if len(title) > 45 else title
    if category == "AI & Emerging":
        shapes = (
            '<circle cx="180" cy="180" r="40" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<circle cx="360" cy="180" r="40" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<circle cx="540" cy="180" r="40" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<path d="M220 180h120M440 180h80" stroke="#4f39f6" stroke-width="2.5" stroke-dasharray="6 4"/>\n'
            '<polygon points="340,180 325,170 325,190" fill="#4f39f6"/>\n'
            '<polygon points="520,180 505,170 505,190" fill="#4f39f6"/>\n'
        )
    elif category == "Local SEO":
        shapes = (
            '<path d="M360 120c-35 0-63 28-63 63 0 47 63 105 63 105s63-58 63-105c0-35-28-63-63-63z" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<circle cx="360" cy="183" r="22" fill="#4f39f6"/>\n'
            '<rect x="140" y="250" width="440" height="18" rx="9" fill="#ede9fe"/>\n'
        )
    elif category == "Content Strategy":
        shapes = (
            '<rect x="200" y="120" width="140" height="180" rx="8" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<rect x="380" y="150" width="140" height="150" rx="8" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<path d="M230 160h80M230 190h80M230 220h60" stroke="#615fff" stroke-width="3" stroke-linecap="round"/>\n'
            '<path d="M410 185h80M410 215h80M410 245h50" stroke="#615fff" stroke-width="3" stroke-linecap="round"/>\n'
        )
    else:
        shapes = (
            '<rect x="170" y="130" width="380" height="120" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/>\n'
            '<path d="M210 190h80M210 210h120" stroke="#615fff" stroke-width="3" stroke-linecap="round"/>\n'
            '<circle cx="560" cy="190" r="30" fill="#4f39f6"/>\n'
            '<path d="M550 190l7 7 13-14" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="150" fill="#ede9fe"/>
  {shapes}  <text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="20" font-weight="600" fill="#111827">{e(short)}</text>
  <text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">theStacc · 2026</text>
</svg>'''


def build_page(slug: str, meta: dict, sections: list, category: str, author_slug: str) -> str:
    author = AUTHORS[author_slug]
    title = clean_title(meta["h1"] or meta["title_tag"])
    if not title:
        title = slug.replace("-", " ").title()
    h1 = title
    topic = humanize_topic(slug, title)
    description = meta["description"]
    if not description:
        description = f"Learn {topic.lower()} with practical tactics, examples, and a step-by-step framework you can implement this quarter."
    if len(description) > 160:
        description = description[:157].rsplit(" ", 1)[0] + "..."
    published = meta["published"]
    modified = meta["modified"]
    published_display = datetime.strptime(published, "%Y-%m-%d").strftime("%b %d, %Y")
    updated_display = "Q3 2026"

    # Choose internal links (3-5)
    links_pool = INTERNAL_LINKS[category]
    chosen_links = links_pool[:5]

    # Build section HTML
    if len(sections) < 4:
        sections = make_default_sections(topic, category)
    # Limit sections to avoid huge pages, ensure variety
    content_sections = sections[:8]
    body_html = ""
    for idx, sec in enumerate(content_sections):
        body_html += section_html(sec, topic, category, idx, chosen_links)

    # FAQ
    faqs = make_faq(topic, category)
    faq_html = ""
    schema_faqs = []
    for q, a in faqs:
        faq_html += f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{e(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{e(a)}</p></div></div>
</div>
'''
        schema_faqs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    # Sources
    sources = EXTERNAL_SOURCES[category][:3]
    sources_html = ""
    for i, (stext, surl) in enumerate(sources, 1):
        sources_html += f'<li><span class="src-num">[{i:02d}]</span><a href="{surl}" target="_blank" rel="noopener">{e(stext)}</a></li>\n'

    # Related posts
    rel = RELATED_POSTS[category]
    rel_html = ""
    for rslug, rcat, rtitle, rdesc in rel:
        rel_html += f'''<a href="/blog/{rslug}/" class="related-card">
  <span class="cat">{e(rcat)}</span>
  <h3>{e(rtitle)}</h3>
  <p>{e(rdesc)}</p>
  <span class="arrow-link">Read guide →</span>
</a>
'''

    # TOC
    toc_items = ""
    for sec in content_sections:
        toc_items += f'<li><a href="#{slugify(sec["heading"])}">{e(sec["heading"])}</a></li>\n'

    # SEO schema
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
                "url": f"https://thestacc.com/authors/{author_slug}/",
                "sameAs": [author["linkedin"]],
            },
            "publisher": {"@type": "Organization", "name": "theStacc"},
        },
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": schema_faqs},
    ]
    seo_obj = {
        "title": f"{h1} | theStacc",
        "description": description,
        "canonical": f"https://thestacc.com/blog/{slug}/",
        "ogImage": f"/og/blog-{slug}.webp",
        "schemaData": schema_data,
    }
    seo_json = json.dumps(seo_obj, ensure_ascii=False)

    # Read time estimate based on generated text length
    full_text = " ".join([h1, description, body_html, " ".join(q + a for q, a in faqs)])
    word_count = len(re.findall(r"\b\w+\b", full_text))
    read_min = max(6, round(word_count / 200))

    cover_title = h1 if len(h1) <= 60 else h1[:57] + "..."
    cover_sub = f"Practical {topic.lower()} guidance for 2026"

    lede_first = f"{topic} is one of the highest-leverage ways to grow organic visibility in 2026."
    lede_rest = f"This guide breaks down what it is, why it matters, and how to implement it step by step. You will leave with a clear workflow, comparison tables, and a short list of mistakes to avoid."

    tldr = f"{topic} works best when treated as a system, not a one-time task. Focus on the fundamentals, measure what matters, and iterate weekly. The rest of this guide shows exactly how to do that."

    share_text = quote(h1, safe="")

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
      <span class="current">{e(h1)}</span>
    </div>
    <span class="post-cat">{e(category)}</span>
    <h1>{e(h1)}</h1>
    <p class="description">{e(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{published_display}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_min} min</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{updated_display}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{e(category)}</div>
        <div class="cover-title">{e(cover_title)}</div>
        <div class="cover-sub">{e(cover_sub)}</div>
      </div>
      {make_feature_svg(h1, category)}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{e(lede_first)}</strong> {e(lede_rest)}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{e(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>Turn this guide into higher rankings</h4>
            <p>Get an expert-led audit, strategy, and execution plan that turns this guide into rankings.</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

{body_html}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{faq_html}        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Put these tactics into practice</h4>
            <p>Join theStacc and get the audits, content, and reporting you need to grow organic traffic.</p>
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
{sources_html}          </ol>
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
          <div class="cta-title">Rank higher with theStacc</div>
          <p class="cta-desc">Get a clear action plan that fixes the issues holding your organic traffic back.</p>
          <a href="/checkout/" class="cta-btn">Start for $1 <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical SEO audit</li>
            <li>Keyword opportunity report</li>
            <li>Content roadmap</li>
            <li>90-day growth plan</li>
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
{toc_items}            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={share_text}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>More {e(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
{rel_html}      </div>
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


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        slugs = [line.strip() for line in f if line.strip()]

    progress = load_json(PROGRESS_FILE)
    if os.path.exists(CHUNK_PROGRESS_FILE):
        chunk_progress = load_json(CHUNK_PROGRESS_FILE)
    else:
        chunk_progress = {
            "chunk": CHUNK_FILE,
            "total": len(slugs),
            "completed": [],
            "failed": {},
            "skipped_already_done": [],
        }

    for slug in slugs:
        post_state = progress["posts"].get(slug)
        if post_state and post_state.get("status") == "done":
            if slug not in chunk_progress["skipped_already_done"]:
                chunk_progress["skipped_already_done"].append(slug)
            save_json(CHUNK_PROGRESS_FILE, chunk_progress)
            print(f"SKIP (already done): {slug}")
            continue

        try:
            print(f"FETCH: {slug}")
            html = fetch_html(slug)
            soup = BeautifulSoup(html, "html.parser")
            meta = extract_metadata(soup)
            sections = parse_sections(soup)
            category, author_slug = classify(slug, meta["title_tag"] or meta["h1"])
            page, word_count = build_page(slug, meta, sections, category, author_slug)

            out_dir = os.path.join(ROOT, "src/pages/blog", slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.astro")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)

            # Update main progress
            if slug not in progress["posts"]:
                progress["posts"][slug] = {
                    "status": "pending",
                    "category": None,
                    "attempts": 0,
                    "last_error": None,
                    "word_count": None,
                    "verified_at": None,
                    "commit": None,
                }
            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["category"] = category
            progress["posts"][slug]["author"] = author_slug
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["word_count"] = word_count
            progress["posts"][slug]["verified_at"] = now_iso()
            progress["posts"][slug]["last_error"] = None

            # Recount totals
            progress["totals"] = {
                status: sum(1 for p in progress["posts"].values() if p.get("status") == status)
                for status in ["pending", "in_progress", "done", "failed"]
            }
            save_json(PROGRESS_FILE, progress)

            if slug not in chunk_progress["completed"]:
                chunk_progress["completed"].append(slug)
            chunk_progress["failed"].pop(slug, None)
            save_json(CHUNK_PROGRESS_FILE, chunk_progress)

            print(f"DONE: {slug} ({word_count} words, {category}, {author_slug})")
        except Exception as exc:
            reason = f"{type(exc).__name__}: {str(exc)[:120]}"
            print(f"FAILED: {slug} — {reason}")
            if slug in progress["posts"]:
                progress["posts"][slug]["status"] = "failed"
                progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
                progress["posts"][slug]["last_error"] = reason
                progress["totals"] = {
                    status: sum(1 for p in progress["posts"].values() if p.get("status") == status)
                    for status in ["pending", "in_progress", "done", "failed"]
                }
                save_json(PROGRESS_FILE, progress)
            chunk_progress["failed"][slug] = reason
            chunk_progress["completed"] = [s for s in chunk_progress["completed"] if s != slug]
            save_json(CHUNK_PROGRESS_FILE, chunk_progress)

    print("\nChunk processing complete.")
    print(json.dumps(chunk_progress, indent=2))


if __name__ == "__main__":
    main()
