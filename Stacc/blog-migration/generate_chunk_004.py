#!/usr/bin/env python3
"""Generate Astro files for chunk-004 blog migration."""
import json, os, re, html
from datetime import datetime, timezone

ROOT = '/home/ritik/thestacc.com-astro/thestacc-2026-site'
CHUNK_FILE = f'{ROOT}/Stacc/blog-migration/small-chunks/chunk-004.txt'
PROGRESS_FILE = f'{ROOT}/Stacc/blog-migration/progress.json'
CHUNK_PROGRESS_FILE = f'{CHUNK_FILE}.progress.json'
SRC_DIR = '/tmp/blog-src-chunk-004'

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal', 'role': 'Founder · theStacc', 'initials': 'SG',
        'full_role': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.',
        'x': 'https://x.com/sidgangal', 'handle': '@sidgangal',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/'
    },
    'akshay-vr': {
        'name': 'Akshay VR', 'role': 'Marketing Head · theStacc', 'initials': 'AVR',
        'full_role': 'Marketing Head · theStacc',
        'bio': 'Akshay runs marketing and editorial strategy at theStacc. He specializes in B2B SaaS demand generation, SEO-led content operations, and building brand voice that converts.',
        'x': 'https://x.com/akshayvr_', 'handle': '@akshayvr_',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/'
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev', 'role': 'Growth Manager · theStacc', 'initials': 'RN',
        'full_role': 'Growth Manager · theStacc',
        'bio': 'Ritik leads growth systems at theStacc, with a focus on programmatic SEO, analytics, CRO, and funnel operations. He writes about scaling organic traffic through data-driven experiments.',
        'x': 'https://x.com/ritiknamdev_', 'handle': '@ritiknamdev_',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/'
    }
}

def escape_braces(s):
    """Escape literal { and } for Astro output in text/HTML."""
    if s is None: return ''
    s = str(s)
    # Escape braces not already part of Astro expressions
    s = s.replace('{', "{'{'}")
    s = s.replace('}', "{'}'}")
    return s

def clean_text(s):
    if s is None: return ''
    s = re.sub(r'\s+', ' ', str(s)).strip()
    return s

def slugify_id(s):
    s = re.sub(r'[^\w\s-]', '', s.lower())
    return re.sub(r'[-\s]+', '-', s).strip('-')

def render_html(s):
    """Convert plain text to HTML paragraphs, preserving existing tags."""
    if not s: return ''
    if '<' in s and '>' in s:
        return s
    parts = s.split('\n\n')
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(f'<p>{p}</p>')
    return '\n'.join(out)

def make_table(headers, rows):
    head = '<tr>' + ''.join(f'<th>{escape_braces(h)}</th>' for h in headers) + '</tr>'
    body = ''
    for row in rows:
        body += '<tr>' + ''.join(f'<td>{escape_braces(c)}</td>' for c in row) + '</tr>\n'
    return f'<div class="table-wrap"><table><thead>{head}</thead><tbody>{body}</tbody></table></div>'

def make_ol(items):
    return '<ol>\n' + ''.join(f'<li>{escape_braces(item)}</li>\n' for item in items) + '</ol>'

def make_ul(items):
    return '<ul>\n' + ''.join(f'<li>{escape_braces(item)}</li>\n' for item in items) + '</ul>'

def make_faq(faqs):
    items = []
    for q, a in faqs:
        items.append(f'''<div class="faq-item">
            <button class="faq-q" onclick="toggleFaq(this)">
              <span class="faq-q-text">{escape_braces(q)}</span>
              <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
            </button>
            <div class="faq-a"><div class="faq-a-inner"><p>{escape_braces(a)}</p></div></div>
          </div>''')
    return '<div class="faq-list">\n' + '\n'.join(items) + '\n</div>'

def make_schema_faq(faqs):
    entities = []
    for q, a in faqs:
        entities.append(json.dumps({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        }, ensure_ascii=False))
    return ',\n        '.join(entities)

SVG_CACHE = {}

