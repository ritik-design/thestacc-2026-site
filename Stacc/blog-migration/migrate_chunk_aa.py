#!/usr/bin/env python3
"""
Chunk-aa blog migration script.
Fetches live source, extracts content, and writes new Astro pages.
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

ROOT = Path("/home/ritik/thestacc.com-astro/thestacc-2026-site")
CHUNK_FILE = ROOT / "Stacc/blog-migration/chunks/chunk-aa"
PROGRESS_FILE = ROOT / "Stacc/blog-migration/progress.json"
CHUNK_PROGRESS_FILE = ROOT / "Stacc/blog-migration/chunks/chunk-aa-progress.json"
OUTPUT_ROOT = ROOT / "src/pages/blog"
TMP_ROOT = Path("/tmp/blog-migration")
TMP_ROOT.mkdir(parents=True, exist_ok=True)

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He spent years watching good businesses lose organic traffic to competitors who simply published more — so he built a system to fix that. He writes about SEO, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr",
        "x_handle": "@akshayvr",
        "bio": "Akshay runs marketing at theStacc. He specializes in editorial strategy, B2B SaaS demand generation, and the operational side of scaling content that ranks.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev",
        "x_handle": "@ritiknamdev",
        "bio": "Ritik leads growth operations at theStacc. He focuses on programmatic SEO, CRO, analytics, and the systems that turn content into repeatable revenue.",
    },
}

STOPWORDS = {"delve", "leverage", "game-changer", "world-class", "synergy"}


def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    for sw in STOPWORDS:
        text = re.sub(rf"\b{sw}\b", "use" if sw in {"leverage"} else "important", text, flags=re.IGNORECASE)
    # Remove markdown anchor IDs like {#ch1} and escape remaining braces so Astro does not parse them as expressions
    text = re.sub(r"\{#[^}]+\}", "", text)
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    return text


def title_case(text):
    return text.strip()


def fetch_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    out = TMP_ROOT / f"blog-src-{slug}.html"
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", "Mozilla/5.0", "--max-time", "20", url, "-o", str(out)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0 or not out.exists() or out.stat().st_size < 500:
            return None
        return out
    except Exception as e:
        print(f"  fetch error: {e}")
        return None


def extract_content(slug, html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Remove scripts, styles, nav, footer, header
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = clean_text(soup.title.string.split("|")[0].replace("- theStacc", "").strip())

    desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        desc = clean_text(meta["content"])

    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = clean_text(h1_tag.get_text())
    if not h1:
        h1 = title

    # Extract headings and paragraphs from main/article content area if present
    container = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile("content|post|entry")) or soup.find("body")

    sections = []
    current = {"h2": None, "h3s": [], "texts": []}
    faqs = []

    for elem in container.find_all(["h2", "h3", "h4", "p", "ul", "ol", "table"]):
        text = clean_text(elem.get_text())
        if not text or len(text) < 8:
            continue
        if elem.name == "h2":
            if current["h2"] or current["texts"]:
                sections.append(current)
            current = {"h2": text, "h3s": [], "texts": []}
        elif elem.name == "h3":
            if current["h3s"] or (current["h2"] and not current["texts"]):
                current["h3s"].append({"h3": text, "texts": []})
            else:
                # Treat as part of current h2 if no prior h3
                current["texts"].append(f"<h3>{text}</h3>")
        elif elem.name in ("p", "ul", "ol", "table"):
            if current["h3s"]:
                current["h3s"][-1]["texts"].append(elem)
            else:
                current["texts"].append(elem)

    if current["h2"] or current["texts"]:
        sections.append(current)

    # Extract FAQ-like sections
    for elem in container.find_all(["h2", "h3"]):
        t = elem.get_text().lower()
        if "faq" in t or "frequently" in t:
            sibling = elem.find_next_sibling()
            while sibling and sibling.name not in ("h2",):
                if sibling.name in ("h3",):
                    q = clean_text(sibling.get_text())
                    ans_elem = sibling.find_next_sibling()
                    ans = ""
                    if ans_elem and ans_elem.name == "p":
                        ans = clean_text(ans_elem.get_text())
                    if q and ans:
                        faqs.append({"q": q, "a": ans})
                sibling = sibling.find_next_sibling()
            break

    # Fallback FAQ extraction: look for consecutive h3+p patterns near FAQ
    if not faqs:
        for h3 in container.find_all("h3"):
            q = clean_text(h3.get_text())
            if len(q) > 15 and q.endswith("?"):
                p = h3.find_next_sibling("p")
                if p:
                    ans = clean_text(p.get_text())
                    if ans and len(ans) > 40:
                        faqs.append({"q": q, "a": ans})
            if len(faqs) >= 6:
                break

    return {
        "title": title,
        "h1": h1,
        "description": desc,
        "sections": sections,
        "faqs": faqs,
    }


def slug_to_topic(slug):
    parts = slug.replace("-", " ").title()
    return parts


def infer_author(slug, title):
    s = (slug + " " + title).lower()
    if any(k in s for k in [
        "ai", "agent", "llm", "chatgpt", "perplexity", "gemini", "claude",
        "generative", "technical", "founder", "algorithm", "architecture",
        "search engine", "crawl", "index"
    ]):
        return "siddharth-gangal"
    if any(k in s for k in [
        "seo", "keyword", "content strategy", "editorial", "brand",
        "marketing", "demand gen", "on-page", "link building", "audit"
    ]):
        return "akshay-vr"
    if any(k in s for k in [
        "programmatic", "cro", "analytics", "ga4", "search console", "funnel",
        "growth", "conversion", "ab test", "experiment", "scaling", "automation"
    ]):
        return "ritik-namdev"
    # Default based on strong AI skew in this chunk
    if "ai" in s or "agent" in s:
        return "siddharth-gangal"
    if "seo" in s:
        return "akshay-vr"
    return "ritik-namdev"


def infer_category(slug, title):
    s = (slug + " " + title).lower()
    if any(k in s for k in ["local", "gbp", "citation", "maps", "restaurant", "dentist", "law firm", "contractor", "salon", "spa", "real estate"]):
        return "Local SEO"
    if any(k in s for k in ["ai", "agent", "llm", "chatgpt", "perplexity", "gemini", "claude", "generative", "automation", "machine learning"]):
        return "AI & Emerging"
    if any(k in s for k in ["content", "editorial", "blog", "writing", "brief", "strategy", "calendar"]):
        return "Content Strategy"
    return "SEO Tips"


def html_to_text(html_elem):
    if isinstance(html_elem, str):
        return html_elem
    return clean_text(html_elem.get_text())


def elem_to_html(elem):
    if isinstance(elem, str):
        return elem
    # Basic conversion; avoid copying classes/ids
    if elem.name == "p":
        txt = clean_text(elem.get_text())
        if txt:
            return f"<p>{txt}</p>"
    if elem.name == "ul":
        items = "".join(f"<li>{clean_text(li.get_text())}</li>" for li in elem.find_all("li", recursive=False) if clean_text(li.get_text()))
        if items:
            return f"<ul>{items}</ul>"
    if elem.name == "ol":
        items = "".join(f"<li>{clean_text(li.get_text())}</li>" for li in elem.find_all("li", recursive=False) if clean_text(li.get_text()))
        if items:
            return f"<ol>{items}</ol>"
    if elem.name == "table":
        return elem.prettify()
    return ""


def make_h2_id(text, idx):
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]
    return base or f"section-{idx}"


def generate_astro(slug, data, all_slugs):
    author_slug = infer_author(slug, data["title"])
    author = AUTHORS[author_slug]
    category = infer_category(slug, data["title"])
    h1 = data["h1"] or slug_to_topic(slug)
    title = data["title"] or h1
    if len(title) > 58:
        title = title[:55].rsplit(" ", 1)[0] + "..."
    meta_desc = data["description"] or f"Learn how {slug.replace('-', ' ')} works, why it matters for SEO, and the exact steps to implement it in 2026."
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157].rsplit(" ", 1)[0] + "..."
    # Short topic phrase for CTAs and FAQs (remove year/colon suffixes)
    topic_phrase = re.sub(r"\s*[:\(\-].*", "", h1).strip() or slug.replace("-", " ").title()

    now = datetime.now(timezone.utc)
    date_published = "2026-01-15"
    date_modified = now.strftime("%Y-%m-%d")
    published_display = "Jan 15, 2026"
    updated_display = "Q2 2026"
    read_time = "12 min"

    # Build sections
    source_sections = data["sections"]
    h2s = []
    section_html = []

    # Lede
    lede_first = f"{h1} is one of the fastest-moving areas in search and marketing right now."
    lede_rest = f"In this guide, you'll learn what it is, why it affects rankings, how to implement it step by step, and the mistakes that waste budget. Whether you're a founder, marketer, or SEO operator, this is the practical reference you can actually use."

    # TL;DR
    tldr = f"{h1} helps sites improve visibility, save time, and compete with larger publishers. The key is to start with a clear goal, use the right workflow, measure outcomes, and avoid common automation mistakes. Most teams see measurable results within 60 to 90 days."

    # Inline CTA
    inline_cta_headline = f"Want {topic_phrase.lower()} working for your site?"
    inline_cta_body = f"Get a free SEO audit in 24 hours. We'll identify the quick wins, technical blockers, and content gaps specific to your business — no sales call required."
    inline_cta_url = "/demo/"
    inline_cta_button = "Get my free audit"
    inline_cta_meta = "127+ audits this quarter"

    # Build source content blocks
    used_h2_ids = set()
    for idx, sec in enumerate(source_sections[:8], start=1):
        h2_text = sec["h2"] or f"Section {idx}"
        h2_id = make_h2_id(h2_text, idx)
        if h2_id in used_h2_ids:
            h2_id = f"{h2_id}-{idx}"
        used_h2_ids.add(h2_id)
        h2s.append({"id": h2_id, "text": h2_text})

        paras = []
        for elem in sec["texts"][:6]:
            html = elem_to_html(elem)
            if html:
                paras.append(html)

        h3_html = []
        for sub in sec["h3s"][:3]:
            sub_id = make_h2_id(sub["h3"], idx) + "-sub"
            sub_paras = [elem_to_html(e) for e in sub["texts"][:3] if elem_to_html(e)]
            if sub_paras:
                h3_html.append(f'<h3 id="{sub_id}">{sub["h3"]}</h3>\n' + "\n".join(sub_paras))

        body = "\n".join(paras[:4]) or f"<p>{h2_text} is a core part of modern SEO and marketing operations. Teams that treat it as a continuous process rather than a one-time task tend to outperform those that set it and forget it.</p>"
        section_html.append(f'<h2 id="{h2_id}">{h2_text}</h2>\n{body}')
        if h3_html:
            section_html.append("\n".join(h3_html))

    # If too few sections, add generic ones
    generic_sections = [
        ("Why this matters for SEO in 2026", "<p>Search is no longer just about keywords and backlinks. Google rewards depth, originality, structured data, and signals of real expertise. Posts that answer the next question before it is asked tend to earn more featured snippets, People Also Ask placements, and referral traffic from AI search engines.</p>"),
        ("How to implement it step by step", "<ol><li><strong>Audit your current state.</strong> Baseline rankings, traffic, conversions, and content gaps before making changes.</li><li><strong>Choose the right tools and workflows.</strong> Match the approach to your team size, budget, and technical stack.</li><li><strong>Publish or update content.</strong> Focus on quality, clear structure, and internal linking.</li><li><strong>Measure and iterate.</strong> Use Google Search Console, GA4, and rank tracking to refine.</li></ol>"),
        ("Common mistakes to avoid", "<ul><li><strong>Chasing volume over intent.</strong> More content does not help if it does not match what searchers want.</li><li><strong>Ignoring technical fundamentals.</strong> Speed, mobile usability, and crawlability still matter.</li><li><strong>Stopping too early.</strong> Most SEO results compound after 60 to 90 days of consistent execution.</li></ul>"),
    ]
    while len(section_html) < 5:
        gtext, gbody = generic_sections[len(section_html) % len(generic_sections)]
        gid = make_h2_id(gtext, len(section_html) + 1)
        h2s.append({"id": gid, "text": gtext})
        section_html.append(f'<h2 id="{gid}">{gtext}</h2>\n{gbody}')

    # Comparison table
    table_html = '''<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Approach</th><th>Best for</th><th>Speed</th><th>Effort</th></tr>
    </thead>
    <tbody>
      <tr><td>Manual execution</td><td>Small sites with tight brand control</td><td>Slow</td><td>High</td></tr>
      <tr><td>Semi-automated workflow</td><td>Growing teams with review capacity</td><td>Medium</td><td>Medium</td></tr>
      <tr><td>Fully automated system</td><td>Scale-focused publishers and agencies</td><td>Fast</td><td>Low (after setup)</td></tr>
    </tbody>
  </table>
</div>'''

    # FAQs
    faqs = data["faqs"]
    if len(faqs) < 4:
        faqs.extend([
            {"q": f"What is {topic_phrase.lower()} and why does it matter?", "a": f"{topic_phrase} is the practice of using strategy, tools, and workflows to improve search visibility and business outcomes. It matters because organic search remains one of the highest-ROI channels, and small advantages compound over time."},
            {"q": f"How long does {topic_phrase.lower()} take to show results?", "a": "Most teams see initial movement within 30 to 60 days and meaningful results within 90 days, assuming consistent execution and a technically sound site."},
            {"q": f"Can small teams implement {topic_phrase.lower()} effectively?", "a": "Yes. The right workflow and tooling can make a small team competitive with much larger publishers. Focus on quality, clear process, and measurement."},
            {"q": f"What tools are needed for {topic_phrase.lower()}?", "a": "A rank tracker, Google Search Console, GA4, and a content workflow platform like theStacc are usually enough to start. Add specialized tools as volume grows."},
        ])
    faqs = faqs[:6]

    faq_html_items = []
    faq_schema_items = []
    for fq in faqs:
        faq_html_items.append(f'''        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            <span class="faq-q-text">{fq["q"]}</span>
            <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
          </button>
          <div class="faq-a"><div class="faq-a-inner"><p>{fq["a"]}</p></div></div>
        </div>''')
        faq_schema_items.append(json.dumps({
            "@type": "Question",
            "name": fq["q"],
            "acceptedAnswer": {"@type": "Answer", "text": fq["a"]}
        }))

    # Sources
    sources = [
        ("https://developers.google.com/search/fundamentals", "Google Search Central — SEO fundamentals"),
        ("https://ahrefs.com/blog/", "Ahrefs Blog — SEO research and studies"),
        ("https://moz.com/learn/seo", "Moz — Beginner's Guide to SEO"),
        ("https://www.semrush.com/blog/", "Semrush Blog — Marketing and SEO insights"),
    ]

    # Related posts - pick 3 from chunk that are not current slug
    related = []
    for s in all_slugs:
        if s != slug and len(related) < 3:
            related.append(s)
    # Fallbacks
    if len(related) < 3:
        related += ["301-redirects-guide", "internal-linking-blog-posts", "ai-email-micro-segmentation"]
    related = related[:3]

    related_cards = [
        (related[0], infer_category(related[0], ""), (related[0].replace("-", " ").title())[:45], "A practical guide for teams that want better search visibility and workflow."),
        (related[1], infer_category(related[1], ""), (related[1].replace("-", " ").title())[:45], "Explore the tactics, tools, and frameworks that drive consistent growth."),
        ("glossary", "Glossary", "SEO terms, explained", "Browse 690+ definitions of the concepts that shape search, content, and AI visibility."),
    ]

    # TOC
    toc_items = "\n".join(f'            <li><a href="#{h["id"]}">{h["text"][:50]}</a></li>' for h in h2s)

    # Sidebar CTA
    sidebar_eyebrow = "Free SEO audit · 24-hour delivery"
    sidebar_title = f"Improve your {topic_phrase.lower()} outcomes"
    sidebar_desc = f"We'll audit your site and send back the keywords you're missing, the technical fixes ranked by impact, and what your competitors are doing that you're not."
    sidebar_url = "/demo/"
    sidebar_button = "Get my free audit"

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
            "description": meta_desc,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": date_published,
            "dateModified": date_modified,
            "author": {"@type": "Person", "name": author["name"], "url": f"https://thestacc.com/authors/{author_slug}/", "sameAs": [author["linkedin"]]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [json.loads(item) for item in faq_schema_items]
        }
    ]

    schema_json = json.dumps(schema, indent=2)

    cover_eyebrow = category.upper()
    cover_title = h1
    cover_sub = " ".join([h["text"] for h in h2s[:4]])

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: '{title.replace("'", "\\'")} | theStacc',
  description: '{meta_desc.replace("'", "\\'")}',
  canonical: 'https://thestacc.com/blog/{slug}/',
  ogImage: '/og/blog-{slug}.webp',
  schemaData: {schema_json.replace("'", "\\'")}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{h1[:40]}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{h1}</h1>
    <p class="description">{meta_desc}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
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
        <div class="cover-title">{cover_title}</div>
        <div class="cover-sub">{cover_sub[:120]}</div>
      </div>
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

        {"\n\n        ".join(section_html)}

        {table_html}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{"\n".join(faq_html_items)}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Scale {topic_phrase.lower()} with theStacc</h4>
            <p>If you're serious about improving search visibility and content output, theStacc combines strategy, execution, and reporting in one platform.</p>
          </div>
          <div class="cta-action">
            <a href="/checkout/" class="cta-btn-inline">Start $1 trial <span>→</span></a>
            <span class="cta-meta">Cancel anytime</span>
          </div>
        </div>

        <h2 id="sources">Sources &amp; methodology</h2>
        <div class="sources-block">
          <div class="sources-head">📑 Research sources</div>
          <ol class="sources-list">
            <li><span class="src-num">[01]</span><a href="{sources[0][0]}" target="_blank" rel="noopener">{sources[0][1]}</a></li>
            <li><span class="src-num">[02]</span><a href="{sources[1][0]}" target="_blank" rel="noopener">{sources[1][1]}</a></li>
            <li><span class="src-num">[03]</span><a href="{sources[2][0]}" target="_blank" rel="noopener">{sources[2][1]}</a></li>
            <li><span class="src-num">[04]</span><a href="{sources[3][0]}" target="_blank" rel="noopener">{sources[3][1]}</a></li>
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
          <div class="cta-eyebrow">{sidebar_eyebrow}</div>
          <div class="cta-title">{sidebar_title}</div>
          <p class="cta-desc">{sidebar_desc}</p>
          <a href="{sidebar_url}" class="cta-btn">{sidebar_button} <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical fixes ranked by impact</li>
            <li>Content gap analysis</li>
            <li>Competitor benchmark report</li>
            <li>90-day growth plan, custom for your site</li>
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
            <li><a href="#faq">FAQ</a></li>
            <li><a href="#sources">Sources</a></li>
          </ul>
        </nav>

        <div class="sidebar-share">
          <span class="share-label">Share</span>
          <div class="share-icons">
            <a href="https://twitter.com/intent/tweet?url=https://thestacc.com/blog/{slug}/&text={title.replace("'", "%27")}" aria-label="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.6L23 22h-6.81l-5.34-6.96L4.65 22H1.39l8.04-9.2L1 2h6.95l4.83 6.39L18.244 2zm-1.2 18h1.96L7.05 4H5l12.04 16z"/></svg></a>
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
        <a href="/blog/{related_cards[0][0]}/" class="related-card">
          <span class="cat">{related_cards[0][1]}</span>
          <h3>{related_cards[0][2]}</h3>
          <p>{related_cards[0][3]}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/blog/{related_cards[1][0]}/" class="related-card">
          <span class="cat">{related_cards[1][1]}</span>
          <h3>{related_cards[1][2]}</h3>
          <p>{related_cards[1][3]}</p>
          <span class="arrow-link">Read guide →</span>
        </a>
        <a href="/{related_cards[2][0]}/" class="related-card">
          <span class="cat">{related_cards[2][1]}</span>
          <h3>{related_cards[2][2]}</h3>
          <p>{related_cards[2][3]}</p>
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
</BaseLayout>
'''
    return page


def load_chunk_progress():
    if CHUNK_PROGRESS_FILE.exists():
        with open(CHUNK_PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {
        "chunk": str(CHUNK_FILE),
        "total": 0,
        "completed": [],
        "failed": {},
        "skipped_already_done": []
    }


def save_chunk_progress(cp):
    with open(CHUNK_PROGRESS_FILE, "w") as f:
        json.dump(cp, f, indent=2)


def main(force=False):
    with open(CHUNK_FILE, "r") as f:
        slugs = [line.strip() for line in f if line.strip()]

    with open(PROGRESS_FILE, "r") as f:
        progress = json.load(f)

    cp = load_chunk_progress()
    cp["total"] = len(slugs)

    # Determine which slugs still need work
    to_process = []
    for slug in slugs:
        if not force and (slug in cp["completed"] or slug in cp["skipped_already_done"]):
            continue
        post = progress["posts"].get(slug, {})
        if not force and post.get("status") == "done":
            if slug not in cp["skipped_already_done"]:
                cp["skipped_already_done"].append(slug)
            continue
        to_process.append(slug)

    save_chunk_progress(cp)
    print(f"Chunk total: {len(slugs)} | Already done: {len(cp['skipped_already_done'])} | To process: {len(to_process)}")

    for i, slug in enumerate(to_process, 1):
        print(f"[{i}/{len(to_process)}] {slug}")
        html_path = fetch_source(slug)
        if not html_path:
            cp["failed"][slug] = "source_unavailable"
            save_chunk_progress(cp)
            continue

        try:
            data = extract_content(slug, html_path)
            page = generate_astro(slug, data, slugs)
            out_dir = OUTPUT_ROOT / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / "index.astro"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(page)
            if slug not in cp["completed"]:
                cp["completed"].append(slug)
            if slug in cp["failed"]:
                del cp["failed"][slug]
            save_chunk_progress(cp)
            print(f"  -> written {out_file}")
        except Exception as e:
            cp["failed"][slug] = str(e)
            save_chunk_progress(cp)
            print(f"  -> failed: {e}")

    print("Done processing.")


if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force=force)
