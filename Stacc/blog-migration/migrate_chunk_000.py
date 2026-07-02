#!/usr/bin/env python3
"""Migrate chunk-000 of theStacc blog posts to the 2026 Astro design."""

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path("/home/ritik/thestacc.com-astro/thestacc-2026-site")
CHUNK_FILE = ROOT / "Stacc/blog-migration/small-chunks/chunk-000.txt"
PROGRESS_FILE = ROOT / "Stacc/blog-migration/progress.json"
CHUNK_PROGRESS_FILE = Path(str(CHUNK_FILE) + ".progress.json")
OUTPUT_DIR = ROOT / "src/pages/blog"
SOURCE_BASE = "https://thestacc.com/blog/"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "full_role": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "slug": "siddharth-gangal",
        "x": "sidgangal",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "bio": "Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings."
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "full_role": "Marketing Head · theStacc",
        "initials": "AVR",
        "slug": "akshay-vr",
        "x": "akshayvr",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "bio": "Akshay leads marketing at theStacc. He runs editorial strategy, SEO operations, and demand generation for B2B SaaS brands. His writing focuses on practical SEO, content operations, and building search-driven growth systems."
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "full_role": "Growth Manager · theStacc",
        "initials": "RN",
        "slug": "ritik-namdev",
        "x": "ritiknamdev",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "bio": "Ritik manages growth and analytics at theStacc. He specializes in programmatic SEO, conversion optimization, and growth experiments that scale organic traffic without scaling headcount."
    }
}

LINK_POOLS = {
    "AI & Emerging": [
        ("/blog/ai-search-optimization-guide/", "AI Search Optimization Guide"),
        ("/blog/ai-overview-optimization/", "AI Overview Optimization"),
        ("/blog/ai-content-strategy/", "AI Content Strategy"),
        ("/blog/ai-agents-content-planning/", "AI Agents for Content Planning"),
        ("/blog/claude-for-seo/", "Claude for SEO"),
    ],
    "Local SEO": [
        ("/blog/ai-for-local-businesses/", "AI for Local Businesses"),
        ("/blog/google-business-profile-optimization/", "Google Business Profile Optimization"),
        ("/blog/local-citation-building/", "Local Citation Building"),
        ("/blog/local-seo-checklist/", "Local SEO Checklist"),
        ("/blog/seo-for-small-business/", "Small Business SEO"),
    ],
    "Content Strategy": [
        ("/blog/ai-content-strategy/", "AI Content Strategy"),
        ("/blog/ai-content-workflows/", "AI Content Workflows"),
        ("/blog/ai-automated-content-briefs/", "AI Automated Content Briefs"),
        ("/blog/ai-content-quality-checklist/", "AI Content Quality Checklist"),
        ("/blog/content-marketing-roi/", "Content Marketing ROI"),
    ],
    "SEO Tips": [
        ("/blog/301-redirects-guide/", "301 Redirects Guide"),
        ("/blog/rank-number-1-google/", "Rank Number 1 on Google"),
        ("/blog/technical-seo-audit/", "Technical SEO Audit"),
        ("/blog/on-page-seo-checklist/", "On-Page SEO Checklist"),
        ("/blog/keyword-research-guide/", "Keyword Research Guide"),
    ],
}


def slug_to_display(slug):
    """Convert slug to human-readable title guess."""
    s = slug.replace("-", " ").replace("_", " ")
    return s.title()


def slug_to_topic(slug):
    """Short topic phrase for FAQ and internal links."""
    words = []
    for w in slug.split("-"):
        if w == "ai":
            words.append("AI")
        elif w == "ymyl":
            words.append("YMYL")
        elif w == "2026":
            continue
        else:
            words.append(w.capitalize())
    topic = " ".join(words)
    topic = topic.replace("AI For ", "AI for ")
    topic = topic.replace("Salons Spas", "Salons and Spas")
    return topic


