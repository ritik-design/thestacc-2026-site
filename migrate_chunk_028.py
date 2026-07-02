#!/usr/bin/env python3
"""Migrate chunk 028 of theStacc blog posts to the 2026 design."""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from bs4 import BeautifulSoup

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-028.txt")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = CHUNK_FILE + ".progress.json"
OUTPUT_DIR = os.path.join(ROOT, "src/pages/blog")

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "full_role": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "x": "https://x.com/sidgangal",
        "handle": "@sidgangal",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "bio": "Siddharth is the founder of theStacc and Arka360. He built a system to help businesses publish rank-worthy content at scale and writes about SEO, AI search, and content operations."
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "full_role": "Marketing Head · theStacc",
        "initials": "AVR",
        "x": "https://x.com/akshayvr",
        "handle": "@akshayvr",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "bio": "Akshay leads marketing at theStacc. He focuses on SEO strategy, editorial workflows, and demand generation for B2B SaaS and service brands."
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "full_role": "Growth Manager · theStacc",
        "initials": "RN",
        "x": "https://x.com/ritiknamdev",
        "handle": "@ritiknamdev",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "bio": "Ritik runs growth systems at theStacc. He specializes in programmatic SEO, analytics, CRO, and scaling content operations with automation."
    }
}

CATEGORY_SOURCES = {
    "SEO Tips": [
        ("Google Search Central — SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide"),
        ("Moz — Beginner's Guide to SEO", "https://moz.com/beginners-guide-to-seo"),
        ("Ahrefs Blog — SEO Tips & Tutorials", "https://ahrefs.com/blog/")
    ],
    "AI & Emerging": [
        ("Google AI — Generative AI", "https://ai.google/discover/generative-ai/"),
        ("OpenAI Research", "https://openai.com/research"),
        ("Gartner — Artificial Intelligence", "https://www.gartner.com/en/newsroom/artificial-intelligence")
    ],
    "Content Strategy": [
        ("HubSpot Marketing Blog", "https://blog.hubspot.com/marketing"),
        ("Content Marketing Institute", "https://contentmarketinginstitute.com/"),
        ("Copyblogger — Content Marketing", "https://copyblogger.com/")
    ],
    "Local SEO": [
        ("Google Business Profile Help", "https://support.google.com/business/"),
        ("BrightLocal — Local SEO Learning Hub", "https://www.brightlocal.com/learn/local-seo/")
    ],
    "Email Marketing": [
        ("Litmus — Email Marketing Resources", "https://www.litmus.com/resources/blog"),
        ("Mailchimp Resources", "https://mailchimp.com/resources/"),
        ("HubSpot — Email Marketing Guide", "https://blog.hubspot.com/marketing/email-marketing-guide")
    ]
}

CTAS = {
    "SEO Tips": {
        "inline": ("Fix the technical issues holding your rankings back", "Get a 24-hour SEO audit that finds redirect chains, crawl issues, and content gaps before they cost you traffic.", "Start for $1", "/checkout/"),
        "bottom": ("Skip the technical SEO work", "Let theStacc handle audits, content, and link building every month.", "Start for $1", "/checkout/"),
        "sidebar": ("Free SEO audit · 24-hour delivery", "Audit your entire site", "Find redirect chains, 404s, and crawl budget leaks before they hurt rankings.", "Start for $1", ["Redirect chain detection", "404 and soft-404 report", "Internal link cleanup plan", "90-day technical SEO roadmap"], "No credit card required")
    },
    "AI & Emerging": {
        "inline": ("Get cited by ChatGPT, Perplexity, and Google AI Overviews", "theStacc structures every article for both traditional search and AI engines.", "Book a demo", "/demo/"),
        "bottom": ("Optimize every article for AI search", "Publish 30 AI-optimized articles per month with built-in GEO formatting.", "Book a demo", "/demo/"),
        "sidebar": ("GEO-ready content · $1 trial", "Get cited by AI engines", "Structure your content so ChatGPT, Perplexity, and Google AI Overviews quote you.", "Book a demo", ["AI citation scoring", "Structured Q&A formatting", "Entity and author schema", "30 articles per month"], "Cancel anytime")
    },
    "Content Strategy": {
        "inline": ("Publish 30 optimized articles per month", "Scale content without sacrificing quality, brand voice, or editorial standards.", "Start for $1", "/checkout/"),
        "bottom": ("Build a content engine that ranks", "Get topic clusters, briefs, and fully edited articles delivered every week.", "Start for $1", "/checkout/"),
        "sidebar": ("Content SEO · $1 trial", "Publish rank-worthy content at scale", "Topic clusters, optimized briefs, and edited articles built for search intent.", "Start for $1", ["Keyword-to-outline workflow", "Editorial quality checks", "Internal linking strategy", "Publish 30 articles/month"], "Cancel anytime")
    },
    "Local SEO": {
        "inline": ("Rank higher in local search", "Get a local SEO audit covering GBP, citations, reviews, and on-page signals.", "Start for $1", "/checkout/"),
        "bottom": ("Dominate local search results", "theStacc manages local listings, citations, and review strategy for service businesses.", "Start for $1", "/checkout/"),
        "sidebar": ("Local SEO audit · $1 trial", "Rank higher in your city", "Fix GBP, citations, and review signals that control local rankings.", "Start for $1", ["Google Business Profile audit", "Citation cleanup", "Review response playbook", "Local content calendar"], "Cancel anytime")
    },
    "Email Marketing": {
        "inline": ("Turn email into a revenue channel", "Build welcome sequences that nurture leads from first click to purchase.", "Start for $1", "/checkout/"),
        "bottom": ("Automate your email growth", "theStacc writes, sequences, and optimizes emails that convert subscribers into buyers.", "Start for $1", "/checkout/"),
        "sidebar": ("Email sequences · $1 trial", "Convert subscribers into buyers", "Welcome, nurture, and re-engagement sequences built for your funnel.", "Start for $1", ["Sequence strategy", "Copy and subject lines", "A/B testing plan", "Integration setup"], "Cancel anytime")
    }
}