def make_feature_svg(slug, title, category):
    # Return a themed SVG based on slug keywords
    base = '''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="720" height="360" fill="#f5f3ff"/>
      <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
      <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="180" y="120" width="360" height="120" rx="14" fill="#ffffff"/>
        <path d="M230 180h260" stroke-dasharray="6 4"/>
        <circle cx="210" cy="180" r="16" fill="#4f39f6" stroke="none"/>
        <circle cx="510" cy="180" r="16" fill="#615fff" stroke="none"/>
        <text x="360" y="170" text-anchor="middle" font-family="Geist, sans-serif" font-size="18" fill="#111827" font-weight="600">{TITLE}</text>
        <text x="360" y="210" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="#57534e">{SUB}</text>
      </g>
    </svg>'''
    sub = 'Data-driven SEO · Updated for 2026'
    if 'local' in slug or 'gbp' in slug or 'map' in slug:
        sub = 'Local SEO · Google Business Profile · 2026'
    elif 'geo' in slug or 'ai' in slug or 'generative' in slug:
        sub = 'Generative Engine Optimization · AI Search · 2026'
    elif 'traffic' in slug:
        sub = 'Organic Growth · Content Strategy · 2026'
    elif 'inp' in slug:
        sub = 'Core Web Vitals · Performance · 2026'
    elif 'instagram' in slug:
        sub = 'Social Media · Local Marketing · 2026'
    elif 'ads' in slug:
        sub = 'PPC vs SEO · Channel Strategy · 2026'
    elif 'ghost' in slug:
        sub = 'Ghost CMS · Technical SEO · 2026'
    elif 'algorithm' in slug:
        sub = 'Google Updates · Recovery · 2026'
    elif 'snippet' in slug:
        sub = 'SERP Features · Position Zero · 2026'
    return base.replace('{TITLE}', escape_braces(title[:45])).replace('{SUB}', escape_braces(sub))


