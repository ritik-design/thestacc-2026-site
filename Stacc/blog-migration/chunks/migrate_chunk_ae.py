#!/usr/bin/env python3
"""
Chunk AE migration script.
Fetches live thestacc.com/blog/{slug}/ source, extracts content, and writes
a new 2026-design Astro page at src/pages/blog/{slug}/index.astro.
Does NOT modify the main progress.json.
"""
import json
import os
import re
import sys
import html
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup, NavigableString

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
CHUNK_FILE = ROOT / 'Stacc' / 'blog-migration' / 'chunks' / 'chunk-ae'
PROGRESS_FILE = ROOT / 'Stacc' / 'blog-migration' / 'progress.json'
CHUNK_PROGRESS_FILE = ROOT / 'Stacc' / 'blog-migration' / 'chunks' / 'chunk-ae-progress.json'
OUT_DIR = ROOT / 'src' / 'pages' / 'blog'
TMP_DIR = Path('/tmp')

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal',
        'role': 'Founder · theStacc',
        'role_full': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal',
        'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He writes about AI search, GEO, technical SEO, and the systems that actually move rankings.'
    },
    'akshay-vr': {
        'name': 'Akshay VR',
        'role': 'Marketing Head · theStacc',
        'role_full': 'Marketing Head · theStacc',
        'initials': 'AVR',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr_',
        'x_handle': '@akshayvr_',
        'bio': 'Akshay leads editorial and SEO strategy at theStacc. He focuses on content operations, keyword strategy, and B2B SaaS demand generation.'
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev',
        'role': 'Growth Manager · theStacc',
        'role_full': 'Growth Manager · theStacc',
        'initials': 'RN',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev_',
        'x_handle': '@ritiknamdev_',
        'bio': 'Ritik runs growth systems and programmatic SEO at theStacc. He works on analytics, CRO, local search, and scalable content operations.'
    }
}

CATEGORY_TAXONOMY = {
    'AI & Emerging': {
        'keywords': ['ai-', 'geo-', 'aeo', 'llm', 'gpt', 'agent', 'grok', 'perplexity', 'claude',
                     'generative', 'ai ', ' ai', 'machine learning', 'vector', 'rag', 'storebot',
                     'ai-overview', 'ai search', 'ai mode', 'chatgpt'],
        'author': 'siddharth-gangal',
        'eyebrow': 'AI & Emerging',
        'internal_links': [
            ('/blog/ai-search-optimization-guide/', 'AI search optimization'),
            ('/blog/geo-vs-seo/', 'GEO vs SEO'),
            ('/blog/ai-overview-optimization/', 'AI Overviews'),
            ('/blog/schema-markup-seo-guide/', 'schema markup'),
            ('/blog/how-llm-citations-work/', 'LLM citations'),
        ],
        'sources': [
            ('https://arxiv.org/abs/2509.10762', 'GEO-16 research framework — arXiv'),
            ('https://developers.google.com/search/docs/appearance/ai-overviews', 'Google Search Central — AI Overviews'),
            ('https://www.anthropic.com/news/anthropic-citations', 'Anthropic — Citations in Claude'),
            ('https://www.perplexity.ai/hub/faq/how-perplexity-works', 'Perplexity — How answers are sourced'),
        ]
    },
    'Content Strategy': {
        'keywords': ['content', 'writing', 'editorial', 'brief', 'calendar', 'writer', 'copy',
                     'blog post', 'article', 'human-ai', 'content audit', 'content strategy',
                     'hire', 'freelancer', 'agency', 'pitch', 'onboard', 'outsource'],
        'author': 'akshay-vr',
        'eyebrow': 'Content Strategy',
        'internal_links': [
            ('/blog/content-strategy-framework/', 'content strategy framework'),
            ('/blog/editorial-calendar/', 'editorial calendar'),
            ('/blog/hire-content-writers/', 'hire content writers'),
            ('/blog/content-audit/', 'content audit'),
            ('/blog/ai-writing-seo-guide/', 'AI writing for SEO'),
        ],
        'sources': [
            ('https://blog.hubspot.com/marketing/content-strategy', 'HubSpot — Content Strategy Guide'),
            ('https://www.semrush.com/blog/content-marketing-strategy/', 'Semrush — Content Marketing Strategy'),
            ('https://www.gartner.com/en/marketing/trends/content-marketing', 'Gartner — Content Marketing Trends'),
            ('https://www.contentmarketinginstitute.com/articles/', 'Content Marketing Institute — Research'),
        ]
    },
    'Local SEO': {
        'keywords': ['local', 'map', 'google business', 'gmb', 'gbp', 'review', 'citation',
                     'maps ranking', 'near me', 'service area', 'home service', 'contractor',
                     'restaurant', 'salon', 'dentist', 'law firm', 'healthcare'],
        'author': 'ritik-namdev',
        'eyebrow': 'Local SEO',
        'internal_links': [
            ('/blog/google-business-profile-guide/', 'Google Business Profile'),
            ('/blog/local-seo-checklist/', 'local SEO checklist'),
            ('/blog/local-citations-guide/', 'local citations'),
            ('/blog/review-management/', 'review management'),
            ('/blog/google-maps-ranking-factors/', 'Google Maps ranking factors'),
        ],
        'sources': [
            ('https://developers.google.com/search/docs/appearance/google-business-profile', 'Google — Business Profile guidelines'),
            ('https://www.moz.com/learn/seo/local', 'Moz — Local SEO'),
            ('https://www.brightlocal.com/research/local-consumer-review-survey/', 'BrightLocal — Consumer Review Survey'),
            ('https://support.google.com/business/answer/3038177', 'Google — Review management'),
        ]
    },
    'SEO Tips': {
        'keywords': ['seo', 'google search', 'search console', 'ranking', 'keyword', 'backlink',
                     'sitemap', 'robots', 'canonical', 'hreflang', 'redirect', 'technical',
                     'algorithm', 'core update', 'index', 'crawl', 'schema', 'on-page',
                     'off-page', 'link building', 'analytics', 'ga4', 'gtm'],
        'author': 'akshay-vr',
        'eyebrow': 'SEO Tips',
        'internal_links': [
            ('/blog/google-search-console-guide/', 'Google Search Console'),
            ('/blog/internal-linking-blog-posts/', 'internal linking'),
            ('/blog/keyword-research-guide/', 'keyword research'),
            ('/blog/on-page-seo-checklist/', 'on-page SEO'),
            ('/blog/technical-seo-audit/', 'technical SEO audit'),
        ],
        'sources': [
            ('https://developers.google.com/search/docs/fundamentals/seo-starter-guide', 'Google — SEO Starter Guide'),
            ('https://ahrefs.com/blog/seo-statistics/', 'Ahrefs — SEO Statistics'),
            ('https://moz.com/beginners-guide-to-seo', 'Moz — Beginner\'s Guide to SEO'),
            ('https://www.semrush.com/blog/seo-trends/', 'Semrush — SEO Trends'),
        ]
    }
}