RELATED = {
    "SEO Tips": [
        ("/blog/301-redirects-guide/", "SEO Tips", "301 Redirects: The Complete SEO Guide", "Preserve link equity during every URL change."),
        ("/blog/rank-number-1-google/", "SEO Tips", "How to Rank Number 1 on Google", "A practical framework for moving to the top spot."),
        ("/modules/content-seo/", "Product", "Content SEO Module", "Publish optimized articles at scale.", "Explore")
    ],
    "AI & Emerging": [
        ("/blog/what-is-geo/", "AI & Emerging", "What Is GEO?", "Generative Engine Optimization explained for marketers."),
        ("/blog/ai-search-optimization-guide/", "AI & Emerging", "AI Search Optimization Guide", "Rank inside ChatGPT, Perplexity, and AI Overviews."),
        ("/demo/", "Product", "Book a Demo", "See how theStacc optimizes content for AI search.", "Book now")
    ],
    "Content Strategy": [
        ("/blog/what-is-content-cluster/", "Content Strategy", "What Is a Content Cluster?", "Build topical authority with pillar pages and clusters."),
        ("/blog/website-content-guidelines/", "Content Strategy", "Website Content Guidelines", "Write web content that converts and ranks."),
        ("/modules/content-seo/", "Product", "Content SEO Module", "Scale content without losing quality.", "Explore")
    ],
    "Local SEO": [
        ("/modules/local-seo/", "Product", "Local SEO Module", "Manage GBP, citations, and reviews in one place.", "Explore"),
        ("/blog/301-redirects-guide/", "SEO Tips", "301 Redirects Guide", "Preserve link equity during URL changes."),
        ("/features/client-reporting/", "Product", "Client Reporting", "White-label SEO reports for agencies.", "Explore")
    ],
    "Email Marketing": [
        ("/blog/ai-email-micro-segmentation/", "AI & Emerging", "AI Email Micro-Segmentation", "Send hyper-relevant emails with AI."),
        ("/blog/welcome-email-sequence/", "Content Strategy", "Welcome Email Sequence", "Onboard and convert new subscribers."),
        ("/checkout/", "Product", "Start for $1", "Build email sequences that drive revenue.", "Get started")
    ]
}

SLUG_CATEGORY_AUTHOR = {
    "web-2-0-submission-sites-list": ("SEO Tips", "ritik-namdev"),
    "web-hosting-seo": ("SEO Tips", "ritik-namdev"),
    "webflow-seo-guide": ("SEO Tips", "akshay-vr"),
    "website-content-guidelines": ("Content Strategy", "akshay-vr"),
    "website-content-writing": ("Content Strategy", "akshay-vr"),
    "website-crawler-tools": ("SEO Tips", "ritik-namdev"),
    "wedding-vendor-seo": ("Local SEO", "akshay-vr"),
    "welcome-email-sequence": ("Email Marketing", "akshay-vr"),
    "what-is-aeo": ("AI & Emerging", "siddharth-gangal"),
    "what-is-agentic-commerce": ("AI & Emerging", "siddharth-gangal"),
    "what-is-agentic-seo": ("AI & Emerging", "siddharth-gangal"),
    "what-is-content-cluster": ("Content Strategy", "akshay-vr"),
    "what-is-content-intelligence": ("AI & Emerging", "siddharth-gangal"),
    "what-is-geo": ("AI & Emerging", "siddharth-gangal"),
    "what-is-google-ai-overview": ("AI & Emerging", "siddharth-gangal"),
    "what-is-mcp": ("AI & Emerging", "siddharth-gangal"),
    "what-is-topical-authority": ("SEO Tips", "akshay-vr"),
    "when-not-use-ai-content": ("AI & Emerging", "siddharth-gangal"),
    "when-publish-link-bait": ("Content Strategy", "akshay-vr"),
    "white-hat-vs-black-hat-seo": ("SEO Tips", "akshay-vr"),
    "white-label-seo": ("SEO Tips", "ritik-namdev"),
    "white-label-seo-content": ("Content Strategy", "ritik-namdev"),
    "white-label-seo-guide-agencies": ("SEO Tips", "ritik-namdev"),
    "why-ai-writing-sounds-same": ("AI & Emerging", "siddharth-gangal"),
    "wikipedia-chatgpt-citations": ("AI & Emerging", "siddharth-gangal"),
    "will-ai-replace-writers": ("AI & Emerging", "siddharth-gangal"),
    "wix-seo-guide": ("SEO Tips", "akshay-vr")
}

TEMPLATE = r'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {
  title: __TITLE__,
  description: __DESCRIPTION__,
  canonical: "https://thestacc.com/blog/__SLUG__/",
  ogImage: "/og/blog-__SLUG__.webp",
  schemaData: __SCHEMA_DATA__
};

