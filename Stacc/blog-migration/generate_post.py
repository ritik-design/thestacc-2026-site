#!/usr/bin/env python3
"""Generate a theStacc 2026 blog post Astro file from structured inputs."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')

def slugify_id(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s[:60]

def author_for_topic(category, title):
    t = (title + ' ' + category).lower()
    if any(x in t for x in ['ai ', 'geo', 'llm', 'agent', 'chatgpt', 'perplexity', 'generative', 'technical', 'architecture', 'product strategy', 'founder']):
        return 'siddharth-gangal'
    if any(x in t for x in ['growth', 'analytics', 'ga4', 'search console', 'cro', 'ab test', 'funnel', 'programmatic', 'pseo', 'automation', 'experiment', 'kpi', 'metrics', 'velocity', 'budget', 'crawl']):
        return 'ritik-namdev'
    return 'akshay-vr'

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal',
        'role_short': 'Founder · theStacc',
        'role_full': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal',
        'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.',
    },
    'akshay-vr': {
        'name': 'Akshay VR',
        'role_short': 'Marketing Head · theStacc',
        'role_full': 'Marketing Head · theStacc',
        'initials': 'AVR',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr_',
        'x_handle': '@akshayvr_',
        'bio': 'Akshay leads marketing at theStacc. He runs editorial strategy, keyword research, and brand voice for B2B SaaS content programs. He writes about SEO strategy, editorial workflows, and demand generation.',
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev',
        'role_short': 'Growth Manager · theStacc',
        'role_full': 'Growth Manager · theStacc',
        'initials': 'RN',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev_',
        'x_handle': '@ritiknamdev_',
        'bio': 'Ritik manages growth systems at theStacc. He specializes in programmatic SEO, analytics, CRO, and scaling content operations without adding headcount.',
    },
}

def escape_quotes(s):
    return s.replace('"', '\\"')

def generate(slug, title, description, category, h1, hero_desc, published, modified,
             lede, tldr, inline_cta, sections, mistakes, faqs, bottom_cta,
             sources, related, cover_title, cover_sub, cover_eyebrow=None,
             sidebar=None):
    """sections is list of dicts: {id, h2, body, (h3, table, ol, ul)}"""
    author_slug = author_for_topic(category, title)
    a = AUTHORS[author_slug]
    cover_eyebrow = cover_eyebrow or category

    # Build TOC
    toc_items = []
    for sec in sections:
        toc_items.append(f'<li><a href="#{sec["id"]}">{sec.get("toc", sec["h2"])}</a></li>')
    toc_items.append('<li><a href="#common-mistakes">Common mistakes</a></li>')
    toc_items.append('<li><a href="#faq">FAQ</a></li>')
    toc_items.append('<li><a href="#sources">Sources</a></li>')

    # Build content
    content_body = []
    content_body.append(f'<p class="lede-p"><strong>{lede["strong"]}</strong> {lede["rest"]}</p>')
    content_body.append(f'<div class="callout callout-tldr"><div class="callout-label">⚡ TL;DR — The 30-second verdict</div><p>{tldr}</p></div>')
    content_body.append('<div class="inline-cta"><div class="cta-copy"><h4>' + inline_cta['headline'] + '</h4><p>' + inline_cta['body'] + '</p></div><div class="cta-action"><a href="' + inline_cta['url'] + '" class="cta-btn-inline">' + inline_cta['button'] + ' <span>→</span></a><span class="cta-meta">' + inline_cta['meta'] + '</span></div></div>')

    for sec in sections:
        content_body.append(f'<h2 id="{sec["id"]}">{sec["h2"]}</h2>')
        if 'body' in sec:
            for p in sec['body']:
                content_body.append(f'<p>{p}</p>')
        if 'h3s' in sec:
            for h3 in sec['h3s']:
                content_body.append(f'<h3 id="{slugify_id(h3["title"])}">{h3["title"]}</h3>')
                for p in h3.get('body', []):
                    content_body.append(f'<p>{p}</p>')
                if 'ol' in h3:
                    content_body.append('<ol>' + ''.join(f'<li><strong>{item["title"]}</strong> {item["body"]}</li>' for item in h3['ol']) + '</ol>')
                if 'ul' in h3:
                    content_body.append('<ul>' + ''.join(f'<li><strong>{item["title"]}</strong> {item["body"]}</li>' for item in h3['ul']) + '</ul>')
        if 'ol' in sec:
            content_body.append('<ol>' + ''.join(f'<li><strong>{item["title"]}</strong> {item["body"]}</li>' for item in sec['ol']) + '</ol>')
        if 'ul' in sec:
            content_body.append('<ul>' + ''.join(f'<li><strong>{item["title"]}</strong> {item["body"]}</li>' for item in sec['ul']) + '</ul>')
        if 'table' in sec:
            tbl = sec['table']
            rows = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in tbl['cols']) + '</tr></thead>'
            rows += '<tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in tbl['rows']) + '</tbody>'
            content_body.append(f'<div class="table-wrap"><table>{rows}</table></div>')
        if 'pre' in sec:
            content_body.append(f'<pre><code>{sec["pre"]}</code></pre>')

    content_body.append('<h2 id="common-mistakes">Common mistakes to avoid</h2>')
    content_body.append(f'<p>{mistakes["intro"]}</p>')
    content_body.append('<ul>' + ''.join(f'<li><strong>{m["title"]}</strong> {m["fix"]}</li>' for m in mistakes['items']) + '</ul>')

    content_body.append('<h2 id="faq">Frequently asked questions</h2>')
    content_body.append('<div class="faq-list">')
    for fq in faqs:
        content_body.append(f'<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)"><span class="faq-q-text">{fq["q"]}</span><span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span></button><div class="faq-a"><div class="faq-a-inner"><p>{fq["a"]}</p></div></div></div>')
    content_body.append('</div>')

    content_body.append('<div class="inline-cta dark"><div class="cta-copy"><h4>' + bottom_cta['headline'] + '</h4><p>' + bottom_cta['body'] + '</p></div><div class="cta-action"><a href="' + bottom_cta['url'] + '" class="cta-btn-inline">' + bottom_cta['button'] + ' <span>→</span></a><span class="cta-meta">' + bottom_cta['meta'] + '</span></div></div>')

    content_body.append('<h2 id="sources">Sources &amp; methodology</h2>')
    content_body.append('<div class="sources-block"><div class="sources-head">📑 Research sources</div><ol class="sources-list">')
    for i, src in enumerate(sources, 1):
        num = f'{i:02d}'
        content_body.append(f'<li><span class="src-num">[{num}]</span><a href="{src["url"]}" target="_blank" rel="noopener">{src["text"]}</a></li>')
    content_body.append('</ol></div>')

    content_body.append('<div class="author-block"><div class="author-avatar-lg">' + a['initials'] + '</div><div class="author-info"><h4><a href="/authors/' + author_slug + '/">' + a['name'] + '</a></h4><div class="role">' + a['role_full'] + '</div><p>' + a['bio'] + '</p><div class="author-links-row"><a href="' + a['x'] + '">' + a['x_handle'] + '</a><a href="' + a['linkedin'] + '">LinkedIn</a><a href="/about/">About theStacc</a></div></div></div>')

    # FAQ schema
    faq_schema = []
    for fq in faqs:
        faq_schema.append('{\n          "@type": "Question",\n          "name": "' + escape_quotes(fq['q']) + '",\n          "acceptedAnswer": { "@type": "Answer", "text": "' + escape_quotes(fq['a']) + '" }\n        }')

    # Related posts
    rel_cards = []
    for r in related:
        rel_cards.append(f'<a href="{r["url"]}" class="related-card"><span class="cat">{r["cat"]}</span><h3>{r["title"]}</h3><p>{r["desc"]}</p><span class="arrow-link">{r["cta"]} →</span></a>')

    sidebar = sidebar or {}
    sidebar_bullets = sidebar.get('bullets', ['SEO-optimized content briefs', 'Editorial workflow automation', 'Performance dashboard', 'Weekly growth reports'])
    sidebar_social = sidebar.get('social_proof', 'No credit card required')

    file_content = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{escape_quotes(title)} | theStacc",
  description: "{escape_quotes(description)}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: [
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/" }},
        {{ "@type": "ListItem", "position": 3, "name": "{escape_quotes(h1)}", "item": "https://thestacc.com/blog/{slug}/" }}
      ]
    }},
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{escape_quotes(h1)}",
      "description": "{escape_quotes(description)}",
      "image": "https://thestacc.com/og/blog-{slug}.webp",
      "datePublished": "{published}",
      "dateModified": "{modified}",
      "author": {{ "@type": "Person", "name": "{a['name']}", "url": "https://thestacc.com/authors/{author_slug}/", "sameAs": ["{a['linkedin']}"] }},
      "publisher": {{ "@type": "Organization", "name": "theStacc" }}
    }},
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {','.join(faq_schema)}
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
      <span class="current">{h1}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{h1}</h1>
    <p class="description">{hero_desc}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{a['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{a['name']}</a></span>
          <span class="meta-author-role">{a['role_short']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{datetime.strptime(published, "%Y-%m-%d").strftime("%b %d, %Y")}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{sidebar.get('read_time', '12 min')}</span></div>
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
      <svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="80" y="120" width="180" height="120" rx="12" fill="#ffffff"/>
          <rect x="460" y="120" width="180" height="120" rx="12" fill="#ffffff"/>
          <path d="M260 180h200" stroke-dasharray="6 4"/>
          <polygon points="460,180 445,170 445,190" fill="#4f39f6" stroke="none"/>
          <text x="170" y="175" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">INPUT</text>
          <text x="550" y="175" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">OUTPUT</text>
          <text x="360" y="170" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="#111827" font-weight="600">{cover_sub}</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{cover_title}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">thestacc.com/blog/{slug}</text>
      </svg>
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">
        {''.join(content_body)}
      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{sidebar.get('eyebrow', 'Free content audit · 24-hour delivery')}</div>
          <div class="cta-title">{sidebar.get('title', 'Scale your content engine')}</div>
          <p class="cta-desc">{sidebar.get('desc', 'Get a content strategy audit, editorial roadmap, and 90-day growth plan built for your site.')}</p>
          <a href="{sidebar.get('cta_url', '/checkout/')}" class="cta-btn">{sidebar.get('cta_button', 'Start for $1')} <span>→</span></a>
          <ul class="cta-bullets">
            {''.join(f'<li>{b}</li>' for b in sidebar_bullets)}
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
            {''.join(toc_items)}
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={escape_quotes(title)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>{sidebar.get('related_head', 'More ' + category + ' guides')}</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        {''.join(rel_cards)}
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

    out_path = ROOT / 'src/pages/blog' / slug / 'index.astro'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(file_content)
    return out_path

if __name__ == '__main__':
    import sys
    # Expect JSON on stdin
    data = json.load(sys.stdin)
    out = generate(**data)
    print(out)