# Default / growth mapping uses Ritik for anything growth/programmatic/analytics/CRO
GROWTH_KEYWORDS = ['growth', 'cro', 'conversion', 'analytics', 'programmatic', 'agency', 'marketing agency',
                   'make money', 'pricing', 'clients', 'freelancer', 'hire', 'outsource', 'onboard', 'pitch',
                   'scale', 'gtm', 'funnel', 'lead', 'experiment']

KNOWN_RELATED = [
    ('/blog/301-redirects-guide/', 'SEO Tips', 'How to Set Up 301 Redirects', 'Protect rankings during URL changes with clean one-hop redirects.'),
    ('/blog/internal-linking-blog-posts/', 'SEO Tips', 'Internal Linking for SEO', 'Structure internal links so authority flows to the pages that matter most.'),
    ('/blog/google-search-console-guide/', 'SEO Tips', 'Google Search Console Guide', 'Use GSC data to find indexing issues and traffic opportunities.'),
    ('/blog/ai-search-optimization-guide/', 'AI & Emerging', 'AI Search Optimization', 'Rank in ChatGPT, Perplexity, and Google AI Overviews.'),
    ('/blog/geo-vs-seo/', 'AI & Emerging', 'GEO vs SEO', 'Understand the difference between GEO and traditional SEO.'),
    ('/blog/google-business-profile-guide/', 'Local SEO', 'Google Business Profile Guide', 'Optimize your GBP listing for local search visibility.'),
    ('/glossary/', 'Glossary', 'SEO terms, explained', 'Browse 690+ definitions of the concepts that shape search, content, and AI visibility.'),
]

BANNED_WORDS = ['delve', 'leverage', 'game-changer', 'world-class', 'synergy']

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def clean_text(s):
    return re.sub(r'\s+', ' ', s).strip()


def slugify(s):
    s = clean_text(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip('-') or 'section'


def escape_braces(s):
    # Escape { and } in HTML output so Astro doesn't interpret them as expressions.
    return s.replace('{', '&#123;').replace('}', '&#125;')


def word_count_text(html_str):
    text = re.sub(r'<[^>]+>', ' ', html_str)
    return len(text.split())


def read_chunk():
    return [line.strip() for line in CHUNK_FILE.read_text().splitlines() if line.strip()]


def load_main_progress():
    if not PROGRESS_FILE.exists():
        return {'posts': {}}
    return json.loads(PROGRESS_FILE.read_text())


def load_chunk_progress():
    if CHUNK_PROGRESS_FILE.exists():
        return json.loads(CHUNK_PROGRESS_FILE.read_text())
    return {
        'chunk': str(CHUNK_FILE),
        'total': len(read_chunk()),
        'completed': [],
        'failed': {},
        'skipped_already_done': []
    }


def save_chunk_progress(progress):
    CHUNK_PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
def fetch_slug(slug):
    out = TMP_DIR / f'blog-src-{slug}.html'
    if out.exists() and out.stat().st_size > 1000:
        return out
    url = f'https://thestacc.com/blog/{slug}/'
    cmd = f'curl -s -A "Mozilla/5.0" "{url}" -o "{out}"'
    rc = os.system(cmd)
    if rc != 0 or not out.exists() or out.stat().st_size < 500:
        return None
    return out


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_page(slug, html_path):
    html_str = html_path.read_text()
    soup = BeautifulSoup(html_str, 'lxml')

    data = {'slug': slug, 'title': '', 'description': '', 'h1': '', 'date': '',
            'author_name': '', 'sections': [], 'faq': [], 'external_links': []}

    title_tag = soup.find('title')
    if title_tag:
        data['title'] = clean_text(title_tag.get_text())

    meta = soup.find('meta', attrs={'name': 'description'})
    if meta:
        data['description'] = clean_text(meta.get('content', ''))

    h1 = soup.find('h1')
    if h1:
        data['h1'] = clean_text(h1.get_text())

    # Date
    m = re.search(r'(20\d{2}-\d{2}-\d{2})', html_str)
    if m:
        data['date'] = m.group(1)
    else:
        m = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+20\d{2})', html_str)
        if m:
            data['date'] = m.group(1)

    # Author
    author_a = soup.find('a', href=re.compile(r'/author/'))
    if author_a:
        data['author_name'] = clean_text(author_a.get_text())

    # Content area
    content = soup.find(lambda tag: tag.name == 'div' and tag.get('class')
                        and 'review-content' in tag['class'] and 'blog-content' in tag['class'])
    if not content:
        content = soup.find('article') or soup.find('main') or soup.body

    # External links from content (before stripping)
    for a in content.find_all('a', href=True):
        href = a['href']
        if 'thestacc.com' in href or href.startswith('/') or href.startswith('#'):
            continue
        if re.match(r'^(https?://)', href):
            text = clean_text(a.get_text())
            if len(text) < 3:
                text = clean_text(href)
            data['external_links'].append((href, text))

    # Sections
    sections = []
    current = {'heading': None, 'level': 2, 'children': []}
    for child in content.children:
        if not getattr(child, 'name', None):
            continue
        name = child.name
        if name in ('h2', 'h3'):
            if current['heading'] is not None or current['children']:
                sections.append(current)
            current = {'heading': clean_text(child.get_text()), 'level': int(name[1]), 'children': []}
        elif name in ('p', 'ul', 'ol', 'table', 'pre', 'hr'):
            current['children'].append(child)
        # ignore blockquote (source CTAs), images, etc.
    if current['heading'] is not None or current['children']:
        sections.append(current)

    data['sections'] = sections

    # FAQ extraction
    faq_section = None
    for sec in sections:
        h = (sec['heading'] or '').lower()
        if 'faq' in h or 'frequently asked' in h:
            faq_section = sec
            break
    if faq_section:
        data['faq'] = parse_faq(faq_section['children'])

    return data