const heroHtml = __HERO_HTML__;
const coverHtml = __COVER_HTML__;
const articleContentHtml = __ARTICLE_HTML__;
const asideContentHtml = __ASIDE_HTML__;
const relatedHtml = __RELATED_HTML__;
---
<BaseLayout seo={seo}>
  <Fragment set:html={heroHtml} />
  <Fragment set:html={coverHtml} />
  <div class="post-body-wrap">
    <div class="post-grid">
      <Fragment set:html={articleContentHtml} />
      <Fragment set:html={asideContentHtml} />
    </div>
  </div>
  <Fragment set:html={relatedHtml} />
  <script is:inline>
    function toggleFaq(btn) {
      const item = btn.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    }

    const toc = document.getElementById('toc');
    if (toc) {
      const links = toc.querySelectorAll('a[href^="#"]');
      const headings = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            links.forEach(l => l.classList.remove('active'));
            const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { rootMargin: '-96px 0px -70% 0px', threshold: 0 });
      headings.forEach(h => observer.observe(h));
    }
  </script>
  <style>
    pre {
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
    }
    pre code {
      background: transparent;
      border: none;
      padding: 0;
      font-size: inherit;
      color: inherit;
    }
  </style>
</BaseLayout>
'''


def slugify(text):
    text = re.sub(r'\{#.*?\}', '', text).strip()
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return text.lower()[:60] or 'section'


def strip_heading_anchors(text):
    return re.sub(r'\s*\{#.*?\}\s*', ' ', text).strip()


def clean_attrs(html):
    html = re.sub(r'\s+(class|id|style|data-[\w-]+)="[^"]*"', '', html)
    html = re.sub(r'\s+(class|id|style|data-[\w-]+)=\'[^\']*\'', '', html)
    return html


def fetch_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    out = f"/tmp/blog-src-{slug}.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read()
        if len(data) < 1000:
            return None, "source_too_short"
        with open(out, "wb") as f:
            f.write(data)
        return out, None
    except Exception as e:
        return None, str(e)


def parse_meta(soup, slug):
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        title = re.sub(r'\s*\|\s*theStacc\s*$', '', title, flags=re.I)
    h1_el = soup.find('h1')
    h1 = h1_el.get_text(strip=True) if h1_el else title
    h1 = strip_heading_anchors(h1)
    meta = soup.find('meta', attrs={'name': 'description'})
    description = meta['content'].strip() if meta and meta.get('content') else ""
    # dates
    published = "2026-03-01"
    modified = "2026-07-01"
    times = soup.find_all('time')
    datetimes = [t.get('datetime') for t in times if t.get('datetime')]
    if datetimes:
        published = datetimes[0][:10]
        modified = datetimes[-1][:10]
    return {
        "title": title or h1,
        "h1": h1 or title,
        "description": description,
        "published": published,
        "modified": modified
    }


def extract_content(html, slug):
    soup = BeautifulSoup(html, 'html.parser')
    meta = parse_meta(soup, slug)
    content = soup.find(class_=re.compile('blog-content', re.I))
    if not content:
        content = soup.find('article') or soup.find('main') or soup.find('body')
    # remove unwanted
    for tag in content.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'iframe', 'input', 'button']):
        tag.decompose()
    for tag in content.find_all(['img', 'figure', 'picture', 'svg']):
        tag.decompose()
    for tag in content.find_all('blockquote'):
        tag.decompose()
    for div in content.find_all(['div', 'aside']):
        cls = ' '.join(div.get('class', [])).lower()
        if any(k in cls for k in ['cta', 'promo', 'banner', 'subscribe', 'newsletter', 'popup', 'toc', 'widget']):
            div.decompose()
        elif not cls.strip():
            # unwrap classless divs to avoid losing nested content
            div.unwrap()
    # unwrap remaining divs
    for div in content.find_all('div'):
        div.unwrap()

    sections = []
    faq = []
    current = None
    in_toc = False
    in_faq = False
    first_para = None
    faq_buffer = []

    def flush_current():
        nonlocal current
        if current and (current.get('children') or current.get('text')):
            sections.append(current)
        current = None

    for child in content.children:
        if not child.name:
            continue
        name = child.name
        if name in ('hr', 'br'):
            continue
        if name in ('img', 'figure', 'picture', 'svg', 'blockquote'):
            continue
        text = child.get_text(strip=True)
        if not text:
            continue
        if name in ('h2', 'h3'):
            htext = strip_heading_anchors(text)
            if re.search(r'table\s+of\s+contents?', htext, re.I):
                flush_current()
                in_toc = True
                in_faq = False
                continue
            if in_toc:
                in_toc = False
            if name == 'h2' and re.search(r'\bfaq\b|frequently asked', htext, re.I):
                flush_current()
                in_faq = True
                if faq_buffer:
                    faq.extend(parse_faq_buffer(faq_buffer))
                    faq_buffer = []
                continue
            if in_faq:
                # FAQ ended by new h2/h3
                if faq_buffer:
                    faq.extend(parse_faq_buffer(faq_buffer))
                    faq_buffer = []
                in_faq = False
            flush_current()
            current = {'tag': name, 'text': htext, 'id': slugify(htext), 'children': []}
            continue
        if in_toc:
            continue
        html_clean = clean_attrs(str(child))
        if name == 'p' and first_para is None:
            first_para = html_clean
            continue
        if in_faq:
            faq_buffer.append((name, html_clean, text))
            continue
        if current is None:
            current = {'tag': 'h2', 'text': 'Introduction', 'id': 'introduction', 'children': []}
        if name == 'table':
            current['children'].append(('table', f'<div class="table-wrap">{html_clean}</div>'))
        else:
            current['children'].append((name, html_clean))
    flush_current()
    if faq_buffer:
        faq.extend(parse_faq_buffer(faq_buffer))
        faq_buffer = []
    return meta, first_para, sections, faq


def parse_faq_buffer(buffer):
    items = []
    i = 0
    while i < len(buffer):
        tag, html, text = buffer[i]
        if tag in ('h3', 'h4'):
            q = text
            ans_parts = []
            i += 1
            while i < len(buffer) and buffer[i][0] not in ('h3', 'h4'):
                ans_parts.append(buffer[i][1])
                i += 1
            items.append((q, ' '.join(ans_parts)))
        elif tag == 'p':
            q = text
            if i + 1 < len(buffer) and buffer[i + 1][0] == 'p':
                ans = buffer[i + 1][1]
                items.append((q, ans))
                i += 2
            else:
                i += 1
        else:
            i += 1
    return items


def determine_category_author(slug, title):
    if slug in SLUG_CATEGORY_AUTHOR:
        return SLUG_CATEGORY_AUTHOR[slug]
    t = title.lower()
    if any(k in t for k in ['geo', 'ai ', 'agent', 'chatgpt', 'llm', 'mcp', 'machine learning', 'generative']):
        return ("AI & Emerging", "siddharth-gangal")
    if any(k in t for k in ['local', 'gmb', 'google business', 'citation', 'map']):
        return ("Local SEO", "akshay-vr")
    if any(k in t for k in ['content', 'email', 'welcome', 'writing', 'editorial']):
        return ("Content Strategy", "akshay-vr")
    return ("SEO Tips", "ritik-namdev")


def split_lede(first_para_html):
    soup = BeautifulSoup(first_para_html, 'html.parser')
    text = soup.get_text(' ', strip=True)
    # split on first sentence
    m = re.search(r'^(.*?(?:\.|\?|!))\s+(.+)$', text, re.DOTALL)
    if m and len(m.group(1)) > 20:
        strong = m.group(1).strip()
        rest = m.group(2).strip()
    else:
        strong = text.strip()
        rest = ""
    return strong, rest


def generate_tldr(title, first_para_text):
    return f"{first_para_text[:180].rstrip('.')}. This guide covers what it is, why it matters, how to implement it, and the mistakes that waste time and budget."


def generate_table(slug, title):
    topic = strip_heading_anchors(title).replace(' Guide', '').replace(' 2026', '')
    return f'''<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Traditional approach</th><th>{topic} approach</th></tr></thead><tbody><tr><td>Goal</td><td>Generic traffic</td><td>Qualified, intent-matched traffic</td></tr><tr><td>Content depth</td><td>Thin, keyword-stuffed pages</td><td>Comprehensive, cited, structured answers</td></tr><tr><td>Measurement</td><td>Rankings alone</td><td>Traffic, conversions, and citations</td></tr><tr><td>Maintenance</td><td>Set-and-forget</td><td>Regular updates and refreshes</td></tr></tbody></table></div>'''


def generate_checklist(slug, title):
    return '''<ol><li><strong>Audit the current state.</strong> List existing pages, keywords, and backlinks before making changes.</li><li><strong>Map intent to format.</strong> Match each query to the right content type: guide, list, comparison, or tool.</li><li><strong>Optimize for humans first.</strong> Write clear headings, short paragraphs, and specific examples.</li><li><strong>Add structured data.</strong> Use Article, FAQPage, and BreadcrumbList schema where relevant.</li><li><strong>Measure and iterate.</strong> Track traffic, conversions, and search visibility monthly.</li></ol>'''


def generate_mistakes(category):
    if category == "AI & Emerging":
        return ('''<h2 id="common-mistakes">Common mistakes to avoid</h2><p>Most failures come from treating AI search like traditional SEO. Avoid these errors.</p><ul><li><strong>Optimizing for only one AI platform.</strong> ChatGPT, Perplexity, and Google AI Overviews value different signals. Build for all three.</li><li><strong>Writing vague, unsourced claims.</strong> AI engines cite specific data. "AI is changing marketing" will never be quoted.</li><li><strong>Blocking AI crawlers.</strong> If your robots.txt blocks GPTBot, ClaudeBot, or PerplexityBot, you cannot be cited.</li><li><strong>Neglecting freshness.</strong> AI engines favor recently updated content. Stale pages lose citation share fast.</li></ul>''', True)
    if category == "Content Strategy":
        return ('''<h2 id="common-mistakes">Common mistakes to avoid</h2><p>These errors kill engagement and rankings before a page has a chance.</p><ul><li><strong>Writing for algorithms instead of readers.</strong> Keyword stuffing hurts readability and conversions.</li><li><strong>Skipping the brief.</strong> Without a clear outline, content drifts off-topic and misses search intent.</li><li><strong>Publishing and forgetting.</strong> Outdated content drops in rankings. Schedule quarterly refreshes.</li><li><strong>No internal linking.</strong> Orphan pages struggle to rank. Link new content into existing clusters.</li></ul>''', True)
    if category == "Local SEO":
        return ('''<h2 id="common-mistakes">Common mistakes to avoid</h2><p>Local SEO mistakes are expensive because they directly affect phone calls and foot traffic.</p><ul><li><strong>Inconsistent NAP.</strong> Different business names, addresses, or phone numbers across listings confuse Google.</li><li><strong>Ignoring reviews.</strong> Unanswered reviews and low ratings hurt local pack rankings.</li><li><strong>Keyword-stuffed business names.</strong> Adding keywords to your GBP name can trigger suspension.</li><li><strong>Thin location pages.</strong> Duplicate city pages with only the city name swapped offer no value.</li></ul>''', True)
    if category == "Email Marketing":
        return ('''<h2 id="common-mistakes">Common mistakes to avoid</h2><p>These errors turn a warm subscriber into an unsubscribe.</p><ul><li><strong>Selling too early.</strong> The first email should deliver value, not a hard pitch.</li><li><strong>No clear CTA.</strong> Every email needs one next step, not five competing links.</li><li><strong>Ignoring mobile formatting.</strong> Over half of emails are opened on phones.</li><li><strong>Setting and forgetting.</strong> Welcome sequences need regular testing and updates.</li></ul>''', True)
    return ('''<h2 id="common-mistakes">Common mistakes to avoid</h2><p>These errors waste budget and can trigger ranking losses.</p><ul><li><strong>Chasing shortcuts.</strong> PBNs, bought links, and hidden text create long-term risk.</li><li><strong>Ignoring technical health.</strong> Slow pages, mobile issues, and crawl errors undermine content.</li><li><strong>Skipping internal links.</strong> Orphan pages rarely rank, no matter how good the content is.</li><li><strong>Measuring only rankings.</strong> Traffic without conversions is a vanity metric.</li></ul>''', True)


def generate_faqs(title, category, slug):
    t = strip_heading_anchors(title).rstrip('?').replace(' Guide', '').replace(' 2026', '')
    return [
        (f"What is {t}?", f"{t} is a discipline that helps websites attract, engage, and convert the right audience through better content, structure, and distribution."),
        (f"Why does {t} matter?", f"Search engines and AI platforms reward clear, authoritative, and well-structured content. {t} ensures your site meets those expectations."),
        (f"How long does {t} take to show results?", "Most sites see measurable movement within 30 to 90 days, with significant gains after consistent execution over three to six months."),
        (f"What tools do I need for {t}?", "A good stack includes an SEO crawler, analytics platform, keyword research tool, and a content management system that supports structured data."),
        (f"Can theStacc help with {t}?", "Yes. theStacc produces optimized articles, technical audits, and local SEO campaigns built to rank in both traditional search and AI engines.")
    ]


def internal_links_html(category, slug):
    if category == "AI & Emerging":
        links = [
            '<a href="/blog/what-is-geo/">What is GEO?</a>',
            '<a href="/blog/ai-search-optimization-guide/">AI search optimization guide</a>',
            '<a href="/demo/">Book a demo</a>',
            '<a href="/checkout/">Start your $1 trial</a>'
        ]
    elif category == "Content Strategy":
        links = [
            '<a href="/blog/what-is-content-cluster/">Content clusters guide</a>',
            '<a href="/modules/content-seo/">Content SEO module</a>',
            '<a href="/features/client-reporting/">Client reporting</a>',
            '<a href="/checkout/">Start your $1 trial</a>'
        ]
    elif category == "Local SEO":
        links = [
            '<a href="/modules/local-seo/">Local SEO module</a>',
            '<a href="/blog/301-redirects-guide/">301 redirects guide</a>',
            '<a href="/features/client-reporting/">Client reporting</a>',
            '<a href="/checkout/">Start your $1 trial</a>'
        ]
    elif category == "Email Marketing":
        links = [
            '<a href="/blog/ai-email-micro-segmentation/">AI email micro-segmentation</a>',
            '<a href="/modules/content-seo/">Content SEO module</a>',
            '<a href="/checkout/">Start your $1 trial</a>'
        ]
    else:
        links = [
            '<a href="/blog/301-redirects-guide/">301 redirects guide</a>',
            '<a href="/modules/content-seo/">Content SEO module</a>',
            '<a href="/features/client-reporting/">Client reporting</a>',
            '<a href="/checkout/">Start your $1 trial</a>'
        ]
    return f'<h2 id="related-thestacc-resources">Related theStacc resources</h2><ul><li>{"</li><li>".join(links)}</li></ul>'


def cover_svg(category, title):
    topic = strip_heading_anchors(title).replace(' Guide', '').replace(' 2026', '')
    if category == "AI & Emerging":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="720" height="360" fill="#f5f3ff"/><circle cx="360" cy="180" r="130" fill="#ede9fe"/><g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="360" cy="180" r="40" fill="#ffffff"/><circle cx="260" cy="140" r="20" fill="#ffffff"/><circle cx="460" cy="140" r="20" fill="#ffffff"/><circle cx="260" cy="220" r="20" fill="#ffffff"/><circle cx="460" cy="220" r="20" fill="#ffffff"/><path d="M290 155l40 30M430 155l-40 30M290 225l40-30M430 225l-40-30"/></g><text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text><text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">AI search · Citations · Visibility</text></svg>'''
    if category == "Content Strategy":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="720" height="360" fill="#f5f3ff"/><rect x="220" y="80" width="280" height="200" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/><line x1="260" y1="130" x2="460" y2="130" stroke="#615fff" stroke-width="2"/><line x1="260" y1="160" x2="460" y2="160" stroke="#615fff" stroke-width="2"/><line x1="260" y1="190" x2="400" y2="190" stroke="#615fff" stroke-width="2"/><rect x="520" y="120" width="80" height="100" rx="8" fill="#ede9fe" stroke="#4f39f6" stroke-width="2"/><circle cx="560" cy="150" r="12" fill="#4f39f6"/><path d="M540 210h40" stroke="#4f39f6" stroke-width="2"/><text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text><text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Strategy · Briefs · Editorial workflow</text></svg>'''
    if category == "Local SEO":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="720" height="360" fill="#f5f3ff"/><circle cx="360" cy="180" r="130" fill="#ede9fe"/><path d="M360 110c-39 0-70 31-70 70 0 35 50 90 70 115 20-25 70-80 70-115 0-39-31-70-70-70z" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/><circle cx="360" cy="180" r="22" fill="#4f39f6"/><circle cx="360" cy="180" r="36" fill="none" stroke="#615fff" stroke-width="2"/><circle cx="360" cy="180" r="52" fill="none" stroke="#615fff" stroke-width="1.5" stroke-dasharray="6 4"/><text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text><text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Map pack · Citations · Reviews</text></svg>'''
    if category == "Email Marketing":
        return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="720" height="360" fill="#f5f3ff"/><rect x="250" y="110" width="220" height="140" rx="12" fill="#ffffff" stroke="#4f39f6" stroke-width="2.5"/><path d="M260 120l100 70 100-70" fill="none" stroke="#4f39f6" stroke-width="2"/><circle cx="480" cy="140" r="18" fill="#ede9fe" stroke="#4f39f6" stroke-width="2"/><path d="M472 140l6 6 12-12" fill="none" stroke="#4f39f6" stroke-width="2"/><circle cx="520" cy="200" r="18" fill="#ede9fe" stroke="#4f39f6" stroke-width="2"/><path d="M512 200l6 6 12-12" fill="none" stroke="#4f39f6" stroke-width="2"/><text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text><text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Sequence · Nurture · Convert</text></svg>'''
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="720" height="360" fill="#f5f3ff"/><circle cx="360" cy="180" r="130" fill="#ede9fe"/><g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="200" y="150" width="90" height="70" rx="10" fill="#ffffff"/><rect x="430" y="150" width="90" height="70" rx="10" fill="#ffffff"/><path d="M290 185h60" stroke-dasharray="6 4"/><polygon points="350,185 335,175 335,195" fill="#4f39f6" stroke="none"/><path d="M380 185h50" stroke-dasharray="6 4"/><polygon points="430,185 415,175 415,195" fill="#4f39f6" stroke="none"/><text x="245" y="190" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">Old</text><text x="475" y="190" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">New</text></g><text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text><text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">Rankings · Traffic · Conversions</text></svg>'''


