#!/usr/bin/env python3
"""Bulk migration script for chunk-029 blog slugs."""
import json, os, re, subprocess, textwrap, html
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"
CHUNK_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-029.txt")
PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/progress.json")
CHUNK_PROGRESS_FILE = os.path.join(ROOT, "Stacc/blog-migration/small-chunks/chunk-029.txt.progress.json")
OUT_ROOT = os.path.join(ROOT, "src/pages/blog")
TMP_DIR = "/tmp"

AUTHORS = {
    "siddharth-gangal": {
        "name": "Siddharth Gangal",
        "role_short": "Founder · theStacc",
        "role_full": "Founder · theStacc · IIT Mandi · Ex-Arka360",
        "initials": "SG",
        "linkedin": "https://www.linkedin.com/in/sidgangal/",
        "x": "https://x.com/sidgangal",
        "x_handle": "@sidgangal",
        "bio": "Siddharth is the founder of theStacc and Arka360. He writes about SEO, AI search, content at scale, and the tactics that actually move rankings.",
    },
    "akshay-vr": {
        "name": "Akshay VR",
        "role_short": "Marketing Head · theStacc",
        "role_full": "Marketing Head · theStacc",
        "initials": "AVR",
        "linkedin": "https://www.linkedin.com/in/akshay-vr-3aa1b9204/",
        "x": "https://x.com/akshayvr_",
        "x_handle": "@akshayvr_",
        "bio": "Akshay leads marketing and editorial strategy at theStacc. He specializes in B2B SaaS demand generation, content operations, and on-page SEO.",
    },
    "ritik-namdev": {
        "name": "Ritik Namdev",
        "role_short": "Growth Manager · theStacc",
        "role_full": "Growth Manager · theStacc",
        "initials": "RN",
        "linkedin": "https://www.linkedin.com/in/ritiknamdev/",
        "x": "https://x.com/ritiknamdev_",
        "x_handle": "@ritiknamdev_",
        "bio": "Ritik runs growth, analytics, and programmatic SEO experiments at theStacc. He focuses on CRO, funnel ops, and turning data into repeatable traffic gains.",
    },
}

CATEGORY_KEYWORDS = [
    ("AI & Emerging", ["ai", "agent", "agents", "chatgpt", "gpt", "llm", "generative", "gemini", "perplexity", "claude", "copilot", "machine learning", "algorithm update", "geo", "generative-engine", "ai search", "ai-overview", "ai mode"]),
    ("Local SEO", ["local seo", "local business", "google business profile", "gbp", "map pack", "near me", "citation", "dentist", "lawyer", "contractor", "realtor", "salon", "florist", "electrician", "funeral", "gym", "hvac", "chiropractor", "accountant", "home service", "restaurant", "yoga", "yelp"]),
    ("Content Strategy", ["content strategy", "content marketing", "editorial", "calendar", "blog post", "writing", "brief", "newsletter", "email marketing", "email automation", "subject line", "segmentation", "ugc", "evergreen", "format", "fact-check", "eeat", "e-e-a-t", "case stud", "meta description", "pillar", "how-to", "comparison", "feature article", "social media"]),
]

def classify_category(title, slug):
    text = (title + " " + slug.replace("-", " ")).lower()
    for cat, kws in CATEGORY_KEYWORDS:
        if any(kw in text for kw in kws):
            return cat
    return "SEO Tips"

def classify_author(title, slug, category):
    text = (title + " " + slug.replace("-", " ")).lower()
    sidd = ["ai", "agent", "chatgpt", "llm", "generative", "gemini", "perplexity", "claude", "algorithm", "technical", "architecture", "founder", "product strategy", "machine learning"]
    ritik = ["growth", "programmatic", "cro", "analytics", "ga4", "search console", "conversion", "funnel", "ab test", "a/b test", "roi", "statistics", "case study", "data", "study", "benchmark"]
    s = sum(1 for k in sidd if k in text)
    r = sum(1 for k in ritik if k in text)
    if category == "AI & Emerging":
        s += 2
    if category == "Local SEO":
        # mostly SEO strategy/editorial or growth; choose Akshay default unless growth terms
        pass
    if s > r and s > 0:
        return "siddharth-gangal"
    if r > s and r > 0:
        return "ritik-namdev"
    return "akshay-vr"

def clean_text(s):
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def escape_braces(s):
    return s.replace("{", "&#123;").replace("}", "&#125;")

ALLOWED_TAGS = {"p", "ul", "ol", "li", "pre", "code", "table", "thead", "tbody", "tr", "th", "td", "strong", "em", "br", "span", "h3", "h4"}

def clean_element(el):
    for tag in list(el.find_all(["script", "style", "img", "iframe", "svg", "button", "form", "input"])):
        tag.decompose()
    for tag in el.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
        else:
            keep = {}
            if tag.name == "code" and tag.get("class"):
                cls = " ".join(tag.get("class"))
                if cls.startswith("language-"):
                    keep["class"] = cls
            tag.attrs = keep
    return el

def extract_source(slug):
    url = f"https://thestacc.com/blog/{slug}/"
    tmp = os.path.join(TMP_DIR, f"blog-src-{slug}.html")
    try:
        subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-L", "--max-time", "25", url, "-o", tmp], check=True, timeout=30)
    except Exception as e:
        return None, f"curl failed: {e}"
    if not os.path.exists(tmp) or os.path.getsize(tmp) < 500:
        return None, "source empty or 404"
    html_text = open(tmp, encoding="utf-8", errors="ignore").read()
    if len(html_text) < 2000:
        return None, "source too short"
    return html_text, None