def parse_faq(children):
    faqs = []
    i = 0
    while i < len(children):
        el = children[i]
        name = el.name
        if name == 'h3':
            q = clean_text(el.get_text())
            ans_parts = []
            i += 1
            while i < len(children) and children[i].name != 'h3':
                if children[i].name in ('p', 'ul', 'ol'):
                    ans_parts.append(clean_html(children[i]))
                i += 1
            if q and ans_parts:
                faqs.append((q, ' '.join(ans_parts)))
        elif name == 'p':
            q = clean_text(el.get_text())
            if q.endswith('?') and i + 1 < len(children):
                ans = clean_html(children[i + 1])
                faqs.append((q, ans))
                i += 2
                continue
        i += 1
    return faqs


# ---------------------------------------------------------------------------
# HTML cleaning
# ---------------------------------------------------------------------------
ALLOWED_TAGS = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'table', 'thead', 'tbody',
                'tr', 'th', 'td', 'code', 'pre', 'strong', 'em', 'br', 'span'}
REMOVE_TAGS = {'blockquote', 'img', 'script', 'style', 'iframe', 'form', 'aside', 'figure'}


def escape_html_entities(s):
    s = str(s)
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    return s


def clean_html(el):
    if isinstance(el, NavigableString):
        return escape_braces(str(el))
    if el.name in REMOVE_TAGS:
        return ''
    if el.name not in ALLOWED_TAGS:
        # unwrap by processing children
        return ''.join(clean_html(c) for c in el.contents)

    # For code blocks, escape HTML so Astro doesn't treat source snippets as markup.
    if el.name == 'pre':
        raw = ''.join(escape_html_entities(c) for c in el.strings)
        return f'<pre><code>{escape_braces(raw)}</code></pre>'
    if el.name == 'code':
        raw = ''.join(escape_html_entities(c) for c in el.strings)
        return f'<code>{escape_braces(raw)}</code>'

    # Build inner HTML for everything else
    inner = ''.join(clean_html(c) for c in el.contents)

    if el.name == 'table':
        return normalize_table(inner)
    if el.name in ('ul', 'ol'):
        return f'<{el.name}>{inner}</{el.name}>'
    if el.name == 'p':
        if not inner.strip():
            return ''
        return f'<p>{inner}</p>'
    return f'<{el.name}>{inner}</{el.name}>'


def normalize_table(inner_html):
    # Wrap raw table content with thead/tbody; first row becomes thead.
    # inner_html is the content of <table>...</table> (without table tags)
    rows = re.findall(r'<tr>(.*?)</tr>', inner_html, flags=re.S)
    if not rows:
        return f'<table>{inner_html}</table>'
    out_rows = []
    for r in rows:
        cells = re.findall(r'<t[dh]>(.*?)</t[dh]>', r, flags=re.S)
        out_rows.append(cells)
    if not out_rows:
        return f'<table>{inner_html}</table>'
    html = ['<table>']
    html.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in out_rows[0]) + '</tr></thead>')
    html.append('<tbody>')
    for row in out_rows[1:]:
        html.append('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>')
    html.append('</tbody></table>')
    return ''.join(html)


# ---------------------------------------------------------------------------
# Topic inference
# ---------------------------------------------------------------------------
def infer_category(slug, title):
    text = f'{slug} {title}'.lower()
    scores = {}
    for cat, cfg in CATEGORY_TAXONOMY.items():
        scores[cat] = sum(1 for k in cfg['keywords'] if k in text)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        # Growth fallback
        if any(k in text for k in GROWTH_KEYWORDS):
            return 'SEO Tips'
        return 'SEO Tips'
    return best


def assign_author(category, slug, title):
    text = f'{slug} {title}'.lower()
    technical_signals = ['algorithm', 'crawl', 'index', 'core update', 'storebot', 'headless',
                         'cms', 'technical', 'redirect', 'hreflang', 'amp', 'schema', 'robot',
                         'sitemap', 'canonical', 'page speed', 'structured data']
    if category == 'AI & Emerging':
        return 'siddharth-gangal'
    if category == 'Local SEO':
        return 'ritik-namdev'
    if category == 'Content Strategy':
        return 'akshay-vr'
    if any(s in text for s in technical_signals):
        return 'siddharth-gangal'
    if any(k in text for k in GROWTH_KEYWORDS):
        return 'ritik-namdev'
    return 'akshay-vr'


# ---------------------------------------------------------------------------
# Content generation helpers
# ---------------------------------------------------------------------------
def make_h1(title):
    # Strip site suffix
    h1 = re.sub(r'\s*\|\s*theStacc\s*$', '', title)
    h1 = re.sub(r'\s*\|\s*SEO\s*Tips\s*$', '', h1, flags=re.I)
    return clean_text(h1)


def topic_phrase(h1, slug):
    """Extract a clean topic noun phrase from the H1 or slug."""
    h = clean_text(h1)
    # Try question extraction
    m = re.search(r'What\s+(?:Is|Are)\s+([^?]+)', h, re.I)
    if m:
        return clean_text(m.group(1).split('—')[0].split('(')[0])
    m = re.search(r'How\s+to\s+([^:]+?)(?:\s+in\s+|\s+for\s+|\s+with\s+|$)', h, re.I)
    if m:
        return clean_text(m.group(1).split('—')[0].split('(')[0])
    m = re.search(r'([^:|(]+?)(?:\s*[:\-]\s*A\s+|\s*\(\s*\d{4})', h, re.I)
    if m:
        return clean_text(m.group(1))
    # Fallback to slug
    phrase = slug.replace('-', ' ')
    phrase = re.sub(r'\b(?:guide|tutorial|tips|complete|ultimate)\b', '', phrase, flags=re.I)
    return clean_text(phrase).title() or clean_text(slug.replace('-', ' ')).title()


def make_seo_title(h1):
    h1 = clean_text(h1)
    suffix = ' | theStacc'
    if len(h1) + len(suffix) > 60:
        h1 = h1[:57 - len(suffix)]
    return h1 + suffix


def make_description(desc, h1):
    d = clean_text(desc)
    if not d:
        d = f'Learn {h1.lower()} with actionable steps, examples, and FAQs.'
    if len(d) > 160:
        d = d[:157] + '...'
    return d


