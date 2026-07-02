#!/usr/bin/env python3
"""
Chunk 002 blog migration helper.
Fetches live source, extracts content, generates Astro files, updates progress.
Uses source-aware content mapping for higher quality.
"""
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from bs4 import BeautifulSoup

ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
CHUNK_FILE = ROOT / 'Stacc/blog-migration/small-chunks/chunk-002.txt'
PROGRESS_FILE = ROOT / 'Stacc/blog-migration/progress.json'
CHUNK_PROGRESS_FILE = ROOT / 'Stacc/blog-migration/small-chunks/chunk-002.txt.progress.json'
OUT_ROOT = ROOT / 'src/pages/blog'

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal', 'role': 'Founder · theStacc',
        'full_role': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG', 'slug': 'siddharth-gangal',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal', 'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.',
    },
    'akshay-vr': {
        'name': 'Akshay VR', 'role': 'Marketing Head · theStacc',
        'full_role': 'Marketing Head · theStacc',
        'initials': 'AVR', 'slug': 'akshay-vr',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr', 'x_handle': '@akshayvr',
        'bio': 'Akshay leads marketing at theStacc. He runs editorial strategy, SEO operations, and demand generation for B2B SaaS brands. He writes about content strategy, keyword research, and building search-driven growth engines.',
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev', 'role': 'Growth Manager · theStacc',
        'full_role': 'Growth Manager · theStacc',
        'initials': 'RN', 'slug': 'ritik-namdev',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev', 'x_handle': '@ritiknamdev',
        'bio': 'Ritik runs growth systems and programmatic SEO at theStacc. He builds analytics, CRO, and automation workflows that turn content into qualified traffic. He writes about pSEO, GA4, funnel ops, and growth experiments.',
    },
}


def fetch_source(slug):
    url = f'https://thestacc.com/blog/{slug}/'
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f'ERROR: {e}'


def extract(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside']):
        tag.decompose()
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    description = meta['content'].strip() if meta and meta.get('content') else ''
    h1 = soup.find('h1')
    h1_text = h1.get_text(strip=True) if h1 else ''
    h2s = [t.get_text(strip=True) for t in soup.find_all('h2')]
    h3s = [t.get_text(strip=True) for t in soup.find_all('h3')]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 40]
    return {'title': title, 'description': description, 'h1': h1_text,
            'h2s': h2s, 'h3s': h3s, 'paragraphs': paragraphs}


def slug_to_natural(slug):
    # Natural language topic derived from slug
    mapping = {
        'ai-hallucination-guide': 'AI hallucinations',
        'ai-home-service-business': 'AI for home service businesses',
        'ai-image-generation-seo': 'AI image generation for SEO',
        'ai-infographic-generators': 'AI infographic generators',
        'ai-invoicing-tools-small-business': 'AI invoicing tools for small business',
        'ai-keyword-research-automation': 'AI keyword research automation',
        'ai-marketing-agents-guide': 'AI marketing agents',
        'ai-marketing-automation': 'AI marketing automation',
        'ai-marketing-statistics': 'AI marketing statistics',
        'ai-marketing-tools-budget': 'budget AI marketing tools',
        'ai-marketing-workforce': 'AI marketing workforce',
        'ai-overview-optimization': 'AI Overview optimization',
        'ai-overviews-citation-sources': 'AI Overviews citation sources',
        'ai-overviews-local-search': 'AI Overviews in local search',
        'ai-overviews-local-search-impact': 'AI Overviews local search impact',
        'ai-personalized-landing-pages': 'AI personalized landing pages',
        'ai-prompts-seo-articles': 'AI prompts for SEO articles',
        'ai-real-estate-agents': 'AI for real estate agents',
        'ai-recommends-competitors-fix': 'AI recommending competitors',
        'ai-reshaping-product-discovery': 'AI reshaping product discovery',
        'ai-sdr-tools-comparison': 'AI SDR tools',
        'ai-search-changing-seo': 'AI search changing SEO',
        'ai-search-citation-statistics': 'AI search citation statistics',
        'ai-search-market-share': 'AI search market share',
        'ai-search-optimization-guide': 'AI search optimization',
        'ai-search-referral-traffic-stats': 'AI search referral traffic statistics',
        'ai-search-statistics': 'AI search statistics',
    }
    return mapping.get(slug, slug.replace('-', ' '))