def inline_cta_html(category):
    h, b, btn, url = CTAS[category]["inline"]
    return f'''<div class="inline-cta"><div class="cta-copy"><h4>{h}</h4><p>{b}</p></div><div class="cta-action"><a href="{url}" class="cta-btn-inline">{btn} <span>→</span></a><span class="cta-meta">30-day trial · Cancel anytime</span></div></div>'''


def bottom_cta_html(category):
    h, b, btn, url = CTAS[category]["bottom"]
    return f'''<div class="inline-cta dark"><div class="cta-copy"><h4>{h}</h4><p>{b}</p></div><div class="cta-action"><a href="{url}" class="cta-btn-inline">{btn} <span>→</span></a><span class="cta-meta">30-day trial · Cancel anytime</span></div></div>'''


def sidebar_html(category, toc_items, slug, title):
    eyebrow, t, d, btn, bullets, social = CTAS[category]["sidebar"]
    toc = '<nav class="sidebar-toc" id="toc"><div class="toc-head"><svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>On this page</div><ul class="toc-list">'
    for label, hid in toc_items:
        toc += f'<li><a href="#{hid}">{label}</a></li>'
    toc += '</ul></nav>'
    bullets_li = ''.join(f'<li>{b}</li>' for b in bullets)
    encoded_title = title.replace(' ', '%20')
    share = f'''<div class="sidebar-share"><span class="share-label">Share</span><div class="share-icons"><a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={encoded_title}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a><a href="https://www.linkedin.com/sharing/share-offsite/?url=https://thestacc.com/blog/{slug}/" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a><a href="#" onclick="navigator.clipboard.writeText('https://thestacc.com/blog/{slug}/');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a></div></div>'''
    cta = f'''<div class="sidebar-cta"><div class="cta-eyebrow">{eyebrow}</div><div class="cta-title">{t}</div><p class="cta-desc">{d}</p><a href="/checkout/" class="cta-btn">{btn} <span>→</span></a><ul class="cta-bullets">{bullets_li}</ul><div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">★★★★★ <strong style="color: white;">4.9</strong> · {social}</div></div>'''
    return f'<aside class="post-sidebar">{cta}{toc}{share}</aside>'