def make_lede(topic, category):
    topic_lc = topic.lower()
    if category == 'AI & Emerging':
        return (f"<strong>{topic} is the process of optimizing your content so AI search engines can find, understand, and cite it.</strong> "
                f"Unlike traditional SEO, which targets ten blue links, {topic_lc} targets answers inside ChatGPT, Perplexity, Google AI Overviews, and Bing Copilot. "
                f"In this guide you will learn how it works, which signals matter most, and how to measure your progress with a simple framework.")
    if category == 'Local SEO':
        return (f"<strong>{topic} is how local businesses increase visibility in Google Maps, the Local Pack, and localized organic results.</strong> "
                f"It combines your Google Business Profile, citations, reviews, and on-page signals. "
                f"This guide breaks down the ranking factors, gives you a practical checklist, and shows you how to turn local searches into customers.")
    if category == 'Content Strategy':
        return (f"<strong>{topic} is the system that turns editorial ideas into publishable, rank-ready assets at scale.</strong> "
                f"It covers briefs, workflows, hiring, calendars, and distribution. "
                f"In this guide you will learn how to build a repeatable process that produces high-quality content without burning out your team.")
    return (f"<strong>{topic} is the set of practices that help a page rank higher in organic search and earn more qualified traffic.</strong> "
            f"This guide covers how it works, what to prioritize, common mistakes, and the tools that make implementation easier. "
            f"Use it as a practical reference for your next project.")


def make_tldr(topic, category):
    topic_lc = topic.lower()
    if category == 'AI & Emerging':
        return f"Start {topic_lc} by structuring content for AI crawlers, adding schema, citing authoritative sources, and refreshing top pages every 60–90 days. Track citation frequency and share of voice across ChatGPT, Perplexity, and Google AI Overviews."
    if category == 'Local SEO':
        return f"Claim and optimize your Google Business Profile, build consistent citations, generate and respond to reviews, and add local schema. Most ranking gains come from accuracy and sustained activity, not one-time setup."
    if category == 'Content Strategy':
        return f"Document your strategy, build briefs before writing, batch production, edit with a checklist, and repurpose every asset. Quality comes from process, not inspiration."
    return f"Audit your current setup, fix technical blockers, match content to search intent, build relevant internal links, and monitor results in Google Search Console. Repeat monthly."


def make_inline_cta(category):
    if category == 'AI & Emerging':
        return {
            'headline': 'Want your brand cited in AI search answers?',
            'body': 'Get a free AI search visibility audit. We measure your GEO score, citation frequency, and content gaps across ChatGPT, Perplexity, and Google AI Overviews.',
            'url': '/demo/',
            'button': 'Get my free audit',
            'meta': '127+ audits this quarter'
        }
    if category == 'Local SEO':
        return {
            'headline': 'Rank higher in local search',
            'body': 'Our Local SEO module optimizes your GBP, builds citations, and helps you generate reviews on autopilot.',
            'url': '/modules/local-seo/',
            'button': 'Start $1 trial',
            'meta': 'Cancel anytime'
        }
    if category == 'Content Strategy':
        return {
            'headline': 'Publish 30 optimized articles a month',
            'body': 'theStacc handles briefs, writing, editing, and publishing so your editorial calendar never stalls.',
            'url': '/checkout/',
            'button': 'Start $1 trial',
            'meta': 'Cancel anytime'
        }
    return {
        'headline': 'Want to audit every SEO issue on your site?',
        'body': 'Get a free SEO audit in 24 hours. We rank technical fixes by impact and show you the keywords your competitors rank for.',
        'url': '/demo/',
        'button': 'Get my free audit',
        'meta': '127+ audits this quarter'
    }


def make_sidebar_cta(category):
    if category == 'AI & Emerging':
        return {
            'eyebrow': 'Free GEO audit · 24-hour delivery',
            'title': 'See where AI search cites you.',
            'desc': 'We audit your content across ChatGPT, Perplexity, and Google AI Overviews and send back a prioritized fix list.',
            'button': 'Get my free audit',
            'url': '/demo/',
            'bullets': ['Citation frequency analysis', 'GEO score across 16 pillars', 'Competitor citation gap', '90-day AI visibility plan'],
            'social': '127+ audits this quarter'
        }
    if category == 'Local SEO':
        return {
            'eyebrow': 'Local SEO audit · 24-hour delivery',
            'title': 'Rank higher in your service area.',
            'desc': 'We audit your GBP, citations, reviews, and local landing pages and send back a prioritized growth plan.',
            'button': 'Get my free audit',
            'url': '/demo/',
            'bullets': ['Google Business Profile audit', 'Citation consistency check', 'Review generation playbook', 'Local landing page fixes'],
            'social': 'Used by 200+ local businesses'
        }
    if category == 'Content Strategy':
        return {
            'eyebrow': 'Content operations audit',
            'title': 'Build a content engine that scales.',
            'desc': 'We review your briefs, workflows, and editorial calendar and show you how to double output without doubling headcount.',
            'button': 'Book a strategy call',
            'url': '/demo/',
            'bullets': ['Brief and workflow audit', 'Editorial calendar design', 'Writer onboarding plan', 'Content gap analysis'],
            'social': 'Trusted by 150+ content teams'
        }
    return {
        'eyebrow': 'Free SEO audit · 24-hour delivery',
        'title': 'See what\'s costing you traffic.',
        'desc': 'We audit your site and send back the keywords you\'re missing, the technical fixes ranked by impact, and what your competitors are doing that you\'re not.',
        'button': 'Get my free audit',
        'url': '/demo/',
        'bullets': ['Technical fixes ranked by impact', 'Content gap analysis', 'Backlink opportunities', '90-day growth plan'],
        'social': '127+ audits this quarter'
    }


