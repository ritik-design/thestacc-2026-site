#!/usr/bin/env python3
"""Migrate blog posts that exist in Old Website but are missing from the new site.

Preserves 100% of the original markdown content by converting it to HTML and
wrapping it in the new Astro blog template.
"""
import re
import json
import html
from pathlib import Path
from datetime import datetime
import markdown

ROOT = Path(__file__).parent
OLD_BLOG = ROOT / "Old Website" / "src" / "content" / "blog"
NEW_BLOG = ROOT / "src" / "pages" / "blog"

MISSING_SLUGS = [
    "http-status-codes-seo",
    "off-page-seo-guide",
    "seo-proposal-template",
    "technical-seo-checklist",
    "what-is-keyword-cannibalization",
]

AUTHORS = {
    "Siddharth Gangal": {
        "slug": "siddharth-gangal",
        "initials": "SG",
        "role": "Founder · theStacc",
    },
    "Akshay VR": {
        "slug": "akshay-vr",
        "initials": "AVR",
        "role": "Marketing Head · theStacc",
    },
    "Ritik Namdev": {
        "slug": "ritik-namdev",
        "initials": "RN",
        "role": "Growth Manager · theStacc",
    },
}


def extract_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 3 :].strip()
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def classify_category(title: str, slug: str) -> str:
    text = (title + " " + slug.replace("-", " ")).lower()
    if any(k in text for k in ["local seo", "gbp", "map pack", "citation", "review", "franchise"]):
        return "Local SEO"
    if any(k in text for k in ["ai", "agent", "chatgpt", "llm", "perplexity", "claude"]):
        return "AI Search"
    if any(k in text for k in ["content", "blog", "writing", "brief", "editorial"]):
        return "Content Strategy"
    return "SEO Tips"


def estimate_read_time(word_count: int) -> str:
    minutes = max(1, round(word_count / 225))
    return f"{minutes} min"


def md_to_html(body: str) -> str:
    """Convert markdown body to HTML and apply new-design wrappers."""
    # Replace --- horizontal rules with section breaks (optional)
    body = re.sub(r"\n---\n", "\n\n", body)

    html_body = markdown.markdown(body, extensions=["tables", "fenced_code"])

    # Add design classes
    html_body = html_body.replace("<table>", '<table>')
    html_body = re.sub(
        r"<table>(.*?)</table>",
        r'<div class="table-wrap"><table>\1</table></div>',
        html_body,
        flags=re.DOTALL,
    )
    html_body = html_body.replace("<img ", '<img loading="lazy" ')

    # Escape braces so Astro doesn't treat them as JSX expressions
    html_body = html_body.replace("{", "&#123;").replace("}", "&#125;")

    return html_body


def extract_faqs(html_body: str) -> list[dict]:
    """Extract FAQ headings (h3 ending in ?) and following paragraphs."""
    faqs = []
    matches = list(re.finditer(r"<h3[^>]*>(.*?)</h3>", html_body, flags=re.IGNORECASE))
    for i, m in enumerate(matches):
        question = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if not question.endswith("?"):
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_body)
        answer_html = html_body[start:end]
        # Keep only the first paragraph or list as the answer
        answer = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", "", answer_html, flags=re.DOTALL | re.IGNORECASE).strip()
        if answer:
            faqs.append({"question": question, "answer": answer})
    return faqs


def build_faq_section(faqs: list[dict]) -> str:
    if not faqs:
        return ""
    items = []
    for f in faqs:
        q = html.escape(f["question"]).replace("'", "\\'")
        a = f["answer"].replace("'", "\\'")
        items.append(
            f'''  <div class="faq-item">
    <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">
      <span class="faq-q-text">{f["question"]}</span>
      <span class="faq-toggle" aria-hidden="true"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
    </button>
    <div class="faq-a"><div class="faq-a-inner">{f["answer"]}</div></div>
  </div>'''
        )
    return "\n".join([
        '<h2 id="frequently-asked-questions">Frequently asked questions</h2>',
        '<div class="faq-list">',
    ] + items + ['</div>'])


def build_schema(title: str, description: str, slug: str, date: str, author_name: str, faqs: list[dict]) -> dict:
    canonical = f"https://thestacc.com/blog/{slug}/"
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": date,
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "author": {"@type": "Person", "name": author_name},
            "publisher": {"@type": "Organization", "name": "theStacc"},
        },
    ]
    if faqs:
        schema.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["answer"]).strip()},
                }
                for f in faqs[:5]
            ],
        })
    return schema


def render_post(slug: str):
    old_path = OLD_BLOG / f"{slug}.md"
    if not old_path.exists():
        print(f"SKIP: old source missing for {slug}")
        return

    fm, body = extract_frontmatter(old_path.read_text(encoding="utf-8"))
    title = fm.get("title", slug.replace("-", " ").title())
    description = fm.get("description", "")
    date = fm.get("date", "2026-01-01")
    author_name = fm.get("author", "Siddharth Gangal")
    category = fm.get("category", classify_category(title, slug))

    author = AUTHORS.get(author_name, AUTHORS["Siddharth Gangal"])
    html_body = md_to_html(body)
    faqs = extract_faqs(html_body)
    faq_section = build_faq_section(faqs)
    schema = build_schema(title, description, slug, date, author_name, faqs)

    # Strip trailing FAQ section from body if we rendered it separately
    # (We already extracted, but the HTML still contains it.)
    # For simplicity, append FAQ section at the end if it wasn't included.
    if faqs and '<h2 id="frequently-asked-questions">' not in html_body:
        html_body += "\n" + faq_section

    word_count = len(re.findall(r"\b\w+\b", html_body))
    read_time = estimate_read_time(word_count)

    published_fmt = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d, %Y")

    og_image = f"/og/blog-{slug}.webp"

    astro_content = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{title}",
  description: "{description}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "{og_image}",
  schemaData: {json.dumps(schema, indent=2)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{title}</span>
    </div>
    <span class="post-cat">{category}</span>
    <h1>{title}</h1>
    <p class="description">{description}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author["slug"]}/">{author_name}</a></span>
          <span class="meta-author-role">{author["role"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{published_fmt}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">
{html_body}
      </article>
    </div>
  </div>

</BaseLayout>
'''

    out_dir = NEW_BLOG / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.astro"
    out_file.write_text(astro_content, encoding="utf-8")
    print(f"MIGRATED: {out_file} ({word_count} words, {len(faqs)} FAQs)")


def main():
    for slug in MISSING_SLUGS:
        render_post(slug)


if __name__ == "__main__":
    main()
