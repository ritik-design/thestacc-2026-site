#!/usr/bin/env python3
"""Generate Astro blog posts for chunk-013."""
import json, os, re, html
from datetime import datetime, timezone

ROOT = '/home/ritik/thestacc.com-astro/thestacc-2026-site'
AUTHORS = {
    'siddharth-gangal': {'name':'Siddharth Gangal','role':'Founder · theStacc','initials':'SG','slug':'siddharth-gangal','linkedin':'https://www.linkedin.com/in/sidgangal/','x':'https://x.com/sidgangal','x_handle':'@sidgangal','bio':'Siddharth is the founder of theStacc and Arka360. He writes about SEO, content at scale, and the tactics that actually move rankings.'},
    'akshay-vr': {'name':'Akshay VR','role':'Marketing Head · theStacc','initials':'AVR','slug':'akshay-vr','linkedin':'https://www.linkedin.com/in/akshay-vr-3aa1b9204/','x':'https://x.com/akshayvr_','x_handle':'@akshayvr_','bio':'Akshay leads marketing at theStacc and focuses on SEO strategy, editorial workflows, and demand generation for B2B SaaS.'},
    'ritik-namdev': {'name':'Ritik Namdev','role':'Growth Manager · theStacc','initials':'RN','slug':'ritik-namdev','linkedin':'https://www.linkedin.com/in/ritiknamdev/','x':'https://x.com/ritiknamdev_','x_handle':'@ritiknamdev_','bio':'Ritik runs growth systems at theStacc, specializing in programmatic SEO, analytics, and conversion experiments.'}
}

def escape_json(s):
    return json.dumps(s)