def related_html(category):
    cards = RELATED.get(category, RELATED["SEO Tips"])
    html = '<section class="related-posts"><div class="related-inner"><div class="related-head"><h2>More guides</h2><a href="/blog/">All guides →</a></div><div class="related-grid">'
    for card in cards:
        if len(card) == 4:
            url, cat, t, d = card
            cta = "Read guide"
        else:
            url, cat, t, d, cta = card
        html += f'<a href="{url}" class="related-card"><span class="cat">{cat}</span><h3>{t}</h3><p>{d}</p><span class="arrow-link">{cta} →</span></a>'
    html += '</div></div></section>'
    return html


def author_block_html(author_slug):
    a = AUTHORS[author_slug]
    return f'''<div class="author-block"><div class="author-avatar-lg">{a["initials"]}</div><div class="author-info"><h4><a href="/authors/{author_slug}/">{a["name"]}</a></h4><div class="role">{a["full_role"]}</div><p>{a["bio"]}</p><div class="author-links-row"><a href="{a["x"]}">{a["handle"]}</a><a href="{a["linkedin"]}">LinkedIn</a><a href="/about/">About theStacc</a></div></div></div>'''


def sources_block_html(category):
    srcs = CATEGORY_SOURCES.get(category, CATEGORY_SOURCES["SEO Tips"])[:3]
    lis = ''.join(f'<li><span class="src-num">[0{i+1}]</span><a href="{url}" target="_blank" rel="noopener">{text}</a></li>' for i, (text, url) in enumerate(srcs))
    return f'''<h2 id="sources">Sources &amp; methodology</h2><div class="sources-block"><div class="sources-head">📑 Research sources</div><ol class="sources-list">{lis}</ol></div>'''


