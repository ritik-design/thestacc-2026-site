#!/usr/bin/env python3
"""Generate Astro blog posts for chunk-024 from fetched live sources."""
import json
import os
import re
import html
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from pathlib import Path

ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
SRC_DIR = ROOT / 'src/pages/blog'
PROGRESS_FILE = ROOT / 'Stacc/blog-migration/progress.json'
CHUNK_FILE = ROOT / 'Stacc/blog-migration/small-chunks/chunk-024.txt'
CHUNK_PROGRESS_FILE = Path(str(CHUNK_FILE) + '.progress.json')
SOURCE_DIR = Path('/tmp/blog-src')

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal', 'role': 'Founder · theStacc', 'initials': 'SG',
        'full_role': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.',
        'x': 'https://x.com/sidgangal', 'linkedin': 'https://www.linkedin.com/in/sidgangal/'
    },
    'akshay-vr': {
        'name': 'Akshay VR', 'role': 'Marketing Head · theStacc', 'initials': 'AVR',
        'full_role': 'Marketing Head · theStacc',
        'bio': 'Akshay leads marketing and editorial strategy at theStacc. He specializes in SEO strategy, content operations, and demand generation for B2B SaaS brands.',
        'x': 'https://x.com/akshayvr_', 'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/'
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev', 'role': 'Growth Manager · theStacc', 'initials': 'RN',
        'full_role': 'Growth Manager · theStacc',
        'bio': 'Ritik runs growth experiments, analytics, and programmatic SEO at theStacc. He focuses on scalable systems, conversion optimization, and turning traffic into revenue.',
        'x': 'https://x.com/ritiknamdev', 'linkedin': 'https://www.linkedin.com/in/ritiknamdev/'
    }
}


def load_progress():
    with open(PROGRESS_FILE) as f:
        return json.load(f)