def strip_html(s):
    return re.sub(r'<[^>]+>', '', s)

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def render_astro(slug, data):
    author = AUTHORS[data['author']]
    title = data['title']
    h1 = data.get('h1', title)
    desc = data['description']
    category = data['category']
    date_pub = data.get('datePublished', '2026-04-01')
    date_mod = data.get('dateModified', '2026-07-01')
    published_display = data.get('published_display', 'Apr 2026')
    updated_display = data.get('updated_display', 'Q3 2026')
    read_time = data.get('read_time', '12 min')
    cover_title = data.get('cover_title', h1)
    cover_sub = data.get('cover_sub', '')
    lede = data['lede']
    tldr = data['tldr']
    sections = data['sections']
    faqs = data['faqs']
    sources = data['sources']
    inline_cta = data['inline_cta']
    bottom_cta = data['bottom_cta']
    sidebar_cta = data['sidebar_cta']
    related = data['related']
    svg = data.get('svg', '')
    schema_faqs = []
    for q,a in faqs:
        schema_faqs.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':strip_html(a)}})
    schema_data = [
        {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Home','item':'https://thestacc.com/'},
            {'@type':'ListItem','position':2,'name':'Blog','item':'https://thestacc.com/blog/'},
            {'@type':'ListItem','position':3,'name':h1,'item':f'https://thestacc.com/blog/{slug}/'}
        ]},
        {'@context':'https://schema.org','@type':'Article','headline':h1,'description':desc,'image':f'https://thestacc.com/og/blog-{slug}.webp','datePublished':date_pub,'dateModified':date_mod,'author':{'@type':'Person','name':author['name'],'url':f'https://thestacc.com/authors/{author["slug"]}/','sameAs':[author['linkedin']]},'publisher':{'@type':'Organization','name':'theStacc'}},
        {'@context':'https://schema.org','@type':'FAQPage','mainEntity':schema_faqs}
    ]

    toc_items = []
    for sec in sections:
        if sec.get('toc'):
            toc_items.append((sec['id'], sec['toc']))
    toc_html = '\n'.join(f'            <li><a href="#{cid}">{html.escape(label)}</a></li>' for cid,label in toc_items)

    def render_sections(secs):
        out = []
        for sec in secs:
            if 'h2' in sec:
                out.append(f'        <h2 id="{sec["id"]}">{sec["h2"]}</h2>')
            if 'h3' in sec:
                out.append(f'        <h3 id="{sec["id"]}">{sec["h3"]}</h3>')
            if 'body' in sec:
                out.append(f'        {sec["body"]}')
            if 'table' in sec:
                thead = ''.join(f'<th>{html.escape(c)}</th>' for c in sec['table'][0])
                tbody = ''
                for row in sec['table'][1:]:
                    tbody += '<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in row) + '</tr>'
                out.append(f'        <div class="table-wrap"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>')
            if 'ol' in sec:
                items = ''.join(f'<li><strong>{html.escape(i[0])}.</strong> {i[1]}</li>' for i in sec['ol'])
                out.append(f'        <ol>{items}</ol>')
            if 'ul' in sec:
                items = ''.join(f'<li><strong>{html.escape(i[0])}.</strong> {i[1]}</li>' for i in sec['ul'])
                out.append(f'        <ul>{items}</ul>')
            if 'pre' in sec:
                out.append(f'        <pre><code>{html.escape(sec["pre"])}</code></pre>')
        return '\n\n'.join(out)

    faq_html = '\n'.join(f'''        <div class="faq-item">
            <button class="faq-q" onclick="toggleFaq(this)">
              <span class="faq-q-text">{html.escape(q)}</span>
              <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
            </button>
            <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
          </div>''' for q,a in faqs)

    sources_html = '\n'.join(f'            <li><span class="src-num">[{i+1:02d}]</span><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(text)}</a></li>' for i,(text,url) in enumerate(sources))

    related_html = '\n'.join(f'''        <a href="{html.escape(r['url'])}" class="related-card">
          <span class="cat">{html.escape(r['cat'])}</span>
          <h3>{html.escape(r['title'])}</h3>
          <p>{html.escape(r['desc'])}</p>
          <span class="arrow-link">{html.escape(r['cta'])} →</span>
        </a>''' for r in related)

    schema_json = json.dumps(schema_data, indent=2)

    return f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {escape_json(title + ' | theStacc')},
  description: {escape_json(desc)},
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {schema_json}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{html.escape(h1)}</span>
    </div>
    <span class="post-cat">{html.escape(category)}</span>
    <h1>{html.escape(h1)}</h1>
    <p class="description">{html.escape(desc)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{author['name']}</a></span>
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
        <div class="cover-mono">{html.escape(category)}</div>
        <div class="cover-title">{html.escape(cover_title)}</div>
        <div class="cover-sub">{html.escape(cover_sub)}</div>
      </div>
      {svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{html.escape(lede[0])}</strong> {html.escape(lede[1])}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{html.escape(inline_cta['headline'])}</h4>
            <p>{html.escape(inline_cta['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{html.escape(inline_cta['url'])}" class="cta-btn-inline">{html.escape(inline_cta['button'])} <span>→</span></a>
            <span class="cta-meta">{html.escape(inline_cta['meta'])}</span>
          </div>
        </div>

{render_sections(sections)}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{faq_html}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>{html.escape(bottom_cta['headline'])}</h4>
            <p>{html.escape(bottom_cta['body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{html.escape(bottom_cta['url'])}" class="cta-btn-inline">{html.escape(bottom_cta['button'])} <span>→</span></a>
            <span class="cta-meta">{html.escape(bottom_cta['meta'])}</span>
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
            <div class="role">{author['role']}</div>
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
          <div class="cta-eyebrow">{html.escape(sidebar_cta['eyebrow'])}</div>
          <div class="cta-title">{html.escape(sidebar_cta['title'])}</div>
          <p class="cta-desc">{html.escape(sidebar_cta['desc'])}</p>
          <a href="{html.escape(sidebar_cta['url'])}" class="cta-btn">{html.escape(sidebar_cta['button'])} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{html.escape(sidebar_cta['bullets'][0])}</li>
            <li>{html.escape(sidebar_cta['bullets'][1])}</li>
            <li>{html.escape(sidebar_cta['bullets'][2])}</li>
            <li>{html.escape(sidebar_cta['bullets'][3])}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {html.escape(sidebar_cta['social_proof'])}
          </div>
        </div>

        <nav class="sidebar-toc" id="toc">
          <div class="toc-head">
            <svg viewBox="0 0 12 12" fill="none"><path d="M1 2h10M1 6h10M1 10h7" stroke="currentColor" stroke-width="1.5"/></svg>
            On this page
          </div>
          <ul class="toc-list">
{toc_html}
            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={html.escape(title)}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <h2>{html.escape('More ' + category + ' guides')}</h2>
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

def write(slug, data):
    out_dir = os.path.join(ROOT, 'src/pages/blog', slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.astro')
    astro = render_astro(slug, data)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(astro)
    return out_path


# SVG helpers
def svg_local_purple(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="250" y="110" width="220" height="140" rx="14" fill="#ffffff"/>
          <circle cx="320" cy="160" r="22" fill="#ede9fe" stroke="none"/>
          <text x="320" y="166" text-anchor="middle" font-family="Geist, sans-serif" font-size="18" fill="#4f39f6" font-weight="700">★</text>
          <path d="M360 150h80M360 175h60M360 200h90" stroke="#615fff" stroke-width="2"/>
          <path d="M210 250l80-40 60 30 80-50 80 60" stroke="#4f39f6" stroke-width="3"/>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

def svg_geo_brain(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M280 180c0-44 36-80 80-80s80 36 80 80-36 80-80 80" fill="#ffffff"/>
          <circle cx="330" cy="160" r="6" fill="#4f39f6" stroke="none"/>
          <circle cx="390" cy="160" r="6" fill="#4f39f6" stroke="none"/>
          <circle cx="360" cy="205" r="6" fill="#4f39f6" stroke="none"/>
          <path d="M330 160l30 45 30-45M360 100v-20M260 180h-20M460 180h20M360 280v20"/>
          <rect x="470" y="120" width="90" height="34" rx="6" fill="#ffffff" stroke="#615fff"/>
          <text x="515" y="141" text-anchor="middle" font-family="Geist Mono, monospace" font-size="11" fill="#4f39f6">AI cites</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

def svg_search_compare(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="160" y="120" width="140" height="120" rx="12" fill="#ffffff"/>
          <rect x="420" y="120" width="140" height="120" rx="12" fill="#ffffff"/>
          <text x="230" y="180" text-anchor="middle" font-family="Geist, sans-serif" font-size="16" font-weight="700" fill="#4f39f6">Gemini</text>
          <text x="490" y="180" text-anchor="middle" font-family="Geist, sans-serif" font-size="16" font-weight="700" fill="#615fff">ChatGPT</text>
          <path d="M300 180h120" stroke-dasharray="6 4" stroke="#615fff"/>
          <polygon points="420,180 405,170 405,190" fill="#615fff" stroke="none"/>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

def svg_stats_chart(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="220" y="230" width="40" height="70" rx="4" fill="#ffffff"/>
          <rect x="280" y="190" width="40" height="110" rx="4" fill="#ffffff"/>
          <rect x="340" y="150" width="40" height="150" rx="4" fill="#4f39f6"/>
          <rect x="400" y="170" width="40" height="130" rx="4" fill="#ffffff"/>
          <rect x="460" y="200" width="40" height="100" rx="4" fill="#ffffff"/>
          <path d="M200 250h300"/>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

def svg_traffic_funnel(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="240,120 480,120 440,180 280,180" fill="#ffffff"/>
          <polygon points="280,190 440,190 410,240 310,240" fill="#ffffff"/>
          <polygon points="310,250 410,250 390,290 330,290" fill="#4f39f6"/>
          <text x="360" y="155" text-anchor="middle" font-family="Geist, sans-serif" font-size="13" fill="#111827">Traffic</text>
          <text x="360" y="220" text-anchor="middle" font-family="Geist, sans-serif" font-size="13" fill="#111827">Leads</text>
          <text x="360" y="275" text-anchor="middle" font-family="Geist, sans-serif" font-size="12" fill="#ffffff">Conversions</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

def svg_ghost_cms(title, sub):
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="720" height="360" fill="#f5f3ff"/>
        <circle cx="360" cy="180" r="130" fill="#ede9fe"/>
        <g fill="none" stroke="#4f39f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M360 110c-39 0-70 31-70 70s31 70 70 70 70-31 70-70" fill="#ffffff"/>
          <path d="M360 130v30l25 15" stroke="#615fff" stroke-width="3"/>
          <circle cx="360" cy="180" r="8" fill="#4f39f6" stroke="none"/>
          <text x="360" y="275" text-anchor="middle" font-family="Geist Mono, monospace" font-size="14" fill="#4f39f6" font-weight="600">Ghost CMS</text>
        </g>
        <text x="360" y="320" text-anchor="middle" font-family="Geist, sans-serif" font-size="22" font-weight="600" fill="#111827">{html.escape(title)}</text>
        <text x="360" y="345" text-anchor="middle" font-family="Geist Mono, monospace" font-size="12" fill="#57534e">{html.escape(sub)}</text>
      </svg>'''

POSTS = {
}

if __name__ == '__main__':
    import json, datetime
    with open(os.path.join(ROOT, 'Stacc/blog-migration/progress.json')) as f:
        progress = json.load(f)
    completed = []
    failed = {}
    for slug, data in POSTS.items():
        try:
            write(slug, data)
            progress['posts'][slug]['status'] = 'done'
            progress['posts'][slug]['category'] = data['category']
            progress['posts'][slug]['author'] = data['author']
            progress['posts'][slug]['attempts'] = progress['posts'][slug].get('attempts', 0) + 1
            progress['posts'][slug]['word_count'] = len(re.findall(r"\w+", open(os.path.join(ROOT, 'src/pages/blog', slug, 'index.astro')).read()))
            progress['posts'][slug]['verified_at'] = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            completed.append(slug)
        except Exception as e:
            failed[slug] = str(e)
            progress['posts'][slug]['status'] = 'failed'
            progress['posts'][slug]['attempts'] = progress['posts'][slug].get('attempts', 0) + 1
            progress['posts'][slug]['last_error'] = str(e)
    progress['totals'] = {s: sum(1 for t in progress['posts'].values() if t.get('status') == s) for s in ['pending','in_progress','done','failed']}
    with open(os.path.join(ROOT, 'Stacc/blog-migration/progress.json'), 'w') as f:
        json.dump(progress, f, indent=2)
    chunk_progress = {
        'chunk': os.path.join(ROOT, 'Stacc/blog-migration/small-chunks/chunk-013.txt'),
        'total': len(POSTS),
        'completed': completed,
        'failed': failed,
        'skipped_already_done': []
    }
    with open(os.path.join(ROOT, 'Stacc/blog-migration/small-chunks/chunk-013.txt.progress.json'), 'w') as f:
        json.dump(chunk_progress, f, indent=2)
    print(f"Completed: {len(completed)}, Failed: {len(failed)}")
    for s,e in failed.items():
        print(f"  {s}: {e}")