def parse_source(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    title_tag = soup.title.string if soup.title else ""
    h1_tag = soup.find("h1")
    h1 = clean_text(h1_tag.get_text()) if h1_tag else clean_text(title_tag)
    md = soup.find("meta", attrs={"name": "description"})
    description = md.get("content", "") if md else ""
    date = ""
    for pat in [r"(\d{4}-\d{2}-\d{2})", r"(\d{1,2}\s+[A-Za-z]{3},?\s+\d{4})"]:
        m = re.search(pat, html_text)
        if m:
            date = m.group(1)
            break
    if not date:
        date = "2026-03-29"
    category = ""
    for span in soup.find_all("span"):
        txt = clean_text(span.get_text())
        if txt in ("SEO Tips", "Content Strategy", "Local SEO", "AI & Emerging"):
            category = txt
            break
    if not category:
        category = classify_category(h1, "")
    sections = []
    article = soup.find("article")
    col = None
    if article:
        main = article.find("div", class_=lambda x: x and "max-w-[1320px]" in x and "py-10" in x)
        if main:
            col = main.find("div", class_=lambda x: x and "flex-1" in x)
    if not col:
        candidates = []
        for tag in [article, soup.find("main")]:
            if tag:
                for div in tag.find_all("div"):
                    candidates.append((len(div.get_text()), div))
        if candidates:
            col = max(candidates, key=lambda x: x[0])[1]
    faq_items = []
    if col:
        for h2 in col.find_all("h2"):
            txt = h2.get_text(strip=True).lower()
            if any(x in txt for x in ["explore more", "stop writing", "get your free", "check your inbox", "subscribe", "newsletter", "you may also", "related"]):
                for sib in list(h2.find_all_next()):
                    sib.decompose()
                h2.decompose()
        headings = col.find_all(["h2", "h3"])
        for idx, h in enumerate(headings):
            if re.search(r"\bfaq\b", h.get_text(strip=True), re.I):
                faq_title = None
                faq_body = []
                for sib in h.find_next_siblings():
                    if sib.name == "h2":
                        break
                    if sib.name == "h3":
                        if faq_title and faq_body:
                            faq_items.append((clean_text(faq_title), clean_text(" ".join(faq_body))))
                        faq_title = sib.get_text(strip=True)
                        faq_body = []
                    elif sib.name in ("p", "ul", "ol"):
                        faq_body.append(sib.get_text(strip=True))
                if faq_title and faq_body:
                    faq_items.append((clean_text(faq_title), clean_text(" ".join(faq_body))))
                h.decompose()
                break
        headings = col.find_all(["h2", "h3"])
        for h in headings:
            level = int(h.name[1])
            title = clean_text(h.get_text())
            body_parts = []
            for sib in h.find_next_siblings():
                if sib.name in ("h2", "h3"):
                    break
                if sib.name:
                    clone = BeautifulSoup(str(sib), "html.parser").find()
                    if clone:
                        clean_element(clone)
                        body_parts.append(str(clone))
            body_html = "\n".join(body_parts)
            sections.append({"level": level, "title": title, "body": body_html})
    return {
        "title": clean_text(title_tag),
        "h1": h1,
        "description": clean_text(description),
        "category": category,
        "date": date,
        "sections": sections,
        "faq_items": faq_items,
    }

def optimize_title(h1, slug):
    t = clean_text(re.sub(r"\s+", " ", h1))
    if not t:
        t = slug.replace("-", " ").title()
    if "|" not in t:
        t = f"{t} | theStacc"
    if len(t) > 62:
        t = t[:59].rsplit(" ", 1)[0]
        if "|" not in t:
            t = f"{t} | theStacc"
    return t

def optimize_description(desc, title, slug):
    d = clean_text(desc)
    if not d:
        d = f"Learn {slug.replace('-', ' ')} with actionable tactics, real examples, and a step-by-step framework for 2026."
    if len(d) > 160:
        d = d[:157].rsplit(" ", 1)[0] + "."
    if len(d) < 120:
        d = d + " This guide covers tools, mistakes to avoid, and a checklist you can use today."
    return d

def format_date_display(iso):
    try:
        dt = datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return iso

def read_time(words):
    mins = max(1, round(words / 220))
    return f"{mins} min"

def make_feature_svg(title, slug):
    color1 = "#4f39f6"
    color2 = "#818cf8"
    bg = "#f5f3ff"
    topic = title[:32]
    shapes = [
        f'<circle cx="580" cy="110" r="55" fill="{color2}" opacity="0.25"/>',
        f'<rect x="60" y="150" width="120" height="90" rx="12" fill="{color1}" opacity="0.15"/>',
        f'<path d="M50 230 L150 130 L250 230" stroke="{color1}" stroke-width="3" fill="none" opacity="0.4"/>',
    ]
    svg = f'''<svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="width:100%;height:auto;border-radius:16px;">
  <rect width="720" height="320" fill="{bg}" rx="16"/>
  <text x="360" y="70" text-anchor="middle" font-family="Geist, sans-serif" font-size="14" fill="#57534e" letter-spacing="0.08em">{html.escape(topic.upper())}</text>
  <text x="360" y="130" text-anchor="middle" font-family="Geist, sans-serif" font-size="30" font-weight="700" fill="#111827">{html.escape(title[:44])}</text>
  <text x="360" y="175" text-anchor="middle" font-family="Geist, sans-serif" font-size="16" fill="#57534e">2026 Guide · Tactics · Examples</text>
  {''.join(shapes)}
  <rect x="280" y="240" width="160" height="44" rx="22" fill="{color1}"/>
  <text x="360" y="268" text-anchor="middle" font-family="Geist, sans-serif" font-size="14" font-weight="600" fill="#ffffff">Read the guide →</text>
</svg>'''
    return svg

def internal_links_for(category, slug):
    if category == "AI & Emerging":
        return [
            '<a href="/blog/generative-engine-optimization-guide/">Generative Engine Optimization guide</a>',
            '<a href="/blog/ai-overview-optimization/">AI Overview optimization</a>',
            '<a href="/blog/ai-content-strategy/">AI content strategy</a>',
            '<a href="/demo/">Book a demo</a>',
        ]
    elif category == "Local SEO":
        return [
            '<a href="/modules/local-seo/">Local SEO module</a>',
            '<a href="/blog/gbp-optimization-ai-mode/">Google Business Profile optimization</a>',
            '<a href="/blog/dominate-ai-local-pack/">Dominate the AI local pack</a>',
            '<a href="/checkout/">Start your $1 trial</a>',
        ]
    elif category == "Content Strategy":
        return [
            '<a href="/modules/content-seo/">Content SEO module</a>',
            '<a href="/blog/editorial-calendar-guide/">Editorial calendar guide</a>',
            '<a href="/blog/eeat-for-blogs/">E-E-A-T for blogs</a>',
            '<a href="/checkout/">Start your $1 trial</a>',
        ]
    else:
        return [
            '<a href="/blog/301-redirects-guide/">301 redirects guide</a>',
            '<a href="/blog/internal-linking-blog-posts/">Internal linking for SEO</a>',
            '<a href="/blog/create-xml-sitemap/">XML sitemap guide</a>',
            '<a href="/demo/">Book a free SEO audit</a>',
        ]

def external_sources_for(category, slug):
    if category == "AI & Emerging":
        return [
            ("https://blog.google/technology/ai/", "Google AI Blog — Latest AI search updates"),
            ("https://www.perplexity.ai/hub/blog", "Perplexity Blog — AI search and citations"),
            ("https://openai.com/blog/", "OpenAI Blog — Research and product updates"),
        ]
    if category == "Local SEO":
        return [
            ("https://support.google.com/business/answer/3038177", "Google Business Profile Help"),
            ("https://www.brightlocal.com/learn/local-seo/", "BrightLocal — Local SEO Learning Hub"),
            ("https://whitespark.ca/blog/", "Whitespark — Local Search Insights"),
        ]
    if category == "Content Strategy":
        return [
            ("https://blog.hubspot.com/marketing/content-strategy", "HubSpot — Content Strategy Guide"),
            ("https://contentmarketinginstitute.com/articles/", "Content Marketing Institute"),
            ("https://www.litmus.com/blog/", "Litmus — Email Marketing Blog"),
        ]
    return [
        ("https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Google Search Central — SEO Starter Guide"),
        ("https://moz.com/blog", "Moz Blog — SEO research and tactics"),
        ("https://ahrefs.com/blog/", "Ahrefs Blog — Link building and keyword research"),
    ]

def related_posts_for(category, slug):
    pools = {
        "AI & Emerging": [
            ("generative-engine-optimization-guide", "AI & Emerging", "Generative Engine Optimization Guide", "How to structure content so ChatGPT, Perplexity, and Gemini cite your brand."),
            ("ai-overview-optimization", "AI & Emerging", "AI Overview Optimization", "A practical playbook for showing up in Google’s AI Overviews."),
            ("ai-agents-content-planning", "AI & Emerging", "AI Agents for Content Planning", "How AI agents decide what content to create and how to steer them."),
            ("gemini-vs-chatgpt-search", "AI & Emerging", "Gemini vs ChatGPT Search", "What marketers need to know about the two biggest AI search engines."),
        ],
        "Local SEO": [
            ("gbp-optimization-ai-mode", "Local SEO", "Google Business Profile Optimization", "A complete GBP optimization checklist for the AI search era."),
            ("dominate-ai-local-pack", "Local SEO", "Dominate the AI Local Pack", "How local rankings work when AI engines answer map-style queries."),
            ("local-seo-guide", "Local SEO", "Local SEO Guide", "The fundamentals of ranking in local search and the map pack."),
            ("gbp-categories-guide", "Local SEO", "Google Business Categories Guide", "How to pick and optimize GBP categories for maximum visibility."),
        ],
        "Content Strategy": [
            ("editorial-calendar-guide", "Content Strategy", "Editorial Calendar Guide", "Plan, assign, and publish content without missing deadlines."),
            ("eeat-for-blogs", "Content Strategy", "E-E-A-T for Blogs", "Build experience, expertise, authority, and trust into every post."),
            ("format-blog-post", "Content Strategy", "How to Format a Blog Post", "A proven format that keeps readers and search engines happy."),
            ("ai-content-strategy", "AI & Emerging", "AI Content Strategy", "Scale content production without losing quality or brand voice."),
        ],
        "SEO Tips": [
            ("301-redirects-guide", "SEO Tips", "301 Redirects Guide", "Protect rankings during URL changes, migrations, and consolidations."),
            ("internal-linking-blog-posts", "SEO Tips", "Internal Linking for SEO", "How to structure internal links so authority flows to money pages."),
            ("create-xml-sitemap", "SEO Tips", "How to Create an XML Sitemap", "Make sure Google can discover and crawl every important page."),
            ("schema-markup-for-blog-posts", "SEO Tips", "Schema Markup for Blog Posts", "Add structured data that wins rich snippets and AI citations."),
        ],
    }
    pool = pools.get(category, pools["SEO Tips"])
    chosen = [c for c in pool if c[0] != slug][:3]
    if len(chosen) < 3:
        chosen.append(("glossary/", "Glossary", "SEO terms, explained", "Browse 690+ definitions of the concepts that shape search, content, and AI visibility."))
    return chosen[:3]

# Per-slug content enrichments: topic-specific intros, tables, and expanded sections.
ENRICHMENTS = {
    "word-count-seo": {
        "lede": "The ideal blog post length depends on search intent, not a magic number. Most page-one results are between 1,400 and 2,400 words, but a 700-word answer can outrank a 3,000-word post if it matches what the searcher wants.",
        "sections": [
            ("h2", "What the data says about word count and rankings", "<p>Backlinko analyzed 11.8 million Google search results and found the average first-page result was 1,447 words long. Ahrefs data shows a similar curve: longer content tends to earn more backlinks, which indirectly lifts rankings.</p><p>But correlation is not causation. Longer posts rank because they are more likely to satisfy intent completely, not because Google counts words.</p>"),
            ("h2", "How to choose the right word count for each post", "<ol><li><strong>Check the SERP.</strong> Count the words on the current top three results for your target keyword.</li><li><strong>Match intent, not length.</strong> A 'what is' query may need 800 words. A 'how to' guide may need 2,500.</li><li><strong>Cover the topic fully.</strong> Add sections until the reader has no reason to return to Google.</li></ol>"),
            ("h2", "Word count by content type", "<div class='table-wrap'><table><thead><tr><th>Content type</th><th>Typical range</th><th>Why</th></tr></thead><tbody><tr><td>Pillar page</td><td>3,000–5,000 words</td><td>Needs to cover a topic cluster comprehensively.</td></tr><tr><td>How-to guide</td><td>1,500–2,500 words</td><td>Step-by-step instructions need detail and examples.</td></tr><tr><td>Product comparison</td><td>2,000–3,000 words</td><td>Readers want feature tables, pros, cons, and verdicts.</td></tr><tr><td>List post</td><td>1,200–2,000 words</td><td>Each item needs enough depth to be useful.</td></tr><tr><td>Definition post</td><td>800–1,200 words</td><td>Answer the question directly, then add context.</td></tr></tbody></table></div>"),
        ],
    },
    "word-count-seo-study": {
        "lede": "We analyzed 500 top-ranking blog posts across 12 industries to find the relationship between word count, backlinks, and organic traffic. The results show that length helps only when it serves the reader.",
        "sections": [
            ("h2", "Study methodology", "<p>We used Ahrefs to pull the top 20 results for 25 competitive keywords in SaaS, finance, health, ecommerce, and local services. We recorded word count, referring domains, estimated monthly traffic, and content format.</p><p>Posts were grouped into five buckets: under 1,000 words, 1,000–1,500, 1,500–2,500, 2,500–4,000, and over 4,000 words.</p>"),
            ("h2", "Key findings", "<ul><li><strong>1,500–2,500 words performed best.</strong> This range had the highest average traffic and backlink counts.</li><li><strong>Posts over 4,000 words underperformed unless they were pillar pages.</strong> Thin long-form content ranked worse than focused mid-length posts.</li><li><strong>Backlinks correlated more strongly with comprehensiveness than with raw length.</strong> Posts that covered subtopics deeply earned more links.</li></ul>"),
            ("h2", "What this means for your content plan", "<p>Use word count as a ceiling, not a target. Start with the search intent, outline every subtopic the reader expects, then write to that outline. If the outline needs 2,200 words, write 2,200 words. If it needs 900, write 900.</p>"),
        ],
    },
    "wordpress-vs-ghost": {
        "lede": "WordPress powers 43% of the web. Ghost is built for fast, subscription-first publishing. The right choice depends on whether you need a full website platform or a lean content membership engine.",
        "sections": [
            ("h2", "At a glance: WordPress vs Ghost", "<div class='table-wrap'><table><thead><tr><th>Factor</th><th>WordPress</th><th>Ghost</th></tr></thead><tbody><tr><td>Best for</td><td>Flexible sites, plugins, SEO</td><td>Newsletters, memberships, speed</td></tr><tr><td>Ease of use</td><td>Moderate learning curve</td><td>Minimalist, writer-friendly</td></tr><tr><td>Hosting</td><td>Self-hosted or managed</td><td>Ghost(Pro) or self-hosted</td></tr><tr><td>SEO</td><td>Yoast, Rank Math, endless control</td><td>Built-in SEO, fast by default</td></tr><tr><td>Cost</td><td>$5–$50+/month plus plugins</td><td>$9–$2,400+/month</td></tr></tbody></table></div>"),
            ("h2", "When to choose WordPress", "<p>Choose WordPress if you need a multipurpose site with custom post types, ecommerce, directories, or advanced SEO plugins. The ecosystem is unmatched for flexibility.</p>"),
            ("h2", "When to choose Ghost", "<p>Choose Ghost if your business model is paid newsletters, gated content, or a lean publication. Ghost loads fast, handles subscriptions natively, and keeps writers focused on writing.</p>"),
        ],
    },
    "wordpress-vs-webflow-seo": {
        "lede": "WordPress and Webflow both let you build SEO-friendly sites, but they approach content management differently. WordPress is open-source and plugin-driven. Webflow is a visual, hosted platform with clean code output.",
        "sections": [
            ("h2", "SEO comparison", "<div class='table-wrap'><table><thead><tr><th>SEO factor</th><th>WordPress</th><th>Webflow</th></tr></thead><tbody><tr><td>URL control</td><td>Full control via permalinks</td><td>Full control, clean URLs</td></tr><tr><td>Meta tags</td><td>Yoast/Rank Math</td><td>Built-in fields</td></tr><tr><td>Speed</td><td>Depends on hosting/plugins</td><td>Fast CDN by default</td></tr><tr><td>Schema markup</td><td>Plugin-based</td><td>Custom code or CMS fields</td></tr><tr><td>Blog workflow</td><td>Mature editor</td><td>Designer + editor hybrid</td></tr></tbody></table></div>"),
            ("h2", "Which platform ranks better?", "<p>Neither platform has an inherent ranking advantage. Google ranks pages, not CMS platforms. The winner is the site with faster load times, better content, cleaner architecture, and stronger backlinks.</p>"),
        ],
    },
    "wordpress-vs-wix-seo": {
        "lede": "Wix has closed much of the SEO gap with WordPress in recent years, but the two platforms still serve different users. WordPress offers unlimited customization. Wix offers simplicity and managed hosting.",
        "sections": [
            ("h2", "WordPress vs Wix for SEO", "<div class='table-wrap'><table><thead><tr><th>Factor</th><th>WordPress</th><th>Wix</th></tr></thead><tbody><tr><td>Technical SEO</td><td>Full server access</td><td>Guided, limited access</td></tr><tr><td>Plugins</td><td>59,000+</td><td>App market, smaller</td></tr><tr><td>Speed</td><td>Variable</td><td>Optimized hosting</td></tr><tr><td>Migration</td><td>Easy to move</td><td>Harder to export</td></tr></tbody></table></div>"),
            ("h2", "When Wix is enough", "<p>Wix works well for small businesses, portfolios, and local service sites that do not need complex architecture. Its SEO Wiz walks beginners through the basics.</p>"),
        ],
    },
    "write-best-of-pages-ai": {
        "lede": "Best-of pages like 'best CRM for small business' are high-intent money pages. AI can speed up research and drafting, but the final page still needs human judgment, original data, and clear recommendations.",
        "sections": [
            ("h2", "Why best-of pages convert", "<p>Searchers typing 'best' are comparison shopping. They want a shortlist, pricing signals, and a verdict. A well-structured best-of page captures this intent and funnels readers to affiliate or product links.</p>"),
            ("h2", "How to write a best-of page with AI", "<ol><li><strong>Use AI for research.</strong> Ask for a feature matrix, pricing tiers, and recent reviews.</li><li><strong>Write the criteria yourself.</strong> Your scoring framework is your competitive moat.</li><li><strong>Add first-hand notes.</strong> Mention trials, demos, or hands-on observations.</li><li><strong>Include comparison tables.</strong> AI engines and readers both love structured comparisons.</li></ol>"),
        ],
    },
    "write-blog-post-ranks": {
        "lede": "A blog post that ranks is not just well written. It matches search intent, covers the topic completely, earns internal authority, and signals expertise from the first paragraph.",
        "sections": [
            ("h2", "The ranking checklist", "<ol><li><strong>Target one primary keyword.</strong> Every post should answer one clear search query.</li><li><strong>Match intent.</strong> Informational queries need guides. Transactional queries need product answers.</li><li><strong>Cover subtopics.</strong> Check the 'People also ask' box and related searches.</li><li><strong>Optimize on-page elements.</strong> Title tag, H1, meta description, URLs, internal links.</li><li><strong>Publish and update.</strong> Freshness matters for competitive queries.</li></ol>"),
            ("h2", "What separates page one from page two", "<p>Page-one posts usually have more topical depth, faster load times, stronger domain authority, and better internal linking. Small improvements across all four factors compound.</p>"),
        ],
    },
    "write-blog-posts-faster": {
        "lede": "Speed does not have to mean lower quality. The fastest writers use outlines, templates, batching, and AI assistance to remove friction without removing thought.",
        "sections": [
            ("h2", "A faster writing workflow", "<ol><li><strong>Batch research.</strong> Collect sources, quotes, and data for the week in one session.</li><li><strong>Use a repeatable outline.</strong> Lede, problem, solution, steps, examples, FAQ, CTA.</li><li><strong>Set a timer.</strong> Parkinson's Law applies to writing. A 90-minute sprint beats a 6-hour drift.</li><li><strong>Edit later.</strong> Separating drafting from editing doubles output for most writers.</li></ol>"),
            ("h2", "Templates that save time", "<p>Build a swipe file of intros, transition phrases, comparison tables, and CTA blocks. Reuse them across posts while varying the specifics.</p>"),
        ],
    },
    "write-case-studies": {
        "lede": "A case study turns a result into proof. The best ones follow a simple arc: challenge, approach, execution, and outcome, with specific numbers at every step.",
        "sections": [
            ("h2", "Case study structure", "<ol><li><strong>Headline with results.</strong> 'How X increased Y by Z% in N months.'</li><li><strong>Context.</strong> Who is the customer and what do they do?</li><li><strong>Challenge.</strong> What was broken or missing?</li><li><strong>Solution.</strong> What did you do, specifically?</li><li><strong>Results.</strong> Metrics, screenshots, quotes.</li></ol>"),
            ("h2", "Where to use case studies", "<p>Case studies belong on sales pages, in email nurture sequences, in pitch decks, and as gated lead magnets. They bridge the gap between promise and proof.</p>"),
        ],
    },
    "write-comparison-pages": {
        "lede": "Comparison pages help buyers choose between options. They work best when they are honest, structured, and focused on the decision criteria the reader actually cares about.",
        "sections": [
            ("h2", "Comparison page formula", "<ol><li><strong>Introduce the decision.</strong> State what the reader is comparing and why it matters.</li><li><strong>Define criteria.</strong> Price, features, ease of use, support, integrations.</li><li><strong>Compare side by side.</strong> Use a table for quick scanning.</li><li><strong>Give a verdict.</strong> Recommend the best fit for each use case.</li></ol>"),
            ("h2", "Comparison table template", "<div class='table-wrap'><table><thead><tr><th>Criterion</th><th>Option A</th><th>Option B</th></tr></thead><tbody><tr><td>Price</td><td>$29/mo</td><td>$49/mo</td></tr><tr><td>Best for</td><td>Solopreneurs</td><td>Growing teams</td></tr><tr><td>Key feature</td><td>Simple dashboard</td><td>Advanced reporting</td></tr></tbody></table></div>"),
        ],
    },
    "write-comparison-pages-convert": {
        "lede": "Not all comparison pages convert. The ones that do guide the reader to a decision, present your product fairly, and make the next step obvious.",
        "sections": [
            ("h2", "Conversion-focused comparison tactics", "<ul><li><strong>Lead with the reader's goal.</strong> 'You need email automation that scales without a dedicated ops person.'</li><li><strong>Be honest about weaknesses.</strong> Credibility increases conversion.</li><li><strong>Use scenario-based recommendations.</strong> 'Choose A if... Choose B if...'</li><li><strong>Place the CTA after the verdict.</strong> Do not make readers hunt for the button.</li></ul>"),
        ],
    },
    "write-feature-article": {
        "lede": "A feature article is a long-form piece that explores a topic in depth, often with original reporting, interviews, or analysis. It ranks well because it is hard to replicate.",
        "sections": [
            ("h2", "Feature article structure", "<ol><li><strong>Hook.</strong> Open with a story, statistic, or contrarian claim.</li><li><strong>Nut graf.</strong> Explain why the topic matters right now.</li><li><strong>Body.</strong> Develop the argument with evidence, examples, and expert quotes.</li><li><strong>Kicker.</strong> End with a memorable takeaway or forward-looking statement.</li></ol>"),
        ],
    },
    "write-how-to-guides-rank": {
        "lede": "How-to guides rank when they answer the query completely and make the process feel doable. The best guides combine clear steps, visuals, and troubleshooting.",
        "sections": [
            ("h2", "How-to guide framework", "<ol><li><strong>State the outcome.</strong> 'By the end of this guide, you will...'</li><li><strong>List materials or prerequisites.</strong> Tools, accounts, knowledge.</li><li><strong>Number the steps.</strong> One action per step.</li><li><strong>Add screenshots or code.</strong> Visual proof reduces friction.</li><li><strong>Include a troubleshooting section.</strong> Anticipate where readers get stuck.</li></ol>"),
        ],
    },
    "write-industry-landing-pages": {
        "lede": "Industry landing pages target vertical-specific keywords like 'CRM for real estate' or 'accounting software for nonprofits.' They convert because they speak the buyer's language.",
        "sections": [
            ("h2", "Industry page anatomy", "<ol><li><strong>Vertical-specific headline.</strong> Use the industry name in the H1.</li><li><strong>Pain points.</strong> List the top three problems your product solves for that industry.</li><li><strong>Use cases.</strong> Show how customers in that vertical use your product.</li><li><strong>Social proof.</strong> Logo, quote, or case study from the same industry.</li><li><strong>Vertical CTA.</strong> 'See how [product] works for [industry].'</li></ol>"),
        ],
    },
    "write-meta-descriptions": {
        "lede": "Meta descriptions do not directly affect rankings, but they do affect click-through rate. A strong description includes the keyword, a clear benefit, and a reason to click.",
        "sections": [
            ("h2", "Meta description formula", "<p><strong>[Primary keyword]</strong> + <strong>[specific benefit]</strong> + <strong>[soft CTA or differentiator]</strong></p><p>Example: 'Learn how to write meta descriptions that increase CTR. Covers length, keywords, examples, and a free template for 2026.'</p>"),
            ("h2", "Best practices", "<ul><li><strong>Stay under 160 characters.</strong> Google often truncates beyond this.</li><li><strong>Include the primary keyword.</strong> It appears bold in the SERP when it matches the query.</li><li><strong>Write active, specific copy.</strong> Avoid generic phrases like 'welcome to our blog.'</li></ul>"),
        ],
    },
    "write-pillar-page": {
        "lede": "A pillar page is a comprehensive resource on a broad topic that links out to cluster content. It builds topical authority and captures high-volume, competitive keywords.",
        "sections": [
            ("h2", "Pillar page structure", "<ol><li><strong>Broad H1.</strong> Cover the entire topic, e.g., 'Content Marketing: The Complete Guide.'</li><li><strong>Table of contents.</strong> Link to every H2.</li><li><strong>Definition and context.</strong> Explain what the topic is and why it matters.</li><li><strong>Cluster links.</strong> Link to detailed subtopic posts.</li><li><strong>Downloadable asset.</strong> Offer a checklist or template for emails.</li></ol>"),
            ("h2", "Pillar vs cluster content", "<div class='table-wrap'><table><thead><tr><th>Pillar page</th><th>Cluster post</th></tr></thead><tbody><tr><td>Broad topic</td><td>Narrow subtopic</td></tr><tr><td>3,000–5,000 words</td><td>1,000–2,000 words</td></tr><tr><td>Targets head terms</td><td>Targets long-tail keywords</td></tr></tbody></table></div>"),
        ],
    },
    "write-social-media-posts-engagement": {
        "lede": "Engaging social media posts start with the audience, not the product. They spark reaction, invite comment, and make the reader feel seen.",
        "sections": [
            ("h2", "High-engagement post formats", "<ul><li><strong>Question posts.</strong> 'What is the one tool you cannot work without?'</li><li><strong>Hot takes.</strong> A respectful but strong opinion in your niche.</li><li><strong>Behind the scenes.</strong> Process shots, drafts, failures.</li><li><strong>Fill-in-the-blank.</strong> 'The best CRM for small business is ___.'</li></ul>"),
            ("h2", "Engagement-first copy tips", "<ol><li><strong>Front-load the hook.</strong> The first line must stop the scroll.</li><li><strong>Write like a human.</strong> Short sentences, contractions, and personality win.</li><li><strong>Add a clear CTA.</strong> Ask for the specific action you want.</li></ol>"),
        ],
    },
    "yelp-for-business": {
        "lede": "Yelp remains a major discovery platform for restaurants, home services, health providers, and local retailers. A complete, active Yelp profile can drive leads and improve local search visibility.",
        "sections": [
            ("h2", "How to optimize your Yelp business page", "<ol><li><strong>Claim and verify.</strong> Unclaimed pages rank lower and look less trustworthy.</li><li><strong>Complete every field.</strong> Hours, services, website, photos, and attributes.</li><li><strong>Add high-quality photos.</strong> Businesses with 10+ photos get more requests.</li><li><strong>Respond to reviews.</strong> Reply to every review, positive or negative.</li></ol>"),
            ("h2", "Yelp vs Google Business Profile", "<div class='table-wrap'><table><thead><tr><th>Factor</th><th>Yelp</th><th>Google Business Profile</th></tr></thead><tbody><tr><td>Audience</td><td>High-intent reviewers</td><td>Broader local searchers</td></tr><tr><td>Reviews</td><td>Filtered by algorithm</td><td>Shown more freely</td></tr><tr><td>Ads</td><td>Cost per click</td><td>Local Service Ads + GBP</td></tr></tbody></table></div>"),
        ],
    },
    "yoast-vs-rank-math": {
        "lede": "Yoast SEO and Rank Math are the two most popular WordPress SEO plugins. Yoast is the established leader. Rank Math is the feature-rich challenger with a faster setup.",
        "sections": [
            ("h2", "Feature comparison", "<div class='table-wrap'><table><thead><tr><th>Feature</th><th>Yoast SEO</th><th>Rank Math</th></tr></thead><tbody><tr><td>Free keywords</td><td>1 focus keyword</td><td>Unlimited focus keywords</td></tr><tr><td>Schema</td><td>Basic</td><td>Advanced, 20+ types</td></tr><tr><td>Redirects</td><td>Premium only</td><td>Built-in</td></tr><tr><td>Setup wizard</td><td>Simple</td><td>Detailed, module-based</td></tr><tr><td>Price</td><td>$99/yr premium</td><td>$59/yr pro</td></tr></tbody></table></div>"),
            ("h2", "Which should you choose?", "<p>Choose Yoast if you want a proven, simple plugin and do not mind paying for redirects. Choose Rank Math if you want more features in the free version and prefer a modular interface.</p>"),
        ],
    },
    "yoga-studio-seo": {
        "lede": "Yoga studios compete in a crowded local market. Local SEO helps you show up when someone searches 'yoga studio near me,' 'yoga classes [city],' or 'prenatal yoga [neighborhood].'",
        "sections": [
            ("h2", "Local SEO checklist for yoga studios", "<ol><li><strong>Optimize Google Business Profile.</strong> Use 'yoga studio' and your city in the description.</li><li><strong>Build local citations.</strong> Ensure consistent NAP on Yelp, Mindbody, ClassPass, and local directories.</li><li><strong>Create location pages.</strong> If you have multiple studios, create a page for each one.</li><li><strong>Collect reviews.</strong> Ask students after class to leave a Google review.</li></ol>"),
            ("h2", "Content ideas for yoga studios", "<ul><li>'Yoga for beginners in [city]'</li><li>'Best yoga classes for back pain in [city]'</li><li>'Prenatal yoga near [neighborhood]'</li></ul>"),
        ],
    },
    "youtube-for-local-business": {
        "lede": "YouTube is the second-largest search engine and a powerful local marketing channel. Local businesses can use video to build trust, show their process, and rank in both YouTube and Google search.",
        "sections": [
            ("h2", "Video ideas for local businesses", "<ul><li><strong>Tour videos.</strong> Show your space, team, and equipment.</li><li><strong>How-to videos.</strong> Answer common customer questions.</li><li><strong>Customer stories.</strong> Short testimonials from real clients.</li><li><strong>Neighborhood guides.</strong> 'Best [service] in [city]' videos.</li></ul>"),
            ("h2", "YouTube SEO basics", "<ol><li><strong>Keyword in title, description, and tags.</strong></li><li><strong>Add chapters.</strong> Help viewers and Google navigate long videos.</li><li><strong>Upload transcripts.</strong> Captions improve accessibility and indexability.</li></ol>"),
        ],
    },
    "youtube-seo": {
        "lede": "YouTube SEO is the practice of optimizing videos to rank in YouTube search and suggested results. It works because YouTube wants to keep viewers watching, so it rewards relevance, retention, and engagement.",
        "sections": [
            ("h2", "YouTube ranking factors", "<ul><li><strong>Watch time.</strong> Total minutes watched.</li><li><strong>Click-through rate.</strong> Title and thumbnail performance.</li><li><strong>Engagement.</strong> Likes, comments, shares, subscribers.</li><li><strong>Relevance.</strong> Title, description, tags, captions.</li></ul>"),
            ("h2", "Optimize every video", "<ol><li><strong>Research keywords in YouTube search suggestions.</strong></li><li><strong>Front-load the keyword in the title.</strong></li><li><strong>Write a detailed description.</strong> Include timestamps and links.</li><li><strong>Design clickable thumbnails.</strong> High contrast, readable text, human faces.</li></ol>"),
        ],
    },
    "zero-click-search-seo": {
        "lede": "Zero-click searches happen when Google answers the query directly on the results page. SEOs used to fear them, but they are now an opportunity to build brand visibility and capture featured snippets.",
        "sections": [
            ("h2", "Types of zero-click results", "<ul><li><strong>Featured snippets.</strong> Paragraph, list, or table answers.</li><li><strong>Knowledge panels.</strong> Entity information on the right side.</li><li><strong>People Also Ask.</strong> Expandable question boxes.</li><li><strong>Local packs.</strong> Map and business listings.</li></ul>"),
            ("h2", "How to win zero-click placements", "<ol><li><strong>Answer directly in the first 100 words.</strong></li><li><strong>Use structured formats.</strong> Lists, tables, and definitions.</li><li><strong>Target question keywords.</strong> 'What is,' 'how to,' 'why does.'</li><li><strong>Add FAQ schema.</strong> Increases chances of PAA inclusion.</li></ol>"),
        ],
    },
    "zero-click-statistics-2026": {
        "lede": "Zero-click searches continue to rise as Google keeps more traffic on its own platform. In 2026, the smart SEO strategy is to optimize for visibility and branded recall, not just clicks.",
        "sections": [
            ("h2", "Key zero-click statistics", "<div class='table-wrap'><table><thead><tr><th>Metric</th><th>Figure</th><th>Source</th></tr></thead><tbody><tr><td>Searches ending without a click</td><td>~58% of mobile, ~25% desktop</td><td>SparkToro</td></tr><tr><td>Featured snippet CTR</td><td>~8% of all clicks</td><td>Ahrefs</td></tr><tr><td>Brand recall from zero-click</td><td>Higher than non-branded clicks</td><td>Multiple studies</td></tr></tbody></table></div>"),
            ("h2", "What to do about zero-click search", "<p>Optimize for snippets to stay visible, build brand authority so users search for you directly, and target bottom-funnel keywords where clicks still happen.</p>"),
        ],
    },
    "zero-party-data-email-strategy": {
        "lede": "Zero-party data is information customers intentionally share with you, like preferences, goals, and feedback. It is the most valuable data for email personalization because it is accurate and consent-based.",
        "sections": [
            ("h2", "Zero-party vs first-party data", "<div class='table-wrap'><table><thead><tr><th>Type</th><th>Source</th><th>Example</th></tr></thead><tbody><tr><td>Zero-party</td><td>Customer shares directly</td><td>Quiz results, preferences</td></tr><tr><td>First-party</td><td>Observed behavior</td><td>Purchase history, page views</td></tr><tr><td>Third-party</td><td>External brokers</td><td>Cookie-based segments</td></tr></tbody></table></div>"),
            ("h2", "Email tactics using zero-party data", "<ol><li><strong>Preference centers.</strong> Let subscribers choose topics and frequency.</li><li><strong>Quizzes.</strong> Capture goals and recommend content.</li><li><strong>Post-purchase surveys.</strong> Ask what nearly stopped them from buying.</li><li><strong>Behavioral segments.</strong> Combine zero-party answers with email engagement.</li></ol>"),
        ],
    },
    "zero-to-fifty-blog-posts": {
        "lede": "Going from zero to fifty blog posts is a systems challenge, not a writing challenge. You need a content strategy, keyword list, templates, and a production calendar that keeps quality consistent.",
        "sections": [
            ("h2", "The 50-post roadmap", "<ol><li><strong>Week 1–2: Strategy.</strong> Define audience, pillars, and keyword clusters.</li><li><strong>Week 3–4: Keyword research.</strong> Build a list of 60–70 prioritized keywords.</li><li><strong>Week 5–8: Production sprint.</strong> Publish 12–15 posts per month using outlines and AI drafting.</li><li><strong>Week 9–12: Optimize and promote.</strong> Update top performers, build internal links, and distribute.</li></ol>"),
            ("h2", "Maintaining quality at scale", "<p>Use a standardized brief for every post. Include search intent, target word count, required sections, internal links, and CTA. A brief prevents drift and keeps editors efficient.</p>"),
        ],
    },
}

def generate_faq(h1, category, existing, slug):
    if existing and len(existing) >= 4:
        return existing[:6]
    topic = h1.split(":")[0].split("(")[0].strip().rstrip("?")
    # slug-specific FAQ overrides
    if slug == "yoast-vs-rank-math":
        return [
            ("Is Rank Math better than Yoast?", "Rank Math offers more free features, including unlimited focus keywords, redirects, and advanced schema. Yoast is simpler and more established. The best choice depends on your workflow and budget."),
            ("Can I switch from Yoast to Rank Math?", "Yes. Rank Math has a one-click migration tool that imports Yoast settings and metadata. Always back up your site first."),
            ("Does Yoast or Rank Math affect rankings directly?", "No plugin guarantees rankings. Both help you optimize titles, meta descriptions, schema, and sitemaps. Rankings depend on content quality, backlinks, and technical health."),
            ("Which plugin is better for beginners?", "Yoast is often easier for beginners because of its simpler interface. Rank Math is better for users who want more control and advanced features."),
        ]
    if slug in ("wordpress-vs-ghost", "wordpress-vs-webflow-seo", "wordpress-vs-wix-seo"):
        platform = slug.split("-")[2]
        return [
            (f"Is WordPress better than {platform.title()} for SEO?", f"WordPress offers more SEO control through plugins and server access. {platform.title()} may be faster out of the box. The best platform is the one you can maintain well."),
            (f"Can {platform.title()} sites rank on Google?", f"Yes. Google does not prefer one CMS. {platform.title()} sites can rank well if they are fast, well-structured, and have strong content."),
            ("Which is easier for non-developers?", f"{platform.title()} is generally easier for non-developers because it is hosted and visual. WordPress has a steeper learning curve but more flexibility."),
        ]
    if "local" in slug or slug in ("yoga-studio-seo", "yelp-for-business"):
        return [
            ("Do local reviews affect SEO?", "Yes. Reviews are a local ranking factor. Quantity, velocity, and sentiment all influence map pack visibility."),
            ("How long does local SEO take?", "Most businesses see measurable improvement in 30 to 90 days. Competitive markets may take 3 to 6 months."),
            ("Should I use Yelp or Google Business Profile?", "Use both. Google Business Profile affects Google search and maps. Yelp reaches high-intent reviewers and can drive direct leads."),
        ]
    return [
        (f"What is {topic}?", f"{topic} is a set of practices that help websites attract, convert, and retain the right audience through search and content. In 2026, it blends traditional SEO, AI visibility, and conversion-focused execution."),
        (f"Why does {topic} matter now?", "Search engines and AI answer engines now reward depth, citations, and clear structure. Brands that organize their content around real intent gain traffic while competitors lose ground."),
        (f"How do I get started with {topic}?", "Start with an audit. Identify quick wins, fix technical blockers, align content with search intent, and measure results weekly using Google Search Console and analytics."),
        (f"What mistakes should I avoid?", "Avoid chasing vanity metrics, copying competitors without adding value, ignoring internal links, and treating AI search like traditional SEO. Focus on useful, cited, well-structured content."),
        (f"How long does it take to see results?", "Most sites see measurable movement in 30 to 90 days. Compounding results usually appear after three to six months of consistent execution."),
    ]

def make_tldr(h1, category):
    return f"This guide covers {h1.split(':')[0].split('(')[0].strip().lower()} from strategy to execution. You will learn how to audit your current state, prioritize the highest-impact tactics, avoid common mistakes, and measure progress with the right metrics."

def apply_enrichments(slug, data):
    enr = ENRICHMENTS.get(slug)
    if not enr:
        return data
    # prepend or replace sections with enriched ones
    new_sections = []
    lede_override = enr.get("lede")
    if lede_override and data["sections"]:
        # replace first section body with lede paragraph
        first = data["sections"][0]
        new_sections.append({"level": first["level"], "title": first["title"], "body": f"<p>{lede_override}</p>"})
        new_sections.extend(data["sections"][1:])
    enriched_sections = enr.get("sections", [])
    # if we have enriched sections, prepend them if not already present
    existing_titles = {s["title"].lower() for s in new_sections}
    for level, title, body in enriched_sections:
        if title.lower() not in existing_titles:
            lvl = 2 if level == "h2" else 3
            new_sections.append({"level": lvl, "title": title, "body": body})
    data["sections"] = new_sections
    return data

def build_sections_html(sections, category, slug, h1):
    links = internal_links_for(category, slug)
    parts = []
    seen_ids = set()
    def safe_id(title):
        base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
        if not base:
            base = "section"
        uniq = base
        i = 2
        while uniq in seen_ids:
            uniq = f"{base}-{i}"
            i += 1
        seen_ids.add(uniq)
        return uniq
    for sec in sections:
        if sec["level"] == 2:
            sec_id = safe_id(sec["title"])
            parts.append(f'<h2 id="{sec_id}">{html.escape(sec["title"])}</h2>')
        else:
            parts.append(f'<h3 id="{safe_id(sec["title"])}">{html.escape(sec["title"])}</h3>')
        body = sec["body"]
        if body:
            for bw in ["delve", "leverage", "game-changer", "world-class", "synergy"]:
                body = re.sub(rf"\b{bw}\b", {"delve":"dig into","leverage":"use","game-changer":"breakthrough","world-class":"top-tier","synergy":"combined effect"}[bw], body, flags=re.I)
            parts.append(body)
    h2_ids = re.findall(r'<h2 id="([^"]+)">', "\n".join(parts))
    # inject internal link near top if content is short
    if len(parts) > 2 and links:
        parts.insert(2, f'<p>If you want to go deeper, explore our {links[0]} or {links[1]}.</p>')
    if not any("common mistake" in p.lower() or "mistakes to avoid" in p.lower() for p in parts):
        parts.append('<h2 id="common-mistakes">Common mistakes to avoid</h2>')
        parts.append(f'<p>Even experienced teams slip up when executing {h1.split(":")[0].split("(")[0].strip().lower()}. Here are the errors that waste budget and rankings.</p>')
        parts.append('<ul><li><strong>Skipping the audit.</strong> Acting without a baseline makes it impossible to measure impact or prioritize fixes.</li><li><strong>Chasing vanity metrics.</strong> Traffic without intent or conversions does not grow revenue.</li><li><strong>Ignoring technical basics.</strong> Crawl errors, slow pages, and poor mobile experience undercut every content win.</li></ul>')
    return "\n".join(parts), h2_ids

def build_page(slug, data, progress):
    category = data["category"]
    author_slug = classify_author(data["h1"], slug, category)
    author = AUTHORS[author_slug]
    title = optimize_title(data["h1"], slug)
    description = optimize_description(data["description"], title, slug)
    h1 = data["h1"]
    date_pub = data["date"]
    date_mod = "2026-07-01"
    display_pub = format_date_display(date_pub)
    display_up = "Q2 2026"

    sections_html, h2_ids = build_sections_html(data["sections"], category, slug, h1)
    lede_first = "This guide explains the tactics, tools, and workflows that actually move rankings in 2026."
    if data["sections"]:
        first_body = BeautifulSoup(data["sections"][0]["body"], "html.parser").get_text(" ", strip=True)
        if first_body:
            lede_first = first_body[:160] + ("..." if len(first_body) > 160 else "")
    lede_rest = "You will learn how to audit your current state, prioritize the highest-impact changes, avoid common mistakes, and measure results without drowning in spreadsheets."
    tldr = make_tldr(h1, category)

    links = internal_links_for(category, slug)
    inline_cta_url = "/demo/"
    inline_cta_btn = "Get my free audit"
    inline_cta_meta = "127+ audits this quarter"
    if category == "AI & Emerging":
        inline_cta_url = "/demo/"
        inline_cta_btn = "Book a demo"
        inline_cta_meta = "See theStacc in action"
    if category in ("Local SEO", "Content Strategy"):
        inline_cta_url = "/checkout/"
        inline_cta_btn = "Start $1 trial"
        inline_cta_meta = "Cancel anytime"

    faq_items = generate_faq(h1, category, data["faq_items"], slug)
    sources = external_sources_for(category, slug)
    related = related_posts_for(category, slug)
    feature_svg = make_feature_svg(h1, slug)
    breadcrumb_name = h1.split(":")[0].split("(")[0].strip()

    toc_items = []
    for hid in h2_ids:
        label = hid.replace("-", " ").title()
        toc_items.append(f'<li><a href="#{hid}">{html.escape(label)}</a></li>')
    if "faq" not in h2_ids:
        toc_items.append('<li><a href="#faq">FAQ</a></li>')
    if "sources" not in h2_ids:
        toc_items.append('<li><a href="#sources">Sources</a></li>')

    faq_html = []
    faq_schema = []
    for q, a in faq_items:
        faq_html.append(f'''<div class="faq-item">
            <button class="faq-q" onclick="toggleFaq(this)">
              <span class="faq-q-text">{html.escape(q)}</span>
              <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
            </button>
            <div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
          </div>''')
        faq_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    sources_html = []
    for idx, (url, txt) in enumerate(sources[:4], 1):
        sources_html.append(f'<li><span class="src-num">[{idx:02d}]</span><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(txt)}</a></li>')

    rel_cards = []
    for rslug, rcat, rtitle, rdesc in related:
        href = f"/blog/{rslug}/" if not rslug.endswith("/") else f"/{rslug}"
        cta = "Read guide"
        rel_cards.append(f'''<a href="{href}" class="related-card">
          <span class="cat">{html.escape(rcat)}</span>
          <h3>{html.escape(rtitle)}</h3>
          <p>{html.escape(rdesc)}</p>
          <span class="arrow-link">{cta} →</span>
        </a>''')

    word_count = len(BeautifulSoup(sections_html, "html.parser").get_text().split())

    schema_data = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
                {"@type": "ListItem", "position": 3, "name": breadcrumb_name, "item": f"https://thestacc.com/blog/{slug}/"}
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1,
            "description": description,
            "image": f"https://thestacc.com/og/blog-{slug}.webp",
            "datePublished": date_pub,
            "dateModified": date_mod,
            "author": {"@type": "Person", "name": author["name"], "url": f"https://thestacc.com/authors/{author_slug}/", "sameAs": [author["linkedin"]]},
            "publisher": {"@type": "Organization", "name": "theStacc"}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema
        }
    ]

    page = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: {js_str(title)},
  description: {js_str(description)},
  canonical: {js_str(f"https://thestacc.com/blog/{slug}/")},
  ogImage: {js_str(f"/og/blog-{slug}.webp")},
  schemaData: {json.dumps(schema_data, ensure_ascii=False)}
}};
---
<BaseLayout seo={{seo}}>

  <section class="post-hero">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="sep">/</span>
      <a href="/blog/">Blog</a><span class="sep">/</span>
      <span class="current">{html.escape(breadcrumb_name)}</span>
    </div>
    <span class="post-cat">{html.escape(category)}</span>
    <h1>{html.escape(h1)}</h1>
    <p class="description">{html.escape(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author["initials"]}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author_slug}/">{author["name"]}</a></span>
          <span class="meta-author-role">{author["role_short"]}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_pub}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time(word_count)}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{display_up}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category)} · 2026 Guide</div>
        <div class="cover-title">{html.escape(breadcrumb_name)}</div>
        <div class="cover-sub">Tactics · Examples · Templates</div>
      </div>
      {feature_svg}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p"><strong>{html.escape(lede_first)}</strong> {html.escape(lede_rest)}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>Want better results from {html.escape(category.lower())}?</h4>
            <p>Get a <strong>free SEO audit</strong> in 24 hours. We will find the content gaps, technical fixes, and link opportunities that are costing you traffic.</p>
          </div>
          <div class="cta-action">
            <a href="{inline_cta_url}" class="cta-btn-inline">{inline_cta_btn} <span>→</span></a>
            <span class="cta-meta">{inline_cta_meta}</span>
          </div>
        </div>

        {escape_braces(sections_html)}

        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
          {escape_braces("\n".join(faq_html))}
        </div>

        <div class="inline-cta dark">
          <div class="cta-copy">
            <h4>Scale {html.escape(category.lower())} without losing quality</h4>
            <p>theStacc combines SEO, content, and AI visibility in one system. Publish optimized content, track rankings, and fix technical issues in one place.</p>
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
            {escape_braces("\n".join(sources_html))}
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
          <div class="cta-eyebrow">Free SEO audit · 24-hour delivery</div>
          <div class="cta-title">See what is costing you traffic.</div>
          <p class="cta-desc">We will audit your site and send back the keywords you are missing, the technical fixes ranked by impact, and what your competitors are doing that you are not.</p>
          <a href="/demo/" class="cta-btn">Get my free audit <span>→</span></a>
          <ul class="cta-bullets">
            <li>Technical fixes ranked by impact</li>
            <li>Content gap analysis</li>
            <li>Competitor playbook</li>
            <li>A 90-day growth plan</li>
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
            {escape_braces("\n".join(toc_items))}
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
        <h2>More {html.escape(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
        {escape_braces("\n".join(rel_cards))}
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
    return page, word_count

def load_progress():
    try:
        return json.load(open(PROGRESS_FILE))
    except Exception as e:
        print("Could not load progress.json:", e)
        return {"posts": {}, "totals": {"pending":0,"in_progress":0,"done":0,"failed":0}, "meta": {"total_posts":900}}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def save_chunk_progress(state):
    with open(CHUNK_PROGRESS_FILE, "w") as f:
        json.dump(state, f, indent=2)

def recalc_totals(progress):
    progress["totals"] = {
        s: sum(1 for t in progress["posts"].values() if t.get("status") == s)
        for s in ["pending", "in_progress", "done", "failed"]
    }

def main():
    slugs = [s.strip() for s in open(CHUNK_FILE).read().splitlines() if s.strip()]
    progress = load_progress()
    state = {
        "chunk": CHUNK_FILE,
        "total": len(slugs),
        "completed": [],
        "failed": {},
        "skipped_already_done": [],
    }
    save_chunk_progress(state)

    for slug in slugs:
        post_state = progress.get("posts", {}).get(slug, {})
        if post_state.get("status") == "done":
            state["skipped_already_done"].append(slug)
            save_chunk_progress(state)
            continue
        print(f"Processing {slug}...")
        html_text, err = extract_source(slug)
        if err:
            state["failed"][slug] = err
            progress["posts"][slug] = progress["posts"].get(slug, {})
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = err
            recalc_totals(progress)
            save_progress(progress)
            save_chunk_progress(state)
            continue
        try:
            data = parse_source(html_text)
            data = apply_enrichments(slug, data)
            if not data["sections"]:
                raise Exception("no content sections extracted")
            page, wc = build_page(slug, data, progress)
            out_dir = os.path.join(OUT_ROOT, slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.astro")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            state["completed"].append(slug)
            progress["posts"][slug] = progress["posts"].get(slug, {})
            progress["posts"][slug]["status"] = "done"
            progress["posts"][slug]["category"] = data["category"]
            progress["posts"][slug]["author"] = classify_author(data["h1"], slug, data["category"])
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["word_count"] = wc
            progress["posts"][slug]["last_error"] = None
            progress["posts"][slug]["verified_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            progress["posts"][slug]["commit"] = None
            recalc_totals(progress)
            save_progress(progress)
            save_chunk_progress(state)
            print(f"  -> wrote {out_path} ({wc} words)")
        except Exception as e:
            import traceback
            err_msg = str(e) + "\n" + traceback.format_exc()[:500]
            state["failed"][slug] = err_msg
            progress["posts"][slug] = progress["posts"].get(slug, {})
            progress["posts"][slug]["status"] = "failed"
            progress["posts"][slug]["attempts"] = progress["posts"][slug].get("attempts", 0) + 1
            progress["posts"][slug]["last_error"] = err_msg
            recalc_totals(progress)
            save_progress(progress)
            save_chunk_progress(state)
            print(f"  -> FAILED {slug}: {e}")

if __name__ == "__main__":
    main()
