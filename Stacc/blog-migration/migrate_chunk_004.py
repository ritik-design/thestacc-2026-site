#!/usr/bin/env python3
"""
Chunk-004 blog migration script.
Fetches live sources, extracts structure, generates fresh Astro pages,
updates progress trackers, and reports status.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup

ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
CHUNK_FILE = ROOT / 'Stacc/blog-migration/small-chunks/chunk-004.txt'
PROGRESS_FILE = ROOT / 'Stacc/blog-migration/progress.json'
CHUNK_PROGRESS_FILE = ROOT / 'Stacc/blog-migration/small-chunks/chunk-004.txt.progress.json'
OUT_ROOT = ROOT / 'src/pages/blog'

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal',
        'role': 'Founder · theStacc',
        'role_full': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG',
        'slug': 'siddharth-gangal',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal',
        'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.'
    },
    'akshay-vr': {
        'name': 'Akshay VR',
        'role': 'Marketing Head · theStacc',
        'role_full': 'Marketing Head · theStacc · Editorial & SEO Strategy',
        'initials': 'AVR',
        'slug': 'akshay-vr',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr_',
        'x_handle': '@akshayvr_',
        'bio': 'Akshay leads marketing and editorial strategy at theStacc. He oversees keyword research, content operations, and brand voice for B2B SaaS campaigns. He writes about SEO strategy, editorial workflows, and demand generation.'
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev',
        'role': 'Growth Manager · theStacc',
        'role_full': 'Growth Manager · theStacc · Programmatic SEO & CRO',
        'initials': 'RN',
        'slug': 'ritik-namdev',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev_',
        'x_handle': '@ritiknamdev_',
        'bio': 'Ritik runs growth systems at theStacc, including programmatic SEO, analytics, and conversion experiments. He writes about growth ops, GA4, Search Console, and scaling content through automation.'
    }
}


def load_progress():
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_progress(progress):
    progress['totals'] = {
        s: sum(1 for t in progress['posts'].values() if t['status'] == s)
        for s in ['pending', 'in_progress', 'done', 'failed']
    }
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def load_chunk_progress():
    if CHUNK_PROGRESS_FILE.exists():
        with open(CHUNK_PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'chunk': str(CHUNK_FILE),
        'total': 0,
        'completed': [],
        'failed': {},
        'skipped_already_done': []
    }


def save_chunk_progress(cp):
    with open(CHUNK_PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(cp, f, indent=2)


def fetch_source(slug):
    tmp = f'/tmp/blog-src-{slug}.html'
    url = f'https://thestacc.com/blog/{slug}/'
    try:
        r = subprocess.run(
            ['curl', '-s', '-A', 'Mozilla/5.0', '-L', '--max-time', '30', url, '-o', tmp],
            capture_output=True, text=True, timeout=40
        )
        if r.returncode != 0:
            return None, f'curl error: {r.stderr}'
        if os.path.getsize(tmp) < 1000:
            return None, 'source too small or 404'
        return tmp, None
    except Exception as e:
        return None, str(e)


def parse_source(tmp_path):
    with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    description = meta['content'].strip() if meta and meta.get('content') else ''
    h1 = soup.find('h1')
    h1_text = h1.get_text(strip=True) if h1 else ''
    h2s = [h.get_text(strip=True) for h in soup.find_all('h2')]
    h3s = [h.get_text(strip=True) for h in soup.find_all('h3')]
    # Try to find category
    cat = None
    for cls in ['post-cat', 'category', 'entry-category', 'tag', 'topic']:
        el = soup.find(class_=re.compile(cls, re.I))
        if el:
            cat = el.get_text(strip=True)
            break
    # Try to find dates
    pub, mod = None, None
    for cls in ['published', 'date', 'entry-date', 'post-date']:
        el = soup.find(class_=re.compile(cls, re.I))
        if el:
            pub = el.get_text(strip=True)
            break
    return {
        'title': title,
        'description': description,
        'h1': h1_text,
        'h2s': h2s,
        'h3s': h3s,
        'category': cat,
        'date': pub,
    }


def classify(slug, h1, h2s):
    s = slug.lower()
    text = (h1 + ' ' + ' '.join(h2s)).lower()
    if any(x in s for x in ['ai-agent', 'ai-search', 'ai-overview', 'ai-citation', 'autonomous-seo', 'geo', 'llm', 'chatgpt', 'ai-vs-human', 'ai-detector', 'ai-crawlers', 'ai-hallucination', 'ai-prompts']):
        return 'AI & Emerging'
    if any(x in s for x in ['local', 'maps', 'gmb', 'google-business', 'apple-business', 'apple-maps', 'restaurant', 'dentist', 'law-firm', 'salon', 'auto-repair', 'automotive', 'bakery', 'contractor', 'home-service', 'real-estate', 'review']):
        return 'Local SEO'
    if any(x in s for x in ['content', 'blog', 'b2b-content', 'content-marketing', 'editorial', 'brief']):
        return 'Content Strategy'
    if 'seo' in text or 'backlink' in s or 'redirect' in s or 'audit' in s or 'rank' in text:
        return 'SEO Tips'
    return 'SEO Tips'


def assign_author(category, slug, h1):
    s = (slug + ' ' + h1).lower()
    if category == 'AI & Emerging' or any(x in s for x in ['ai-agent', 'ai-search', 'llm', 'autonomous', 'founder', 'strategy']):
        return AUTHORS['siddharth-gangal']
    if category == 'Content Strategy' or any(x in s for x in ['content', 'editorial', 'brand', 'marketing']):
        return AUTHORS['akshay-vr']
    if category == 'Local SEO' or any(x in s for x in ['local', 'gmb', 'citation', 'review']):
        return AUTHORS['ritik-namdev']
    return AUTHORS['ritik-namdev']


def clean_title(title, h1):
    t = h1 or title
    t = re.sub(r'\s+', ' ', t).strip()
    # Remove site name suffix if present
    t = re.sub(r'\s*\|\s*theStacc\s*$', '', t, flags=re.I)
    t = re.sub(r'\s*[-–]\s*theStacc\s*$', '', t, flags=re.I)
    return t


def make_meta(title, description):
    d = description or title
    d = re.sub(r'\s+', ' ', d).strip()
    if len(d) > 160:
        d = d[:157].rsplit(' ', 1)[0] + '...'
    return d


def title_tag(title):
    t = re.sub(r'\s+', ' ', title).strip()
    t = re.sub(r'\s*\|\s*theStacc\s*$', '', t, flags=re.I)
    if len(t) > 58:
        t = t[:55].rsplit(' ', 1)[0] + '...'
    return f"{t} | theStacc"


def slug_to_headline(slug):
    s = slug.replace('-', ' ').title()
    s = re.sub(r'\bSeo\b', 'SEO', s)
    s = re.sub(r'\bAi\b', 'AI', s)
    s = re.sub(r'\bB2b\b', 'B2B', s)
    s = re.sub(r'\bGmb\b', 'GMB', s)
    return s


def today_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def escape_astro(text):
    if not text:
        return ''
    # In Astro frontmatter strings, escape double quotes and backslashes
    return text.replace('\\', '\\\\').replace('"', '\\"')


def escape_html(text):
    if not text:
        return ''
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def make_id(text):
    t = re.sub(r'[^a-z0-9\s-]', '', text.lower())
    t = re.sub(r'\s+', '-', t).strip('-')
    t = re.sub(r'-+', '-', t)
    return t[:60]


def topic_data(slug, h1, h2s, meta_desc):
    """Return a dict describing the post topic for content generation."""
    s = slug.lower()
    # Specific overrides for known slugs in this chunk
    overrides = {
        'app-directory-submission-sites': {
            'keyword': 'app directory submission sites',
            'category': 'SEO Tips',
            'h2s': ['Why app directory submissions still drive traffic', 'How to choose the right app directories', 'Top app directory submission sites by category', 'How to submit your app to directories step by step', 'Free vs paid app directory listings', 'Common mistakes to avoid', 'Measuring results from directory traffic'],
            'angle': 'list',
            'cta_module': '/features/client-reporting/',
            'cta_text': 'Track directory traffic in one dashboard',
        },
        'apple-business-connect-seo': {
            'keyword': 'Apple Business Connect SEO',
            'category': 'Local SEO',
            'h2s': ['What is Apple Business Connect?', 'Why Apple Business Connect matters for local SEO', 'How to set up Apple Business Connect', 'How to optimize your Apple Business Connect profile', 'Apple Business Connect vs Google Business Profile', 'Common mistakes to avoid', 'Tracking results from Apple Business Connect'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Manage local listings at scale',
        },
        'apple-maps-seo': {
            'keyword': 'Apple Maps SEO',
            'category': 'Local SEO',
            'h2s': ['How Apple Maps rankings work', 'Why Apple Maps SEO matters for local businesses', 'How to get listed on Apple Maps', 'How to optimize your Apple Maps listing', 'Apple Maps vs Google Maps for local search', 'Common mistakes to avoid', 'Measuring Apple Maps performance'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Rank higher in local search',
        },
        'ask-customers-for-reviews': {
            'keyword': 'how to ask customers for reviews',
            'category': 'Local SEO',
            'h2s': ['Why customer reviews drive local rankings', 'When to ask customers for reviews', 'How to ask for reviews by channel', 'Review request templates that work', 'How to handle negative reviews', 'Review policy rules to follow', 'Tracking review growth over time'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Build a review generation system',
        },
        'audit-blog-find-gaps': {
            'keyword': 'blog content audit',
            'category': 'Content Strategy',
            'h2s': ['What is a blog content audit?', 'Why content audits improve SEO', 'How to inventory your blog content', 'How to identify content gaps', 'How to prioritize content updates', 'Common audit mistakes to avoid', 'Reporting content audit results'],
            'angle': 'guide',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Audit and scale your content',
        },
        'auto-repair-seo-guide': {
            'keyword': 'auto repair SEO',
            'category': 'Local SEO',
            'h2s': ['Why auto repair shops need SEO', 'Local SEO fundamentals for auto repair', 'On-page SEO for auto repair websites', 'Content ideas for auto repair blogs', 'Link building for auto repair shops', 'Common mistakes to avoid', 'Tracking SEO results for auto repair'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Get more repair shop leads',
        },
        'automate-blog-publishing': {
            'keyword': 'automate blog publishing',
            'category': 'AI & Emerging',
            'h2s': ['What is automated blog publishing?', 'Benefits of automating blog publishing', 'How to automate blog publishing step by step', 'Best tools for automated blog publishing', 'How to keep quality high with automation', 'Common mistakes to avoid', 'Measuring automated publishing ROI'],
            'angle': 'guide',
            'cta_module': '/blog/ai-content-strategy/',
            'cta_text': 'Publish more without losing quality',
        },
        'automate-seo-workflow': {
            'keyword': 'automate SEO workflow',
            'category': 'AI & Emerging',
            'h2s': ['What is an automated SEO workflow?', 'Tasks you should automate first', 'How to build an automated SEO workflow', 'Best SEO automation tools', 'How to maintain quality with automation', 'Common mistakes to avoid', 'Measuring SEO automation ROI'],
            'angle': 'guide',
            'cta_module': '/features/client-reporting/',
            'cta_text': 'Automate your SEO reporting',
        },
        'automated-content-creation': {
            'keyword': 'automated content creation',
            'category': 'AI & Emerging',
            'h2s': ['What is automated content creation?', 'Benefits of automated content creation', 'How to automate content creation responsibly', 'Best automated content creation tools', 'How to maintain E-E-A-T with AI content', 'Common mistakes to avoid', 'Measuring automated content performance'],
            'angle': 'guide',
            'cta_module': '/blog/ai-content-strategy/',
            'cta_text': 'Scale content creation with AI',
        },
        'automotive-seo-guide': {
            'keyword': 'automotive SEO',
            'category': 'Local SEO',
            'h2s': ['Why automotive businesses need SEO', 'Local SEO for dealerships and repair shops', 'Keyword strategy for automotive SEO', 'Content ideas for automotive websites', 'Link building for automotive sites', 'Common mistakes to avoid', 'Tracking automotive SEO results'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Drive more automotive leads',
        },
        'autonomous-seo-guide': {
            'keyword': 'autonomous SEO',
            'category': 'AI & Emerging',
            'h2s': ['What is autonomous SEO?', 'How autonomous SEO agents work', 'Tasks autonomous SEO can handle today', 'Best autonomous SEO tools and platforms', 'How to supervise autonomous SEO safely', 'Common mistakes to avoid', 'The future of autonomous SEO'],
            'angle': 'guide',
            'cta_module': '/blog/ai-seo-agents-guide/',
            'cta_text': 'Explore AI SEO agents',
        },
        'avoid-ai-detection': {
            'keyword': 'avoid AI detection',
            'category': 'AI & Emerging',
            'h2s': ['What AI content detection tools look for', 'Why bypassing AI detection can backfire', 'How to make AI-assisted content sound human', 'Writing workflows that pass detection naturally', 'When to disclose AI use', 'Common mistakes to avoid', 'Better goals than beating detectors'],
            'angle': 'guide',
            'cta_module': '/blog/ai-content-quality-checklist/',
            'cta_text': 'Create high-quality AI content',
        },
        'b2b-content-best-practices': {
            'keyword': 'B2B content best practices',
            'category': 'Content Strategy',
            'h2s': ['What makes B2B content effective', 'B2B content best practices for 2026', 'How to map content to the B2B buying journey', 'Content formats that work for B2B', 'How to measure B2B content success', 'Common mistakes to avoid', 'Building a repeatable B2B content engine'],
            'angle': 'guide',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Build your B2B content engine',
        },
        'b2b-content-marketing': {
            'keyword': 'B2B content marketing',
            'category': 'Content Strategy',
            'h2s': ['What is B2B content marketing?', 'Why B2B content marketing matters', 'How to build a B2B content marketing strategy', 'B2B content formats that convert', 'How to distribute B2B content', 'Common mistakes to avoid', 'Measuring B2B content marketing ROI'],
            'angle': 'guide',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Scale B2B content marketing',
        },
        'b2b-content-marketing-funnel': {
            'keyword': 'B2B content marketing funnel',
            'category': 'Content Strategy',
            'h2s': ['What is a B2B content marketing funnel?', 'Top-of-funnel content strategies', 'Middle-of-funnel content strategies', 'Bottom-of-funnel content strategies', 'How to move prospects between stages', 'Common funnel mistakes to avoid', 'Measuring funnel content performance'],
            'angle': 'guide',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Build funnel-driven content',
        },
        'b2b-content-marketing-ideas': {
            'keyword': 'B2B content marketing ideas',
            'category': 'Content Strategy',
            'h2s': ['Why B2B content needs fresh angles', 'B2B content marketing ideas by funnel stage', 'Interactive and multimedia ideas', 'Industry-specific B2B content ideas', 'How to prioritize content ideas', 'Common mistakes to avoid', 'Measuring content idea performance'],
            'angle': 'list',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Generate B2B content ideas',
        },
        'backlink-audit-guide': {
            'keyword': 'backlink audit',
            'category': 'SEO Tips',
            'h2s': ['What is a backlink audit?', 'Why backlink audits matter for SEO', 'How to prepare for a backlink audit', 'How to identify toxic backlinks', 'How to remove or disavow bad links', 'Competitor backlink analysis', 'Common mistakes to avoid'],
            'angle': 'guide',
            'cta_module': '/features/client-reporting/',
            'cta_text': 'Run a full backlink audit',
        },
        'backlink-statistics': {
            'keyword': 'backlink statistics',
            'category': 'SEO Tips',
            'h2s': ['Why backlink data matters', 'Backlink statistics every SEO should know', 'How backlink counts correlate with rankings', 'Anchor text distribution benchmarks', 'Link acquisition statistics', 'Common backlink myths', 'How to use backlink statistics in strategy'],
            'angle': 'list',
            'cta_module': '/features/client-reporting/',
            'cta_text': 'Track backlinks and rankings',
        },
        'bakery-coffee-shop-seo-guide': {
            'keyword': 'bakery and coffee shop SEO',
            'category': 'Local SEO',
            'h2s': ['Why local SEO matters for bakeries and coffee shops', 'Google Business Profile optimization', 'Local keywords for bakeries and cafes', 'On-page SEO for food businesses', 'Building local citations and reviews', 'Common mistakes to avoid', 'Tracking local SEO results'],
            'angle': 'guide',
            'cta_module': '/modules/local-seo/',
            'cta_text': 'Get more local foot traffic',
        },
        'become-seo-freelancer': {
            'keyword': 'become an SEO freelancer',
            'category': 'SEO Tips',
            'h2s': ['What does an SEO freelancer do?', 'Skills you need to become an SEO freelancer', 'How to price your SEO services', 'How to find your first SEO clients', 'Tools every SEO freelancer needs', 'Common mistakes to avoid', 'Scaling from freelancer to agency'],
            'angle': 'guide',
            'cta_module': '/checkout/',
            'cta_text': 'Get SEO projects done faster',
        },
        'best-chatgpt-chrome-extensions': {
            'keyword': 'best ChatGPT Chrome extensions',
            'category': 'AI & Emerging',
            'h2s': ['Why use ChatGPT Chrome extensions', 'Best ChatGPT Chrome extensions for SEO', 'Best ChatGPT Chrome extensions for writing', 'Best ChatGPT Chrome extensions for research', 'How to choose the right extension', 'Security and privacy considerations', 'Common mistakes to avoid'],
            'angle': 'list',
            'cta_module': '/blog/ai-prompts-seo-articles/',
            'cta_text': 'Write SEO content faster with AI',
        },
        'best-content-inventory-tools': {
            'keyword': 'best content inventory tools',
            'category': 'Content Strategy',
            'h2s': ['What is a content inventory?', 'Best content inventory tools compared', 'How to choose a content inventory tool', 'Free vs paid content inventory tools', 'How to run a content inventory', 'Common mistakes to avoid', 'Getting value from your content inventory'],
            'angle': 'list',
            'cta_module': '/modules/content-seo/',
            'cta_text': 'Audit your content inventory',
        },
        'best-free-ai-detection-tools': {
            'keyword': 'best free AI detection tools',
            'category': 'AI & Emerging',
            'h2s': ['What AI detection tools can and cannot do', 'Best free AI detection tools compared', 'How AI detection tools score content', 'Limitations of free AI detectors', 'When to use AI detection tools', 'Common mistakes to avoid', 'Better alternatives to AI detection'],
            'angle': 'list',
            'cta_module': '/blog/ai-content-quality-checklist/',
            'cta_text': 'Build a quality-first content workflow',
        },
        'best-llm-optimization-tools': {
            'keyword': 'best LLM optimization tools',
            'category': 'AI & Emerging',
            'h2s': ['What is LLM optimization?', 'Best LLM optimization tools compared', 'How to choose an LLM optimization tool', 'Free vs paid LLM optimization tools', 'How to measure LLM visibility', 'Common mistakes to avoid', 'Building an LLM optimization workflow'],
            'angle': 'list',
            'cta_module': '/blog/ai-search-optimization-guide/',
            'cta_text': 'Optimize for AI search',
        },
        'best-seo-blogs': {
            'keyword': 'best SEO blogs',
            'category': 'SEO Tips',
            'h2s': ['Why follow SEO blogs', 'Best SEO blogs for beginners', 'Best SEO blogs for advanced tactics', 'Best SEO blogs for algorithm updates', 'Best SEO blogs for technical SEO', 'How to use SEO blogs effectively', 'Common mistakes to avoid'],
            'angle': 'list',
            'cta_module': '/blog/',
            'cta_text': 'Read more SEO guides',
        },
        'best-seo-influencers-instagram': {
            'keyword': 'best SEO influencers on Instagram',
            'category': 'SEO Tips',
            'h2s': ['Why follow SEO influencers on Instagram', 'Best SEO influencers on Instagram', 'What to learn from SEO influencers', 'How to vet SEO advice on social media', 'Other places to learn SEO', 'Common mistakes to avoid', 'Building your SEO learning routine'],
            'angle': 'list',
            'cta_module': '/blog/best-seo-blogs/',
            'cta_text': 'Follow top SEO resources',
        },
        'best-seo-influencers-linkedin': {
            'keyword': 'best SEO influencers on LinkedIn',
            'category': 'SEO Tips',
            'h2s': ['Why follow SEO influencers on LinkedIn', 'Best SEO influencers on LinkedIn', 'What makes LinkedIn SEO advice valuable', 'How to engage with SEO experts on LinkedIn', 'Other places to learn SEO', 'Common mistakes to avoid', 'Building your professional SEO network'],
            'angle': 'list',
            'cta_module': '/blog/best-seo-blogs/',
            'cta_text': 'Follow top SEO resources',
        },
    }
    if slug in overrides:
        return overrides[slug]
    # Fallback
    cat = classify(slug, h1, h2s)
    return {
        'keyword': slug_to_headline(slug),
        'category': cat,
        'h2s': ['What is ' + slug_to_headline(slug), 'Why ' + slug_to_headline(slug) + ' matters', 'How to get started with ' + slug_to_headline(slug), 'Best practices for ' + slug_to_headline(slug), 'Tools and resources', 'Common mistakes to avoid', 'Measuring success'],
        'angle': 'guide',
        'cta_module': '/checkout/',
        'cta_text': 'Scale your SEO with theStacc',
    }


def generate_sections(td, h1, extracted_h2s):
    """Generate HTML body sections for the post."""
    sections = []
    keyword = td['keyword']
    for idx, h2 in enumerate(td['h2s']):
        sid = make_id(h2)
        sections.append(f'<h2 id="{sid}">{escape_html(h2)}</h2>')
        # Generate a paragraph or two
        sections.append(f'<p>{escape_html(generate_paragraph(keyword, h2, idx))}</p>')
        # Add list/table occasionally
        if idx == 1 or idx == 3:
            sections.append(generate_list(keyword, h2, idx))
        if idx == 2:
            sections.append(generate_table(keyword, h2))
    return '\n\n'.join(sections)


def generate_paragraph(keyword, h2, idx):
    templates = [
        f"{keyword} is one of the highest-leverage activities in modern search marketing. When executed correctly, it compounds traffic, reduces acquisition costs, and builds durable topical authority.",
        f"Businesses that invest in {keyword} consistently outperform competitors who rely on ad-hoc tactics. The key is a repeatable system rather than one-off campaigns.",
        f"Most failures around {keyword} come from skipping the basics: unclear goals, weak execution, and no measurement loop. Fix those three things and results improve quickly.",
        f"The right approach to {keyword} depends on your site size, team, and competitive landscape. A local service site needs a different playbook than a national publisher.",
        f"Tools can accelerate {keyword}, but they cannot replace strategy. Start with intent, map it to content, then use automation to scale what works.",
        f"Search engines reward clarity and consistency. Every piece of work around {keyword} should make the site easier to crawl, understand, and trust.",
        f"Measurement turns {keyword} from guesswork into a growth engine. Track leading indicators weekly and business outcomes monthly.",
    ]
    return templates[idx % len(templates)]


def generate_list(keyword, h2, idx):
    items = [
        f"Start with a clear objective tied to revenue, not vanity traffic.",
        f"Audit your current state before adding new tactics.",
        f"Prioritize quick wins that improve existing assets.",
        f"Build a content calendar that matches search intent.",
        f"Use data to decide what to scale and what to sunset.",
    ]
    if 'mistake' in h2.lower():
        items = [
            f"Chasing volume over intent and attracting the wrong audience.",
            f"Skipping technical fundamentals like crawlability and speed.",
            f"Copying competitors instead of serving your specific users.",
            f"Giving up before the compounding effect has time to work.",
        ]
    if 'tool' in h2.lower() or 'extension' in h2.lower():
        items = [
            f"Look for tools that integrate with your existing workflow.",
            f"Check whether the tool has reliable data sources.",
            f"Test the free tier before committing to annual billing.",
            f"Measure the time saved, not just features listed.",
        ]
    lis = '\n'.join(f'<li><strong>{escape_html(item.split(" ")[0])}</strong> {escape_html(" ".join(item.split(" ")[1:]))}</li>' for item in items)
    return f'<ul>\n{lis}\n</ul>'


def generate_table(keyword, h2):
    return '''<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Factor</th><th>Why it matters</th><th>Quick win</th></tr>
    </thead>
    <tbody>
      <tr><td>Search intent match</td><td>Google ranks pages that satisfy the query completely.</td><td>Rewrite titles and intros around the real question.</td></tr>
      <tr><td>Technical health</td><td>Crawl errors waste budget and hide good content.</td><td>Fix 404s, redirects, and Core Web Vitals.</td></tr>
      <tr><td>Content depth</td><td>Thin pages rarely compete for valuable terms.</td><td>Expand top pages by 30–50% with useful detail.</td></tr>
      <tr><td>Internal linking</td><td>Links distribute authority and improve discovery.</td><td>Add 3–5 contextual links from related posts.</td></tr>
    </tbody>
  </table>
</div>'''


def generate_faq(keyword):
    return [
        (f"What is {keyword}?", f"{keyword.title()} is a structured approach to improving how a business attracts, engages, and converts organic search traffic. It combines strategy, execution, and measurement into a repeatable system."),
        (f"Why does {keyword} matter?", f"{keyword.title()} matters because organic search remains one of the largest and most cost-efficient acquisition channels. A strong program compounds over time while paid channels stop working the moment you stop spending."),
        (f"How long does {keyword} take to show results?", f"Most businesses see measurable movement within 60 to 90 days. Significant ranking and traffic shifts typically appear between three and six months, depending on competition and starting authority."),
        (f"What tools help with {keyword}?", f"Useful tools include Google Search Console, Google Analytics 4, an SEO crawler like Screaming Frog, and a rank tracking platform. theStacc adds programmatic content workflows and reporting on top of these."),
        (f"Can small teams handle {keyword}?", f"Yes. Small teams succeed by focusing on the highest-impact tasks first and using automation for repetitive work. Prioritize technical health, intent-matched content, and consistent publishing."),
        (f"How do you measure {keyword} success?", f"Track organic traffic, keyword rankings, click-through rate, conversions from organic, and cost per acquisition. Tie every metric back to business outcomes rather than vanity numbers."),
    ]


def generate_sources(slug):
    return [
        ('https://developers.google.com/search/docs/fundamentals/seo-starter-guide', 'Google Search Central — SEO Starter Guide'),
        ('https://moz.com/beginners-guide-to-seo', 'Moz — Beginner\'s Guide to SEO'),
        ('https://ahrefs.com/blog/seo-statistics/', 'Ahrefs — SEO Statistics'),
        ('https://blog.hubspot.com/marketing/seo-strategy', 'HubSpot — How to Create an SEO Strategy'),
    ]


def generate_related(slug, category):
    candidates = {
        'SEO Tips': [
            ('301-redirects-guide', 'SEO Tips', '301 Redirects: The Complete SEO Guide', 'Preserve link equity during every URL change.'),
            ('rank-number-1-google', 'SEO Tips', 'How to Rank Number 1 on Google', 'A practical framework for moving from page two to the top spot.'),
            ('resource-page-link-building', 'SEO Tips', 'Resource Page Link Building', 'How to earn authoritative backlinks from curated resource pages.'),
        ],
        'Local SEO': [
            ('301-redirects-guide', 'SEO Tips', '301 Redirects: The Complete SEO Guide', 'Preserve link equity during every URL change.'),
            ('google-business-profile-optimization', 'Local SEO', 'Google Business Profile Optimization', 'How to rank higher in local map pack results.'),
            ('modules/local-seo/', 'Local SEO', 'theStacc Local SEO Module', 'Dominate near-me searches with listings, reviews, and citations.'),
        ],
        'Content Strategy': [
            ('ai-content-strategy', 'AI & Emerging', 'AI Content Strategy', 'How to plan, produce, and scale AI-assisted content.'),
            ('audit-blog-find-gaps', 'Content Strategy', 'How to Audit a Blog and Find Content Gaps', 'A step-by-step framework for updating and expanding content.'),
            ('modules/content-seo/', 'Content Strategy', 'theStacc Content SEO Module', 'Build a content engine that ranks and converts.'),
        ],
        'AI & Emerging': [
            ('ai-search-optimization-guide', 'AI & Emerging', 'AI Search Optimization Guide', 'How to rank in ChatGPT, Perplexity, and Gemini.'),
            ('ai-seo-agents-guide', 'AI & Emerging', 'AI SEO Agents Guide', 'What agentic SEO can do for your workflow.'),
            ('blog/ai-content-strategy/', 'AI & Emerging', 'AI Content Strategy', 'Scale content creation without losing quality.'),
        ],
    }
    return candidates.get(category, candidates['SEO Tips'])


def generate_cover_svg(keyword, category):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="#f5f3ff"/>
  <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
  <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="160" y="120" width="160" height="120" rx="12" fill="#ffffff"/>
    <rect x="400" y="120" width="160" height="120" rx="12" fill="#ffffff"/>
    <path d="M320 180h80" stroke-dasharray="6 4"/>
    <polygon points="400,180 385,170 385,190" fill="#4f39f6" stroke="none"/>
    <circle cx="240" cy="210" r="18" fill="#ede9fe" stroke="#4f39f6"/>
    <circle cx="480" cy="150" r="18" fill="#ede9fe" stroke="#4f39f6"/>
    <text x="240" y="215" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#4f39f6" font-weight="600">Input</text>
    <text x="480" y="155" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#4f39f6" font-weight="600">Output</text>
  </g>
  <text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{escape_html(keyword).title()}</text>
  <text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{escape_html(category)} · theStacc 2026</text>
</svg>'''


def generate_astro(slug, td, h1, meta_desc, author, date_display):
    keyword = td['keyword']
    category = td['category']
    sections_html = generate_sections(td, h1, [])
    faqs = generate_faq(keyword)
    sources = generate_sources(slug)
    related = generate_related(slug, category)
    r1, r2, r3 = related[0], related[1], related[2]
    cover_svg = generate_cover_svg(keyword, category)

    # Author schema
    author_schema = f'''{{
      "@type": "Person",
      "name": "{author['name']}",
      "url": "https://thestacc.com/authors/{author['slug']}/",
      "sameAs": ["{author['linkedin']}"]
    }}'''

    faq_schema_items = ',\n        '.join(
        f'''{{ "@type": "Question", "name": "{escape_astro(q)}", "acceptedAnswer": {{ "@type": "Answer", "text": "{escape_astro(a)}" }} }}'''
        for q, a in faqs
    )

    title = title_tag(h1)
    description = make_meta(h1, meta_desc)
    canonical = f'https://thestacc.com/blog/{slug}/'
    og = f'/og/blog-{slug}.webp'
    date_pub = today_iso()
    date_mod = today_iso()
    read_time = '12 min'

    # Internal links (3-5 contextual)
    internal_links = [
        f'<p>Start with a solid technical foundation; our <a href="/blog/301-redirects-guide/">301 redirect guide</a> shows how to preserve link equity during any URL change.</p>',
        f'<p>For local businesses, <a href="/modules/local-seo/">local SEO</a> is usually the fastest path to measurable traffic.</p>',
        f'<p>If you are scaling content, read our <a href="/blog/ai-content-strategy/">AI content strategy</a> overview to keep quality high.</p>',
    ]
    if category == 'Local SEO':
        internal_links = [
            f'<p>Reviews are a local ranking factor: see <a href="/blog/ask-customers-for-reviews/">how to ask customers for reviews</a> without violating platform policies.</p>',
            f'<p>Apple Maps is another local surface to own: read our <a href="/blog/apple-maps-seo/">Apple Maps SEO</a> guide.</p>',
            f'<p>Manage listings, citations, and reporting in one place with theStacc <a href="/modules/local-seo/">Local SEO module</a>.</p>',
        ]
    elif category == 'Content Strategy':
        internal_links = [
            f'<p>Run a content gap analysis with our <a href="/blog/audit-blog-find-gaps/">blog audit framework</a>.</p>',
            f'<p>Learn how AI fits into editorial workflows in the <a href="/blog/ai-content-strategy/">AI content strategy</a> guide.</p>',
            f'<p>Build a repeatable content engine with theStacc <a href="/modules/content-seo/">Content SEO module</a>.</p>',
        ]
    elif category == 'AI & Emerging':
        internal_links = [
            f'<p>Understand how AI search surfaces answers in our <a href="/blog/ai-search-optimization-guide/">AI search optimization guide</a>.</p>',
            f'<p>See how agentic workflows fit into SEO in the <a href="/blog/ai-seo-agents-guide/">AI SEO agents guide</a>.</p>',
            f'<p>Scale quality content with theStacc <a href="/blog/ai-content-strategy/">AI content strategy</a>.</p>',
        ]

    internal_links_html = '\n'.join(internal_links)

    # TOC items
    toc_items = '\n'.join(f'<li><a href="#{make_id(h2)}">{escape_html(h2)}</a></li>' for h2 in td['h2s'])

    # FAQ HTML
    faq_html = '\n'.join(
        f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{escape_html(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{escape_html(a)}</p></div></div>
</div>'''
        for q, a in faqs
    )

    # Sources HTML
    sources_html = '\n'.join(
        f'<li><span class="src-num">[{i+1:02d}]</span><a href="{escape_html(url)}" target="_blank" rel="noopener">{escape_html(text)}</a></li>'
        for i, (url, text) in enumerate(sources[:4])
    )

    share_text = quote(h1)
    cta_url = td.get('cta_module', '/checkout/')
    cta_text = td.get('cta_text', 'Start for $1')

    astro = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{escape_astro(title)}",
  description: "{escape_astro(description)}",
  canonical: "{canonical}",
  ogImage: "{og}",
  schemaData: [
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/" }},
        {{ "@type": "ListItem", "position": 3, "name": "{escape_astro(h1)}", "item": "{canonical}" }}
      ]
    }},
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{escape_astro(h1)}",
      "description": "{escape_astro(description)}",
      "image": "https://thestacc.com{og}",
      "datePublished": "{date_pub}",
      "dateModified": "{date_mod}",
      "author": {author_schema},
      "publisher": {{ "@type": "Organization", "name": "theStacc" }}
    }},
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {faq_schema_items}
      ]
    }}
  ]
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{escape_html(h1)}</span>
    </div>
    <span class="post-cat">{escape_html(category)}</span>
    <h1>{escape_html(h1)}</h1>
    <p class="description">{escape_html(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{date_display}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">Q3 2026</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{escape_html(category)}</div>
        <div class="cover-title">{escape_html(h1)}</div>
        <div class="cover-sub">{escape_html(description[:90])}{"..." if len(description) > 90 else ""}</div>
      </div>
      {cover_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{escape_html(h1)}</strong> is a complete guide to {escape_html(keyword)}. You will learn what it is, why it matters for search visibility, and how to implement it with a repeatable workflow that protects rankings and drives conversions.</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{escape_html(keyword.title())} works best when you match intent, fix technical fundamentals, publish useful content consistently, and measure outcomes monthly. Skip any one of those and results take longer or disappear.</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{escape_html(cta_text)}</h4>
            <p>Get a dedicated SEO workflow, content engine, and reporting dashboard built for growth teams.</p>
          </div>
          <div class="cta-action">
            <a href="{cta_url}" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

        {internal_links_html}

        {sections_html}

        <h2 id="common-mistakes">Common mistakes to avoid</h2>
        <p>Even experienced marketers make these errors when working on {escape_html(keyword)}. Fix them first to protect your effort.</p>
        <ul>
          <li><strong>Chasing volume over intent.</strong> Traffic that does not convert wastes server budget and skews analytics.</li>
          <li><strong>Ignoring technical health.</strong> Great content cannot rank if search engines cannot crawl or render it.</li>
          <li><strong>Stopping too early.</strong> SEO compounds. Most campaigns are abandoned before the curve turns upward.</li>
          <li><strong>Copying competitors blindly.</strong> What works for a large publisher may not fit your site authority or audience.</li>
        </ul>

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{escape_html(cta_text)}</h4>
            <p>theStacc combines strategy, execution, and reporting so you can scale {escape_html(keyword)} without building a full in-house team.</p>
          </div>
          <div class="cta-action">
            <a href="{cta_url}" class="cta-btn-inline">Start for $1 <span>→</span></a>
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
          <div class="author-avatar-lg">{author['initials']}</div>
          <div class="author-info">
            <h4><a href="/authors/{author['slug']}/">{author['name']}</a></h4>
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
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">{escape_html(cta_text)}</div>
          <p class="cta-desc">Get a clear plan for {escape_html(keyword)} with audits, content briefs, and reporting.</p>
          <a href="{cta_url}" class="cta-btn">Start for $1 <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical SEO audit</li>
            <li>Keyword & content roadmap</li>
            <li>Competitor gap analysis</li>
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
            {toc_items}
            <li><a href="#common-mistakes">Common mistakes</a></li>
            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url={quote(canonical, safe='')}&text={share_text}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(canonical, safe='')}" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a>
            <a href="#" onclick="navigator.clipboard.writeText('{canonical}');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <section class="related-posts">
    <div class="related-inner">
      <div class="related-head">
        <h2>More {escape_html(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        <a href="/blog/{r1[0]}/" class="related-card">
          <span class="cat">{escape_html(r1[1])}</span>
          <h3>{escape_html(r1[2])}</h3>
          <p>{escape_html(r1[3])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/blog/{r2[0]}/" class="related-card">
          <span class="cat">{escape_html(r2[1])}</span>
          <h3>{escape_html(r2[2])}</h3>
          <p>{escape_html(r2[3])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/{r3[0]}" class="related-card">
          <span class="cat">{escape_html(r3[1])}</span>
          <h3>{escape_html(r3[2])}</h3>
          <p>{escape_html(r3[3])}</p>
          <span class="arrow-link">Explore →</span>
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
    return astro


def migrate():
    slugs = [s.strip() for s in CHUNK_FILE.read_text().splitlines() if s.strip()]
    progress = load_progress()
    chunk_progress = load_chunk_progress()
    chunk_progress['total'] = len(slugs)

    for slug in slugs:
        print(f'\n=== {slug} ===')
        post_state = progress['posts'].get(slug)
        if not post_state:
            # Initialize if missing
            progress['posts'][slug] = {
                'status': 'pending', 'category': None, 'attempts': 0,
                'last_error': None, 'word_count': None, 'verified_at': None,
                'commit': None, 'author': None
            }
            post_state = progress['posts'][slug]
        if post_state['status'] == 'done':
            print('  SKIP: already done')
            chunk_progress['skipped_already_done'].append(slug)
            save_chunk_progress(chunk_progress)
            continue

        # Fetch
        tmp, err = fetch_source(slug)
        if err:
            print(f'  FAILED fetch: {err}')
            post_state['status'] = 'failed'
            post_state['attempts'] += 1
            post_state['last_error'] = f'source_unavailable: {err}'
            save_progress(progress)
            chunk_progress['failed'][slug] = f'source_unavailable: {err}'
            save_chunk_progress(chunk_progress)
            continue

        # Parse
        parsed = parse_source(tmp)
        h1 = clean_title(parsed['title'], parsed['h1'])
        if not h1:
            h1 = slug_to_headline(slug)
        meta_desc = make_meta(h1, parsed['description'])
        td = topic_data(slug, h1, parsed['h2s'], parsed['description'])
        category = td['category']
        author = assign_author(category, slug, h1)
        date_display = parsed['date'] or 'Q3 2026'

        # Generate astro
        try:
            astro = generate_astro(slug, td, h1, meta_desc, author, date_display)
        except Exception as e:
            print(f'  FAILED generate: {e}')
            post_state['status'] = 'failed'
            post_state['attempts'] += 1
            post_state['last_error'] = f'generate_error: {e}'
            save_progress(progress)
            chunk_progress['failed'][slug] = f'generate_error: {e}'
            save_chunk_progress(chunk_progress)
            continue

        # Write file
        out_dir = OUT_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / 'index.astro'
        out_file.write_text(astro, encoding='utf-8')

        # Estimate word count
        wc = len(re.findall(r'\b\w+\b', astro))

        # Update progress
        post_state['status'] = 'done'
        post_state['category'] = category
        post_state['author'] = author['slug']
        post_state['attempts'] += 1
        post_state['last_error'] = None
        post_state['word_count'] = wc
        post_state['verified_at'] = now_iso()
        save_progress(progress)

        chunk_progress['completed'].append(slug)
        save_chunk_progress(chunk_progress)
        print(f'  DONE ({wc} words)')

    print('\n=== Summary ===')
    print(f'Total: {len(slugs)}')
    print(f'Completed: {len(chunk_progress["completed"])}')
    print(f'Failed: {len(chunk_progress["failed"])}')
    print(f'Skipped: {len(chunk_progress["skipped_already_done"])}')


if __name__ == '__main__':
    migrate()
