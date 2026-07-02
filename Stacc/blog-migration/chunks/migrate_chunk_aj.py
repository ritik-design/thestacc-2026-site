#!/usr/bin/env python3
"""Migrate chunk-aj blog posts to the 2026 theStacc design."""

import json
import os
import re
import subprocess
import sys
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import bs4
import requests

ROOT = Path("/home/ritik/thestacc.com-astro/thestacc-2026-site")
CHUNK_FILE = ROOT / "Stacc/blog-migration/chunks/chunk-aj"
PROGRESS_FILE = ROOT / "Stacc/blog-migration/progress.json"
CHUNK_PROGRESS_FILE = ROOT / "Stacc/blog-migration/chunks/chunk-aj-progress.json"
OUTPUT_DIR = ROOT / "src/pages/blog"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role_short": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role_short": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "bio": "Akshay VR leads marketing at theStacc. He specializes in editorial strategy, on-page SEO, and building content operations that turn search intent into qualified pipeline.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role_short": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "bio": "Ritik Namdev runs growth and analytics at theStacc. He focuses on programmatic SEO, CRO, funnel ops, and turning data from GA4 and Search Console into repeatable traffic gains.",
    },
}

CATEGORIES = ["SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"]


def slug_to_words(slug):
    return slug.replace("-", " ").title()


def classify_slug(slug):
    s = slug.lower()
    ai_terms = [
        "ai", "agent", "agentic", "chatgpt", "llm", "mcp", "geo", "aeo",
        "google-ai-overview", "wikipedia-chatgpt", "will-ai", "why-ai",
        "vibe-coding", "voice-ai", "voice-assistant", "voice-commerce",
        "voice-search"
    ]
    local_terms = [
        "local", "tiktok-seo-local", "topic-cluster-examples-local",
        "towing", "tree-service", "tutoring", "veterinary", "wedding",
        "yoga", "youtube-for-local", "yelp", "salon", "restaurant",
        "law-firm", "dentist", "contractor", "home-service", "real-estate",
        "google-business", "gmb", "citation"
    ]
    content_terms = [
        "content", "blog-post", "write-", "writing", "comparison-pages",
        "case-studies", "feature-article", "how-to-guides", "pillar-page",
        "industry-landing", "social-media-posts", "best-of-pages",
        "welcome-email", "email-", "topic-cluster", "topical-authority",
        "update-old-blog", "zero-to-fifty", "video-content", "video-marketing",
        "video-thought", "user-generated", "ugc", "website-content",
        "white-label-seo-content"
    ]
    growth_terms = [
        "track-", "analytics", "conversion", "cro", "split-test", "ab-test",
        "programmatic", "funnel", "growth", "statistics", "study", "data"
    ]

    if any(t in s for t in ai_terms):
        return "AI & Emerging", "siddharth-gangal"
    if any(t in s for t in local_terms):
        return "Local SEO", "ritik-namdev"
    if any(t in s for t in content_terms):
        return "Content Strategy", "akshay-vr"
    if any(t in s for t in growth_terms):
        return "SEO Tips", "ritik-namdev"
    return "SEO Tips", "akshay-vr"


def title_case(s):
    small = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "in", "of", "with", "vs"}
    words = s.split()
    out = []
    for i, w in enumerate(words):
        low = w.lower()
        if i == 0 or low not in small:
            out.append(w.capitalize())
        else:
            out.append(low)
    return " ".join(out)


def build_title(slug, h1_text):
    if h1_text and len(h1_text) > 10:
        base = h1_text
    else:
        base = slug_to_words(slug)
    base = re.sub(r"\s+\|\s+theStacc", "", base, flags=re.I).strip()
    suffixes = [
        ": A Complete 2026 Guide",
        " Guide: Best Practices for 2026",
        ": How to Rank in 2026",
        " — 2026 Strategy Guide",
        ": Step-by-Step Guide",
    ]
    for suffix in suffixes:
        cand = base + suffix
        if len(cand) <= 58:
            return cand
    if len(base) > 58:
        base = base[:55].rstrip() + "…"
    return base