def save_progress(progress):
    progress['totals'] = {
        status: sum(1 for t in progress['posts'].values() if t['status'] == status)
        for status in ['pending', 'in_progress', 'done', 'failed']
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def load_chunk_progress():
    if CHUNK_PROGRESS_FILE.exists():
        with open(CHUNK_PROGRESS_FILE) as f:
            return json.load(f)
    return {
        'chunk': str(CHUNK_FILE),
        'total': 0,
        'completed': [],
        'failed': {},
        'skipped_already_done': []
    }


def save_chunk_progress(cp):
    with open(CHUNK_PROGRESS_FILE, 'w') as f:
        json.dump(cp, f, indent=2)


def parse_source(slug):
    path = SOURCE_DIR / f'{slug}.html'
    with open(path) as f:
        html_text = f.read()
    if not html_text.strip():
        return None
    soup = BeautifulSoup(html_text, 'html.parser')
    # Remove nav, footer, script, style
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        tag.decompose()
    title = soup.title.string if soup.title else ''
    h1 = soup.find('h1')
    h1_text = h1.get_text(strip=True) if h1 else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    desc = meta['content'] if meta else ''
    h2s = []
    for h in soup.find_all('h2'):
        txt = h.get_text(strip=True)
        if txt and 'Explore More' not in txt and 'Related Tools' not in txt and 'Related Statistics' not in txt:
            h2s.append(txt)
    h3s = [h.get_text(strip=True) for h in soup.find_all('h3')]
    # Extract paragraphs under each h2
    sections = []
    main = soup.find('main') or soup.find('article') or soup.find('body')
    if main:
        current = {'h2': 'Introduction', 'paragraphs': []}
        for el in main.find_all(['h2', 'h3', 'p', 'ul', 'ol', 'table']):
            if el.name == 'h2':
                if current['paragraphs'] or current.get('h3s'):
                    sections.append(current)
                current = {'h2': el.get_text(strip=True), 'paragraphs': [], 'h3s': []}
            elif el.name == 'h3':
                current.setdefault('h3s', []).append({'h3': el.get_text(strip=True), 'paragraphs': []})
            elif el.name == 'p':
                txt = el.get_text(strip=True)
                if txt:
                    if current.get('h3s'):
                        current['h3s'][-1]['paragraphs'].append(txt)
                    else:
                        current['paragraphs'].append(txt)
            elif el.name in ('ul', 'ol'):
                items = [li.get_text(strip=True) for li in el.find_all('li') if li.get_text(strip=True)]
                if items:
                    if current.get('h3s'):
                        current['h3s'][-1].setdefault('list', []).extend(items)
                    else:
                        current.setdefault('list', []).extend(items)
        if current['paragraphs'] or current.get('h3s'):
            sections.append(current)
    return {
        'title': title, 'h1': h1_text, 'description': desc,
        'h2s': h2s, 'h3s': h3s, 'sections': sections
    }


def slug_to_display(slug):
    return slug.replace('-', ' ').title()


def classify_post(slug, h2s, title):
    s = slug.lower()
    t = title.lower()
    h = ' '.join(h2s).lower()
    if 'statistics' in s or 'stats' in s:
        return 'statistics'
    if 'vs' in s or 'versus' in t or ' vs ' in h:
        return 'comparison'
    if 'alternatives' in s or 'alternative' in t:
        return 'alternatives'
    if 'case study' in s or 'case-study' in s:
        return 'case-study'
    if 'trends' in s or 'trend' in t:
        return 'trends'
    if 'tools' in s:
        return 'tools'
    if 'checklist' in t or 'steps' in h or 'step' in h:
        return 'guide'
    if 'guide' in s or 'guide' in t:
        return 'guide'
    return 'guide'


def assign_category(slug, h2s, title):
    s = slug.lower()
    t = title.lower()
    h = ' '.join(h2s).lower()
    if 'local' in s or 'service area' in s or 'gbp' in h:
        return 'Local SEO'
    if 'ai' in s or 'artificial intelligence' in h or 'agent' in s or 'machine learning' in h or 'mcp' in s:
        return 'AI & Emerging'
    if 'social media' in s or 'social-media' in s:
        return 'Content Strategy'
    if 'content' in s or 'content' in t:
        return 'Content Strategy'
    if 'ppc' in s or 'sem' in s or 'marketing' in s:
        return 'Content Strategy'
    return 'SEO Tips'


def assign_author(category, slug, h2s):
    s = slug.lower()
    h = ' '.join(h2s).lower()
    if category == 'AI & Emerging' or 'ai' in s or 'agent' in s or 'mcp' in s or 'generative' in h:
        return 'siddharth-gangal'
    if category == 'Content Strategy' or 'content' in s or 'social' in s or 'ppc' in s or 'sem' in s:
        return 'akshay-vr'
    if 'statistics' in s or 'stats' in s or 'case-study' in s or 'workflow' in s or 'automation' in s:
        return 'ritik-namdev'
    # Default rotation based on length parity
    return 'akshay-vr'


def make_id(text):
    t = re.sub(r"[^a-z0-9\s-]", '', text.lower()).strip()
    t = re.sub(r"\s+", '-', t)
    return t[:60]


def clean(text):
    return html.escape(text).replace('{', '&#123;').replace('}', '&#125;')


def shorten(text, n):
    if len(text) <= n:
        return text
    return text[:n-1].rsplit(' ', 1)[0] + '…'


def generate_feature_svg(topic, slug):
    # A generic but topic-representative SVG; can be customized by slug below
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="120" y="120" width="160" height="120" rx="12" fill="#ffffff"/>
          <rect x="440" y="120" width="160" height="120" rx="12" fill="#ffffff"/>
          <path d="M280 180h160" stroke-dasharray="6 4"/>
          <polygon points="440,180 425,170 425,190" fill="#4f39f6" stroke="none"/>
          <circle cx="200" cy="180" r="22" fill="#ede9fe" stroke="#4f39f6"/>
          <circle cx="520" cy="180" r="22" fill="#ede9fe" stroke="#4f39f6"/>
          <text x="200" y="186" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#4f39f6" font-weight="600">A</text>
          <text x="520" y="186" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#4f39f6" font-weight="600">B</text>
          <text x="360" y="170" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="#111827" font-weight="600">{clean(topic[:35])}</text>
          <text x="360" y="205" text-anchor="middle" font-family="Geist, sans-serif" font-size="12" fill="#57534e">Optimized · Data-backed · Actionable</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{clean(topic[:55])}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">thestacc.com/blog/{slug}</text>
      </svg>'''


def generate_related(slug, category):
    pools = {
        'SEO Tips': [
            ('301-redirects-guide', 'SEO Tips', '301 Redirects: The Complete SEO Guide', 'Preserve link equity during every URL change.'),
            ('rank-number-1-google', 'SEO Tips', 'How to Rank Number 1 on Google', 'A practical framework for moving from page two to the top spot.'),
            ('recover-helpful-content-update', 'SEO Tips', 'Recover from the Helpful Content Update', 'What to fix and how to rebuild trust after a Google helpful-content hit.'),
            ('resource-page-link-building', 'SEO Tips', 'Resource Page Link Building', 'How to earn authoritative backlinks from curated resource pages.'),
            ('serp-features-guide', 'SEO Tips', 'SERP Features Guide', 'How to win featured snippets, People Also Ask, and rich results.'),
        ],
        'Local SEO': [
            ('local-seo-checklist', 'Local SEO', 'Local SEO Checklist', 'A step-by-step checklist for ranking in local search.'),
            ('google-business-profile-optimization', 'Local SEO', 'Google Business Profile Optimization', 'How to optimize GBP for maximum local visibility.'),
            ('service-area-pages-seo', 'Local SEO', 'Service Area Pages SEO', 'Build location pages that rank without doorway-page risk.'),
        ],
        'AI & Emerging': [
            ('ai-search-optimization-guide', 'AI & Emerging', 'AI Search Optimization Guide', 'How to rank inside ChatGPT, Perplexity, and Gemini.'),
            ('ai-overview-optimization', 'AI & Emerging', 'AI Overview Optimization', 'Structure content so Google cites you in AI Overviews.'),
            ('generative-engine-optimization', 'AI & Emerging', 'Generative Engine Optimization', 'The complete GEO playbook for AI search engines.'),
        ],
        'Content Strategy': [
            ('content-marketing-strategy', 'Content Strategy', 'Content Marketing Strategy', 'Build an editorial system that compounds organic traffic.'),
            ('seo-content-brief-template', 'Content Strategy', 'SEO Content Brief Template', 'The brief format that produces rank-worthy articles.'),
            ('social-media-content-ideas', 'Content Strategy', 'Social Media Content Ideas', 'A reusable library of post formats for B2B brands.'),
        ]
    }
    pool = pools.get(category, pools['SEO Tips'])
    # Pick 3 that are not the current slug
    chosen = [c for c in pool if c[0] != slug][:3]
    if len(chosen) < 3:
        chosen += pool[:3 - len(chosen)]
    return chosen


def generate_faqs(topic, slug, post_type):
    return [
        (f"What is {topic}?", f"{topic} refers to the strategies, tools, and workflows that help businesses attract organic traffic from search engines. It covers keyword research, on-page optimization, technical health, and link building — all aligned with what searchers actually want."),
        (f"Why does {topic} matter in 2026?", f"Search is changing faster than ever. AI Overviews, zero-click results, and personalized SERPs mean that basic optimization is no longer enough. A focused {topic} strategy protects rankings and captures high-intent traffic before competitors do."),
        (f"How long does it take to see results from {topic}?", "Most businesses see measurable movement within 60 to 90 days when they execute consistently. Complex niches or competitive keywords can take 4 to 6 months, but early signals often appear within the first 30 days."),
        (f"What tools do I need for {topic}?", "Start with Google Search Console and Google Analytics 4. Add a keyword research tool, a site crawler, and an AI-assisted content platform like theStacc to scale research, briefs, and optimization."),
        (f"Can small businesses compete with {topic}?", "Yes. Small businesses often win by targeting specific long-tail keywords, local intent, and faster execution. Focused content and clean technical SEO can outrank larger sites with weaker relevance."),
        (f"Should I do {topic} in-house or hire an agency?", "If you have time and internal expertise, in-house works for content and basic optimization. For technical SEO, link building, and scale, an agency or platform like theStacc delivers faster ROI.")
    ]


def generate_sources(post_type, topic):
    common = [
        ('https://developers.google.com/search/docs/fundamentals/seo-starter-guide', 'Google Search Central — SEO Starter Guide'),
        ('https://ahrefs.com/blog/seo-statistics/', 'Ahrefs — SEO Statistics'),
        ('https://moz.com/beginners-guide-to-seo', 'Moz — Beginner\'s Guide to SEO'),
        ('https://backlinko.com/seo-this-year', 'Backlinko — SEO This Year'),
    ]
    if post_type == 'statistics':
        return [
            ('https://www.statista.com/topics/1714/search-engine-optimization/', 'Statista — SEO Market Data'),
            ('https://ahrefs.com/blog/seo-statistics/', 'Ahrefs — SEO Statistics'),
            ('https://www.hubspot.com/marketing-statistics', 'HubSpot — Marketing Statistics'),
            ('https://developers.google.com/search/blog/', 'Google Search Central Blog')
        ]
    if 'shopify' in topic.lower():
        return [
            ('https://help.shopify.com/en/manual/promoting-marketing/seo', 'Shopify Help Center — SEO'),
            ('https://developers.google.com/search/docs/appearance/structured-data/product', 'Google Search Central — Product Structured Data'),
            ('https://moz.com/learn/seo/ecommerce', 'Moz — Ecommerce SEO'),
            ('https://www.semrush.com/blog/shopify-seo/', 'Semrush — Shopify SEO Guide')
        ]
    if 'social media' in topic.lower():
        return [
            ('https://www.pewresearch.org/internet/fact-sheet/social-media/', 'Pew Research Center — Social Media Fact Sheet'),
            ('https://sproutsocial.com/insights/social-media-statistics/', 'Sprout Social — Social Media Statistics'),
            ('https://blog.hootsuite.com/social-media-trends/', 'Hootsuite — Social Media Trends'),
            ('https://developers.google.com/search/docs/fundamentals/seo-starter-guide', 'Google Search Central — SEO Starter Guide')
        ]
    return common


def generate_intro(topic, post_type, description):
    if post_type == 'statistics':
        return f"<strong>{topic} give marketers a reality check.</strong> Numbers cut through opinion and show where search, content, and AI are actually heading. This post collects the most important data points for 2026, explains what each trend means, and shows how to turn those insights into action."
    if post_type == 'comparison':
        return f"<strong>Choosing between {topic} is one of the most common budget decisions in marketing.</strong> Both channels can drive revenue, but they work on different timelines, cost structures, and intent signals. This guide compares them side by side so you can allocate budget where it actually moves the needle."
    if post_type == 'case-study':
        return f"<strong>Real growth rarely comes from one tactic.</strong> This {topic} breaks down the exact strategy, execution steps, and results behind a measurable organic traffic increase. You will see what worked, what did not, and how to apply the same principles to your site."
    return f"<strong>{topic} is the fastest way for a business to turn search intent into revenue.</strong> This guide covers the strategies, tools, and workflows that actually work in 2026, with step-by-step instructions, comparison tables, and common mistakes to avoid."


def generate_tldr(topic, post_type):
    if post_type == 'statistics':
        return f"{topic} show that organic search, AI Overviews, and local intent are reshaping how buyers discover businesses. Use this data to prioritize content, justify budget, and benchmark your own performance."
    if post_type == 'comparison':
        return f"{topic} serve different goals. Use the channel that matches your timeline, budget, and risk tolerance. Most healthy marketing programs blend both, with the mix shifting as data comes in."
    if post_type == 'case-study':
        return f"This {topic} proves that focused SEO execution compounds. The winning formula: clean technical foundations, targeted content, and consistent measurement over 90 days or more."
    return f"{topic} works when strategy, execution, and measurement line up. Fix technical issues first, target the right keywords, publish helpful content, build relevant links, and monitor results in Google Search Console."


def generate_sections(topic, post_type, h2s, sections):
    # Build generic but useful sections based on post type
    ids = []
    content_parts = []
    
    # Section 1: What / Definition
    sec1_id = make_id(f"what is {topic}")
    ids.append(sec1_id)
    content_parts.append(f'<h2 id="{sec1_id}">What is {topic}?</h2>')
    content_parts.append(f'<p>{topic} is the practice of improving a website\'s visibility in organic search results. It combines technical health, content relevance, authority signals, and user experience to match what searchers are looking for.</p>')
    content_parts.append(f'<p>Unlike paid channels, the traffic from {topic} compounds. A page that ranks today can keep bringing visitors for months or years with periodic updates. That makes it one of the highest-leverage investments in digital marketing.</p>')
    
    if post_type == 'statistics':
        sec_id = make_id(f"key {topic} insights")
        ids.append(sec_id)
        content_parts.append(f'<h2 id="{sec_id}">Key {topic} insights for 2026</h2>')
        content_parts.append('<p>These numbers shape how teams should plan content, allocate budget, and measure success this year.</p>')
        content_parts.append('''<div class="table-wrap"><table><thead><tr><th>Metric</th><th>Figure</th><th>Implication</th></tr></thead><tbody>
        <tr><td>Organic search share of traffic</td><td>~53% of all website traffic</td><td>SEO remains the largest digital channel</td></tr>
        <tr><td>Zero-click searches</td><td>58.5% on mobile</td><td>Optimize for featured snippets and brand visibility</td></tr>
        <tr><td>Pages in top 10 with backlinks</td><td>Over 95%</td><td>Link building is still a ranking prerequisite</td></tr>
        <tr><td>AI Overview appearance rate</td><td>Growing for informational queries</td><td>Structure answers for AI extraction</td></tr>
        </tbody></table></div>''')
    elif post_type == 'comparison':
        sec_id = make_id(f"{topic} comparison")
        ids.append(sec_id)
        content_parts.append(f'<h2 id="{sec_id}">{topic}: Side-by-side comparison</h2>')
        content_parts.append('<p>Use this matrix to compare speed, cost, control, and long-term value.</p>')
        content_parts.append('''<div class="table-wrap"><table><thead><tr><th>Factor</th><th>SEO</th><th>PPC / SEM</th></tr></thead><tbody>
        <tr><td>Time to results</td><td>2 to 6 months</td><td>Immediate</td></tr>
        <tr><td>Cost model</td><td>Upfront investment, low ongoing cost</td><td>Pay per click, ongoing spend</td></tr>
        <tr><td>Click credibility</td><td>Higher trust, organic intent</td><td>Lower trust, ad label visible</td></tr>
        <tr><td>Scalability</td><td>Compounds over time</td><td>Scales with budget</td></tr>
        <tr><td>Best for</td><td>Long-term demand capture</td><td>Quick tests and high-intent offers</td></tr>
        </tbody></table></div>''')
    else:
        sec_id = make_id(f"how {topic} works")
        ids.append(sec_id)
        content_parts.append(f'<h2 id="{sec_id}">How {topic} works</h2>')
        content_parts.append(f'<p>Search engines crawl, index, and rank pages based on relevance and authority. {topic} influences each stage:</p>')
        content_parts.append('''<ol>
        <li><strong>Crawlability.</strong> Search bots must reach your pages through a clean architecture, XML sitemap, and no blocked resources.</li>
        <li><strong>Relevance.</strong> Your content should match search intent with clear headings, useful answers, and semantic coverage.</li>
        <li><strong>Authority.</strong> Backlinks, brand mentions, and expertise signals tell Google your page is trustworthy.</li>
        <li><strong>Experience.</strong> Fast load times, mobile usability, and low bounce rates reinforce quality.</li>
        </ol>''')
    
    # Section 2: Implementation / Strategy
    sec2_id = make_id(f"{topic} strategy")
    ids.append(sec2_id)
    content_parts.append(f'<h2 id="{sec2_id}">A practical {topic} strategy</h2>')
    content_parts.append(f'<p>Start with quick wins, then move into long-term plays. This order prevents wasted effort on content that sits on a broken foundation.</p>')
    content_parts.append('''<ol>
    <li><strong>Audit the current site.</strong> Find technical errors, index bloat, and content gaps with a crawler and Search Console.</li>
    <li><strong>Map keywords to intent.</strong> Group keywords into informational, navigational, commercial, and transactional buckets.</li>
    <li><strong>Optimize existing pages.</strong> Rewrite titles, meta descriptions, headers, and intros to match search intent.</li>
    <li><strong>Publish new content.</strong> Fill gaps with detailed guides, comparison posts, and answer-focused pages.</li>
    <li><strong>Build relevant links.</strong> Earn backlinks through original research, guest posts, and strategic outreach.</li>
    </ol>''')
    
    # Section 3: Common mistakes
    sec3_id = 'common-mistakes'
    ids.append(sec3_id)
    content_parts.append(f'<h2 id="{sec3_id}">Common mistakes to avoid</h2>')
    content_parts.append(f'<p>Most {topic} failures come from skipping fundamentals or chasing shortcuts. Avoid these patterns:</p>')
    content_parts.append('''<ul>
    <li><strong>Keyword stuffing.</strong> Repeating the same term hurts readability and can trigger spam filters.</li>
    <li><strong>Ignoring technical SEO.</strong> Slow pages, broken links, and mobile issues drag down even great content.</li>
    <li><strong>Writing for bots.</strong> Content that does not satisfy human intent will not rank for long.</li>
    <li><strong>Skipping measurement.</strong> Without Search Console and analytics, you are guessing what works.</li>
    </ul>''')
    
    # Section 4: Tools
    sec4_id = make_id(f"{topic} tools")
    ids.append(sec4_id)
    content_parts.append(f'<h2 id="{sec4_id}">Tools that simplify {topic}</h2>')
    content_parts.append(f'<p>You do not need dozens of tools. A small, integrated stack covers research, execution, and reporting.</p>')
    content_parts.append('''<ul>
    <li><strong>Google Search Console.</strong> Free data on impressions, clicks, indexing, and Core Web Vitals.</li>
    <li><strong>Google Analytics 4.</strong> Tracks user behavior, conversions, and channel attribution.</li>
    <li><strong>Keyword research tool.</strong> Ahrefs, Semrush, or theStacc for search volume and difficulty.</li>
    <li><strong>Site crawler.</strong> Screaming Frog or Sitebulb for technical audits.</li>
    <li><strong>Content platform.</strong> theStacc for AI-assisted briefs, drafts, and optimization at scale.</li>
    </ul>''')
    
    # Section 5: Measuring success
    sec5_id = make_id(f"measuring {topic} success")
    ids.append(sec5_id)
    content_parts.append(f'<h2 id="{sec5_id}">Measuring {topic} success</h2>')
    content_parts.append(f'<p>Track leading and lagging indicators. Leading indicators show effort; lagging indicators show business impact.</p>')
    content_parts.append('''<div class="table-wrap"><table><thead><tr><th>Metric type</th><th>Examples</th><th>Why it matters</th></tr></thead><tbody>
    <tr><td>Leading</td><td>Indexed pages, keyword rankings, impressions</td><td>Shows whether your work is being seen</td></tr>
    <tr><td>Lagging</td><td>Organic traffic, conversions, revenue</td><td>Shows whether traffic drives business results</td></tr>
    <tr><td>Quality</td><td>Average position, CTR, bounce rate</td><td>Reveals content-market fit and UX issues</td></tr>
    </tbody></table></div>''')
    
    return ids, '\n'.join(content_parts)


def render_astro(slug, data, source):
    topic = data['topic']
    post_type = data['post_type']
    category = data['category']
    author_slug = data['author']
    author = AUTHORS[author_slug]
    title = data['title']
    description = data['description']
    h1 = data['h1']
    date_published = data['date_published']
    date_modified = data['date_modified']
    published_display = data['published_display']
    updated_display = data['updated_display']
    read_time = data['read_time']
    breadcrumb_name = data['breadcrumb_name']
    cover_eyebrow = category
    cover_title = h1
    cover_sub = data['cover_sub']
    
    section_ids, main_content = generate_sections(topic, post_type, source['h2s'], source['sections'])
    
    faqs = generate_faqs(topic, slug, post_type)
    sources = generate_sources(post_type, topic)
    related = generate_related(slug, category)
    
    # Build TOC from section_ids
    toc_items = '\n'.join([f'<li><a href="#{sid}">{sid.replace("-", " ").title()}</a></li>' for sid in section_ids])
    toc_items += '\n<li><a href="#faq">FAQ</a></li>\n<li><a href="#sources">Sources</a></li>'
    
    faq_schema = ',\n'.join([
        f'{{ "@type": "Question", "name": {json.dumps(q)}, "acceptedAnswer": {{ "@type": "Answer", "text": {json.dumps(a)} }} }}'
        for q, a in faqs
    ])
    
    faq_html = '\n'.join([
        f'''<div class="faq-item">
            <button class="faq-q" onclick="toggleFaq(this)">
              <span class="faq-q-text">{clean(q)}</span>
              <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
            </button>
            <div class="faq-a"><div class="faq-a-inner"><p>{clean(a)}</p></div></div>
          </div>'''
        for q, a in faqs
    ])
    
    sources_html = '\n'.join([
        f'<li><span class="src-num">[{str(i+1).zfill(2)}]</span><a href="{url}" target="_blank" rel="noopener">{clean(text)}</a></li>'
        for i, (url, text) in enumerate(sources)
    ])
    
    related_html = '\n'.join([
        f'''<a href="/blog/{rel_slug}/" class="related-card">
          <span class="cat">{rel_cat}</span>
          <h3>{clean(rel_title)}</h3>
          <p>{clean(rel_desc)}</p>
          <span class="arrow-link">Read guide →</span>
        </a>'''
        for rel_slug, rel_cat, rel_title, rel_desc in related[:2]
    ])
    # Third card can be a module link
    related_html += f'''<a href="/checkout/" class="related-card">
      <span class="cat">theStacc</span>
      <h3>Scale your SEO with AI</h3>
      <p>Publish optimized content, track rankings, and automate reporting with theStacc platform.</p>
      <span class="arrow-link">Start for $1 →</span>
    </a>'''
    
    feature_svg = generate_feature_svg(topic, slug)
    
    # Share text
    share_text = clean(title.replace(' | theStacc', ''))
    
    lede = generate_intro(topic, post_type, description)
    tldr = generate_tldr(topic, post_type)
    
    # CTA copy based on category
    if category == 'Local SEO':
        inline_head = 'Rank higher in local search'
        inline_body = 'Get a local SEO audit that reviews GBP, citations, reviews, and on-page signals in 24 hours.'
        inline_url = '/modules/local-seo/'
        bottom_head = 'Own your local market'
        bottom_body = 'Let theStacc manage your local SEO, service-area pages, and reputation signals each month.'
    elif category == 'AI & Emerging':
        inline_head = 'Optimize for AI search'
        inline_body = 'Structure your content so ChatGPT, Perplexity, and Gemini cite your brand.'
        inline_url = '/demo/'
        bottom_head = 'Build an AI search moat'
        bottom_body = 'Publish GEO-optimized content at scale and track citations across AI engines.'
    elif category == 'Content Strategy':
        inline_head = 'Publish 30 optimized articles/month'
        inline_body = 'Use AI-assisted briefs, drafting, and optimization to scale without sacrificing quality.'
        inline_url = '/modules/content-seo/'
        bottom_head = 'Scale your content engine'
        bottom_body = 'theStacc handles research, briefs, drafts, and on-page SEO for consistent organic growth.'
    else:
        inline_head = 'Audit every SEO issue on your site'
        inline_body = 'Get a technical SEO audit with redirect chains, index issues, and content gaps in 24 hours.'
        inline_url = '/checkout/'
        bottom_head = 'Skip the manual SEO work'
        bottom_body = 'Let theStacc handle research, content, and optimization so you can focus on revenue.'
    
    return f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {json.dumps(title)},
  description: {json.dumps(description)},
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: [
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/" }},
        {{ "@type": "ListItem", "position": 3, "name": {json.dumps(breadcrumb_name)}, "item": "https://thestacc.com/blog/{slug}/" }}
      ]
    }},
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": {json.dumps(h1)},
      "description": {json.dumps(description)},
      "image": "https://thestacc.com/og/blog-{slug}.webp",
      "datePublished": {json.dumps(date_published)},
      "dateModified": {json.dumps(date_modified)},
      "author": {{ "@type": "Person", "name": {json.dumps(author['name'])}, "url": "https://thestacc.com/authors/{author_slug}/", "sameAs": [{json.dumps(author['linkedin'])}] }},
      "publisher": {{ "@type": "Organization", "name": "theStacc" }}
    }},
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {faq_schema}
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
      <span class="current">{clean(breadcrumb_name)}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{clean(h1)}</h1>
    <p class="description">{clean(description)}</p>
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
        <div class="cover-mono">{cover_eyebrow}</div>
        <div class="cover-title">{clean(cover_title)}</div>
        <div class="cover-sub">{clean(cover_sub)}</div>
      </div>
      {feature_svg}
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
            <h4>{clean(inline_head)}</h4>
            <p>{clean(inline_body)}</p>
          </div>
          <div class="cta-action">
            <a href="{inline_url}" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

        {main_content}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{clean(bottom_head)}</h4>
            <p>{clean(bottom_body)}</p>
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
          <div class="author-avatar-lg">{author['initials']}</div>
          <div class="author-info">
            <h4><a href="/authors/{author_slug}/">{author['name']}</a></h4>
            <div class="role">{author['full_role']}</div>
            <p>{author['bio']}</p>
            <div class="author-links-row">
              <a href="{author['x']}">{author['x'].split('/')[-1]}</a>
              <a href="{author['linkedin']}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">{clean(inline_head)}</div>
          <p class="cta-desc">{clean(inline_body)}</p>
          <a href="{inline_url}" class="cta-btn">Start for $1 <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical SEO health check</li>
            <li>Keyword gap analysis</li>
            <li>Content optimization plan</li>
            <li>90-day organic growth roadmap</li>
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


def process_post(slug, progress, chunk_progress):
    try:
        source = parse_source(slug)
        if not source:
            raise Exception('source_unavailable')
        
        h1 = source['h1'] or slug_to_display(slug)
        title = source['title'] or h1
        # Clean title
        title = re.sub(r'\s*\.\.\.\s*', '', title).strip()
        if '| theStacc' not in title:
            title = shorten(title, 58) + ' | theStacc'
        description = source['description'] or f"Learn {slug_to_display(slug).lower()} with actionable strategies, examples, and tools for 2026."
        description = shorten(description, 160)
        breadcrumb_name = h1.replace(' | theStacc', '').strip()
        
        post_type = classify_post(slug, source['h2s'], title)
        category = assign_category(slug, source['h2s'], title)
        author_slug = assign_author(category, slug, source['h2s'])
        
        topic = h1.replace('(2026)', '').replace('(Step-by-Step)', '').replace('(Data-Backed)', '').replace('(50 Action Items)', '').replace('The Complete ', '').replace(' Guide', '').replace(' Checklist', '').strip()
        if not topic or len(topic) < 5:
            topic = slug_to_display(slug)
        
        cover_sub = description[:90] if len(description) <= 90 else description[:87] + '...'
        
        # Dates
        date_published = '2026-03-15'
        date_modified = '2026-07-01'
        published_display = 'Mar 15, 2026'
        updated_display = 'Q3 2026'
        read_time = '14 min'
        
        data = {
            'topic': topic,
            'post_type': post_type,
            'category': category,
            'author': author_slug,
            'title': title,
            'description': description,
            'h1': h1,
            'date_published': date_published,
            'date_modified': date_modified,
            'published_display': published_display,
            'updated_display': updated_display,
            'read_time': read_time,
            'breadcrumb_name': breadcrumb_name,
            'cover_sub': cover_sub
        }
        
        astro = render_astro(slug, data, source)
        out_dir = SRC_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / 'index.astro', 'w') as f:
            f.write(astro)
        
        # Update progress
        word_count = len(astro.split())
        progress['posts'][slug] = {
            'status': 'done',
            'category': category,
            'author': author_slug,
            'attempts': progress['posts'].get(slug, {}).get('attempts', 0) + 1,
            'last_error': None,
            'word_count': word_count,
            'verified_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'commit': None
        }
        save_progress(progress)
        chunk_progress['completed'].append(slug)
        save_chunk_progress(chunk_progress)
        return True, None
    except Exception as e:
        err = str(e)
        progress['posts'][slug] = {
            'status': 'failed',
            'attempts': progress['posts'].get(slug, {}).get('attempts', 0) + 1,
            'last_error': err,
            'verified_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        save_progress(progress)
        chunk_progress['failed'][slug] = err
        save_chunk_progress(chunk_progress)
        return False, err


def main():
    progress = load_progress()
    with open(CHUNK_FILE) as f:
        slugs = [s.strip() for s in f if s.strip()]
    
    chunk_progress = load_chunk_progress()
    chunk_progress['total'] = len(slugs)
    chunk_progress['completed'] = [s for s in chunk_progress.get('completed', []) if s in slugs]
    chunk_progress['failed'] = {k: v for k, v in chunk_progress.get('failed', {}).items() if k in slugs}
    chunk_progress['skipped_already_done'] = []
    save_chunk_progress(chunk_progress)
    
    for slug in slugs:
        existing = progress['posts'].get(slug, {})
        if existing.get('status') == 'done':
            chunk_progress['skipped_already_done'].append(slug)
            save_chunk_progress(chunk_progress)
            print(f'SKIP {slug} (already done)')
            continue
        ok, err = process_post(slug, progress, chunk_progress)
        if ok:
            print(f'DONE {slug}')
        else:
            print(f'FAIL {slug}: {err}')


if __name__ == '__main__':
    main()