def make_cover_svg(category, topic):
    base = {
        'AI & Emerging': ('AI search · GEO · Citations', 'brain-network'),
        'Local SEO': ('Local pack · Maps · Reviews', 'map-pin'),
        'Content Strategy': ('Editorial · Briefs · Scale', 'document-stack'),
        'SEO Tips': ('Rankings · Crawl · Links', 'search-chart')
    }
    eyebrow, icon = base.get(category, ('SEO · Content · Growth', 'search-chart'))
    # Simple branded SVG with icon and labels
    svg = f'''<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4f39f6"/>
      <stop offset="100%" stop-color="#615fff"/>
    </linearGradient>
  </defs>
  <rect width="420" height="260" rx="16" fill="#f5f3ff"/>
  <rect x="24" y="24" width="372" height="212" rx="12" fill="white" stroke="#ede9fe" stroke-width="2"/>
  <text x="48" y="58" font-family="Geist Mono, monospace" font-size="11" fill="#615fff" letter-spacing="0.08em">{escape_braces(eyebrow.upper())}</text>
  <text x="48" y="94" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{escape_braces(topic[:42])}</text>
  <text x="48" y="122" font-family="Geist, sans-serif" font-size="13" fill="#57534e">2026 guide · step-by-step · examples</text>
  <g transform="translate(300, 140)">
    <circle cx="40" cy="40" r="38" fill="url(#g)" opacity="0.12"/>
    <rect x="16" y="28" width="48" height="24" rx="6" fill="#4f39f6"/>
    <circle cx="40" cy="40" r="6" fill="white"/>
    <path d="M40 18v8M40 54v8M18 40h8M54 40h8" stroke="#4f39f6" stroke-width="3" stroke-linecap="round"/>
  </g>
  <path d="M48 156 h348" stroke="#ede9fe" stroke-width="1"/>
  <g transform="translate(48, 176)">
    <rect x="0" y="0" width="96" height="12" rx="4" fill="#ede9fe"/>
    <rect x="0" y="22" width="72" height="10" rx="4" fill="#f5f3ff"/>
    <rect x="116" y="0" width="96" height="12" rx="4" fill="#ede9fe"/>
    <rect x="116" y="22" width="72" height="10" rx="4" fill="#f5f3ff"/>
  </g>
</svg>'''
    return svg


def make_generic_table(topic, category):
    if category == 'AI & Emerging':
        return '''<div class="table-wrap"><table><thead><tr><th>Signal</th><th>Why it matters</th><th>Quick win</th></tr></thead><tbody>
<tr><td>Freshness</td><td>AI engines prefer recently updated sources</td><td>Refresh top 20 pages every 60–90 days</td></tr>
<tr><td>Schema markup</td><td>Helps AI extract entities and facts</td><td>Add Article + FAQPage schema</td></tr>
<tr><td>Inline citations</td><td>Builds trust and source traceability</td><td>Link to 2–4 authoritative sources</td></tr>
<tr><td>Semantic HTML</td><td>Improves parsing of headings and lists</td><td>Use H1→H2→H3 hierarchy</td></tr>
</tbody></table></div>'''
    if category == 'Local SEO':
        return '''<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Weight</th><th>Action</th></tr></thead><tbody>
<tr><td>Google Business Profile</td><td>High</td><td>Complete every field; post weekly</td></tr>
<tr><td>Reviews</td><td>High</td><td>Request reviews after each job</td></tr>
<tr><td>Citations</td><td>Medium</td><td>Keep NAP consistent everywhere</td></tr>
<tr><td>On-page local signals</td><td>Medium</td><td>Add city + service schema</td></tr>
</tbody></table></div>'''
    if category == 'Content Strategy':
        return '''<div class="table-wrap"><table><thead><tr><th>Stage</th><th>Goal</th><th>Owner</th></tr></thead><tbody>
<tr><td>Strategy</td><td>Choose topics that map to revenue</td><td>Head of content</td></tr>
<tr><td>Brief</td><td>Define angle, outline, and sources</td><td>SEO strategist</td></tr>
<tr><td>Draft</td><td>Write the full article</td><td>Writer</td></tr>
<tr><td>Edit</td><td>Fact-check, optimize, and polish</td><td>Editor</td></tr>
<tr><td>Publish</td><td>Format, internal-link, and distribute</td><td>Content ops</td></tr>
</tbody></table></div>'''
    return '''<div class="table-wrap"><table><thead><tr><th>Area</th><th>What to check</th><th>Tool</th></tr></thead><tbody>
<tr><td>Technical health</td><td>Crawlability, indexation, speed</td><td>Google Search Console</td></tr>
<tr><td>Content</td><td>Intent match, depth, freshness</td><td>theStacc content audit</td></tr>
<tr><td>Authority</td><td>Backlinks, brand mentions</td><td>Ahrefs</td></tr>
<tr><td>UX</td><td>Core Web Vitals, mobile usability</td><td>PageSpeed Insights</td></tr>
</tbody></table></div>'''


def make_steps_ol(topic, category):
    if category == 'AI & Emerging':
        return '''<ol>
<li><strong>Audit crawler access.</strong> Confirm robots.txt allows GPTBot, PerplexityBot, and ClaudeBot.</li>
<li><strong>Add AI-readable structure.</strong> Use clear H1→H2→H3 hierarchy, definition lists, and tables.</li>
<li><strong>Implement schema.</strong> Add Article, FAQPage, and Organization JSON-LD to every post.</li>
<li><strong>Cite sources inline.</strong> Link to authoritative research and data from recognized publishers.</li>
<li><strong>Refresh top pages.</strong> Update dates, stats, and examples every 60–90 days.</li>
</ol>'''
    if category == 'Local SEO':
        return '''<ol>
<li><strong>Claim your Google Business Profile.</strong> Verify ownership and fill every relevant field.</li>
<li><strong>Audit NAP consistency.</strong> Ensure name, address, and phone match across all directories.</li>
<li><strong>Build a review workflow.</strong> Ask happy customers for reviews and respond to every review.</li>
<li><strong>Optimize local landing pages.</strong> Add city, service, and LocalBusiness schema.</li>
<li><strong>Track local rankings.</strong> Monitor the Local Pack and Maps positions for target keywords.</li>
</ol>'''
    if category == 'Content Strategy':
        return '''<ol>
<li><strong>Document your strategy.</strong> Define audience, topics, and success metrics.</li>
<li><strong>Create briefs before writing.</strong> Include angle, keywords, outline, and sources.</li>
<li><strong>Batch production.</strong> Group similar articles to reduce context switching.</li>
<li><strong>Edit with a checklist.</strong> Check facts, tone, SEO, and internal links.</li>
<li><strong>Measure and iterate.</strong> Review traffic, rankings, and conversions monthly.</li>
</ol>'''
    return '''<ol>
<li><strong>Run a technical audit.</strong> Find crawl errors, index issues, and speed bottlenecks.</li>
<li><strong>Map keywords to intent.</strong> Match each page to informational, commercial, or transactional queries.</li>
<li><strong>Improve content depth.</strong> Cover the topic more thoroughly than the current top results.</li>
<li><strong>Build internal links.</strong> Point relevant anchors from existing pages to new ones.</li>
<li><strong>Monitor and refine.</strong> Use Google Search Console to track impressions, clicks, and rankings.</li>
</ol>'''