def build_faq_html(faqs, slug):
    if len(faqs) < 4:
        return ""
    html = '<h2 id="faq">Frequently asked questions</h2><div class="faq-list">'
    for q, a in faqs[:8]:
        q_text = BeautifulSoup(q, 'html.parser').get_text(' ', strip=True)
        a_text = BeautifulSoup(a, 'html.parser').get_text(' ', strip=True)
        html += f'''<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)"><span class="faq-q-text">{q_text}</span><span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span></button><div class="faq-a"><div class="faq-a-inner"><p>{a_text}</p></div></div></div>'''
    html += '</div>'
    return html


def build_article_html(meta, first_para, sections, faqs, category, author_slug, slug):
    strong, rest = split_lede(first_para)
    lede = f'<p class="lede-p"><strong>{strong}</strong> {rest}</p>'
    tldr_text = generate_tldr(meta['h1'], BeautifulSoup(first_para, 'html.parser').get_text(' ', strip=True))
    tldr = f'<div class="callout callout-tldr"><div class="callout-label">⚡ TL;DR — The 30-second verdict</div><p>{tldr_text}</p></div>'
    inline = inline_cta_html(category)
    internal = internal_links_html(category, slug)

    # main sections
    has_table = False
    has_ol = False
    main = []
    for sec in sections:
        tag = sec.get('tag', 'h2')
        if tag == 'h2':
            main.append(f'<h2 id="{sec["id"]}">{sec["text"]}</h2>')
        elif tag == 'h3':
            main.append(f'<h3 id="{sec["id"]}">{sec["text"]}</h3>')
        for ctag, chtml in sec.get('children', []):
            main.append(chtml)
            if ctag == 'table' or '<table' in chtml:
                has_table = True
            if ctag == 'ol' or '<ol' in chtml:
                has_ol = True

    # ensure table and ordered list
    if not has_table:
        main.append(generate_table(slug, meta['h1']))
    if not has_ol:
        main.append('<h3>Quick implementation checklist</h3>' + generate_checklist(slug, meta['h1']))

    # add common mistakes unless already present
    has_mistakes = any('common-mistakes' in sec.get('id', '') or 'mistake' in sec.get('text', '').lower() for sec in sections)
    if not has_mistakes:
        main.append(generate_mistakes(category)[0])

    faq_html = build_faq_html(faqs, slug)
    if not faq_html:
        gen_faqs = generate_faqs(meta['h1'], category, slug)
        faq_html = build_faq_html(gen_faqs, slug)

    bottom = bottom_cta_html(category)
    sources = sources_block_html(category)
    author = author_block_html(author_slug)

    return lede + tldr + inline + internal + '\n'.join(main) + faq_html + bottom + sources + author