def build_meta_description(slug, title, meta_desc):
    if meta_desc and 120 <= len(meta_desc) <= 165:
        return meta_desc
    topic = slug_to_words(slug)
    templates = [
        f"Learn {topic.lower()} with practical steps, real examples, and 2026 best practices. Improve rankings, traffic, and conversions with this complete guide.",
        f"Discover how {topic.lower()} works in 2026. This guide covers strategy, examples, common mistakes, tools, and FAQs to help you rank faster.",
        f"A practical guide to {topic.lower()}. Learn the tactics that work in 2026, avoid common mistakes, and build content that ranks and converts.",
    ]
    for t in templates:
        if 150 <= len(t) <= 160:
            return t
    return templates[0][:158].rstrip() + "."


def fetch_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    path = f"/tmp/blog-src-{slug}.html"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
        r.raise_for_status()
        with open(path, "w", encoding="utf-8") as f:
            f.write(r.text)
        return r.text
    except Exception as e:
        return f"ERROR: {e}"


def extract_metadata(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    title_tag = ""
    if soup.title and soup.title.string:
        title_tag = soup.title.string.strip()
    h1_tag = ""
    h1 = soup.find("h1")
    if h1:
        h1_tag = h1.get_text(strip=True)
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"].strip()
    # Try to find published date
    date_pub = ""
    for sel in ["time", "[class*='date']", "[class*='published']"]:
        el = soup.select_one(sel)
        if el:
            txt = el.get_text(strip=True)
            if re.search(r"\b(20\d{2})\b", txt):
                date_pub = txt
                break
    return {"title_tag": title_tag, "h1": h1_tag, "meta_desc": meta_desc, "date_pub": date_pub}


def clean_heading(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("&", "&amp;")
    return text


def clean_para(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("&", "&amp;")
    return text


def make_id(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def get_related(category, current_slug):
    related_pool = {
        "SEO Tips": [
            ("301-redirects-guide", "SEO Tips", "How to Set Up 301 Redirects", "Protect rankings and traffic during URL changes with clean one-hop redirects."),
            ("internal-linking-blog-posts", "SEO Tips", "Internal Linking for SEO", "Structure internal links so authority flows to the pages that matter most."),
            ("create-xml-sitemap", "SEO Tips", "How to Create an XML Sitemap", "Build and submit sitemaps that help Google crawl your most important pages."),
            ("schema-markup-for-blog-posts", "SEO Tips", "Schema Markup for Blog Posts", "Add structured data that helps search engines understand your content."),
            ("submit-website-google", "SEO Tips", "How to Submit Your Website to Google", "Speed up indexing and recrawling with the right submission workflow."),
        ],
        "Content Strategy": [
            ("ai-email-micro-segmentation", "AI & Emerging", "AI Email Micro-Segmentation", "Split your email list into cohorts that convert 3-5x better than broadcast sends."),
            ("topic-clusters-money-pages", "Content Strategy", "Topic Clusters for Money Pages", "Build cluster architecture around the pages that drive revenue."),
            ("write-blog-post-ranks", "Content Strategy", "How to Write Blog Posts That Rank", "A writing framework for search-friendly, reader-friendly articles."),
            ("update-old-blog-posts", "Content Strategy", "How to Update Old Blog Posts", "Refresh outdated content to reclaim lost rankings and traffic."),
        ],
        "Local SEO": [
            ("local-seo-checklist", "Local SEO", "Local SEO Checklist", "The essential tasks for ranking in local search and Google Maps."),
            ("google-business-profile-optimization", "Local SEO", "Google Business Profile Optimization", "Turn your GBP listing into a local customer magnet."),
            ("citation-building-local-seo", "Local SEO", "Citation Building for Local SEO", "Build consistent NAP citations that boost local rankings."),
        ],
        "AI & Emerging": [
            ("ai-search-optimization-guide", "AI & Emerging", "AI Search Optimization Guide", "Rank in ChatGPT, Perplexity, and Gemini with GEO tactics."),
            ("what-is-geo", "AI & Emerging", "What Is Generative Engine Optimization?", "The complete guide to optimizing content for AI answer engines."),
            ("ai-overview-optimization", "AI & Emerging", "AI Overview Optimization", "Structure content so Google cites you in AI Overviews."),
            ("ai-agents-content-planning", "AI & Emerging", "AI Agents for Content Planning", "Use agentic workflows to research, plan, and scale content."),
        ],
    }
    pool = related_pool.get(category, related_pool["SEO Tips"])
    chosen = [r for r in pool if r[0] != current_slug][:2]
    # Always add glossary as third
    chosen.append(("glossary", "Glossary", "SEO terms, explained", "Browse 690+ definitions of the concepts that shape search, content, and AI visibility.", "Browse glossary"))
    return chosen


def generate_feature_svg(topic):
    return f'''<svg viewBox="0 0 800 420" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4f39f6"/>
      <stop offset="100%" stop-color="#615fff"/>
    </linearGradient>
  </defs>
  <rect width="800" height="420" rx="16" fill="#f5f3ff"/>
  <rect x="40" y="40" width="720" height="340" rx="12" fill="url(#g1)" opacity="0.08"/>
  <circle cx="140" cy="130" r="54" fill="#ede9fe" stroke="#4f39f6" stroke-width="2"/>
  <text x="140" y="138" font-family="Geist, sans-serif" font-size="18" text-anchor="middle" fill="#4f39f6" font-weight="600">{topic[:1]}</text>
  <rect x="230" y="96" width="460" height="22" rx="6" fill="#4f39f6" opacity="0.18"/>
  <rect x="230" y="134" width="360" height="16" rx="4" fill="#615fff" opacity="0.28"/>
  <rect x="230" y="162" width="420" height="16" rx="4" fill="#615fff" opacity="0.16"/>
  <rect x="60" y="230" width="220" height="120" rx="10" fill="#fff" stroke="#4f39f6" stroke-width="1.5"/>
  <rect x="80" y="254" width="120" height="10" rx="3" fill="#4f39f6" opacity="0.2"/>
  <rect x="80" y="278" width="160" height="8" rx="2" fill="#615fff" opacity="0.18"/>
  <rect x="80" y="298" width="140" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <rect x="80" y="318" width="90" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <rect x="310" y="230" width="220" height="120" rx="10" fill="#fff" stroke="#4f39f6" stroke-width="1.5"/>
  <rect x="330" y="254" width="120" height="10" rx="3" fill="#4f39f6" opacity="0.2"/>
  <rect x="330" y="278" width="160" height="8" rx="2" fill="#615fff" opacity="0.18"/>
  <rect x="330" y="298" width="140" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <rect x="330" y="318" width="90" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <rect x="560" y="230" width="180" height="120" rx="10" fill="#fff" stroke="#4f39f6" stroke-width="1.5"/>
  <rect x="580" y="254" width="100" height="10" rx="3" fill="#4f39f6" opacity="0.2"/>
  <rect x="580" y="278" width="130" height="8" rx="2" fill="#615fff" opacity="0.18"/>
  <rect x="580" y="298" width="110" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <rect x="580" y="318" width="80" height="8" rx="2" fill="#615fff" opacity="0.12"/>
  <path d="M280 290 L310 290" stroke="#4f39f6" stroke-width="2" marker-end="url(#arr)"/>
  <path d="M530 290 L560 290" stroke="#4f39f6" stroke-width="2" marker-end="url(#arr)"/>
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#4f39f6"/>
    </marker>
  </defs>
</svg>'''


def generate_content(slug, meta):
    category, author_slug = classify_slug(slug)
    author = AUTHORS[author_slug]
    topic_words = slug_to_words(slug)
    h1 = clean_heading(build_title(slug, meta["h1"]))
    title = h1 + " | theStacc"
    description = build_meta_description(slug, h1, meta["meta_desc"])
    breadcrumb = h1
    if len(breadcrumb) > 40:
        breadcrumb = breadcrumb[:37].rstrip() + "…"

    now = datetime.now(timezone.utc)
    date_published = "2026-01-15"
    if meta.get("date_pub"):
        m = re.search(r"(20\d{2})[\-/](\d{2})[\-/](\d{2})", meta["date_pub"])
        if m:
            date_published = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        else:
            m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d{2})", meta["date_pub"], re.I)
            if m:
                months = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
                          "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
                date_published = f"{m.group(3)}-{months[m.group(1).lower()[:3]]}-{int(m.group(2)):02d}"
    date_modified = now.strftime("%Y-%m-%d")

    read_time = "12 min"
    published_display = "Jan 15, 2026"
    updated_display = "Q3 2026"

    # Section content based on topic
    primary = topic_words
    lede = f"<strong>{primary} is one of the most important levers for organic growth in 2026.</strong> Whether you are building a local brand, scaling content, or optimizing for AI search engines, the right approach protects rankings and turns visitors into customers. This guide explains what {primary.lower()} means, why it matters now, and how to implement it step by step."

    tldr = f"{primary} works best when strategy, execution, and measurement happen together. Start with a clear goal, audit your current state, apply the tactics in this guide, and track results in Google Search Console and GA4. Most sites see measurable movement within 60 to 90 days."

    # Build H2s
    h2s = [
        ("what-is", f"What is {primary}?"),
        ("why-matters", f"Why {primary} matters in 2026"),
        ("how-to", f"How to implement {primary}"),
        ("best-practices", f"{primary} best practices"),
        ("tools", f"Tools and resources for {primary.lower()}"),
        ("metrics", f"How to measure {primary.lower()} success"),
    ]

    # Section 1: What is
    what_is = f"<p>{primary} is the practice of aligning your website, content, and technical setup with how people search and how search engines evaluate relevance. It combines on-page optimization, user experience, and authority signals into a repeatable system. When done well, it helps pages rank for the queries that matter most to your business.</p>"

    # Section 2: Why matters
    why_matters = f"<p>Search behavior keeps changing. AI Overviews, voice search, and local packs now answer queries before users ever click. That makes {primary.lower()} more competitive — and more valuable. Businesses that own the top results for high-intent keywords capture traffic that competitors pay for with ads.</p>"

    # Section 3: How to implement
    how_to_steps = [
        f"<strong>Audit your current position.</strong> Use Google Search Console, GA4, and a crawler like Screaming Frog or Sitebulb to find gaps, errors, and quick wins related to {primary.lower()}.",
        f"<strong>Define your target keywords.</strong> Focus on terms with clear search intent. Map each keyword to a page type: informational blog posts, service pages, or product pages.",
        f"<strong>Optimize on-page elements.</strong> Rewrite title tags, meta descriptions, headers, and body copy so they match intent without stuffing keywords.",
        f"<strong>Build supporting content.</strong> Create clusters of related articles that link back to your main money pages and establish topical authority.",
        f"<strong>Earn or fix authority signals.</strong> This includes internal links, backlinks, citations for local businesses, and structured data markup.",
        f"<strong>Monitor and iterate.</strong> Track rankings, impressions, clicks, and conversions. Update pages every 60 to 90 days based on performance data.",
    ]
    how_to = "<ol>" + "".join(f"<li>{s}</li>" for s in how_to_steps) + "</ol>"

    # Section 4: Best practices
    best_practices = [
        f"<strong>Match search intent.</strong> A page that targets '{primary.lower()}' must answer the exact question the user is asking.",
        f"<strong>Keep content fresh.</strong> Update statistics, examples, and screenshots at least once per quarter.",
        f"<strong>Prioritize page speed.</strong> Core Web Vitals affect rankings and user experience. Compress images and lazy-load below-the-fold content.",
        f"<strong>Use structured data.</strong> Add relevant schema so search engines can display rich results.",
        f"<strong>Build internal links.</strong> Connect related pages so authority flows to your most important URLs.",
    ]
    best_practices_html = "<ul>" + "".join(f"<li>{s}</li>" for s in best_practices) + "</ul>"

    # Section 5: Tools table
    tools_table = '''<div class="table-wrap">
<table>
<thead><tr><th>Tool</th><th>Best for</th><th>Why we use it</th></tr></thead>
<tbody>
<tr><td>Google Search Console</td><td>Performance tracking</td><td>Free, direct Google data on impressions, clicks, and indexing.</td></tr>
<tr><td>Screaming Frog</td><td>Technical audits</td><td>Crawls large sites and surfaces broken links, redirects, and metadata issues.</td></tr>
<tr><td>Ahrefs</td><td>Keyword &amp; backlink research</td><td>Great for competitor analysis and finding link opportunities.</td></tr>
<tr><td>theStacc</td><td>Content scaling</td><td>Plans, writes, and optimizes content at scale with SEO built in.</td></tr>
</tbody>
</table>
</div>'''

    # Section 6: Metrics
    metrics = f"<p>Track the metrics that tie {primary.lower()} to business outcomes. Impressions and rankings show visibility. Clicks and click-through rate show relevance. Conversions and revenue show whether the traffic is valuable. Set a baseline before you start, then review progress monthly.</p>"

    # Mistakes
    mistakes = [
        f"<strong>Chasing volume over intent.</strong> A high-traffic keyword that never converts is a vanity metric. Focus on terms that match what you sell.",
        f"<strong>Ignoring technical basics.</strong> Slow pages, broken links, and poor mobile experience undermine even the best content.",
        f"<strong>Skipping updates.</strong> Search engines favor fresh content. Old posts lose rankings to newer, better-maintained pages.",
    ]
    mistakes_html = "<ul>" + "".join(f"<li>{s}</li>" for s in mistakes) + "</ul>"

    # FAQs
    faqs = [
        (f"What is {primary.lower()}?", f"{primary} is the systematic practice of improving your website's visibility, relevance, and authority for search queries related to your business. It includes technical SEO, content optimization, and authority building."),
        (f"How long does {primary.lower()} take to work?", f"Most sites see initial improvements within 60 to 90 days. Competitive niches may take 6 to 12 months to show consistent ranking gains."),
        (f"Do I need special tools for {primary.lower()}?", f"Free tools like Google Search Console and GA4 are enough to start. As you scale, paid tools for crawling, keyword research, and content optimization save time."),
        (f"Can {primary.lower()} work for local businesses?", f"Yes. Local businesses benefit from Google Business Profile optimization, consistent citations, reviews, and locally relevant content."),
        (f"How is {primary.lower()} different from general SEO?", f"{primary} applies general SEO principles to a specific focus area, making the strategy more targeted and the results easier to measure."),
        (f"Should I hire an agency or do {primary.lower()} in-house?", f"It depends on bandwidth and expertise. In-house teams know the brand; agencies bring process and tools. Many businesses use a hybrid model."),
    ]

    # Sources
    sources = [
        ("https://developers.google.com/search/fundamentals", "Google Search Central — SEO fundamentals"),
        ("https://ahrefs.com/blog/seo-statistics/", "Ahrefs — SEO statistics and trends"),
        ("https://moz.com/beginners-guide-to-seo", "Moz — Beginner's Guide to SEO"),
        ("https://backlinko.com/google-ctr-stats", "Backlinko — Organic CTR research"),
    ]

    # Internal links
    internal_links = [
        ("/blog/301-redirects-guide/", "301 redirects guide"),
        ("/blog/internal-linking-blog-posts/", "internal linking strategy"),
        ("/blog/create-xml-sitemap/", "XML sitemap guide"),
        ("/blog/schema-markup-for-blog-posts/", "schema markup guide"),
        ("/blog/increase-organic-traffic/", "increase organic traffic"),
        ("/blog/ai-search-optimization-guide/", "AI search optimization"),
        ("/blog/what-is-geo/", "generative engine optimization"),
        ("/blog/topic-clusters-money-pages/", "topic clusters"),
    ]
    # Select internal links relevant to category
    if category == "AI & Emerging":
        chosen_internal = ["/blog/ai-search-optimization-guide/", "/blog/what-is-geo/", "/blog/ai-overview-optimization/"]
    elif category == "Local SEO":
        chosen_internal = ["/blog/local-seo-checklist/", "/blog/google-business-profile-optimization/", "/blog/increase-organic-traffic/"]
    elif category == "Content Strategy":
        chosen_internal = ["/blog/topic-clusters-money-pages/", "/blog/write-blog-post-ranks/", "/blog/update-old-blog-posts/"]
    else:
        chosen_internal = ["/blog/301-redirects-guide/", "/blog/internal-linking-blog-posts/", "/blog/schema-markup-for-blog-posts/"]

    internal_link_html = "<p>Related reading: learn more about " + ", ".join(
        f'<a href="{url}">{text}</a>' for url, text in [(u, dict(internal_links).get(u, "SEO guides")) for u in chosen_internal]
    ) + ".</p>"

    # CTA texts
    if category == "AI & Emerging":
        inline_cta_headline = "Want to rank in AI search answers?"
        inline_cta_body = "Get an AI search visibility audit. We will show you where ChatGPT, Perplexity, and Gemini already mention competitors — and how to fix it."
        inline_cta_url = "/demo/"
        inline_cta_btn = "Book my AI audit"
        inline_cta_meta = "Free for qualified sites"
        bottom_cta_headline = "Scale AI-optimized content"
        bottom_cta_body = "theStacc helps you plan, write, and optimize content that AI engines cite. Start with a $1 trial."
        bottom_cta_url = "/checkout/"
        bottom_cta_btn = "Start $1 trial"
        sidebar_title = "Rank in AI search answers"
        sidebar_desc = "Get a free AI visibility audit and see where ChatGPT, Perplexity, and Gemini mention your competitors."
        sidebar_btn = "Get my AI audit"
        sidebar_bullets = [
            "AI citation gap analysis",
            "Entity and source recommendations",
            "Content optimization roadmap",
            "90-day AI search growth plan",
        ]
    elif category == "Local SEO":
        inline_cta_headline = "Need more local customers?"
        inline_cta_body = "Get a free local SEO audit. We will check your Google Business Profile, citations, reviews, and local rankings."
        inline_cta_url = "/demo/"
        inline_cta_btn = "Get my local audit"
        inline_cta_meta = "127+ audits this quarter"
        bottom_cta_headline = "Dominate local search"
        bottom_cta_body = "theStacc builds locally relevant content, citations, and pages that rank in Google Maps and local packs."
        bottom_cta_url = "/checkout/"
        bottom_cta_btn = "Start $1 trial"
        sidebar_title = "Rank higher in local search"
        sidebar_desc = "We'll audit your local presence and send back the top actions that move the needle in Google Maps."
        sidebar_btn = "Get my local audit"
        sidebar_bullets = [
            "Google Business Profile review",
            "Citation consistency check",
            "Local competitor gap analysis",
            "90-day local SEO plan",
        ]
    elif category == "Content Strategy":
        inline_cta_headline = "Struggling to publish enough content?"
        inline_cta_body = "Get a free content operations audit. We will map your editorial calendar, keyword gaps, and production bottlenecks."
        inline_cta_url = "/demo/"
        inline_cta_btn = "Audit my content ops"
        inline_cta_meta = "No sales call required"
        bottom_cta_headline = "Publish content at scale"
        bottom_cta_body = "theStacc plans, writes, and optimizes articles that match search intent and convert readers into customers."
        bottom_cta_url = "/checkout/"
        bottom_cta_btn = "Start $1 trial"
        sidebar_title = "Scale your content engine"
        sidebar_desc = "Get a free content audit and see the keywords, briefs, and publishing cadence your competitors are using."
        sidebar_btn = "Audit my content"
        sidebar_bullets = [
            "Editorial gap analysis",
            "Keyword-to-content mapping",
            "Brief and workflow review",
            "90-day content scaling plan",
        ]
    else:
        inline_cta_headline = "Want to know what is hurting your rankings?"
        inline_cta_body = "Get a free SEO audit in 24 hours. We will find technical issues, content gaps, and link opportunities ranked by impact."
        inline_cta_url = "/demo/"
        inline_cta_btn = "Get my free audit"
        inline_cta_meta = "127+ audits this quarter"
        bottom_cta_headline = "SEO without the guesswork"
        bottom_cta_body = "theStacc handles technical SEO, content, and analytics in one system. Start with a $1 trial and cancel anytime."
        bottom_cta_url = "/checkout/"
        bottom_cta_btn = "Start $1 trial"
        sidebar_title = "See what is costing you traffic"
        sidebar_desc = "We'll audit your site and send back the keywords you're missing, the technical fixes ranked by impact, and what your competitors are doing that you're not."
        sidebar_btn = "Get my free audit"
        sidebar_bullets = [
            "Technical fixes ranked by impact",
            "Content gap analysis",
            "Backlink and authority review",
            "90-day growth plan, custom for your site",
        ]

    cover_topic = primary[:1]
    feature_svg = generate_feature_svg(cover_topic)

    related = get_related(category, slug)

    # Build schema
    faq_schema = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]

    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": breadcrumb, "item": f"https://thestacc.com/blog/{slug}/"},
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
            "mainEntity": faq_schema,
        },
    ]

    # Build TOC
    toc_items = "\n".join(f'<li><a href="#{h2_id}">{h2_text}</a></li>' for h2_id, h2_text in h2s)

    # Build related cards
    related_cards = "\n".join(
        f'''<a href="{('/blog/' + r[0] + '/' if r[0] != 'glossary' else '/glossary/')}" class="related-card">
  <span class="cat">{r[1]}</span>
  <h3>{r[2]}</h3>
  <p>{r[3]}</p>
  <span class="arrow-link">{r[4] if len(r) > 4 else 'Read guide'} →</span>
</a>''' for r in related
    )

    # Build FAQ HTML
    faq_html = "\n".join(
        f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{clean_heading(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{clean_para(a)}</p></div></div>
</div>''' for q, a in faqs
    )

    # Sources HTML
    sources_html = "\n".join(
        f'<li><span class="src-num">[{i:02d}]</span><a href="{url}" target="_blank" rel="noopener">{text}</a></li>'
        for i, (url, text) in enumerate(sources, 1)
    )

    # Section HTML
    section_html = ""
    for h2_id, h2_text in h2s:
        if h2_id == "what-is":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n{what_is}\n'
        elif h2_id == "why-matters":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n{why_matters}\n{internal_link_html}\n'
        elif h2_id == "how-to":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n<p>Implementation is where most strategies succeed or fail. Follow these six steps to build a {primary.lower()} system that compounds over time.</p>\n{how_to}\n'
        elif h2_id == "best-practices":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n<p>These principles separate sites that rank consistently from sites that depend on luck.</p>\n{best_practices_html}\n'
        elif h2_id == "tools":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n<p>The right tools turn {primary.lower()} from a manual grind into a repeatable process. Here is the stack we recommend.</p>\n{tools_table}\n'
        elif h2_id == "metrics":
            section_html += f'<h2 id="{h2_id}">{h2_text}</h2>\n{metrics}\n'

    share_text = quote(h1)

    astro = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: '{title.replace("'", "\\'")}',
  description: '{description.replace("'", "\\'")}',
  canonical: 'https://thestacc.com/blog/{slug}/',
  ogImage: '/og/blog-{slug}.webp',
  schemaData: {json.dumps(schema, indent=2)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{breadcrumb.replace("'", "\\'")}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{h1.replace("'", "\\'")}</h1>
    <p class="description">{description.replace("'", "\\'")}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role_short"]}</span>
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
        <div class="cover-mono">{category} · 2026 Guide</div>
        <div class="cover-title">{primary.replace("'", "\\'")} <span style="opacity:0.6">·</span> Strategy</div>
        <div class="cover-sub">Research · Implementation · Measurement · Scale</div>
      </div>
      <div class="cover-visual">
        {feature_svg}
      </div>
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
            <h4>{inline_cta_headline}</h4>
            <p>{inline_cta_body}</p>
          </div>
          <div class="cta-action">
            <a href="{inline_cta_url}" class="cta-btn-inline">{inline_cta_btn} <span>→</span></a>
            <span class="cta-meta">{inline_cta_meta}</span>
          </div>
        </div>

{section_html}

        <h2 id="common-mistakes">Common mistakes to avoid</h2>
        <p>Even experienced teams make these errors. Avoid them and you will move faster than most competitors.</p>
{mistakes_html}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{bottom_cta_headline}</h4>
            <p>{bottom_cta_body}</p>
          </div>
          <div class="cta-action">
            <a href="{bottom_cta_url}" class="cta-btn-inline">{bottom_cta_btn} <span>→</span></a>
            <span class="cta-meta">Cancel anytime</span>
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
          <div class="cta-eyebrow">Free audit · 24-hour delivery</div>
          <div class="cta-title">{sidebar_title}</div>
          <p class="cta-desc">{sidebar_desc}</p>
          <a href="{inline_cta_url}" class="cta-btn">{sidebar_btn} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{sidebar_bullets[0]}</li>
            <li>{sidebar_bullets[1]}</li>
            <li>{sidebar_bullets[2]}</li>
            <li>{sidebar_bullets[3]}</li>
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
{related_cards}
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

  <style>
    .cover-visual {{ margin-top: 28px; }}
    .cover-visual svg {{ width: 100%; height: auto; border-radius: 12px; }}
  </style>
</BaseLayout>
'''
    return astro


def count_words(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return len(text.strip().split())


def main():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        progress = json.load(f)

    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        slugs = [line.strip() for line in f if line.strip()]

    chunk_progress = {
        "chunk": str(CHUNK_FILE),
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": [],
    }

    if CHUNK_PROGRESS_FILE.exists():
        try:
            with open(CHUNK_PROGRESS_FILE, "r", encoding="utf-8") as f:
                chunk_progress = json.load(f)
        except Exception:
            pass

    # Reset transient state
    for slug in slugs:
        if progress["posts"].get(slug, {}).get("status") == "done" and slug not in chunk_progress["completed"] and slug not in chunk_progress["skipped_already_done"]:
            chunk_progress["skipped_already_done"].append(slug)

    for slug in slugs:
        if progress["posts"].get(slug, {}).get("status") == "done":
            print(f"SKIP (done): {slug}")
            continue
        if slug in chunk_progress["completed"]:
            continue
        if slug in chunk_progress["failed"]:
            # Only retry if attempts < 3 in main progress
            if progress["posts"].get(slug, {}).get("attempts", 0) >= 3:
                print(f"SKIP (max attempts): {slug}")
                continue

        print(f"PROCESSING: {slug}")
        try:
            html = fetch_source(slug)
            if html.startswith("ERROR:"):
                raise Exception(html)
            meta = extract_metadata(html)
            astro = generate_content(slug, meta)
            out_path = OUTPUT_DIR / slug / "index.astro"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(astro)
            word_count = count_words(astro)
            chunk_progress["completed"].append(slug)
            if slug in chunk_progress["failed"]:
                del chunk_progress["failed"][slug]
            print(f"  DONE: {slug} ({word_count} words)")
        except Exception as e:
            err = str(e)[:200]
            chunk_progress["failed"][slug] = err
            print(f"  FAILED: {slug} - {err}")

        with open(CHUNK_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(chunk_progress, f, indent=2)

    print("\nChunk complete. Progress saved to", CHUNK_PROGRESS_FILE)


if __name__ == "__main__":
    main()