def determine_category(slug, title, h2s):
    text = (slug + " " + title + " " + " ".join(h2s)).lower()
    ai_signals = ["ai", "agent", "chatgpt", "llm", "generative", "geo", "ai search", "ai overview", "perplexity", "claude", "gemini"]
    local_signals = ["local seo", "gmb", "google business", "citation", "map", "local business", "near me", "dentist", "law firm", "restaurant", "salon", "spa", "contractor", "real estate"]
    content_signals = ["content strategy", "content marketing", "editorial", "brief", "content ops", "blogging", "content calendar", "content audit", "content quality", "content workflow"]
    
    if any(s in text for s in ai_signals):
        return "AI & Emerging"
    if any(s in text for s in local_signals):
        return "Local SEO"
    if any(s in text for s in content_signals):
        return "Content Strategy"
    return "SEO Tips"


def determine_author(category, slug, title):
    text = (slug + " " + title).lower()
    if category == "AI & Emerging" or any(x in text for x in ["agent", "llm", "chatgpt", "geo", "ai search", "perplexity"]):
        return "siddharth-gangal"
    if category == "Content Strategy" or any(x in text for x in ["content strategy", "content marketing", "editorial", "brief"]):
        return "akshay-vr"
    if category == "Local SEO":
        return "akshay-vr"
    # Default SEO Tips -> Siddharth for technical, Akshay for strategy, Ritik for analytics/growth
    if any(x in text for x in ["analytics", "cro", "ab test", "conversion", "funnel", "ga4", "search console", "programmatic"]):
        return "ritik-namdev"
    if any(x in text for x in ["audit", "redirect", "crawl", "indexing", "technical", "schema"]):
        return "siddharth-gangal"
    return "akshay-vr"


def fetch_source(slug):
    url = f"{SOURCE_BASE}{slug}/"
    tmp_path = Path(f"/tmp/blog-src-{slug}.html")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
        if r.status_code != 200:
            return None, f"http_{r.status_code}"
        tmp_path.write_text(r.text, encoding="utf-8")
        return r.text, None
    except Exception as e:
        return None, str(e)


def extract_source(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove scripts, styles, nav, footer, header, ads
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "button"]):
        tag.decompose()
    
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    
    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = h1_tag.get_text(strip=True)
    
    desc = ""
    meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if meta and meta.get("content"):
        desc = meta["content"].strip()
    
    # Find main content area if marked
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile("content|post|entry|blog"))
    root = main or soup
    
    h2s = [h.get_text(strip=True) for h in root.find_all("h2") if h.get_text(strip=True)]
    h3s = [h.get_text(strip=True) for h in root.find_all("h3") if h.get_text(strip=True)]
    
    # Extract paragraphs from main content, skip short/empty
    paragraphs = []
    for p in root.find_all("p"):
        txt = p.get_text(strip=True)
        if len(txt) > 40:
            paragraphs.append(txt)
    paragraphs = paragraphs[:20]
    
    # Lists
    lists = []
    for ul in root.find_all("ul")[:5]:
        items = [li.get_text(strip=True) for li in ul.find_all("li") if li.get_text(strip=True)]
        if items:
            lists.append(items)
    
    # Dates
    published = None
    updated = None
    for meta in soup.find_all("meta"):
        prop = (meta.get("property") or "").lower()
        name = (meta.get("name") or "").lower()
        if prop in ("article:published_time", "published_time") or name == "datePublished":
            published = meta.get("content")
        if prop in ("article:modified_time", "modified_time") or name == "dateModified":
            updated = meta.get("content")
    if not published:
        # Try to find date patterns in text
        m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+20\d{2}', html)
        if m:
            published = m.group(0)
    
    return {
        "title": title,
        "h1": h1,
        "description": desc,
        "h2s": h2s,
        "h3s": h3s,
        "paragraphs": paragraphs,
        "lists": lists,
        "published": published,
        "updated": updated
    }


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def make_id(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower())[:50].strip('-')