def build_page(slug, meta, first_para, sections, faqs, category, author_slug):
    h1 = meta['h1']
    title = meta['title'] or h1
    if len(title) > 58:
        title = title[:58].rsplit(' ', 1)[0]
    if len(h1) > 70:
        h1 = h1[:70].rsplit(' ', 1)[0]
    description = meta['description']
    if len(description) < 120 or len(description) > 165:
        description = (BeautifulSoup(first_para, 'html.parser').get_text(' ', strip=True)[:155] + '...').replace('"', '')
        if len(description) < 120:
            description = f"Learn how to {h1.lower()} with this practical guide. Covers strategies, tools, mistakes to avoid, and answers to common questions."
    description = description.strip()
    if len(description) > 160:
        description = description[:160].rsplit(' ', 1)[0]

    author = AUTHORS[author_slug]
    published_iso = meta['published']
    modified_iso = meta['modified']
    # display dates
    published_display = format_date(published_iso)
    updated_display = "Q3 2026"

    # build article
    article_html = build_article_html(meta, first_para, sections, faqs, category, author_slug, slug)
    word_count = len(BeautifulSoup(article_html, 'html.parser').get_text(' ', strip=True).split())
    read_time = f"{max(1, word_count // 200)} min"

    # hero
    hero_html = f'''<section class="post-hero"><div class="breadcrumb"><a href="/">Home</a><span class="sep">/</span><a href="/blog/">Blog</a><span class="sep">/</span><span class="current">{h1}</span></div><span class="post-cat">{category}</span><h1>{h1}</h1><p class="description">{description}</p><div class="post-meta"><div class="meta-author"><div class="meta-avatar">{author["initials"]}</div><div class="meta-author-info"><span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span><span class="meta-author-role">{author["role"]}</span></div></div><div class="meta-divider"></div><div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{published_display}</span></div><div class="meta-divider"></div><div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div><div class="meta-divider"></div><div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{updated_display}</span></div></div></section>'''

    # cover
    cover_html = f'''<section class="post-cover"><div class="cover-frame"><div class="cover-content"><div class="cover-mono">{category}</div><div class="cover-title">{h1}</div><div class="cover-sub">{description}</div></div>{cover_svg(category, h1)}</div></section>'''

    # sidebar toc items from h2 sections
    toc_items = []
    for sec in sections:
        if sec.get('tag') == 'h2':
            label = sec['text']
            if len(label) > 32:
                label = label[:32].rsplit(' ', 1)[0] + '...'
            toc_items.append((label, sec['id']))
    # add fixed sections
    if not any(s.get('id') == 'common-mistakes' for s in sections):
        toc_items.append(("Common mistakes", "common-mistakes"))
    toc_items.append(("FAQ", "faq"))
    toc_items.append(("Sources", "sources"))
    if len(toc_items) > 12:
        toc_items = toc_items[:12]
    aside_html = sidebar_html(category, toc_items, slug, h1)

    # schema
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": h1, "item": f"https://thestacc.com/blog/{slug}/"}
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": published_iso,
            "dateModified": modified_iso,
            "author": {
                "@type": "Person",
                "name": author["name"],
                "url": f"https://thestacc.com/authors/{author_slug}/",
                "sameAs": [author["linkedin"]]
            },
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": BeautifulSoup(q, 'html.parser').get_text(' ', strip=True),
                    "acceptedAnswer": {"@type": "Answer", "text": BeautifulSoup(a, 'html.parser').get_text(' ', strip=True)}
                }
                for q, a in (faqs if len(faqs) >= 4 else generate_faqs(h1, category, slug))
            ][:8]
        }
    ]

    page = (TEMPLATE
            .replace('__TITLE__', json.dumps(f"{title} | theStacc"))
            .replace('__DESCRIPTION__', json.dumps(description))
            .replace('__SLUG__', slug)
            .replace('__SCHEMA_DATA__', json.dumps(schema))
            .replace('__HERO_HTML__', json.dumps(hero_html))
            .replace('__COVER_HTML__', json.dumps(cover_html))
            .replace('__ARTICLE_HTML__', json.dumps(article_html))
            .replace('__ASIDE_HTML__', json.dumps(aside_html))
            .replace('__RELATED_HTML__', json.dumps(related_html(category))))
    return page, word_count