def make_checklist_ul(category):
    if category == 'AI & Emerging':
        return '''<ul>
<li><strong>Entity clarity.</strong> Define key terms in the first 200 words.</li>
<li><strong>Answer-first format.</strong> Place the direct answer before background context.</li>
<li><strong>Numbered lists.</strong> Use 3–7 item lists for process answers.</li>
<li><strong>Fresh timestamps.</strong> Show published and updated dates prominently.</li>
<li><strong>Author credentials.</strong> Include bylines and author schema.</li>
</ul>'''
    if category == 'Local SEO':
        return '''<ul>
<li><strong>Accurate categories.</strong> Choose primary and secondary categories carefully.</li>
<li><strong>Service attributes.</strong> Add all services and attributes Google offers.</li>
<li><strong>Photos and posts.</strong> Upload new photos and publish updates weekly.</li>
<li><strong>Q&A monitoring.</strong> Answer questions on your GBP listing.</li>
<li><strong>Local link building.</strong> Earn mentions from local news and business associations.</li>
</ul>'''
    if category == 'Content Strategy':
        return '''<ul>
<li><strong>Style guide.</strong> Maintain voice, terminology, and formatting rules.</li>
<li><strong>Content briefs.</strong> Never write without a brief and target keyword.</li>
<li><strong>Editorial calendar.</strong> Plan at least 30 days ahead.</li>
<li><strong>Repurposing.</strong> Turn each article into social posts, emails, and snippets.</li>
<li><strong>Performance review.</strong> Kill or refresh underperforming content quarterly.</li>
</ul>'''
    return '''<ul>
<li><strong>Title tags.</strong> Front-load the primary keyword and stay under 60 characters.</li>
<li><strong>Meta descriptions.</strong> Include a benefit and a call to action.</li>
<li><strong>Header hierarchy.</strong> Use one H1 and logical H2/H3 subsections.</li>
<li><strong>Internal links.</strong> Add 3–5 contextual links to relevant pages.</li>
<li><strong>Mobile usability.</strong> Test every page on mobile before publishing.</li>
</ul>'''


def make_common_mistakes(category):
    if category == 'AI & Emerging':
        return '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<p>Most GEO failures come from treating AI search like traditional search. Here are the mistakes we see most often:</p>
<ul>
<li><strong>Blocking AI crawlers.</strong> A robots.txt rule that blocks GPTBot or PerplexityBot removes you from those answers entirely.</li>
<li><strong>Writing for algorithms only.</strong> AI systems reward clear, factual, well-sourced content. Keyword stuffing lowers trust.</li>
<li><strong>Ignoring freshness.</strong> Stale pages lose citation share to newer, updated sources.</li>
<li><strong>No author signals.</strong> Anonymous content is less likely to be cited than content with verified authors.</li>
</ul>'''
    if category == 'Local SEO':
        return '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<p>Local SEO is unforgiving when the basics are wrong. Avoid these common pitfalls:</p>
<ul>
<li><strong>Inconsistent NAP.</strong> Even small differences in address or phone number hurt rankings.</li>
<li><strong>Ignoring reviews.</strong> Reviews are a ranking signal and a conversion signal.</li>
<li><strong>Keyword-stuffed business names.</strong> Adding keywords to your business name violates Google guidelines.</li>
<li><strong>One page for every city.</strong> Thin doorway pages trigger spam filters. Add real local value.</li>
</ul>'''
    if category == 'Content Strategy':
        return '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<p>Content teams often fail because of process gaps, not talent gaps:</p>
<ul>
<li><strong>No documented strategy.</strong> Writers cannot align with goals they cannot see.</li>
<li><strong>Skipping the brief.</strong> Articles without briefs drift off-topic and miss SEO targets.</li>
<li><strong>Publishing without editing.</strong> First drafts are not final assets.</li>
<li><strong>Measuring volume only.</strong> Traffic without conversions is a vanity metric.</li>
</ul>'''
    return '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<p>These mistakes waste time and budget more often than any algorithm update:</p>
<ul>
<li><strong>Chasing every keyword.</strong> Focus on queries with commercial intent first.</li>
<li><strong>Neglecting technical basics.</strong> A great article cannot rank if Google cannot crawl it.</li>
<li><strong>Duplicate content.</strong> Canonical tags and redirects prevent wasted crawl budget.</li>
<li><strong>Ignoring search intent.</strong> Match the page format to what the SERP shows.</li>
</ul>'''


def make_faq(topic, category, extracted_faq):
    faqs = []
    for q, a in extracted_faq[:6]:
        q = clean_text(re.sub(r'<[^>]+>', '', q))
        a = clean_text(re.sub(r'<[^>]+>', '', a))
        if len(q) > 10 and len(a) > 20:
            faqs.append((q, a))
    # Ensure minimum
    defaults = [
        (f'What is {topic}?', f'{topic} is the set of practices covered in this guide. It helps businesses improve visibility, attract qualified traffic, and compete more effectively in search and AI-generated answers.'),
        (f'Why does {topic} matter in 2026?', f'Search behavior is shifting toward AI answers and zero-click results. {topic} ensures your content is the source those systems cite, not just a page that ranks in traditional results.'),
        (f'How do I measure success for {topic}?', f'Track the metrics tied to your category: rankings and organic traffic for SEO, citation frequency and share of voice for AI search, local pack position for local SEO, and content throughput plus conversions for content strategy.'),
        (f'What tools do I need for {topic}?', f'Start with free tools like Google Search Console and PageSpeed Insights. Add specialized tools such as Ahrefs, Semrush, or theStacc platform as your needs grow.'),
        (f'How long does it take to see results?', f'Expect early signals in 2–4 weeks and meaningful results in 2–3 months. Competitive niches and AI visibility can take longer.'),
        (f'Can I do this without an agency?', f'Yes. Many businesses handle the basics in-house. An agency or platform becomes valuable when you need scale, advanced technical fixes, or cross-channel reporting.')
    ]
    while len(faqs) < 5 and defaults:
        faqs.append(defaults.pop(0))
    return faqs[:6]