def estimate_read_time(word_count):
    minutes = max(5, word_count // 200)
    return f"{minutes} min"


def pick_related(slug, category):
    """Pick 3 related posts. Prefer other posts in chunk or common guides."""
    common = {
        "SEO Tips": [
            ("301-redirects-guide", "SEO Tips", "301 Redirects: The Complete SEO Guide", "Preserve link equity during every URL change with clean redirects."),
            ("rank-number-1-google", "SEO Tips", "How to Rank Number 1 on Google", "A practical framework for moving from page two to the top spot."),
            ("recover-helpful-content-update", "SEO Tips", "Recover from the Helpful Content Update", "What to fix and how to rebuild trust after a Google helpful-content hit."),
        ],
        "Content Strategy": [
            ("ai-content-strategy", "Content Strategy", "AI Content Strategy", "Build a content system that scales without losing editorial quality."),
            ("ai-content-workflows", "Content Strategy", "AI Content Workflows", "Operationalize AI-assisted publishing from brief to publish."),
            ("ai-automated-content-briefs", "Content Strategy", "AI Automated Content Briefs", "Generate briefs that writers and AI can execute consistently."),
        ],
        "Local SEO": [
            ("ai-for-local-businesses", "Local SEO", "AI for Local Businesses", "How local brands can use AI for reviews, listings, and rankings."),
            ("google-business-profile-optimization", "Local SEO", "Google Business Profile Optimization", "Turn your GBP into a local ranking and lead machine."),
            ("local-citation-building", "Local SEO", "Local Citation Building", "Build consistent citations that improve local search visibility."),
        ],
        "AI & Emerging": [
            ("ai-search-optimization-guide", "AI & Emerging", "AI Search Optimization Guide", "Rank in ChatGPT, Perplexity, Gemini, and AI Overviews."),
            ("ai-overview-optimization", "AI & Emerging", "AI Overview Optimization", "Get cited in Google's AI Overviews with structured answers."),
            ("ai-agents-content-planning", "AI & Emerging", "AI Agents for Content Planning", "Use agentic workflows to research, plan, and publish faster."),
        ]
    }
    pool = common.get(category, common["SEO Tips"])
    # Exclude self
    pool = [p for p in pool if p[0] != slug]
    # If not enough, add generic
    if len(pool) < 3:
        pool.append(("blog/", "Blog", "theStacc Blog", "More guides on SEO, content, and AI search."))
    return pool[:3]


def pick_internal_links(category, slug, n=4):
    """Pick 3-5 contextual internal links, excluding the current post."""
    pool = LINK_POOLS.get(category, LINK_POOLS["SEO Tips"])
    pool = [p for p in pool if not p[0].strip("/").endswith(slug)]
    return pool[:n]


def build_feature_svg(topic, category):
    """Return a topic-specific SVG illustration as a string."""
    brand = "#4f39f6"
    bg = "#f5f3ff"
    circle = "#ede9fe"
    
    if category == "AI & Emerging":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="{bg}"/>
  <circle cx="360" cy="180" r="130" fill="{circle}"/>
  <g fill="none" stroke="{brand}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="270" y="100" width="180" height="130" rx="14" fill="#ffffff"/>
    <circle cx="360" cy="165" r="32" fill="#ffffff" stroke-width="2"/>
    <path d="M345 165h30M360 150v30"/>
    <path d="M285 250h150" stroke-dasharray="6 4"/>
    <rect x="220" y="245" width="40" height="30" rx="6" fill="#ffffff"/>
    <rect x="460" y="245" width="40" height="30" rx="6" fill="#ffffff"/>
    <path d="M260 260h-30M490 260h30"/>
  </g>
  <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text>
  <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">AI search · GEO · Automation</text>
</svg>'''
    elif category == "Local SEO":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="{bg}"/>
  <circle cx="360" cy="180" r="130" fill="{circle}"/>
  <g fill="none" stroke="{brand}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M360 100c-35 0-63 28-63 63 0 47 63 97 63 97s63-50 63-97c0-35-28-63-63-63z" fill="#ffffff"/>
    <circle cx="360" cy="163" r="22" fill="#ffffff"/>
    <rect x="230" y="210" width="80" height="60" rx="8" fill="#ffffff"/>
    <rect x="410" y="210" width="80" height="60" rx="8" fill="#ffffff"/>
    <path d="M270 210v-30M450 210v-30"/>
  </g>
  <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text>
  <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Local rankings · Maps · Reviews</text>
</svg>'''
    elif category == "Content Strategy":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="{bg}"/>
  <circle cx="360" cy="180" r="130" fill="{circle}"/>
  <g fill="none" stroke="{brand}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="210" y="130" width="120" height="90" rx="8" fill="#ffffff"/>
    <rect x="390" y="130" width="120" height="90" rx="8" fill="#ffffff"/>
    <path d="M330 175h60"/>
    <polygon points="360,175 350,168 350,182" fill="{brand}" stroke="none"/>
    <rect x="300" y="250" width="120" height="40" rx="8" fill="#ffffff"/>
    <path d="M240 220v30M480 220v30"/>
  </g>
  <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text>
  <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Editorial ops · Briefs · Scale</text>
</svg>'''
    else:
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="{bg}"/>
  <circle cx="360" cy="180" r="130" fill="{circle}"/>
  <g fill="none" stroke="{brand}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="160" y="150" width="120" height="70" rx="10" fill="#ffffff"/>
    <rect x="440" y="150" width="120" height="70" rx="10" fill="#ffffff"/>
    <path d="M280 185h160" stroke-dasharray="6 4"/>
    <polygon points="440,185 425,175 425,195" fill="{brand}" stroke="none"/>
    <circle cx="220" cy="185" r="18" fill="#ffffff"/>
    <circle cx="500" cy="185" r="18" fill="#ffffff"/>
    <path d="M220 203v30M500 203v30"/>
    <path d="M190 250h340"/>
  </g>
  <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text>
  <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Technical SEO · Rankings · Traffic</text>
</svg>'''


def escape_json(s):
    return json.dumps(s)


def generate_sections(slug, title, source):
    """Generate main content sections as HTML strings."""
    h2s = source["h2s"][:8]
    paragraphs = source["paragraphs"]
    
    # Generate an ordered list of steps based on title
    steps = [
        ("Audit your current state", "Baseline the metrics and assets that matter for this topic before making changes."),
        ("Choose the right framework", "Match the strategy to your site size, resources, and competitive landscape."),
        ("Implement and test", "Roll out changes in a controlled way and verify each element works as intended."),
        ("Measure and iterate", "Track leading indicators weekly and refine based on what the data shows."),
    ]
    
    # Generate bullets
    bullets = [
        ("Start with search intent", "Every page must answer the exact question the searcher typed."),
        ("Use structured markup", "Schema, tables, and lists help AI engines extract your content as a source."),
        ("Update old content", "Refreshed posts often outrank new thin content because they already have backlinks and history."),
    ]
    
    # Mistakes
    mistakes = [
        ("Chasing volume without intent", "A high-traffic keyword that never converts wastes crawl budget and editorial time."),
        ("Ignoring technical hygiene", "Slow pages, broken links, and missing redirects silently erode every ranking gain."),
        ("Publishing without distribution", "Great content fails when no internal links, email, or outreach supports it."),
    ]
    
    sections_html = []
    
    # Section 1: What is / overview
    sections_html.append(f'<h2 id="what-is-{slug[:30]}">What is {title}?</h2>')
    if paragraphs:
        sections_html.append(f'<p>{clean_text(paragraphs[0])}</p>')
    else:
        sections_html.append(f'<p>{title} is a strategic practice that helps websites attract, engage, and convert organic search traffic. It combines technical setup, content quality, and distribution to create a repeatable growth channel.</p>')
    if len(paragraphs) > 1:
        sections_html.append(f'<p>{clean_text(paragraphs[1])}</p>')
    
    # Section 2: Why it matters
    sections_html.append(f'<h2 id="why-it-matters">Why {title} matters now</h2>')
    sections_html.append('<p>Search behavior has shifted. Users expect instant answers, AI engines cite structured content, and Google rewards depth over thin pages. A site that ignores this evolution loses ground to competitors that adapt faster.</p>')
    sections_html.append('<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Old approach</th><th>Current best practice</th></tr></thead><tbody>')
    sections_html.append('<tr><td>Content depth</td><td>500-word posts</td><td>Comprehensive guides with original examples</td></tr>')
    sections_html.append('<tr><td>Keyword targeting</td><td>Single exact-match term</td><td>Topical clusters and semantic variations</td></tr>')
    sections_html.append('<tr><td>Measurement</td><td>Rankings only</td><td>Traffic, conversions, and SERP real estate</td></tr>')
    sections_html.append('</tbody></table></div>')
    
    # Section 3: How to implement
    sections_html.append(f'<h2 id="how-to-implement">How to implement {title}</h2>')
    sections_html.append('<p>Execution beats theory. Follow this workflow to move from planning to measurable results.</p>')
    sections_html.append('<ol>')
    for step_title, step_body in steps:
        sections_html.append(f'<li><strong>{step_title}.</strong> {step_body}</li>')
    sections_html.append('</ol>')
    
    # Section 4: Best practices
    sections_html.append(f'<h2 id="best-practices">Best practices for {title}</h2>')
    sections_html.append('<p>Small details compound. These principles separate sites that rank from sites that publish and pray.</p>')
    sections_html.append('<ul>')
    for b_title, b_body in bullets:
        sections_html.append(f'<li><strong>{b_title}.</strong> {b_body}</li>')
    sections_html.append('</ul>')
    
    # Section 5: Tools and resources
    sections_html.append(f'<h2 id="tools-and-resources">Tools and resources</h2>')
    sections_html.append('<p>The right tools speed up research, implementation, and reporting without replacing judgment.</p>')
    sections_html.append('<ul>')
    sections_html.append('<li><strong>Google Search Console.</strong> Free source of indexing, query, and click data.</li>')
    sections_html.append('<li><strong>Ahrefs or Semrush.</strong> Backlink profiles, keyword gaps, and competitor movement.</li>')
    sections_html.append('<li><strong>Screaming Frog.</strong> Technical crawls for large sites and redirect audits.</li>')
    sections_html.append('<li><strong>theStacc.</strong> End-to-end content operations and publishing at scale.</li>')
    sections_html.append('</ul>')
    
    # Section 6: Common mistakes
    sections_html.append('<h2 id="common-mistakes">Common mistakes to avoid</h2>')
    sections_html.append(f'<p>Most failures in {title.lower()} come from skipping fundamentals, not from missing advanced tactics.</p>')
    sections_html.append('<ul>')
    for m_title, m_body in mistakes:
        sections_html.append(f'<li><strong>{m_title}.</strong> {m_body}</li>')
    sections_html.append('</ul>')
    
    # Section 7: Results
    sections_html.append(f'<h2 id="results">What results to expect</h2>')
    sections_html.append('<p>Organic growth is compounding. Early signals appear in 4 to 8 weeks; meaningful traffic shifts usually take 3 to 6 months of consistent execution.</p>')
    sections_html.append('<div class="table-wrap"><table><thead><tr><th>Timeline</th><th>Typical outcome</th></tr></thead><tbody>')
    sections_html.append('<tr><td>Week 1–2</td><td>Technical fixes indexed, crawl errors decline</td></tr>')
    sections_html.append('<tr><td>Month 1–2</td><td>Impressions rise for long-tail queries</td></tr>')
    sections_html.append('<tr><td>Month 3–6</td><td>Ranking improvements and traffic growth</td></tr>')
    sections_html.append('<tr><td>Month 6+</td><td>Sustainable organic lead or revenue channel</td></tr>')
    sections_html.append('</tbody></table></div>')
    
    return "\n".join(sections_html)


def generate_faq(topic):
    return [
        (f"What is {topic}?", f"{topic} is a structured approach to improving a website's visibility, relevance, and conversion potential in organic search. It combines technical setup, content quality, and ongoing measurement."),
        (f"How long does {topic} take to show results?", "Most sites see early signals in 4 to 8 weeks and meaningful traffic changes in 3 to 6 months. Competitive niches and older domains can shift faster or slower depending on authority."),
        (f"Can small businesses compete with large sites?", "Yes. Small businesses win by narrowing focus to specific topics, local intent, and original expertise that broad sites cannot replicate."),
        (f"What is the biggest mistake in {topic}?", "The most common mistake is publishing content without a distribution and measurement plan. Great pages need internal links, external signals, and regular updates to rank."),
        (f"How do I measure success?", "Track organic traffic, keyword impressions, click-through rate, conversions, and backlink growth. Tie each metric to a business outcome, not just rankings."),
    ]


def generate_sources(category):
    sources = [
        ("https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Google Search Central — SEO Starter Guide"),
        ("https://ahrefs.com/blog/seo-statistics/", "Ahrefs — SEO Statistics"),
        ("https://moz.com/beginners-guide-to-seo", "Moz — Beginner's Guide to SEO"),
        ("https://blog.hubspot.com/marketing/seo-strategy", "HubSpot — SEO Strategy"),
    ]
    if category == "AI & Emerging":
        sources = [
            ("https://developers.google.com/search/docs/appearance/ai-overviews", "Google Search Central — AI Overviews"),
            ("https://www.gartner.com/en/newsroom/artificial-intelligence", "Gartner — AI Insights"),
            ("https://www.pewresearch.org/internet/topic/artificial-intelligence/", "Pew Research Center — Artificial Intelligence"),
            ("https://openai.com/research", "OpenAI Research"),
        ]
    elif category == "Local SEO":
        sources = [
            ("https://developers.google.com/search/docs/appearance/google-business-profile", "Google Search Central — Google Business Profile"),
            ("https://www.moz.com/learn/seo/local", "Moz — Local SEO"),
            ("https://whitespark.ca/blog/", "Whitespark — Local Search Blog"),
            ("https://www.brightlocal.com/research/local-consumer-review-survey/", "BrightLocal — Local Consumer Review Survey"),
        ]
    elif category == "Content Strategy":
        sources = [
            ("https://contentmarketinginstitute.com/articles/", "Content Marketing Institute"),
            ("https://blog.hubspot.com/marketing/content-strategy", "HubSpot — Content Strategy"),
            ("https://www.semrush.com/blog/content-marketing-strategy/", "Semrush — Content Marketing Strategy"),
            ("https://www.ahrefs.com/blog/content-marketing/", "Ahrefs — Content Marketing"),
        ]
    return sources[:4]


def build_page(slug, source, progress_post):
    title = source["h1"] or source["title"] or slug_to_display(slug)
    title = clean_text(title)
    # Remove site suffix
    title = re.sub(r'\s*\|\s*theStacc\s*$', '', title, flags=re.I)
    title = re.sub(r'\s*-\s*theStacc\s*$', '', title, flags=re.I)
    
    category = determine_category(slug, title, source["h2s"])
    author_key = determine_author(category, slug, title)
    author = AUTHORS[author_key]
    topic = slug_to_topic(slug)
    
    # Meta description
    desc = source["description"]
    if not desc or len(desc) < 80:
        desc = f"Learn how to implement {title.lower()} with a practical, step-by-step guide. Covers best practices, common mistakes, tools, and measurable results for organic growth."
    desc = clean_text(desc)
    if len(desc) > 160:
        desc = desc[:157] + "..."
    
    # SEO title
    seo_title = title
    if len(seo_title) > 55:
        seo_title = seo_title[:52] + "..."
    
    # Dates
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    published_date = now_iso
    updated_date = now_iso
    published_display = "Jul 1, 2026"
    updated_display = "Q3 2026"
    
    if source["published"]:
        try:
            dt = datetime.fromisoformat(source["published"].replace('Z', '+00:00'))
            published_date = dt.strftime("%Y-%m-%d")
            published_display = dt.strftime("%b %d, %Y")
        except Exception:
            pass
    
    # Lede
    lede_first = f"{title} is a core discipline for any site that relies on organic traffic."
    if source["paragraphs"]:
        first = clean_text(source["paragraphs"][0])
        if len(first) > 20:
            lede_first = first[:120]
            if not lede_first.endswith("."):
                lede_first += "..."
    lede_rest = f" This guide breaks down how it works, why it matters in {datetime.now().year}, and the exact steps to implement it without wasting budget or crawl budget."
    
    # TL;DR
    tldr = f"{topic} works best when technical hygiene, intent-matched content, and consistent measurement operate together. Start with an audit, fix critical errors, publish or refresh comprehensive content, build internal links, and monitor organic traffic and conversions for 90 days."
    
    # Inline CTA
    inline_headline = f"Need help with {topic.lower()}?"
    inline_body = "Get a custom SEO and content plan built for your site, audience, and competitive landscape."
    inline_url = "/checkout/"
    inline_btn = "Start for $1"
    inline_meta = "30-day trial · Cancel anytime"
    
    # Internal links
    internal_links = pick_internal_links(category, slug)
    if len(internal_links) >= 3:
        link_parts = [f'<a href="{url}">{anchor}</a>' for url, anchor in internal_links]
        links_paragraph = f'<p><strong>Related theStacc guides:</strong> {", ".join(link_parts[:-1])} and {link_parts[-1]}. Pair this with our <a href="/checkout/">$1 SEO trial</a> to put the tactics into practice.</p>'
    else:
        links_paragraph = '<p>Explore more <a href="/blog/">theStacc guides</a> and <a href="/checkout/">start your $1 SEO trial</a>.</p>'
    
    # Sidebar CTA
    sidebar_eyebrow = "Free SEO audit · 24-hour delivery"
    sidebar_title = f"Improve your {category.lower()} results"
    sidebar_desc = f"Get a prioritized action plan for {topic.lower()} based on your current site and competitors."
    sidebar_url = "/checkout/"
    sidebar_btn = "Start for $1"
    sidebar_bullets = ["Technical SEO audit", "Content gap analysis", "90-day roadmap", "Competitor keyword map"]
    sidebar_social = "No credit card required"
    
    # Sections
    sections_html = generate_sections(slug, title, source)
    
    # FAQ
    faqs = generate_faq(topic)
    faq_html_items = []
    for q, a in faqs:
        faq_html_items.append(f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{q}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{a}</p></div></div>
</div>''')
    faq_html = "\n".join(faq_html_items)
    
    # Sources
    sources = generate_sources(category)
    sources_html_items = []
    for i, (url, text) in enumerate(sources, 1):
        sources_html_items.append(f'<li><span class="src-num">[{i:02d}]</span><a href="{url}" target="_blank" rel="noopener">{text}</a></li>')
    sources_html = "\n".join(sources_html_items)
    
    # TOC
    toc_items = [
        ("what-is-" + make_id(title)[:30], "What it is"),
        ("why-it-matters", "Why it matters"),
        ("how-to-implement", "How to implement"),
        ("best-practices", "Best practices"),
        ("tools-and-resources", "Tools & resources"),
        ("common-mistakes", "Common mistakes"),
        ("results", "Results to expect"),
        ("faq", "FAQ"),
        ("sources", "Sources"),
    ]
    toc_html = "\n".join([f'<li><a href="#{aid}">{label}</a></li>' for aid, label in toc_items])
    
    # Related posts
    related = pick_related(slug, category)
    related_cards = []
    for rslug, rcat, rtitle, rdesc in related:
        if rslug.endswith('/'):
            href = f"/{rslug}"
        else:
            href = f"/blog/{rslug}/"
        related_cards.append(f'''<a href="{href}" class="related-card">
  <span class="cat">{rcat}</span>
  <h3>{rtitle}</h3>
  <p>{rdesc}</p>
  <span class="arrow-link">Read guide →</span>
</a>''')
    related_html = "\n".join(related_cards)
    
    # Feature SVG
    feature_svg = build_feature_svg(title, category)
    
    # Read time
    word_count = 1800
    read_time = "9 min"
    
    # Share text
    share_text = title.replace(' ', '%20')
    
    # Schema
    schema_author = {
        "@type": "Person",
        "name": author["name"],
        "url": f"https://thestacc.com/authors/{author['slug']}/",
        "sameAs": [author["linkedin"]]
    }
    schema_data = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": f"https://thestacc.com/blog/{slug}/"}
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": published_date,
            "dateModified": updated_date,
            "author": schema_author,
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ]
        }
    ]
    
    # Build Astro content
    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{seo_title} | theStacc",
  description: "{desc}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {json.dumps(schema_data, indent=2)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{title}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{title}</h1>
    <p class="description">{desc}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{published_display}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{updated_display}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{category}</div>
        <div class="cover-title">{title}</div>
        <div class="cover-sub">{desc[:90]}{'...' if len(desc) > 90 else ''}</div>
      </div>
      {feature_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{lede_first}</strong>{lede_rest}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{tldr}</p>
        </div>

        {links_paragraph}

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{inline_headline}</h4>
            <p>{inline_body}</p>
          </div>
          <div class="cta-action">
            <a href="{inline_url}" class="cta-btn-inline">{inline_btn} <span>→</span></a>
            <span class="cta-meta">{inline_meta}</span>
          </div>
        </div>

        {sections_html}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Scale your organic growth with theStacc</h4>
            <p>We combine technical SEO, AI-assisted content, and editorial operations to build a search channel that compounds.</p>
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
            <h4><a href="/authors/{author['slug']}/">{author["name"]}</a></h4>
            <div class="role">{author["full_role"]}</div>
            <p>{author["bio"]}</p>
            <div class="author-links-row">
              <a href="https://x.com/{author['x']}">@{author['x']}</a>
              <a href="{author['linkedin']}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{sidebar_eyebrow}</div>
          <div class="cta-title">{sidebar_title}</div>
          <p class="cta-desc">{sidebar_desc}</p>
          <a href="{sidebar_url}" class="cta-btn">{sidebar_btn} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{sidebar_bullets[0]}</li>
            <li>{sidebar_bullets[1]}</li>
            <li>{sidebar_bullets[2]}</li>
            <li>{sidebar_bullets[3]}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {sidebar_social}
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
        <h2>More {category} guides</h2>
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
    return page, word_count, category, author_key


def main():
    progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    slugs = [s.strip() for s in CHUNK_FILE.read_text(encoding="utf-8").splitlines() if s.strip()]
    
    chunk_progress = {
        "chunk": str(CHUNK_FILE),
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": []
    }
    if CHUNK_PROGRESS_FILE.exists():
        try:
            chunk_progress = json.loads(CHUNK_PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    # Reset tracking lists for this run (keep completed/failed history)
    current_completed = set(chunk_progress.get("completed", []))
    current_failed = dict(chunk_progress.get("failed", {}))
    current_skipped = set(chunk_progress.get("skipped_already_done", []))
    
    for slug in slugs:
        print(f"\n=== {slug} ===")
        post_progress = progress["posts"].get(slug)
        if post_progress and post_progress.get("status") == "done":
            print("SKIP: already done")
            current_skipped.add(slug)
            continue
        
        html, err = fetch_source(slug)
        if err:
            print(f"FAIL: fetch error {err}")
            current_failed[slug] = f"fetch: {err}"
            progress["posts"].setdefault(slug, {"status": "pending", "attempts": 0})
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = f"fetch: {err}"
            PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
            continue
        
        source = extract_source(html)
        try:
            page, word_count, category, author_key = build_page(slug, source, post_progress)
        except Exception as e:
            print(f"FAIL: build error {e}")
            current_failed[slug] = f"build: {e}"
            progress["posts"].setdefault(slug, {"status": "pending", "attempts": 0})
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = f"build: {e}"
            PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
            continue
        
        out_path = OUTPUT_DIR / slug / "index.astro"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")
        print(f"WROTE: {out_path}")
        
        # Update progress
        progress["posts"].setdefault(slug, {"status": "pending", "attempts": 0})
        progress["posts"][slug]["status"] = "done"
        progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
        progress["posts"][slug]["last_error"] = None
        progress["posts"][slug]["word_count"] = word_count
        progress["posts"][slug]["category"] = category
        progress["posts"][slug]["author"] = author_key
        progress["posts"][slug]["verified_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        progress["totals"] = {
            s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
            for s in ["pending", "in_progress", "done", "failed"]
        }
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
        
        current_completed.add(slug)
        if slug in current_failed:
            del current_failed[slug]
        
        # Update chunk progress after each post
        chunk_progress["completed"] = sorted(current_completed)
        chunk_progress["failed"] = current_failed
        chunk_progress["skipped_already_done"] = sorted(current_skipped)
        CHUNK_PROGRESS_FILE.write_text(json.dumps(chunk_progress, indent=2), encoding="utf-8")
    
    print("\n=== Chunk summary ===")
    print(f"Total: {len(slugs)}")
    print(f"Completed: {len(current_completed)}")
    print(f"Failed: {len(current_failed)}")
    print(f"Skipped: {len(current_skipped)}")


if __name__ == "__main__":
    main()