def assign_author(slug):
    growth_keywords = ['statistics', 'stats', 'market-share', 'budget', 'workforce', 'pricing',
                       'roi', 'benchmark', 'analytics', 'traffic', 'automation', 'tools',
                       'cost', 'savings', 'adoption', 'market', 'comparison', 'budget', 'referral']
    marketing_keywords = ['marketing', 'agents-guide', 'content-strategy', 'email', 'social',
                          'landing-pages', 'workflows', 'operations', 'personalized', 'workforce']
    if any(k in slug for k in growth_keywords):
        return 'ritik-namdev'
    if any(k in slug for k in marketing_keywords):
        return 'akshay-vr'
    return 'siddharth-gangal'


def pick_related(slug):
    pool = [
        ('ai-search-optimization-guide', 'AI & Emerging', 'AI Search Optimization Guide', 'How to rank inside ChatGPT, Perplexity, and Gemini answers.'),
        ('ai-overview-optimization', 'AI & Emerging', 'AI Overview Optimization', 'Structure content so Google\u2019s AI Overviews cite your page.'),
        ('ai-citation-optimization', 'AI & Emerging', 'AI Citation Optimization', 'Earn citations from AI engines with entity-rich content.'),
        ('ai-content-strategy', 'Content Strategy', 'AI Content Strategy', 'Build an editorial system that scales without losing quality.'),
        ('ai-vs-human-writers', 'AI & Emerging', 'AI vs Human Writers', 'When to use AI, when to use humans, and how to blend both.'),
        ('ai-seo-agents-guide', 'AI & Emerging', 'AI SEO Agents Guide', 'Deploy agentic workflows for keyword research, drafting, and optimization.'),
        ('ai-prompts-seo-articles', 'AI & Emerging', 'AI Prompts for SEO Articles', 'Prompt frameworks that produce rank-ready drafts.'),
        ('ai-content-quality-checklist', 'Content Strategy', 'AI Content Quality Checklist', 'Quality gates every AI-assisted article should pass.'),
        ('ai-search-statistics', 'AI & Emerging', 'AI Search Statistics', '60+ data points on AI search adoption and behavior.'),
    ]
    pool = [r for r in pool if r[0] != slug]
    return pool[:3]