def generate_post(slug, data):
    author = AUTHORS[data['author']]
    h1 = data['h1']
    title = data.get('title', h1)
    desc = data['description']
    cat = data['category']
    pub = data.get('datePublished', '2026-01-15')
    mod = data.get('dateModified', '2026-07-01')
    pub_display = datetime.strptime(pub, '%Y-%m-%d').strftime('%b %d, %Y')
    read_time = data.get('read_time', '12 min')
    updated_display = data.get('updated_display', 'Q3 2026')
    
    # Build schema
    schema_faq = make_schema_faq(data['faqs'])
    schema_data = json.dumps([
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
            "description": desc,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": pub,
            "dateModified": mod,
            "author": {"@type": "Person", "name": author['name'], "url": f"https://thestacc.com/authors/{data['author']}/", "sameAs": [author['linkedin']]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [json.loads(x) for x in schema_faq.split(',\n        ') if x.strip()]
        }
    ], indent=2, ensure_ascii=False)
    
    # Build body sections
    toc_items = []
    sections_html = []
    for sec in data['sections']:
        sid = sec.get('id') or slugify_id(sec['h2'])
        toc_items.append((sid, sec.get('toc', sec['h2'])))
        h = f'<h2 id="{sid}">{escape_braces(sec["h2"])}</h2>'
        body = ''
        if sec.get('intro'):
            body += render_html(escape_braces(sec['intro']))
        if sec.get('table'):
            body += make_table(sec['table']['headers'], sec['table']['rows'])
        if sec.get('ol'):
            body += make_ol(sec['ol'])
        if sec.get('ul'):
            body += make_ul(sec['ul'])
        if sec.get('extra'):
            body += render_html(escape_braces(sec['extra']))
        if sec.get('h3s'):
            for h3_title, h3_body in sec['h3s']:
                body += f'<h3 id="{slugify_id(h3_title)}">{escape_braces(h3_title)}</h3>'
                body += render_html(escape_braces(h3_body))
        sections_html.append(h + '\n' + body)
    
    # Sidebar TOC
    toc_html = '\n'.join(f'<li><a href="#{sid}">{escape_braces(label)}</a></li>' for sid, label in toc_items)
    toc_html += '\n<li><a href="#common-mistakes">Common mistakes</a></li>\n<li><a href="#faq">FAQ</a></li>\n<li><a href="#sources">Sources</a></li>'
    
    # Common mistakes
    mistakes_html = '<h2 id="common-mistakes">Common mistakes to avoid</h2>\n'
    if data.get('mistakes_intro'):
        mistakes_html += f'<p>{escape_braces(data["mistakes_intro"])}</p>\n'
    mistakes_html += make_ul(data['mistakes'])
    
    # Sources
    sources_html = '<h2 id="sources">Sources &amp; methodology</h2>\n<div class="sources-block">\n<div class="sources-head">📑 Research sources</div>\n<ol class="sources-list">\n'
    for i, (url, text) in enumerate(data['sources'], 1):
        sources_html += f'<li><span class="src-num">[{i:02d}]</span><a href="{escape_braces(url)}" target="_blank" rel="noopener">{escape_braces(text)}</a></li>\n'
    sources_html += '</ol>\n</div>'
    
    # Related posts
    related = data['related']
    
    # Inline CTAs
    inline_cta = f'''<div class="inline-cta">
          <div class="cta-copy">
            <h4>{escape_braces(data['inline_cta']['headline'])}</h4>
            <p>{escape_braces(data['inline_cta']['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{escape_braces(data['inline_cta']['url'])}" class="cta-btn-inline">{escape_braces(data['inline_cta']['button'])} <span>→</span></a>
            <span class="cta-meta">{escape_braces(data['inline_cta']['meta'])}</span>
          </div>
        </div>'''
    
    bottom_cta = f'''<div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{escape_braces(data['bottom_cta']['headline'])}</h4>
            <p>{escape_braces(data['bottom_cta']['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{escape_braces(data['bottom_cta']['url'])}" class="cta-btn-inline">{escape_braces(data['bottom_cta']['button'])} <span>→</span></a>
            <span class="cta-meta">{escape_braces(data['bottom_cta']['meta'])}</span>
          </div>
        </div>'''
    
    feature_svg = make_feature_svg(slug, title, cat)
    
    astro = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{escape_braces(title)} | theStacc",
  description: "{escape_braces(desc)}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {schema_data}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{escape_braces(h1)}</span>
    </div>
    <span class="post-cat">{escape_braces(cat)}</span>
    <h1>{escape_braces(h1)}</h1>
    <p class="description">{escape_braces(desc)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{data['author']}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{pub_display}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{updated_display}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{escape_braces(cat)}</div>
        <div class="cover-title">{escape_braces(title)}</div>
        <div class="cover-sub">{escape_braces(data['cover_sub'])}</div>
      </div>
      {feature_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{escape_braces(data['lede_strong'])}</strong> {escape_braces(data['lede_rest'])}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{escape_braces(data['tldr'])}</p>
        </div>

        {inline_cta}

        {'\n'.join(sections_html)}

        {mistakes_html}

        <h2 id="faq">Frequently asked questions</h2>
        {make_faq(data['faqs'])}

        {bottom_cta}

        {sources_html}

        <div class="author-block">
          <div class="author-avatar-lg">{author['initials']}</div>
          <div class="author-info">
            <h4><a href="/authors/{data['author']}/">{author['name']}</a></h4>
            <div class="role">{author['full_role']}</div>
            <p>{author['bio']}</p>
            <div class="author-links-row">
              <a href="{author['x']}">{author['handle']}</a>
              <a href="{author['linkedin']}">LinkedIn</a>
              <a href="/about/">About theStacc</a>
            </div>
          </div>
        </div>

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{escape_braces(data['sidebar']['eyebrow'])}</div>
          <div class="cta-title">{escape_braces(data['sidebar']['title'])}</div>
          <p class="cta-desc">{escape_braces(data['sidebar']['desc'])}</p>
          <a href="{escape_braces(data['sidebar']['url'])}" class="cta-btn">{escape_braces(data['sidebar']['button'])} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{escape_braces(data['sidebar']['bullets'][0])}</li>
            <li>{escape_braces(data['sidebar']['bullets'][1])}</li>
            <li>{escape_braces(data['sidebar']['bullets'][2])}</li>
            <li>{escape_braces(data['sidebar']['bullets'][3])}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {escape_braces(data['sidebar']['social'])}
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
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={escape_braces(title)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>{escape_braces(data['related_headline'])}</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        <a href="/blog/{related[0]['slug']}/" class="related-card">
          <span class="cat">{escape_braces(related[0]['cat'])}</span>
          <h3>{escape_braces(related[0]['title'])}</h3>
          <p>{escape_braces(related[0]['desc'])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/blog/{related[1]['slug']}/" class="related-card">
          <span class="cat">{escape_braces(related[1]['cat'])}</span>
          <h3>{escape_braces(related[1]['title'])}</h3>
          <p>{escape_braces(related[1]['desc'])}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/{related[2]['url']}/" class="related-card">
          <span class="cat">{escape_braces(related[2]['cat'])}</span>
          <h3>{escape_braces(related[2]['title'])}</h3>
          <p>{escape_braces(related[2]['desc'])}</p>
          <span class="arrow-link">{escape_braces(related[2]['cta'])} →</span>
        </a>
      </div>
    </div>
  </section>

  <script is:inline>
    function toggleFaq(btn) &#123;
      const item = btn.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    &#125;

    const toc = document.getElementById('toc');
    if (toc) &#123;
      const links = toc.querySelectorAll('a[href^="#"]');
      const headings = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver((entries) => &#123;
        entries.forEach(entry => &#123;
          if (entry.isIntersecting) &#123;
            links.forEach(l => l.classList.remove('active'));
            const active = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          &#125;
        &#125;);
      &#125;, &#123; rootMargin: '-96px 0px -70% 0px', threshold: 0 &#125;);
      headings.forEach(h => observer.observe(h));
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
    
    out_dir = f'{ROOT}/src/pages/blog/{slug}'
    os.makedirs(out_dir, exist_ok=True)
    out_path = f'{out_dir}/index.astro'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(astro)
    return out_path