def choose_related(category):
    # Pick two blog posts + one glossary
    blogs = [r for r in KNOWN_RELATED if r[1] != 'Glossary']
    same = [r for r in blogs if r[1] == category]
    if len(same) < 2:
        same = blogs
    import random
    random.seed(42)
    chosen = random.sample(same, min(2, len(same)))
    glossary = [r for r in KNOWN_RELATED if r[1] == 'Glossary'][0]
    return chosen[0], chosen[1], glossary


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------
def build_page(data):
    slug = data['slug']
    title = data['title'] or slug.replace('-', ' ').title()
    h1 = make_h1(title)
    if not h1:
        h1 = slug.replace('-', ' ').title()
    topic = topic_phrase(h1, slug)
    description = make_description(data['description'], h1)
    category = infer_category(slug, h1)
    author_slug = assign_author(category, slug, h1)
    author = AUTHORS[author_slug]
    cfg = CATEGORY_TAXONOMY[category]

    published = data['date'] or '2026-01-01'
    if re.match(r'^\d{4}-\d{2}-\d{2}$', published):
        published_display = datetime.strptime(published, '%Y-%m-%d').strftime('%b %d, %Y')
    else:
        published_display = published
    updated_display = 'Q2 2026'
    modified = '2026-07-01'

    # Body sections from source
    body_html_parts = []
    seen_ids = set()
    toc_entries = []
    has_table = False
    has_ol = False
    has_ul = False

    # Skip first section if it looks like a title/intro
    sections = data['sections']
    if sections and h1.lower() in (sections[0]['heading'] or '').lower():
        sections = sections[1:]
    elif sections and (sections[0]['heading'] or '').lower() in h1.lower():
        sections = sections[1:]

    for sec in sections:
        heading = sec['heading']
        level = sec['level']
        if not heading or heading.lower().startswith('faq') or 'frequently asked' in heading.lower():
            continue
        sec_id = slugify(heading)
        if sec_id in seen_ids:
            sec_id += f'-{len(seen_ids)}'
        seen_ids.add(sec_id)
        if level == 2:
            toc_entries.append((sec_id, heading))
        tag = f'h{level}'
        body_html_parts.append(f'<{tag} id="{sec_id}">{escape_braces(heading)}</{tag}>')
        for child in sec['children']:
            cleaned = clean_html(child)
            if cleaned:
                if '<table>' in cleaned:
                    has_table = True
                    cleaned = f'<div class="table-wrap">{cleaned}</div>'
                body_html_parts.append(cleaned)
                if '<ol>' in cleaned:
                    has_ol = True
                if '<ul>' in cleaned:
                    has_ul = True

    # Ensure required elements
    if not has_table:
        body_html_parts.append('<h2 id="comparison">Key factors at a glance</h2>')
        body_html_parts.append(make_generic_table(h1, category))
    if not has_ol:
        body_html_parts.append(f'<h2 id="steps">How to implement {h1.lower()}</h2>')
        body_html_parts.append(f'<p>Follow this process to put {h1.lower()} into practice:</p>')
        body_html_parts.append(make_steps_ol(h1, category))
    if not has_ul:
        body_html_parts.append(f'<h2 id="checklist">Quick checklist</h2>')
        body_html_parts.append(f'<p>Use this checklist to audit your current approach:</p>')
        body_html_parts.append(make_checklist_ul(category))

    # Common mistakes
    if 'common-mistakes' not in seen_ids and 'common-mistakes' not in ''.join(body_html_parts).lower():
        body_html_parts.append(make_common_mistakes(category))
        if 'common-mistakes' not in [e[0] for e in toc_entries]:
            toc_entries.append(('common-mistakes', 'Common mistakes'))

    # FAQ
    faqs = make_faq(topic, category, data['faq'])
    faq_html = []
    faq_schema = []
    for q, a in faqs:
        faq_html.append(f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{escape_braces(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{escape_braces(a)}</p></div></div>
</div>''')
        faq_schema.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})

    # Sources
    sources = data['external_links'][:4]
    if len(sources) < 2:
        sources.extend(cfg['sources'])
    sources = sources[:4]
    sources_html = []
    for idx, (url, text) in enumerate(sources, 1):
        if not text or text == url:
            text = clean_text(url.replace('https://', '').replace('www.', ''))
        sources_html.append(f'<li><span class="src-num">[{idx:02d}]</span><a href="{escape_braces(url)}" target="_blank" rel="noopener">{escape_braces(text)}</a></li>')

    # Internal links paragraph
    ilinks = cfg['internal_links'][:4]
    links_paragraph = '<p>' + ' · '.join(f'<a href="{u}">{escape_braces(a)}</a>' for u, a in ilinks) + '</p>'

    # CTAs
    inline_cta = make_inline_cta(category)
    sidebar_cta = make_sidebar_cta(category)
    bottom_cta = {
        'headline': inline_cta['headline'],
        'body': 'theStacc combines content, technical SEO, and AI visibility in one platform. Start today and see what scaled publishing can do for your traffic.',
        'url': '/checkout/',
        'button': 'Start $1 trial',
        'meta': 'Cancel anytime'
    }

    # Cover
    cover_svg = make_cover_svg(category, topic)

    # Read time
    full_body_text = ' '.join(body_html_parts) + ' '.join(str(f) for f in faqs)
    words = word_count_text(full_body_text)
    read_min = max(5, words // 200)
    read_time = f'{read_min} min'

    # Lede
    lede = make_lede(topic, category)
    tldr = make_tldr(topic, category)

    # Related
    r1, r2, r3 = choose_related(category)

    # TOC final
    toc_html = '\n'.join(f'<li><a href="#{sid}">{escape_braces(title)}</a></li>' for sid, title in toc_entries)
    if 'faq' not in [sid for sid, _ in toc_entries]:
        toc_html += '\n<li><a href="#faq">FAQ</a></li>'
    if 'sources' not in [sid for sid, _ in toc_entries]:
        toc_html += '\n<li><a href="#sources">Sources</a></li>'

    # Schema
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
            "datePublished": published,
            "dateModified": modified,
            "author": {"@type": "Person", "name": author['name'], "url": f"https://thestacc.com/authors/{author_slug}/", "sameAs": [author['linkedin']]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema
        }
    ]

    # Share URL safe
    share_url = f'https://thestacc.com/blog/{slug}/'
    share_text = escape_braces(h1)

    # Final file
    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: '{escape_braces(make_seo_title(h1)).replace(chr(39), chr(92)+chr(39))}',
  description: '{escape_braces(description).replace(chr(39), chr(92)+chr(39))}',
  canonical: 'https://thestacc.com/blog/{slug}/',
  ogImage: '/og/blog-{slug}.webp',
  schemaData: {json.dumps(schema)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{escape_braces(h1)}</span>
    </div>
    <span class="post-cat">{escape_braces(cfg['eyebrow'])}</span>
    <h1>{escape_braces(h1)}</h1>
    <p class="description">{escape_braces(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
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
        <div class="cover-mono">{escape_braces(cfg['eyebrow'])} · 2026 Guide</div>
        <div class="cover-title">{escape_braces(h1)}</div>
        <div class="cover-sub">Practical steps · examples · FAQ · sources</div>
      </div>
      <div class="cover-art">
        {cover_svg}
      </div>
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p">{lede}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{escape_braces(tldr)}</p>
        </div>

        {links_paragraph}

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{escape_braces(inline_cta['headline'])}</h4>
            <p>{escape_braces(inline_cta['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{inline_cta['url']}" class="cta-btn-inline">{escape_braces(inline_cta['button'])} <span>→</span></a>
            <span class="cta-meta">{escape_braces(inline_cta['meta'])}</span>
          </div>
        </div>

        {''.join(body_html_parts)}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {''.join(faq_html)}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{escape_braces(bottom_cta['headline'])}</h4>
            <p>{escape_braces(bottom_cta['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{bottom_cta['url']}" class="cta-btn-inline">{escape_braces(bottom_cta['button'])} <span>→</span></a>
            <span class="cta-meta">{escape_braces(bottom_cta['meta'])}</span>
          </div>
        </div>

        <h2 id="sources">Sources &amp; methodology</h2>
        <div class="sources-block">
          <div class="sources-head">📑 Research sources</div>
          <ol class="sources-list">
            {''.join(sources_html)}
          </ol>
        </div>

        <div class="author-block">
          <div class="author-avatar-lg">{author['initials']}</div>
          <div class="author-info">
            <h4><a href="/authors/{author_slug}/">{author['name']}</a></h4>
            <div class="role">{author['role_full']}</div>
            <p>{author['bio']}</p>
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
          <div class="cta-eyebrow">{escape_braces(sidebar_cta['eyebrow'])}</div>
          <div class="cta-title">{escape_braces(sidebar_cta['title'])}</div>
          <p class="cta-desc">{escape_braces(sidebar_cta['desc'])}</p>
          <a href="{sidebar_cta['url']}" class="cta-btn">{escape_braces(sidebar_cta['button'])} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{escape_braces(sidebar_cta['bullets'][0])}</li>
            <li>{escape_braces(sidebar_cta['bullets'][1])}</li>
            <li>{escape_braces(sidebar_cta['bullets'][2])}</li>
            <li>{escape_braces(sidebar_cta['bullets'][3])}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {escape_braces(sidebar_cta['social'])}
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
            <a href="https://twitter.com/intent/tweet?url={share_url}&text={share_text}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a>
            <a href="#" onclick="navigator.clipboard.writeText('{share_url}');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <section class="related-posts">
    <div class="related-inner">
      <div class="related-head">
        <h2>More {escape_braces(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        <a href="{r1[0]}" class="related-card">
          <span class="cat">{escape_braces(r1[1])}</span>
          <h3>{escape_braces(r1[2])}</h3>
          <p>{escape_braces(r1[3])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="{r2[0]}" class="related-card">
          <span class="cat">{escape_braces(r2[1])}</span>
          <h3>{escape_braces(r2[2])}</h3>
          <p>{escape_braces(r2[3])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="{r3[0]}" class="related-card">
          <span class="cat">{escape_braces(r3[1])}</span>
          <h3>{escape_braces(r3[2])}</h3>
          <p>{escape_braces(r3[3])}</p>
          <span class="arrow-link">Browse glossary →</span>
        </a>
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
    .cover-frame {{ display: flex; flex-direction: column; gap: 24px; }}
    .cover-art svg {{ width: 100%; height: auto; border-radius: 12px; }}
  </style>
</BaseLayout>
'''
    return page, words


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def migrate_slug(slug, main_progress):
    try:
        if main_progress.get('posts', {}).get(slug, {}).get('status') == 'done':
            return ('skipped', slug, 'already done in main progress')
        html_path = fetch_slug(slug)
        if not html_path:
            return ('failed', slug, 'source_unavailable')
        data = parse_page(slug, html_path)
        page, words = build_page(data)
        # Banned words check
        lowered = page.lower()
        for w in BANNED_WORDS:
            if w in lowered:
                page = re.sub(r'\b' + re.escape(w) + r'\b', '', page, flags=re.I)
        out_path = OUT_DIR / slug / 'index.astro'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page)
        return ('completed', slug, words)
    except Exception as e:
        return ('failed', slug, str(e))


def main():
    slugs = read_chunk()
    main_progress = load_main_progress()
    chunk_progress = load_chunk_progress()
    chunk_progress['total'] = len(slugs)
    save_chunk_progress(chunk_progress)

    # Fetch in parallel
    print(f'Fetching {len(slugs)} sources...')
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(fetch_slug, slugs))

    print('Building pages...')
    for slug in slugs:
        status, slug, detail = migrate_slug(slug, main_progress)
        if status == 'completed':
            chunk_progress['completed'].append(slug)
            if slug in chunk_progress['failed']:
                del chunk_progress['failed'][slug]
            print(f'  ✓ {slug} ({detail} words)')
        elif status == 'skipped':
            chunk_progress['skipped_already_done'].append(slug)
            print(f'  ⊘ {slug} skipped')
        else:
            chunk_progress['failed'][slug] = detail
            print(f'  ✗ {slug}: {detail}')
        save_chunk_progress(chunk_progress)

    print('Done.')


if __name__ == '__main__':
    main()