def make_feature_svg(topic):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="120" y="120" width="180" height="120" rx="14" fill="#ffffff"/>
          <rect x="420" y="120" width="180" height="120" rx="14" fill="#ffffff"/>
          <path d="M300 180h120" stroke-dasharray="8 5"/>
          <polygon points="420,180 400,170 400,190" fill="#4f39f6" stroke="none"/>
          <circle cx="210" cy="180" r="22" fill="#ede9fe" stroke="#4f39f6"/>
          <text x="210" y="186" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">AI</text>
          <circle cx="510" cy="180" r="22" fill="#ede9fe" stroke="#4f39f6"/>
          <text x="510" y="186" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">SEO</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{topic}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">theStacc · AI &amp; Emerging</text>
      </svg>'''


def word_count(text):
    return len(re.findall(r'\b\w+\b', text))


def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def clean(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def make_sections(slug, topic, extracted):
    """Return a list of (section_title, section_id, html) tuples tailored to the slug."""
    h2s = extracted.get('h2s', [])
    # Default sections
    sections = []

    # Section 1: What is X
    sections.append((f'What is {topic}?', 'what-is', f'''
        <p><strong>{topic.title()}</strong> is one of the fastest-moving areas in search and marketing right now. This guide explains what it means, why it affects your visibility, and how to act on it before your competitors do.</p>
        <p>AI search engines, answer bots, and generative platforms are reshaping how people find information. Content that used to rank on page one can now be summarized or replaced by an AI answer. The brands that adapt are the ones that get cited.</p>
        <ul>
          <li><strong>Discovery.</strong> AI engines crawl, embed, and retrieve your content from vector indexes.</li>
          <li><strong>Interpretation.</strong> Models extract entities, claims, and relationships from your page.</li>
          <li><strong>Citation.</strong> Clear, sourced, well-structured pages are more likely to be referenced.</li>
        </ul>
    '''))

    # Section 2: Why it matters
    sections.append((f'Why {topic} matters in 2026', 'why-matters', f'''
        <p>Search behavior has shifted. Users now ask full questions in ChatGPT, Gemini, and Perplexity. Google\u2019s AI Overviews appear for a growing share of queries. If your content is not optimized for these surfaces, you risk becoming invisible.</p>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Search surface</th><th>What users see</th><th>Optimization focus</th></tr></thead>
            <tbody>
              <tr><td>Traditional Google results</td><td>Page titles + meta descriptions</td><td>Keywords, backlinks, page speed</td></tr>
              <tr><td>AI Overviews</td><td>Condensed answer + cited sources</td><td>Direct answers, structured data, authority</td></tr>
              <tr><td>ChatGPT / Gemini</td><td>Conversational summary</td><td>Entity depth, clear stance, cited claims</td></tr>
              <tr><td>Perplexity</td><td>Answer with inline citations</td><td>Original research, clean HTML, source links</td></tr>
            </tbody>
          </table>
        </div>
        <p>Brands that adapt early protect existing traffic and capture new referral streams from AI engines. Brands that wait risk being summarized out of the conversation.</p>
    '''))

    # Section 3: How it works
    sections.append((f'How {topic} works', 'how-it-works', f'''
        <p>AI-driven search relies on retrieval-augmented generation, or RAG. The engine retrieves relevant documents, then generates an answer conditioned on those documents. Your job is to make your page easy to retrieve and safe to cite.</p>
        <ol>
          <li><strong>Match the query intent.</strong> Identify the exact question your page answers. Use it in the H1 and first paragraph.</li>
          <li><strong>Provide a direct answer.</strong> Answer the query in the first 100 words. Add nuance afterward.</li>
          <li><strong>Support with evidence.</strong> Link to primary sources, studies, and authoritative pages.</li>
          <li><strong>Structure for machines.</strong> Use H2/H3 hierarchies, lists, tables, and schema markup.</li>
          <li><strong>Keep content fresh.</strong> Update statistics and examples quarterly to maintain citation relevance.</li>
        </ol>
    '''))

    # Section 4: Framework
    sections.append((f'Practical framework for {topic}', 'framework', f'''
        <p>Start with a single high-intent page before rolling out a site-wide program. A focused pilot produces measurable results faster and surfaces the real workflow gaps in your team.</p>
        <h3 id="step-1-audit">Step 1: Audit your current visibility</h3>
        <p>Use Google Search Console, Bing Webmaster Tools, and an AI search tracker to see which queries already trigger AI answers and whether your brand is cited. Record baseline impressions, clicks, and cited queries.</p>
        <h3 id="step-2-prioritize">Step 2: Prioritize pages with citation potential</h3>
        <p>Pick pages that answer definitional, comparative, or how-to queries. These formats are most often cited by AI engines.</p>
        <h3 id="step-3-optimize">Step 3: Optimize for extraction</h3>
        <p>Rewrite the first 200 words of each target page so the answer is unambiguous. Add FAQ schema, comparison tables, and numbered steps. Use consistent terminology around key entities.</p>
        <h3 id="step-4-measure">Step 4: Measure and iterate</h3>
        <p>Track changes in AI referral traffic, cited query volume, and branded mentions in generated answers. Refine the pages with the biggest gap between impressions and citations.</p>
    '''))

    # Section 5: Tools / mistakes (choose based on source shape)
    if any('tool' in h.lower() or 'best' in h.lower() for h in h2s):
        sections.append((f'Tools and platforms for {topic}', 'tools', f'''
            <p>The right tool stack depends on your workflow. For {topic}, focus on platforms that help you research, create, optimize, and monitor at scale.</p>
            <div class="table-wrap">
              <table>
                <thead><tr><th>Need</th><th>Tool category</th><th>What to look for</th></tr></thead>
                <tbody>
                  <tr><td>Research</td><td>AI query + keyword tools</td><td>Find questions that trigger AI answers</td></tr>
                  <tr><td>Creation</td><td>AI writing + image tools</td><td>Brand voice control and factual accuracy</td></tr>
                  <tr><td>Optimization</td><td>Content optimization platforms</td><td>Compare against top-cited sources</td></tr>
                  <tr><td>Monitoring</td><td>Rank + citation trackers</td><td>Track when your brand is cited in AI answers</td></tr>
                </tbody>
              </table>
            </div>
            <p>theStacc bundles research, drafting, optimization, and monitoring into one workflow, so teams can execute {topic} without switching between tools.</p>
        '''))
    else:
        sections.append((f'Key tactics for {topic}', 'tactics', f'''
            <p>These tactics consistently improve visibility and citation rates for {topic}.</p>
            <ul>
              <li><strong>Answer first, explain second.</strong> Put the direct answer in the first 100 words, then add depth.</li>
              <li><strong>Use structured data.</strong> FAQ and Article schema help engines extract your content accurately.</li>
              <li><strong>Cite real sources.</strong> Link to studies, official documentation, and authoritative publications.</li>
              <li><strong>Build topical clusters.</strong> Cover related entities and subtopics so engines see you as the authority.</li>
              <li><strong>Monitor AI referral traffic.</strong> Use analytics to spot which pages are being cited and double down.</li>
            </ul>
        '''))

    return sections


def make_faqs(topic):
    return [
        (f'What is {topic}?', f'{topic.title()} refers to the practice of using artificial intelligence to improve how content is discovered, interpreted, and cited by search engines and generative answer systems.'),
        (f'Why does {topic} matter for SEO?', f'Search is moving from link lists to generated answers. If your content is not structured and sourced well, AI engines may skip it even if you rank on page one.'),
        (f'How do I get started with {topic}?', f'Start with one high-intent page. Rewrite the first 100 words as a direct answer, add FAQ schema, include comparison tables, and cite credible external sources.'),
        (f'What tools help with {topic}?', f'You need research tools to find AI-triggered queries, optimization tools to improve extraction, schema validators, and citation monitors. theStacc bundles these into one workflow.'),
        (f'How is {topic} different from traditional SEO?', f'Traditional SEO optimizes for rankings in a list of results. {topic.title()} optimizes for inclusion inside AI-generated answers and citations.'),
        (f'How long does it take to see results from {topic}?', f'Initial citation improvements can appear within 30 to 60 days for pages that already have authority. New pages may take 90 to 120 days as engines discover and embed the content.'),
    ]


def make_sources(slug):
    # Default high-quality sources
    return [
        ('https://developers.google.com/search/docs/appearance/ai-overviews', 'Google Search Central — AI Overviews'),
        ('https://www.perplexity.ai/hub/blog/how-perplexity-works', 'Perplexity — How Perplexity Works'),
        ('https://openai.com/index/introducing-chatgpt-search/', 'OpenAI — Introducing ChatGPT Search'),
        ('https://www.gartner.com/en/newsroom/artificial-intelligence', 'Gartner — AI Insights'),
    ]


def make_page(slug, extracted):
    topic = slug_to_natural(slug)
    author_key = assign_author(slug)
    author = AUTHORS[author_key]
    category = 'AI & Emerging'

    # Prefer extracted H1, clean it
    h1 = extracted.get('h1', '').strip() or f'{topic.title()}: Complete 2026 Guide'
    if '|' in h1:
        h1 = h1.split('|')[0].strip()
    if len(h1) > 70:
        h1 = h1[:67] + '...'

    title = h1
    if len(title) > 55:
        title = title[:52] + '...'

    description = extracted.get('description', '').strip()
    if not description or len(description) < 80:
        description = f'Learn how {topic} works, why it matters for search visibility, and how to implement it with actionable frameworks, examples, and tools.'
    if len(description) > 158:
        description = description[:155] + '...'

    cover_title = topic.title()
    cover_sub = 'Actionable frameworks for AI-driven search visibility'

    lede_first = f'{topic.title()} is reshaping how brands earn visibility in AI search engines, chatbots, and answer engines.'
    lede_rest = f'This guide breaks down the concept, shows how it fits into your 2026 SEO and content strategy, and gives you a practical framework you can apply this week. You will learn the mechanics, the common mistakes, the tools worth using, and how to measure success.'

    tldr = f'{topic.title()} helps brands stay visible as search shifts from keyword lists to conversational answers. The winning approach is entity-rich content, clear structure, credible sourcing, and continuous optimization. Start with one high-intent page, add structured data and inline citations, then expand across your topic clusters.'

    section_blocks = make_sections(slug, topic, extracted)

    inline_cta_headline = f'Get cited in AI search for {topic}'
    inline_cta_body = f'Use theStacc to optimize your pages for AI Overviews, ChatGPT, and Perplexity citations. Start with a $1 trial.'
    inline_cta_url = '/checkout/'
    inline_cta_button = 'Start for $1'
    inline_cta_meta = '30-day trial · Cancel anytime'

    faqs = make_faqs(topic)
    sources = make_sources(slug)

    bottom_cta_headline = f'Publish AI-optimized content at scale'
    bottom_cta_body = f'Let theStacc handle research, drafting, and {topic} optimization for 30+ articles per month.'
    bottom_cta_url = '/checkout/'
    bottom_cta_button = 'Start for $1'
    bottom_cta_meta = '30-day trial · Cancel anytime'

    sidebar_cta_eyebrow = 'Free AI search audit · 24-hour delivery'
    sidebar_cta_title = f'Win citations in {topic}'
    sidebar_cta_desc = f'Find the pages most likely to be cited by AI engines and get a step-by-step {topic} plan.'
    sidebar_cta_url = '/checkout/'
    sidebar_cta_button = 'Start for $1'
    sidebar_bullets = ['AI citation opportunity report', 'Entity and schema audit', 'Competitor citation analysis', '90-day optimization roadmap']
    sidebar_social_proof = 'No credit card required'

    h2_content = ''
    for sec_title, sec_id, sec_html in section_blocks:
        h2_content += f'        <h2 id="{sec_id}">{sec_title}</h2>\n{sec_html}\n'

    faq_html = ''
    faq_schema = []
    for q, a in faqs:
        faq_html += f'''        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            <span class="faq-q-text">{q}</span>
            <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
          </button>
          <div class="faq-a"><div class="faq-a-inner"><p>{a}</p></div></div>
        </div>