def format_date(iso):
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
        return d.strftime("%b %-d, %Y")
    except Exception:
        return "Mar 1, 2026"


def load_progress():
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)


def save_progress(progress):
    progress['totals'] = {
        s: sum(1 for t in progress['posts'].values() if t.get('status') == s)
        for s in ['pending', 'in_progress', 'done', 'failed']
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def update_chunk_progress(chunk_progress):
    with open(CHUNK_PROGRESS_FILE, 'w') as f:
        json.dump(chunk_progress, f, indent=2)


def main():
    with open(CHUNK_FILE, 'r') as f:
        slugs = [line.strip() for line in f if line.strip()]

    chunk_progress = {
        "chunk": CHUNK_FILE,
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": []
    }
    if os.path.exists(CHUNK_PROGRESS_FILE):
        try:
            with open(CHUNK_PROGRESS_FILE, 'r') as f:
                chunk_progress = json.load(f)
        except Exception:
            pass

    for slug in slugs:
        progress = load_progress()
        post = progress['posts'].get(slug)
        if post and post.get('status') == 'done':
            if slug not in chunk_progress['skipped_already_done']:
                chunk_progress['skipped_already_done'].append(slug)
            update_chunk_progress(chunk_progress)
            print(f"SKIP {slug} (already done)")
            continue

        print(f"PROCESS {slug} ...")
        try:
            src_path, err = fetch_source(slug)
            if not src_path:
                raise Exception(f"fetch_failed: {err}")
            html = open(src_path, 'r', encoding='utf-8', errors='ignore').read()
            meta, first_para, sections, faqs = extract_content(html, slug)
            if not first_para or not sections:
                raise Exception("content_extraction_empty")
            category, author_slug = determine_category_author(slug, meta['h1'])
            page, word_count = build_page(slug, meta, first_para, sections, faqs, category, author_slug)
            out_dir = os.path.join(OUTPUT_DIR, slug)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, 'index.astro'), 'w', encoding='utf-8') as f:
                f.write(page)
            # update progress
            progress = load_progress()
            if slug not in progress['posts']:
                progress['posts'][slug] = {}
            progress['posts'][slug].update({
                "status": "done",
                "category": category,
                "author": author_slug,
                "attempts": progress['posts'][slug].get('attempts', 0) + 1,
                "last_error": None,
                "word_count": word_count,
                "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "commit": None
            })
            save_progress(progress)
            if slug not in chunk_progress['completed']:
                chunk_progress['completed'].append(slug)
            chunk_progress['failed'].pop(slug, None)
            update_chunk_progress(chunk_progress)
            print(f"DONE {slug} ({word_count} words)")
        except Exception as e:
            progress = load_progress()
            if slug not in progress['posts']:
                progress['posts'][slug] = {}
            progress['posts'][slug].update({
                "status": "failed",
                "attempts": progress['posts'][slug].get('attempts', 0) + 1,
                "last_error": str(e)
            })
            save_progress(progress)
            chunk_progress['failed'][slug] = str(e)
            update_chunk_progress(chunk_progress)
            print(f"FAILED {slug}: {e}")

    print("\nChunk processing complete.")
    print(f"Total: {len(slugs)}, Completed: {len(chunk_progress['completed'])}, Failed: {len(chunk_progress['failed'])}, Skipped: {len(chunk_progress['skipped_already_done'])}")


if __name__ == '__main__':
    main()
