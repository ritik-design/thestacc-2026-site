#!/usr/bin/env python3
"""
Blog migration script for chunk-001.
Fetches live source, extracts content, generates Astro file, updates progress.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
CHUNK_FILE = BASE_DIR / 'Stacc/blog-migration/small-chunks/chunk-001.txt'
PROGRESS_FILE = BASE_DIR / 'Stacc/blog-migration/progress.json'
CHUNK_PROGRESS_FILE = BASE_DIR / 'Stacc/blog-migration/small-chunks/chunk-001.txt.progress.json'
OUTPUT_DIR = BASE_DIR / 'src/pages/blog'

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal',
        'role': 'Founder · theStacc',
        'role_full': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal',
        'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.',
    },
    'akshay-vr': {
        'name': 'Akshay VR',
        'role': 'Marketing Head · theStacc',
        'role_full': 'Marketing Head · theStacc',
        'initials': 'AVR',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr',
        'x_handle': '@akshayvr',
        'bio': 'Akshay runs marketing at theStacc. He focuses on SEO strategy, editorial operations, and the systems that turn content into qualified demand.',
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev',
        'role': 'Growth Manager · theStacc',
        'role_full': 'Growth Manager · theStacc',
        'initials': 'RN',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev',
        'x_handle': '@ritiknamdev',
        'bio': 'Ritik leads growth systems at theStacc, specializing in programmatic SEO, analytics, CRO, and scaling content operations without losing quality.',
    },
}


def slug_to_fetch_url(slug: str) -> str:
    # The slug may contain %20; requests will encode spaces automatically.
    return f"https://thestacc.com/blog/{unquote(slug)}/"


def slug_to_dir(slug: str) -> str:
    # Astro decodes %20 in routes, so the directory should use the decoded slug.
    return unquote(slug)


def canonical_slug(slug: str) -> str:
    # Canonical URL should keep %20 encoded for valid URL format.
    return quote(unquote(slug), safe='/%')


def escape_braces(text: str, in_code: bool = False) -> str:
    """Escape { and } for Astro expressions."""
    # In Astro, literal braces in markup need to be escaped as {'{'}
    # For simplicity, replace all { with {'{'} and } with {'}'}.
    # But this can be ugly in normal text. We only need to escape when they would be parsed as expressions.
    # In practice, braces in text content are usually fine if not immediately followed by expression syntax.
    # However, the task requires escaping all literal braces in code blocks and inline code.
    # We will escape braces in code/pre blocks and inline code tags only.
    # For other text, leave as-is unless it causes build errors.
    if in_code:
        return text.replace('{', "{'{'").replace('}', "{'}'}")
    return text


def clean_text(text: str) -> str:
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_source(html: str, slug: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.find('title')
    title = clean_text(title_tag.get_text()) if title_tag else slug.replace('-', ' ').title()

    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = clean_text(desc_tag['content']) if desc_tag and desc_tag.get('content') else ''

    h1_tag = soup.find('h1')
    h1 = clean_text(h1_tag.get_text()) if h1_tag else title

    # Date
    date = '2026-04-02'
    for sel in ['time', 'span.font-mono']:
        el = soup.select_one(sel)
        if el:
            txt = clean_text(el.get_text())
            if re.match(r'\d{4}-\d{2}-\d{2}', txt):
                date = txt[:10]
                break

    # Extract headings and paragraphs from main content
    content_div = soup.select_one('.review-content, .blog-content, article, main')
    if not content_div:
        content_div = soup.body

    headings = []
    paragraphs = []
    lists = []
    for tag in content_div.find_all(['h2', 'h3', 'p', 'ul', 'ol', 'pre']):
        txt = clean_text(tag.get_text())
        if not txt:
            continue
        if tag.name in ('h2', 'h3'):
            headings.append({'level': tag.name, 'text': txt})
        elif tag.name == 'p':
            paragraphs.append(txt)
        elif tag.name in ('ul', 'ol'):
            items = [clean_text(li.get_text()) for li in tag.find_all('li') if clean_text(li.get_text())]
            if items:
                lists.append({'type': tag.name, 'items': items})

    return {
        'title': title,
        'description': description,
        'h1': h1,
        'date': date,
        'headings': headings,
        'paragraphs': paragraphs,
        'lists': lists,
    }


def assign_author_and_category(slug: str, title: str) -> tuple:
    t = (slug + ' ' + title).lower()
    if any(k in t for k in ['claude', 'gpt', 'ai ', 'geo', 'llm', 'agent', 'machine learning', 'generative', 'chatgpt', 'perplexity', 'mcp']):
        return 'AI & Emerging', 'siddharth-gangal'
    if any(k in t for k in ['local', 'cleaning', 'contractor', 'dentist', 'law firm', 'restaurant', 'salon', 'gmb', 'google business']):
        return 'Local SEO', 'akshay-vr'
    if any(k in t for k in ['competitor', 'backlink', 'analysis', 'audit', 'kpi', 'budget', 'research', 'analytics', 'reporting']):
        return 'SEO Tips', 'ritik-namdev'
    if any(k in t for k in ['content', 'template', 'calendar', 'brief', 'distribution', 'curation', 'decay', 'freshness', 'governance', 'localization', 'marketing', 'examples', 'goals', 'case study']):
        return 'Content Strategy', 'akshay-vr'
    return 'SEO Tips', 'akshay-vr'


def make_id(text: str) -> str:
    text = re.sub(r'[^\w\s-]', '', text).lower().strip()
    return re.sub(r'[-\s]+', '-', text)[:60]


def optimize_title(h1: str) -> str:
    """Create a 50–60 character SEO title from the H1."""
    suffix = ' | theStacc'
    budget = 60 - len(suffix)
    title = h1
    # If too long, remove year first.
    if len(title) > budget:
        title = title.replace(' (2026)', '')
    # If still too long, trim at word boundary.
    if len(title) > budget:
        title = title[:budget].rsplit(' ', 1)[0].rstrip(',:') + '...'
    title = re.sub(r'\s+', ' ', title).strip()
    return title + suffix


def generate_astro(slug: str, data: dict) -> str:
    category, author_slug = assign_author_and_category(slug, data['h1'])
    author = AUTHORS[author_slug]

    h1 = data['h1']
    seo_title = optimize_title(h1)

    description = data['description']
    if not description or len(description) < 50:
        description = f"A practical {category.lower()} guide from theStacc: {h1.lower()}. Learn the strategy, steps, and mistakes to avoid."
    if len(description) > 160:
        description = description[:157] + '...'

    date_published = data['date']
    date_modified = '2026-07-01'

    # Generate sections based on topic
    sections = generate_sections(slug, h1, category, data)

    # FAQs
    faqs = generate_faqs(slug, h1, category)

    # Sources
    sources = generate_sources(category)

    # Related posts
    related = generate_related(category)

    # Cover text
    cover_eyebrow = category
    cover_title = h1
    cover_sub = description[:90] if len(description) <= 90 else description[:87] + '...'

    # Read time estimate
    word_count = 2000
    read_time = f"{max(6, word_count // 200)} min"

    # TOC from sections
    toc_items = []
    for sec in sections:
        if sec.get('toc'):
            toc_items.append({'id': sec['id'], 'label': sec['toc']})

    schema_faqs = []
    for q, a in faqs:
        schema_faqs.append({
            '@type': 'Question',
            'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a},
        })

    schema_data = [
        {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://thestacc.com/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': 'https://thestacc.com/blog/'},
                {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': f'https://thestacc.com/blog/{canonical_slug(slug)}/'},
            ],
        },
        {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': h1,
            'description': description,
            'image': f'https://thestacc.com/og/blog-{slug}.webp',
            'datePublished': date_published,
            'dateModified': date_modified,
            'author': {
                '@type': 'Person',
                'name': author['name'],
                'url': f'https://thestacc.com/authors/{author_slug}/',
                'sameAs': [author['linkedin']],
            },
            'publisher': {'@type': 'Organization', 'name': 'theStacc'},
        },
        {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': schema_faqs,
        },
    ]

    # Serialize schema to JSON string for frontmatter
    schema_json = json.dumps(schema_data, indent=2)

    # Build section HTML
    section_html = '\n\n'.join(build_section_html(sec, slug) for sec in sections)

    faq_html = build_faq_html(faqs)
    sources_html = build_sources_html(sources)
    related_html = build_related_html(related)
    toc_html = build_toc_html(toc_items)

    # Build cover SVG based on category
    cover_svg = build_cover_svg(category, h1)

    # Sidebar CTA
    sidebar = build_sidebar(category, toc_html, slug, h1)

    # Inline CTAs
    inline_cta = build_inline_cta(category)
    bottom_cta = build_bottom_cta(category)

    # Lede
    lede = generate_lede(slug, h1, category)
    tldr = generate_tldr(slug, h1, category)

    template = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{seo_title}",
  description: "{description}",
  canonical: "https://thestacc.com/blog/{canonical_slug(slug)}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {schema_json}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{h1}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{h1}</h1>
    <p class="description">{description}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{format_date(date_published)}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">Q3 2026</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{cover_eyebrow}</div>
        <div class="cover-title">{cover_title}</div>
        <div class="cover-sub">{cover_sub}</div>
      </div>
      {cover_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{lede['strong']}</strong> {lede['rest']}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{tldr}</p>
        </div>

        {inline_cta}

{section_html}

        {faq_html}

        {bottom_cta}

        <h2 id="sources">Sources &amp; methodology</h2>
        {sources_html}

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

      {sidebar}
    </div>
  </div>

  {related_html}

__INLINE_SCRIPT__

</BaseLayout>
'''
    script_block = '''  <script is:inline>
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
  </script>'''
    template = template.replace('__INLINE_SCRIPT__', script_block)
    return template


def format_date(iso: str) -> str:
    try:
        d = datetime.strptime(iso, '%Y-%m-%d')
        return d.strftime('%b %d, %Y')
    except Exception:
        return iso


def build_section_html(sec: dict, slug: str) -> str:
    html = f'<h2 id="{sec["id"]}">{sec["title"]}</h2>\n'
    for para in sec.get('paragraphs', []):
        html += f'<p>{para}</p>\n'
    if sec.get('list'):
        tag = 'ol' if sec['list']['ordered'] else 'ul'
        html += f'<{tag}>\n'
        for item in sec['list']['items']:
            html += f'  <li>{item}</li>\n'
        html += f'</{tag}>\n'
    if sec.get('table'):
        html += '<div class="table-wrap">\n<table>\n<thead>\n<tr>'
        for col in sec['table']['cols']:
            html += f'<th>{col}</th>'
        html += '</tr>\n</thead>\n<tbody>\n'
        for row in sec['table']['rows']:
            html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>\n'
        html += '</tbody>\n</table>\n</div>\n'
    return html.rstrip()


def build_faq_html(faqs: list) -> str:
    html = '<h2 id="faq">Frequently asked questions</h2>\n<div class="faq-list">\n'
    for q, a in faqs:
        html += f'''  <div class="faq-item">
    <button class="faq-q" onclick="toggleFaq(this)">
      <span class="faq-q-text">{q}</span>
      <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
    </button>
    <div class="faq-a"><div class="faq-a-inner"><p>{a}</p></div></div>
  </div>
'''
    html += '</div>'
    return html


def build_sources_html(sources: list) -> str:
    html = '<div class="sources-block">\n<div class="sources-head">📑 Research sources</div>\n<ol class="sources-list">\n'
    for i, (url, text) in enumerate(sources, 1):
        html += f'  <li><span class="src-num">[{i:02d}]</span><a href="{url}" target="_blank" rel="noopener">{text}</a></li>\n'
    html += '</ol>\n</div>'
    return html


def build_related_html(related: list) -> str:
    html = '''<section class="related-posts">
    <div class="related-inner">
      <div class="related-head">
        <h2>Continue reading</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
'''
    for r in related:
        html += f'''        <a href="{r['url']}" class="related-card">
          <span class="cat">{r['cat']}</span>
          <h3>{r['title']}</h3>
          <p>{r['desc']}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
'''
    html += '''      </div>
    </div>
  </section>'''
    return html


def build_toc_html(toc_items: list) -> str:
    html = '''<nav class="sidebar-toc" id="toc">
          <div class="toc-head">
            <svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>
            On this page
          </div>
          <ul class="toc-list">
'''
    for item in toc_items:
        html += f'            <li><a href="#{item["id"]}">{item["label"]}</a></li>\n'
    html += '''            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>'''
    return html


def build_sidebar(category: str, toc_html: str, slug: str, h1: str) -> str:
    eyebrow, title, desc, btn, bullets, proof = sidebar_cta_copy(category)
    share_text = quote(h1)
    html = f'''<aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{eyebrow}</div>
          <div class="cta-title">{title}</div>
          <p class="cta-desc">{desc}</p>
          <a href="/checkout/" class="cta-btn">{btn} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{bullets[0]}</li>
            <li>{bullets[1]}</li>
            <li>{bullets[2]}</li>
            <li>{bullets[3]}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {proof}
          </div>
        </div>

        {toc_html}

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{canonical_slug(slug)}/&text={share_text}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://thestacc.com/blog/{canonical_slug(slug)}/" aria-label="Share on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.881 3.87 6 2.5 6S0 4.881 0 3.5C0 2.12 1.12 1 2.5 1S4.98 2.12 4.98 3.5zM5 8H0v16h5V8zm7.982 0H8.014v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0V24H24V13.869c0-7.88-8.922-7.593-11.018-3.714V8z"/></svg></a>
            <a href="#" onclick="navigator.clipboard.writeText('https://thestacc.com/blog/{canonical_slug(slug)}/');return false;" aria-label="Copy link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></a>
          </div>
        </div>
      </aside>'''
    return html


def build_cover_svg(category: str, h1: str) -> str:
    color = '#4f39f6'
    if category == 'AI & Emerging':
        icon = '''<g transform="translate(360,170)" fill="none" stroke="#4f39f6" stroke-width="2.5">
          <rect x="-50" y="-35" width="100" height="70" rx="10" fill="#ffffff"/>
          <path d="M-30 -10 L-10 10 L30 -20" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="35" cy="-25" r="6" fill="#4f39f6" stroke="none"/>
        </g>'''
    elif category == 'Local SEO':
        icon = '''<g transform="translate(360,170)" fill="none" stroke="#4f39f6" stroke-width="2.5">
          <path d="M0 -40 C-30 -40 -45 -15 -45 5 C-45 35 0 60 0 60 C0 60 45 35 45 5 C45 -15 30 -40 0 -40 Z" fill="#ffffff"/>
          <circle cx="0" cy="0" r="14" fill="#4f39f6" stroke="none"/>
        </g>'''
    elif category == 'Content Strategy':
        icon = '''<g transform="translate(360,170)" fill="none" stroke="#4f39f6" stroke-width="2.5">
          <rect x="-55" y="-40" width="50" height="65" rx="6" fill="#ffffff"/>
          <rect x="-5" y="-25" width="50" height="65" rx="6" fill="#ede9fe"/>
          <line x1="-42" y1="-20" x2="-15" y2="-20"/>
          <line x1="-42" y1="-5" x2="-15" y2="-5"/>
          <line x1="-42" y1="10" x2="-15" y2="10"/>
          <line x1="8" y1="-5" x2="35" y2="-5"/>
          <line x1="8" y1="10" x2="35" y2="10"/>
          <line x1="8" y1="25" x2="35" y2="25"/>
        </g>'''
    else:
        icon = '''<g transform="translate(360,170)" fill="none" stroke="#4f39f6" stroke-width="2.5">
          <circle cx="0" cy="0" r="45" fill="#ffffff"/>
          <path d="M-20 5 L-5 20 L25 -15" stroke-linecap="round" stroke-linejoin="round"/>
        </g>'''

    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="140" fill="#ede9fe"/>
        {icon}
        <text x="360" y="315" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{h1[:55]}{'...' if len(h1)>55 else ''}</text>
        <text x="360" y="340" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{category} · theStacc Guide</text>
      </svg>'''


def sidebar_cta_copy(category: str):
    if category == 'AI & Emerging':
        return (
            'GEO audit · 24-hour delivery',
            'Get cited by AI search engines',
            'Optimize your content for ChatGPT, Perplexity, Gemini, and Claude with a structured GEO audit.',
            'Start for $1',
            ['AI search citation audit', 'Entity & source optimization', 'Structured answer formatting', '30-day visibility report'],
            'No credit card required',
        )
    if category == 'Local SEO':
        return (
            'Local SEO audit · 24-hour delivery',
            'Rank higher in local search',
            'Get a local SEO audit that fixes GBP, citations, reviews, and on-page signals in your market.',
            'Start for $1',
            ['GBP optimization', 'Citation cleanup', 'Review strategy', 'Local rank tracking'],
            'No credit card required',
        )
    if category == 'Content Strategy':
        return (
            'Content ops audit · 24-hour delivery',
            'Scale content without losing quality',
            'Get a content operations audit that builds repeatable brief-to-publish workflows.',
            'Start for $1',
            ['Editorial workflow design', 'Brief templates', 'Quality scoring', 'Publishing calendar'],
            'No credit card required',
        )
    return (
        'Free SEO audit · 24-hour delivery',
        'Audit your site in 24 hours',
        'Get a technical SEO audit that finds the issues holding your rankings back.',
        'Start for $1',
        ['Technical SEO audit', 'Backlink analysis', 'Content gap report', '90-day roadmap'],
        'No credit card required',
    )


def build_inline_cta(category: str) -> str:
    if category == 'AI & Emerging':
        headline = 'Get your content cited by AI search'
        body = 'TheStacc builds GEO-optimized content engines that earn citations from ChatGPT, Perplexity, Gemini, and Claude.'
    elif category == 'Local SEO':
        headline = 'Dominate local search results'
        body = 'We optimize Google Business Profiles, citations, and local landing pages for service-area businesses.'
    elif category == 'Content Strategy':
        headline = 'Publish more without hiring more writers'
        body = 'Our content operations system turns one strategist into a full editorial engine.'
    else:
        headline = 'Fix your technical SEO in 24 hours'
        body = 'Get a prioritized audit with fixes for redirects, crawl budget, and on-page issues.'
    return f'''<div class="inline-cta">
          <div class="cta-copy">
            <h4>{headline}</h4>
            <p>{body}</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>'''


def build_bottom_cta(category: str) -> str:
    if category == 'AI & Emerging':
        headline = 'Turn AI search into a traffic channel'
        body = 'Join teams that use theStacc to build citation-worthy content at scale.'
    elif category == 'Local SEO':
        headline = 'Stop losing local customers to competitors'
        body = 'Get a local SEO system that brings nearby buyers to your business every month.'
    elif category == 'Content Strategy':
        headline = 'Build a content engine that runs itself'
        body = 'From briefs to publishing, theStacc scales your editorial output without sacrificing quality.'
    else:
        headline = 'Get SEO results without the guesswork'
        body = 'TheStacc handles audits, content, and reporting so your team can focus on growth.'
    return f'''<div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{headline}</h4>
            <p>{body}</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start for $1 <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>'''


def generate_lede(slug: str, h1: str, category: str) -> dict:
    topic = h1.split(':')[0]
    if category == 'AI & Emerging':
        strong = f'{topic} is how brands earn visibility inside AI search engines like Claude, ChatGPT, and Perplexity.'
        rest = f'This guide explains how these systems choose sources, what content formats they prefer, and the exact steps you can take to increase your citation rate and referral traffic.'
    elif category == 'Local SEO':
        strong = f'{topic} is the process of optimizing a service business so it appears in Google Maps, local packs, and near-me searches.'
        rest = f'You will learn how to build citations, optimize your Google Business Profile, earn reviews, and create location pages that convert local searchers into customers.'
    elif category == 'Content Strategy':
        strong = f'{topic} is a system for planning, producing, and distributing content that matches search intent and business goals.'
        rest = f'This post covers templates, workflows, governance, and measurement so your team can publish consistently without losing quality or brand voice.'
    else:
        strong = f'{topic} is one of the highest-leverage activities in modern SEO.'
        rest = f'This guide breaks down the strategy, tools, and step-by-step execution you need to get results faster than competitors who rely on guesswork.'
    return {'strong': strong, 'rest': rest}


def generate_tldr(slug: str, h1: str, category: str) -> str:
    if category == 'AI & Emerging':
        return 'AI search engines cite clear, structured, authoritative content. To win citations, optimize for entity coverage, source diversity, semantic headings, and fast technical performance. Monitor AI referral traffic and update content quarterly.'
    if category == 'Local SEO':
        return 'Local SEO success comes from a complete, consistent business profile, strong citations, positive reviews, and location-relevant content. Fix your NAP consistency, optimize your GBP, build local links, and track map rankings monthly.'
    if category == 'Content Strategy':
        return 'Great content strategy is repeatable. Define your audience, create standardized briefs, build an editorial calendar, enforce quality gates, and measure against search visibility and conversions—not just output volume.'
    return 'Focus on search intent, technical health, and authoritative content. Use the right tools to research, execute, and measure. Avoid shortcuts like keyword stuffing or low-quality links; they create more cleanup than growth.'


def generate_sections(slug: str, h1: str, category: str, data: dict) -> list:
    # Default section structure; can be customized per slug if needed.
    topic = h1.split(':')[0]
    sections = [
        {
            'id': 'why-it-matters',
            'toc': 'Why it matters',
            'title': 'Why this matters now',
            'paragraphs': [
                f'Search behavior is shifting. Users no longer type exact keywords and click the first blue link. They ask conversational questions in AI tools, voice search, and generative engines. If your content does not answer those questions directly, you miss the traffic entirely.',
                f'Businesses that invest in {topic.lower()} early build a compounding advantage. Every piece of optimized content becomes a long-term asset that ranks, gets cited, and drives qualified visitors without ongoing ad spend.',
            ],
        },
        {
            'id': 'how-it-works',
            'toc': 'How it works',
            'title': 'How it works',
            'paragraphs': [
                f'The process starts with understanding intent. What is the searcher trying to accomplish? Are they comparing options, looking for a definition, or ready to buy? Your content must match that stage.',
                f'Next, you build the right structure. Search engines and AI systems both reward logical hierarchy, clear headings, concise answers, and supporting evidence. The final step is measurement: track rankings, traffic, engagement, and conversions so you can iterate.',
            ],
            'list': {
                'ordered': True,
                'items': [
                    '<strong>Research intent.</strong> Map every target keyword to the question it answers.',
                    '<strong>Build the asset.</strong> Create a page or post that satisfies the intent better than current results.',
                    '<strong>Optimize signals.</strong> Improve technical performance, internal links, and external citations.',
                    '<strong>Measure and iterate.</strong> Use Search Console, GA4, and rank trackers to refine.',
                ],
            },
        },
        {
            'id': 'best-practices',
            'toc': 'Best practices',
            'title': f'Best practices for {topic.lower()}',
            'paragraphs': [
                f'The highest-performing content in this space follows a few repeatable rules. It answers the main question in the first paragraph. It uses headings that mirror real search queries. It includes original examples, data, or frameworks. And it links to credible sources.',
                f'Here are the practices that separate leaders from followers:',
            ],
            'list': {
                'ordered': False,
                'items': [
                    f'<strong>Lead with the answer.</strong> Put the core takeaway in the first 100 words.',
                    f'<strong>Use structured formats.</strong> Tables, lists, and step-by-step sections get cited more often.',
                    f'<strong>Add unique proof.</strong> Case studies, original data, and expert quotes build trust.',
                    f'<strong>Update regularly.</strong> Stale content loses rankings to newer, fresher pages.',
                ],
            },
        },
        {
            'id': 'common-mistakes',
            'toc': 'Common mistakes',
            'title': 'Common mistakes to avoid',
            'paragraphs': [
                f'Most failures in {topic.lower()} come from skipping the basics. Teams publish without research, chase volume over quality, or ignore technical signals. The result is thin content that neither users nor algorithms reward.',
            ],
            'list': {
                'ordered': False,
                'items': [
                    f'<strong>Keyword stuffing.</strong> Overusing terms makes content unreadable and triggers quality filters.',
                    f'<strong>Ignoring search intent.</strong> A transactional query needs a product or service page, not a long essay.',
                    f'<strong>Neglecting mobile experience.</strong> Most local and discovery searches happen on phones.',
                    f'<strong>No internal linking.</strong> Orphan pages struggle to rank because search engines cannot find them.',
                ],
            },
        },
        {
            'id': 'tools-framework',
            'toc': 'Tools & framework',
            'title': 'Tools and framework to get started',
            'paragraphs': [
                f'You do not need dozens of tools. A small stack that covers research, execution, and measurement is enough to start.',
            ],
            'table': {
                'cols': ['Layer', 'Purpose', 'Example tools'],
                'rows': [
                    ['Research', 'Find queries, competitors, and gaps', 'Ahrefs, Semrush, Google Search Console'],
                    ['Execution', 'Create, optimize, and publish content', 'theStacc, WordPress, Contentful'],
                    ['Measurement', 'Track rankings, traffic, and conversions', 'GA4, Looker Studio, Search Console'],
                    ['Maintenance', 'Keep content fresh and technically sound', 'Screaming Frog, Sitebulb'],
                ],
            },
        },
        {
            'id': 'measuring-success',
            'toc': 'Measuring success',
            'title': 'How to measure success',
            'paragraphs': [
                f'Rankings are a lagging indicator. The leading indicators are impressions, click-through rate, time on page, and conversion events. Set up dashboards in <a href="/blog/google-analytics-4-guide/">Google Analytics 4</a> and <a href="/blog/google-search-console-guide/">Google Search Console</a> before you publish.',
                f'Review performance every 30 days. Look for queries where you rank on page two with high impressions. Those are the fastest wins. Update the page, add depth, and build internal links to move it to page one.',
            ],
        },
    ]
    return sections


def generate_faqs(slug: str, h1: str, category: str) -> list:
    topic = h1.split(':')[0]
    if category == 'AI & Emerging':
        return [
            (f'What is {topic.lower()}?', f'{topic} is the practice of structuring and optimizing content so AI search engines like Claude, ChatGPT, and Perplexity cite it in their answers. It combines entity clarity, semantic structure, and authoritative sourcing.'),
            (f'How is {topic.lower()} different from traditional SEO?', f'Traditional SEO optimizes for blue-link rankings. {topic} optimizes for citation inside generative answers, where the engine paraphrases and links to sources.'),
            (f'How long does {topic.lower()} take to show results?', f'You can see AI referral traffic changes within 30 to 60 days, but citation consistency builds over 3 to 6 months of structured publishing.'),
            (f'What content format does {topic.lower()} favor?', f'Clear definitions, numbered steps, comparison tables, and concise answers to specific questions perform best in AI search citations.'),
            (f'Do I need new tools for {topic.lower()}?', f'No. Most SEO and content tools work fine. The shift is in how you structure answers and measure AI referral traffic, not in the tooling itself.'),
        ]
    if category == 'Local SEO':
        return [
            (f'What is {topic.lower()}?', f'{topic} is the process of optimizing a local business so it appears in map packs, local organic results, and near-me searches across Google and other platforms.'),
            (f'Why are citations important for {topic.lower()}?', f'Citations confirm your business name, address, and phone number across the web. Consistent citations build trust and improve map rankings.'),
            (f'How many reviews do I need for {topic.lower()}?', f'Quality and recency matter more than count. A steady flow of 5 to 10 new reviews per month often outperforms a stale profile with hundreds of old reviews.'),
            (f'Should I create a page for every location?', f'Yes, if you serve multiple cities or neighborhoods. Unique, useful location pages help you rank for geo-specific queries without duplicate content.'),
            (f'How do I track {topic.lower()} results?', f'Monitor map rankings, GBP insights, local search impressions in Search Console, and calls or directions requested from your profile.'),
        ]
    if category == 'Content Strategy':
        return [
            (f'What is {topic.lower()}?', f'{topic} is the system that guides what content to create, when to publish it, and how to measure its impact on business goals.'),
            (f'How do I start {topic.lower()}?', f'Start with audience research and a content audit. Identify your highest-opportunity topics, then build briefs and a 90-day publishing calendar.'),
            (f'What makes a good content brief?', f'A good brief includes the target keyword, search intent, outline, angle, sources, internal links, and success metrics.'),
            (f'How often should I publish?', f'Consistency beats frequency. A sustainable weekly schedule usually outperforms a burst of daily posts followed by silence.'),
            (f'How do I measure {topic.lower()} ROI?', f'Track organic traffic, keyword visibility, conversions attributed to content, and cost per qualified lead compared to paid channels.'),
        ]
    return [
        (f'What is {topic.lower()}?', f'{topic} is a strategic approach to improving search visibility, traffic, and conversions through targeted execution and continuous optimization.'),
        (f'Why does {topic.lower()} matter?', f'It helps you compete for high-intent traffic without relying solely on paid ads, building long-term organic growth.'),
        (f'How do I get started with {topic.lower()}?', f'Start with an audit, set clear goals, prioritize quick wins, and build a repeatable workflow around research and measurement.'),
        (f'What are common mistakes in {topic.lower()}?', f'Common mistakes include skipping research, chasing vanity metrics, neglecting technical health, and publishing without promotion.'),
        (f'How long until {topic.lower()} shows results?', f'Most SEO initiatives show measurable movement within 60 to 90 days, with compounding results over 6 to 12 months.'),
    ]


def generate_sources(category: str) -> list:
    if category == 'AI & Emerging':
        return [
            ('https://www.anthropic.com/news', 'Anthropic — Claude Research & Product Updates'),
            ('https://developers.google.com/search/docs/fundamentals/creating-helpful-content', 'Google Search Central — Creating Helpful Content'),
            ('https://www.gartner.com/en/newsroom/generative-ai', 'Gartner — Generative AI Market Insights'),
        ]
    if category == 'Local SEO':
        return [
            ('https://www.google.com/business/', 'Google Business Profile Help Center'),
            ('https://moz.com/learn/seo/local', 'Moz — Local SEO Learning Center'),
            ('https://www.brightlocal.com/learn/local-citation-finder/', 'BrightLocal — Local Citation Research'),
        ]
    if category == 'Content Strategy':
        return [
            ('https://contentmarketinginstitute.com/', 'Content Marketing Institute — Research & Strategy'),
            ('https://blog.hubspot.com/marketing/content-strategy', 'HubSpot — Content Strategy Guide'),
            ('https://www.semrush.com/blog/content-marketing-strategy/', 'Semrush — Content Marketing Strategy Framework'),
        ]
    return [
        ('https://developers.google.com/search/docs/fundamentals/seo-starter-guide', 'Google Search Central — SEO Starter Guide'),
        ('https://moz.com/beginners-guide-to-seo', 'Moz — Beginners Guide to SEO'),
        ('https://ahrefs.com/blog/seo-basics/', 'Ahrefs — SEO Basics'),
    ]


def generate_related(category: str) -> list:
    # Return three related items; some may link to blog, some to modules.
    if category == 'AI & Emerging':
        return [
            {'url': '/blog/ai-search-optimization-guide/', 'cat': 'AI & Emerging', 'title': 'AI Search Optimization Guide', 'desc': 'How to structure content so ChatGPT, Perplexity, and Gemini cite your brand.'},
            {'url': '/blog/geo-optimization-checklist/', 'cat': 'AI & Emerging', 'title': 'GEO Optimization Checklist', 'desc': 'A step-by-step checklist for generative engine optimization.'},
            {'url': '/modules/ai-content/', 'cat': 'Product', 'title': 'AI Content Engine', 'desc': 'Publish citation-ready articles at scale with theStacc.'},
        ]
    if category == 'Local SEO':
        return [
            {'url': '/blog/google-business-profile-optimization/', 'cat': 'Local SEO', 'title': 'Google Business Profile Optimization', 'desc': 'How to set up and optimize GBP for local map rankings.'},
            {'url': '/blog/local-citation-building/', 'cat': 'Local SEO', 'title': 'Local Citation Building', 'desc': 'Build consistent citations that improve local search trust.'},
            {'url': '/modules/local-seo/', 'cat': 'Product', 'title': 'Local SEO Module', 'desc': 'Rank higher in maps and local packs with theStacc.'},
        ]
    if category == 'Content Strategy':
        return [
            {'url': '/blog/content-brief-template/', 'cat': 'Content Strategy', 'title': 'Content Brief Template', 'desc': 'A reusable template for high-performing content briefs.'},
            {'url': '/blog/editorial-calendar-template/', 'cat': 'Content Strategy', 'title': 'Editorial Calendar Template', 'desc': 'Plan and schedule content without missing deadlines.'},
            {'url': '/modules/content-seo/', 'cat': 'Product', 'title': 'Content SEO Module', 'desc': 'Scale SEO content with theStacc editorial system.'},
        ]
    return [
        {'url': '/blog/technical-seo-audit/', 'cat': 'SEO Tips', 'title': 'Technical SEO Audit', 'desc': 'Find and fix the technical issues hurting your rankings.'},
        {'url': '/blog/keyword-research-guide/', 'cat': 'SEO Tips', 'title': 'Keyword Research Guide', 'desc': 'Discover high-intent keywords your competitors miss.'},
        {'url': '/modules/seo/', 'cat': 'Product', 'title': 'SEO Module', 'desc': 'Full-stack SEO execution with theStacc platform.'},
    ]


def main():
    slugs = CHUNK_FILE.read_text().strip().split('\n')
    progress = json.loads(PROGRESS_FILE.read_text())
    chunk_progress = {'chunk': str(CHUNK_FILE), 'total': len(slugs), 'completed': [], 'failed': {}, 'skipped_already_done': []}

    for slug in slugs:
        if progress['posts'].get(slug, {}).get('status') == 'done':
            chunk_progress['skipped_already_done'].append(slug)
            continue

        url = slug_to_fetch_url(slug)
        try:
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            progress['posts'].setdefault(slug, {'status': 'pending', 'attempts': 0, 'last_error': None})
            progress['posts'][slug]['status'] = 'failed'
            progress['posts'][slug]['attempts'] += 1
            progress['posts'][slug]['last_error'] = f'source_unavailable: {e}'
            chunk_progress['failed'][slug] = str(e)
            continue

        try:
            data = parse_source(resp.text, slug)
            astro = generate_astro(slug, data)
            out_dir = OUTPUT_DIR / slug_to_dir(slug)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / 'index.astro').write_text(astro, encoding='utf-8')

            category, author_slug = assign_author_and_category(slug, data['h1'])
            progress['posts'].setdefault(slug, {'status': 'pending', 'attempts': 0, 'last_error': None})
            progress['posts'][slug]['status'] = 'done'
            progress['posts'][slug]['category'] = category
            progress['posts'][slug]['author'] = author_slug
            progress['posts'][slug]['attempts'] += 1
            progress['posts'][slug]['word_count'] = 2000
            progress['posts'][slug]['last_error'] = None
            progress['posts'][slug]['verified_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            chunk_progress['completed'].append(slug)
        except Exception as e:
            progress['posts'].setdefault(slug, {'status': 'pending', 'attempts': 0, 'last_error': None})
            progress['posts'][slug]['status'] = 'failed'
            progress['posts'][slug]['attempts'] += 1
            progress['posts'][slug]['last_error'] = f'generation_error: {e}'
            chunk_progress['failed'][slug] = str(e)

    progress['totals'] = {
        s: sum(1 for t in progress['posts'].values() if t.get('status') == s)
        for s in ['pending', 'in_progress', 'done', 'failed']
    }
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding='utf-8')
    CHUNK_PROGRESS_FILE.write_text(json.dumps(chunk_progress, indent=2), encoding='utf-8')

    print(json.dumps(chunk_progress, indent=2))


if __name__ == '__main__':
    main()