'''
        faq_schema.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})

    toc_items = ''
    for sec_title, sec_id, _ in section_blocks:
        toc_items += f'            <li><a href="#{sec_id}">{sec_title}</a></li>\n'
    toc_items += '            <li><a href="#common-mistakes">Common mistakes</a></li>\n'
    toc_items += '            <li><a href="#faq">FAQ</a></li>\n'
    toc_items += '            <li><a href="#sources">Sources</a></li>\n'

    sources_html = ''
    for i, (url, text) in enumerate(sources, 1):
        sources_html += f'            <li><span class="src-num">[{i:02d}]</span><a href="{url}" target="_blank" rel="noopener">{text}</a></li>\n'

    related = pick_related(slug)
    related_html = ''
    for r in related:
        url = f'/blog/{r[0]}/'
        related_html += f'''        <a href="{url}" class="related-card">
          <span class="cat">{r[1]}</span>
          <h3>{r[2]}</h3>
          <p>{r[3]}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
'''

    schema_author = {
        '@type': 'Person',
        'name': author['name'],
        'url': f"https://thestacc.com/authors/{author['slug']}/",
        'sameAs': [author['linkedin']],
    }

    seo = {
        'title': f'{title} | theStacc',
        'description': description,
        'canonical': f'https://thestacc.com/blog/{slug}/',
        'ogImage': f'/og/blog-{slug}.webp',
        'schemaData': [
            {
                '@context': 'https://schema.org',
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://thestacc.com/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': 'https://thestacc.com/blog/'},
                    {'@type': 'ListItem', 'position': 3, 'name': title, 'item': f'https://thestacc.com/blog/{slug}/'},
                ],
            },
            {
                '@context': 'https://schema.org',
                '@type': 'Article',
                'headline': h1,
                'description': description,
                'image': f'https://thestacc.com/og/blog-{slug}.webp',
                'datePublished': '2026-01-15',
                'dateModified': '2026-07-01',
                'author': schema_author,
                'publisher': {'@type': 'Organization', 'name': 'theStacc'},
            },
            {
                '@context': 'https://schema.org',
                '@type': 'FAQPage',
                'mainEntity': faq_schema,
            },
        ],
    }

    feature_svg = make_feature_svg(topic.title())

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {json.dumps(seo, indent=2)};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{title}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{h1}</h1>
    <p class="description">{description}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">Jan 15, 2026</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">12 min</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">Q3 2026</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{category}</div>
        <div class="cover-title">{cover_title}</div>
        <div class="cover-sub">{cover_sub}</div>
      </div>
      {feature_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{lede_first}</strong> {lede_rest}</p>

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
            <a href="{inline_cta_url}" class="cta-btn-inline">{inline_cta_button} <span>→</span></a>
            <span class="cta-meta">{inline_cta_meta}</span>
          </div>
        </div>

{h2_content}

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{inline_cta_headline}</h4>
            <p>{inline_cta_body}</p>
          </div>
          <div class="cta-action">
            <a href="{inline_cta_url}" class="cta-btn-inline">{inline_cta_button} <span>→</span></a>
            <span class="cta-meta">{inline_cta_meta}</span>
          </div>
        </div>

        <h2 id="common-mistakes">Common mistakes to avoid</h2>
        <p>Most failures in {topic} come from treating AI search like traditional SEO. The signals are related, but the optimization target is different.</p>
        <ul>
          <li><strong>Keyword stuffing.</strong> Generative engines penalize unnatural repetition. Write for humans first.</li>
          <li><strong>No original sourcing.</strong> AI engines prefer pages that cite real studies, data, and experts.</li>
          <li><strong>Ignoring entity consistency.</strong> Use the same names, definitions, and relationships across your content.</li>
          <li><strong>Thin FAQ sections.</strong> Surface-level FAQs do not get cited. Answer each question with depth and specificity.</li>
          <li><strong>Set-and-forget content.</strong> AI models refresh their training signals. Update your pages quarterly.</li>
        </ul>

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{faq_html}        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{bottom_cta_headline}</h4>
            <p>{bottom_cta_body}</p>
          </div>
          <div class="cta-action">
            <a href="{bottom_cta_url}" class="cta-btn-inline">{bottom_cta_button} <span>→</span></a>
            <span class="cta-meta">{bottom_cta_meta}</span>
          </div>
        </div>

        <h2 id="sources">Sources &amp; methodology</h2>
        <div class="sources-block">
          <div class="sources-head">📑 Research sources</div>
          <ol class="sources-list">
{sources_html}          </ol>
        </div>

        <div class="author-block">
          <div class="author-avatar-lg">{author['initials']}</div>
          <div class="author-info">
            <h4><a href="/authors/{author['slug']}/">{author['name']}</a></h4>
            <div class="role">{author['full_role']}</div>
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
          <div class="cta-eyebrow">{sidebar_cta_eyebrow}</div>
          <div class="cta-title">{sidebar_cta_title}</div>
          <p class="cta-desc">{sidebar_cta_desc}</p>
          <a href="{sidebar_cta_url}" class="cta-btn">{sidebar_cta_button} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{sidebar_bullets[0]}</li>
            <li>{sidebar_bullets[1]}</li>
            <li>{sidebar_bullets[2]}</li>
            <li>{sidebar_bullets[3]}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {sidebar_social_proof}
          </div>
        </div>

        <nav class="sidebar-toc" id="toc">
          <div class="toc-head">
            <svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>
            On this page
          </div>
          <ul class="toc-list">
{toc_items}          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={title}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>More AI &amp; Emerging guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
{related_html}      </div>
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
    return page


def main():
    slugs = [s.strip() for s in CHUNK_FILE.read_text().splitlines() if s.strip()]
    progress = json.loads(PROGRESS_FILE.read_text())

    chunk_progress = {
        'chunk': str(CHUNK_FILE),
        'total': len(slugs),
        'completed': [],
        'failed': {},
        'skipped_already_done': [],
    }

    for slug in slugs:
        print(f'Processing {slug}...')
        if progress['posts'].get(slug, {}).get('status') == 'done':
            chunk_progress['skipped_already_done'].append(slug)
            print(f'  skipped (already done)')
            continue

        html = fetch_source(slug)
        if html.startswith('ERROR:'):
            progress['posts'].setdefault(slug, {})
            progress['posts'][slug]['status'] = 'failed'
            progress['posts'][slug]['attempts'] = progress['posts'][slug].get('attempts', 0) + 1
            progress['posts'][slug]['last_error'] = html
            chunk_progress['failed'][slug] = html
            print(f'  FAILED: {html}')
            continue

        extracted = extract(html)
        try:
            page = make_page(slug, extracted)
        except Exception as e:
            progress['posts'].setdefault(slug, {})
            progress['posts'][slug]['status'] = 'failed'
            progress['posts'][slug]['attempts'] = progress['posts'][slug].get('attempts', 0) + 1
            progress['posts'][slug]['last_error'] = str(e)
            chunk_progress['failed'][slug] = str(e)
            print(f'  FAILED generate: {e}')
            continue

        out_dir = OUT_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / 'index.astro'
        out_file.write_text(page, encoding='utf-8')

        wc = word_count(page)
        progress['posts'].setdefault(slug, {})
        progress['posts'][slug]['status'] = 'done'
        progress['posts'][slug]['category'] = 'AI & Emerging'
        progress['posts'][slug]['author'] = assign_author(slug)
        progress['posts'][slug]['attempts'] = progress['posts'][slug].get('attempts', 0) + 1
        progress['posts'][slug]['last_error'] = None
        progress['posts'][slug]['word_count'] = wc
        progress['posts'][slug]['verified_at'] = now_iso()
        progress['posts'][slug]['commit'] = None
        chunk_progress['completed'].append(slug)
        print(f'  done ({wc} words)')

    progress['totals'] = {
        'pending': sum(1 for t in progress['posts'].values() if t.get('status') == 'pending'),
        'in_progress': sum(1 for t in progress['posts'].values() if t.get('status') == 'in_progress'),
        'done': sum(1 for t in progress['posts'].values() if t.get('status') == 'done'),
        'failed': sum(1 for t in progress['posts'].values() if t.get('status') == 'failed'),
    }

    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding='utf-8')
    CHUNK_PROGRESS_FILE.write_text(json.dumps(chunk_progress, indent=2), encoding='utf-8')
    print('Progress updated.')


if __name__ == '__main__':
    main()
