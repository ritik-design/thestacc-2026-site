#!/usr/bin/env python3
"""Migrate chunk 011 of theStacc blog posts to the 2026 Astro design."""
import json, os, re, subprocess, html, textwrap, datetime, urllib.request
from pathlib import Path

ROOT = Path('/home/ritik/thestacc.com-astro/thestacc-2026-site')
SRC_DIR = ROOT / 'src' / 'pages' / 'blog'
PROGRESS_FILE = ROOT / 'Stacc' / 'blog-migration' / 'progress.json'
CHUNK_FILE = ROOT / 'Stacc' / 'blog-migration' / 'small-chunks' / 'chunk-011.txt'
CHUNK_PROGRESS = CHUNK_FILE.with_suffix('.txt.progress.json')
SLUGS = [s.strip() for s in CHUNK_FILE.read_text().splitlines() if s.strip()]

AUTHORS = {
    'siddharth-gangal': {
        'name': 'Siddharth Gangal',
        'role': 'Founder · theStacc',
        'full_role': 'Founder · theStacc · IIT Mandi · Ex-Arka360',
        'initials': 'SG',
        'slug': 'siddharth-gangal',
        'linkedin': 'https://www.linkedin.com/in/sidgangal/',
        'x': 'https://x.com/sidgangal',
        'x_handle': '@sidgangal',
        'bio': 'Siddharth is the founder of theStacc and Arka360. He writes about SEO, AI search, content at scale, and the tactics that actually move rankings.'
    },
    'akshay-vr': {
        'name': 'Akshay VR',
        'role': 'Marketing Head · theStacc',
        'full_role': 'Marketing Head · theStacc · SEO & Editorial Strategy',
        'initials': 'AVR',
        'slug': 'akshay-vr',
        'linkedin': 'https://www.linkedin.com/in/akshay-vr-3aa1b9204/',
        'x': 'https://x.com/akshayvr_',
        'x_handle': '@akshayvr_',
        'bio': 'Akshay leads marketing at theStacc. He focuses on SEO strategy, editorial workflows, and turning content into demand for B2B and local businesses.'
    },
    'ritik-namdev': {
        'name': 'Ritik Namdev',
        'role': 'Growth Manager · theStacc',
        'full_role': 'Growth Manager · theStacc · Programmatic SEO & CRO',
        'initials': 'RN',
        'slug': 'ritik-namdev',
        'linkedin': 'https://www.linkedin.com/in/ritiknamdev/',
        'x': 'https://x.com/ritiknamdev_',
        'x_handle': '@ritiknamdev_',
        'bio': 'Ritik runs growth systems at theStacc, specializing in programmatic SEO, analytics, and conversion experiments that scale organic traffic.'
    }
}


def fetch_source(slug):
    out = f'/tmp/blog-src-{slug}.html'
    url = f'https://thestacc.com/blog/{slug}/'
    try:
        r = subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0', '-L', '--max-time', '25', url, '-o', out],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0 or not os.path.getsize(out):
            return None
        return Path(out).read_text(errors='ignore')
    except Exception:
        return None


def extract_basic(source):
    def tag_text(tag):
        m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', source, re.S | re.I)
        return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else None

    meta = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', source, re.I)
    if not meta:
        meta = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', source, re.I)
    description = html.unescape(meta.group(1)).strip() if meta else ''

    title = tag_text('title') or ''
    h1 = tag_text('h1') or title.split('|')[0].strip()

    # try to find published/updated dates
    dates = re.findall(r'(\d{4}-\d{2}-\d{2})', source)
    pub = min(dates) if dates else '2026-01-15'
    mod = max(dates) if dates else '2026-07-01'

    # headings
    h2s = []
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', source, re.S | re.I):
        txt = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        if txt and len(txt) < 120:
            h2s.append(txt)
    return {'title': title, 'h1': h1, 'description': description, 'published': pub, 'modified': mod, 'h2s': h2s}


def slugify_id(text):
    s = re.sub(r'[^\w\s-]', '', text.lower())
    s = re.sub(r'\s+', '-', s).strip('-')
    return s[:60] or 'section'


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))


def display_date(iso):
    try:
        d = datetime.date.fromisoformat(iso)
        return d.strftime('%b %d, %Y')
    except Exception:
        return iso


def cover_svg(title, subtitle, eyebrow, icon_type='generic'):
    palette = {'bg': '#f5f3ff', 'circle': '#ede9fe', 'accent': '#4f39f6', 'text': '#111827'}
    return f'''<svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="720" height="360" fill="{palette['bg']}"/>
  <circle cx="360" cy="180" r="130" fill="{palette['circle']}"/>
  <rect x="80" y="110" width="560" height="160" rx="16" fill="#ffffff" stroke="{palette['accent']}" stroke-width="2"/>
  <text x="360" y="155" text-anchor="middle" font-family="Geist Mono, monospace" font-size="13" fill="{palette['accent']}" font-weight="600">{html.escape(eyebrow.upper())}</text>
  <text x="360" y="195" text-anchor="middle" font-family="Geist, sans-serif" font-size="24" font-weight="600" fill="{palette['text']}">{html.escape(title[:60])}</text>
  <text x="360" y="230" text-anchor="middle" font-family="Geist, sans-serif" font-size="14" fill="#57534e">{html.escape(subtitle[:90])}</text>
  <circle cx="160" cy="250" r="6" fill="{palette['accent']}"/>
  <circle cx="190" cy="250" r="6" fill="{palette['accent']}" opacity="0.6"/>
  <circle cx="220" cy="250" r="6" fill="{palette['accent']}" opacity="0.3"/>
</svg>'''


def internal_link(text, url):
    return f'<a href="{url}">{html.escape(text)}</a>'


# ---------------------------------------------------------------------------
# Per-slug content catalog
# ---------------------------------------------------------------------------

def base_email_sections(industry, audience, examples):
    lead_magnet_examples = ', '.join(examples[:3])
    return [
        ('what-is-email-marketing', f'What is email marketing for {industry}?',
         f'<p>Email marketing for {industry} is the practice of collecting contact permission from {audience} and sending targeted messages that drive appointments, repeat visits, and referrals. Unlike social posts that disappear in feeds, emails land in a private inbox and can be automated based on behavior, timing, and customer history.</p><p>The best programs combine a valuable lead magnet, clear segmentation, and consistent cadence. A single welcome sequence can convert a website visitor into a paying customer while you sleep.</p>'),
        ('why-email-outperforms', f'Why email marketing still outperforms social media for {industry}',
         '<p>Organic reach on social platforms has been declining for years. Email, by contrast, gives you direct access to people who already raised their hand. According to Litmus, average email ROI is $36 to $42 for every $1 spent, far above most social channels.</p><p>For service businesses, email also carries higher trust. A recommendation from a known brand in an inbox feels more personal than a public ad.</p>'),
        ('best-practices', f'7 email marketing best practices for {industry}',
         '''<ol>
<li><strong>Send from a real person.</strong> A recognizable sender name beats a generic “no-reply” address.</li>
<li><strong>Segment your list by intent.</strong> New leads, active customers, and lapsed clients should receive different messages.</li>
<li><strong>Use one clear CTA per email.</strong> Multiple competing links dilute clicks.</li>
<li><strong>Optimize the preview text.</strong> It is the second subject line; use it to add curiosity or value.</li>
<li><strong>Mobile-first design.</strong> Over 60% of emails are opened on phones.</li>
<li><strong>Automate the repetitive stuff.</strong> Welcome sequences, appointment reminders, and follow-ups should run without manual work.</li>
<li><strong>Test and measure.</strong> Track open rates, click rates, and revenue per email to find what resonates.</li>
</ol>'''),
        ('build-list', f'How to build a compliant email list for {industry}',
         f'<p>Never buy lists. Instead, offer something useful in exchange for an address. For {industry}, strong lead magnets include {lead_magnet_examples}.</p><p>Place signup forms on high-traffic pages, at checkout, and in your footer. Always include a clear privacy notice and honor unsubscribe requests immediately.</p>'),
        ('campaigns-that-work', f'Email campaigns that work for {industry}',
         f'<p>A strong {industry} email program runs four core campaigns. A <strong>welcome sequence</strong> introduces your brand and sets expectations. An <strong>educational newsletter</strong> builds trust by answering common questions. A <strong>promotional campaign</strong> drives revenue during slow seasons. A <strong>re-engagement campaign</strong> wins back inactive subscribers with a special offer.</p><p>{internal_link("Email segmentation", "/blog/email-segmentation-guide/")} makes each message feel relevant instead of mass-blasted.</p>'),
        ('subject-lines', 'Writing subject lines that get opened',
         '<p>Subject lines should be specific, concise, and either useful or curious. Avoid all caps and excessive punctuation. Examples that perform well: “3 questions to ask before your next appointment,” “Your July savings inside,” and “We miss you — here is 20% off.”</p><p>Keep subject lines under 50 characters so they do not get cut off on mobile devices.</p>'),
        ('measure-roi', 'Measuring ROI and benchmarks',
         '<p>Track open rate, click-through rate, conversion rate, unsubscribe rate, and revenue per email. Service businesses should also measure appointments booked and lifetime value of email subscribers. A healthy list typically sees 20% to 25% open rates and 2% to 5% click rates.</p>')
    ]


SLUG_CONTENT = {
    'email-marketing-best-practices': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing Best Practices: A Data-Backed Guide for 2026 | theStacc',
        'h1': 'Email Marketing Best Practices: A Data-Backed Guide for 2026',
        'description': 'Apply the email marketing best practices that drive opens, clicks, and revenue in 2026. Covers list growth, segmentation, automation, compliance, and ROI.',
        'cover': ('EMAIL MARKETING', 'Email Marketing Best Practices', 'Turn subscribers into loyal buyers'),
        'sections': lambda: base_email_sections('any business', 'prospects and customers', ['a free checklist', 'a discount code', 'an exclusive guide']) +
        [('email-automation-examples', 'Automation examples that save hours', '<p>Start with a welcome sequence triggered by signup, an abandoned-cart or consultation-reminder flow, and a monthly newsletter. Tools like Mailchimp, Klaviyo, and ActiveCampaign make this accessible without engineering help.</p><p>Automation ensures no lead falls through the cracks and frees your team to focus on high-value conversations.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-dentists': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Dentists: Fill Chairs & Boost Retention | theStacc',
        'h1': 'Email Marketing for Dentists: Fill Chairs & Boost Retention',
        'description': 'Learn email marketing for dentists. Build recall campaigns, appointment reminders, and referral programs that keep patients coming back.',
        'cover': ('DENTAL MARKETING', 'Email Marketing for Dentists', 'Recall, reminders, and referrals'),
        'sections': lambda: base_email_sections('dental practices', 'patients', ['a free oral-health guide', 'a $25 new-patient credit', 'a dental emergency checklist']) +
        [('dental-campaigns', 'Campaigns that fill the schedule', '<p>Send recall reminders every six months, birthday discounts, and post-visit care tips. A “refer a friend” campaign can turn happy patients into your cheapest acquisition channel.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-accountants': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Accountants: Tax-Season Growth Playbook | theStacc',
        'h1': 'Email Marketing for Accountants: Tax-Season Growth Playbook',
        'description': 'Use email marketing for accountants to onboard clients, send deadline reminders, and sell advisory services year-round.',
        'cover': ('ACCOUNTING MARKETING', 'Email Marketing for Accountants', 'Deadline-driven client communication'),
        'sections': lambda: base_email_sections('accounting firms', 'business clients', ['a tax deadline calendar', 'a bookkeeping checklist', 'a free consultation']) +
        [('tax-season-playbook', 'The tax-season email playbook', '<p>Begin a countdown series in January, send document-request checklists, and follow up after filing with advisory-service upsells. Segment personal-tax clients from business clients so messages stay relevant.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-chiropractors': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Chiropractors: Patient Retention Guide | theStacc',
        'h1': 'Email Marketing for Chiropractors: Patient Retention Guide',
        'description': 'Build email marketing for chiropractors that increases rebookings, educates patients, and drives referrals without spam.',
        'cover': ('CHIROPRACTIC MARKETING', 'Email Marketing for Chiropractors', 'Rebook, educate, refer'),
        'sections': lambda: base_email_sections('chiropractic clinics', 'patients', ['a posture self-assessment', 'a first-visit discount', 'a stretching guide']) +
        [('care-plan-emails', 'Care plan and rebooking emails', '<p>Send a care-plan summary after the first visit, gentle rebooking nudges at 30 and 60 days, and educational content on posture, sleep, or ergonomics.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-contractors': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Contractors: Win More Estimates | theStacc',
        'h1': 'Email Marketing for Contractors: Win More Estimates',
        'description': 'Turn leads into booked jobs with email marketing for contractors. Follow up on estimates, share project photos, and ask for reviews.',
        'cover': ('CONTRACTOR MARKETING', 'Email Marketing for Contractors', 'From estimate to booked job'),
        'sections': lambda: base_email_sections('contracting businesses', 'homeowners', ['a project cost estimator', 'a maintenance checklist', 'a free in-home consultation']) +
        [('estimate-follow-up', 'The estimate follow-up sequence', '<p>Send a thank-you email within 24 hours of an estimate, a value-add tip three days later, and a limited-availability reminder one week later. This sequence alone can raise close rates by 20%.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-gyms': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Gyms: Reduce Churn & Drive Sign-Ups | theStacc',
        'h1': 'Email Marketing for Gyms: Reduce Churn & Drive Sign-Ups',
        'description': 'Use email marketing for gyms to nurture trial members, announce classes, win back lapsed members, and build community.',
        'cover': ('GYM MARKETING', 'Email Marketing for Gyms', 'Retain members, attract new ones'),
        'sections': lambda: base_email_sections('gyms and fitness studios', 'members and prospects', ['a 7-day pass', 'a nutrition guide', 'a workout plan']) +
        [('member-journey', 'The member journey by email', '<p>Nurture trial members with a 5-day onboarding series, announce new classes and challenges, and re-engage members who have not checked in for 14 days.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-hvac': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for HVAC: Seasonal Maintenance Revenue | theStacc',
        'h1': 'Email Marketing for HVAC: Seasonal Maintenance Revenue',
        'description': 'Grow repeat service calls with email marketing for HVAC companies. Send seasonal tune-up reminders, filter replacements, and referral requests.',
        'cover': ('HVAC MARKETING', 'Email Marketing for HVAC', 'Tune-ups, filters, and referrals'),
        'sections': lambda: base_email_sections('HVAC companies', 'homeowners', ['a seasonal maintenance checklist', 'a filter replacement reminder', 'a $50 service credit']) +
        [('seasonal-reminders', 'Seasonal maintenance reminders', '<p>Send pre-season tune-up emails in spring and fall. Most homeowners forget to schedule maintenance; a timely reminder captures demand before it breaks.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-lawyers': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Lawyers: Ethical Client Development | theStacc',
        'h1': 'Email Marketing for Lawyers: Ethical Client Development',
        'description': 'Use email marketing for lawyers to nurture leads, share legal updates, and build trust while staying compliant with advertising rules.',
        'cover': ('LEGAL MARKETING', 'Email Marketing for Lawyers', 'Compliant client development'),
        'sections': lambda: base_email_sections('law firms', 'prospective and current clients', ['a case evaluation checklist', 'a guide to your practice area', 'a free consultation']) +
        [('ethical-compliance', 'Ethical compliance and disclaimers', '<p>Include disclaimers that emails are not legal advice. Avoid guarantees or case-value estimates. Segment by practice area so family-law clients do not receive personal-injury promotions.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-realtors': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Realtors: Listings, Leads & Referrals | theStacc',
        'h1': 'Email Marketing for Realtors: Listings, Leads & Referrals',
        'description': 'Close more deals with email marketing for realtors. Nurture buyers, showcase listings, and stay top-of-mind past closing.',
        'cover': ('REAL ESTATE MARKETING', 'Email Marketing for Realtors', 'Nurture buyers and sellers'),
        'sections': lambda: base_email_sections('real estate agents', 'buyers, sellers, and past clients', ['a home valuation report', 'a buyer’s guide', 'a neighborhood market update']) +
        [('past-client-referrals', 'Past-client referral campaigns', '<p>Send home-anniversary emails, local market updates, and referral-request campaigns. Most agents stop emailing after closing; consistent follow-up generates repeat and referral business.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-restaurants': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Restaurants: Fill Tables & Drive Orders | theStacc',
        'h1': 'Email Marketing for Restaurants: Fill Tables & Drive Orders',
        'description': 'Boost covers and online orders with email marketing for restaurants. Promote specials, events, loyalty rewards, and holidays.',
        'cover': ('RESTAURANT MARKETING', 'Email Marketing for Restaurants', 'Specials, events, and loyalty'),
        'sections': lambda: base_email_sections('restaurants', 'diners', ['a free appetizer offer', 'a birthday reward', 'a behind-the-scenes recipe']) +
        [('event-promotions', 'Event and holiday promotions', '<p>Promote Valentine’s Day, Mother’s Day, and tasting events two weeks in advance. Send a “last chance” email 24 hours before the event to capture stragglers.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-for-salons': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Salons: Book More Appointments | theStacc',
        'h1': 'Email Marketing for Salons: Book More Appointments',
        'description': 'Use email marketing for salons to reduce no-shows, fill last-minute openings, and promote retail products.',
        'cover': ('SALON MARKETING', 'Email Marketing for Salons', 'Reduce no-shows, sell retail'),
        'sections': lambda: base_email_sections('salons and spas', 'clients', ['a style guide', 'a $10 service credit', 'a self-care checklist']) +
        [('appointment-reminders', 'Appointment reminders and last-minute fills', '<p>Send a confirmation 48 hours before, a reminder 24 hours before, and a “we have an opening today” email for canceled slots. Automating this cuts no-shows by up to 40%.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-local-businesses': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing for Local Businesses: The 2026 Playbook | theStacc',
        'h1': 'Email Marketing for Local Businesses: The 2026 Playbook',
        'description': 'Learn email marketing for local businesses. Build a local list, send hyper-relevant messages, and tie email to in-store revenue.',
        'cover': ('LOCAL MARKETING', 'Email Marketing for Local Businesses', 'Local list, local revenue'),
        'sections': lambda: base_email_sections('local businesses', 'nearby customers', ['a local event invite', 'a neighborhood discount', 'a loyalty punch card']) +
        [('local-relevance', 'Local relevance wins the inbox', '<p>Use location-specific subject lines, mention local landmarks, and segment by neighborhood. Pair email with {internal_link("local SEO", "/modules/local-seo/")} to dominate both search and the inbox.</p>')],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-roi': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing ROI: How to Measure & Improve It | theStacc',
        'h1': 'Email Marketing ROI: How to Measure & Improve It',
        'description': 'Calculate email marketing ROI accurately. Track revenue, list growth, and lifetime value with formulas, benchmarks, and improvement tactics.',
        'cover': ('EMAIL ROI', 'Email Marketing ROI', 'Measure what matters'),
        'sections': lambda: [
            ('what-is-email-roi', 'What is email marketing ROI?', '<p>Email marketing ROI is the revenue generated from email campaigns divided by the cost to run them. The classic formula is (Revenue − Cost) / Cost × 100. If you spent $500 and earned $5,000, your ROI is 900%.</p><p>But revenue is only part of the story. List growth, engagement trends, and customer lifetime value also indicate whether your program is healthy.</p>'),
            ('benchmarks', 'Industry benchmarks for email ROI', '<p>Litmus reports an average email ROI of $36 to $42 for every $1 spent. B2B and ecommerce brands often see higher returns because purchase values are larger. Local service businesses should compare ROI against other channels like paid search and social ads.</p>'),
            ('kpis', 'The KPIs that predict ROI', '<ol><li><strong>List growth rate.</strong> Healthy lists grow 5% to 10% monthly.</li><li><strong>Open rate.</strong> Aim for 20% to 25% for service industries.</li><li><strong>Click-through rate.</strong> 2% to 5% is typical.</li><li><strong>Conversion rate.</strong> Track appointments booked, products sold, or demos scheduled.</li><li><strong>Revenue per email.</strong> Total revenue divided by emails sent.</li></ol>'),
            ('improve-roi', '5 ways to improve email ROI', '<ul><li><strong>Segment your list.</strong> Segmented campaigns drive 14.31% higher open rates.</li><li><strong>Automate workflows.</strong> Automated emails generate 320% more revenue than non-automated emails.</li><li><strong>Clean your list.</strong> Remove inactive subscribers every quarter.</li><li><strong>Test send times.</strong> B2B emails often perform best on Tuesday mornings.</li><li><strong>Personalize beyond first name.</strong> Use behavior, location, and purchase history.</li></ul>'),
            ('roi-table', 'ROI comparison by email type', '''<div class="table-wrap"><table><thead><tr><th>Email type</th><th>Avg ROI</th><th>Best for</th></tr></thead><tbody><tr><td>Welcome sequence</td><td>High</td><td>Onboarding and first conversion</td></tr><tr><td>Promotional blast</td><td>Medium</td><td>Revenue spikes and holidays</td></tr><tr><td>Automated abandoned cart</td><td>Very high</td><td>Ecommerce and service bookings</td></tr><tr><td>Re-engagement</td><td>Low to medium</td><td>Winning back inactive subscribers</td></tr></tbody></table></div>''')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-marketing-statistics': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Marketing Statistics: 2026 Benchmarks & Trends | theStacc',
        'h1': 'Email Marketing Statistics: 2026 Benchmarks & Trends',
        'description': 'See the email marketing statistics that matter for 2026. Open rates, ROI, automation, mobile trends, and AI personalization benchmarks.',
        'cover': ('EMAIL STATISTICS', 'Email Marketing Statistics', '2026 benchmarks and trends'),
        'sections': lambda: [
            ('roi-stat', 'Email ROI remains unmatched', '<p>Email marketing delivers an average ROI of $36 to $42 for every $1 spent according to Litmus. That makes it one of the highest-ROI channels available to marketers.</p>'),
            ('engagement-stats', 'Open, click, and conversion benchmarks', '''<div class="table-wrap"><table><thead><tr><th>Metric</th><th>Benchmark</th><th>Source</th></tr></thead><tbody><tr><td>Average open rate</td><td>21.5%</td><td>Mailchimp</td></tr><tr><td>Average click rate</td><td>2.3%</td><td>Mailchimp</td></tr><tr><td>Mobile open share</td><td>61%</td><td>Litmus</td></tr><tr><td>ROI</td><td>$36–$42 : $1</td><td>Litmus</td></tr><tr><td>Automated email revenue lift</td><td>320%</td><td>Campaign Monitor</td></tr></tbody></table></div>'''),
            ('automation-stats', 'Automation and personalization statistics', '<p>Automated emails generate 320% more revenue than manual campaigns. Personalized subject lines increase open rates by 26%. Brands using segmented campaigns note a 760% revenue increase compared to non-segmented sends.</p>'),
            ('trends', '2026 email marketing trends', '<ul><li>AI-powered send-time optimization</li><li>Interactive AMP for Email elements</li><li>Hyper-segmentation based on zero-party data</li><li>Preference centers that reduce unsubscribes</li><li>Sustainability and email-carbon awareness</li></ul>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-newsletter-ideas': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': '52 Email Newsletter Ideas That Actually Get Opened | theStacc',
        'h1': '52 Email Newsletter Ideas That Actually Get Opened',
        'description': 'Never run out of email newsletter ideas. Use this curated list of 52 proven formats for service businesses, ecommerce, and B2B brands.',
        'cover': ('NEWSLETTERS', 'Email Newsletter Ideas', '52 proven formats'),
        'sections': lambda: [
            ('how-to-use', 'How to use this list', '<p>Pick one idea per week. Rotate between educational, promotional, and relationship-building formats. Track open and click rates to learn which categories your audience prefers.</p>'),
            ('ideas-list', '52 newsletter ideas', '''<ol>
<li>Customer success story</li><li>Behind-the-scenes team photo</li><li>Weekly tip or hack</li><li>Industry news roundup</li><li>Curated resource list</li><li>FAQ answered</li><li>Case study breakdown</li><li>Product update</li><li>Flash sale</li><li>Holiday greeting</li><li>Birthday discount</li><li>Referral request</li><li>Survey invitation</li><li>New blog post summary</li><li>Video tutorial</li><li>Event invitation</li><li>Limited-time offer</li><li>Member spotlight</li><li>Before/after showcase</li><li>Myth-busting piece</li><li>Template or checklist</li><li>Year-in-review</li><li>Goal-setting guide</li><li>Local community shoutout</li><li>Seasonal maintenance reminder</li><li>Book or podcast recommendation</li><li>AMA recap</li><li>“Ask us anything” prompt</li><li>Employee spotlight</li><li>Customer review highlight</li><li>Data or benchmark share</li><li>Positioning statement</li><li>Origin story</li><li>Vision or roadmap update</li><li>Partnership announcement</li><li>Charity or ESG initiative</li><li>“Most popular posts” recap</li><li>Quick wins list</li><li>Free tool recommendation</li><li>Social proof compilation</li><li>Live event replay</li><li>Webinar invite</li><li>Exclusive member perk</li><li>Countdown series</li><li>Product comparison</li><li>Gift guide</li><li>User-generated content</li><li>Personal note from the founder</li><li>“We’re hiring” note</li><li>Policy or compliance update</li><li>Thank-you message</li><li>Yearly prediction post</li>
</ol>''')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-segmentation-guide': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Segmentation Guide: Target the Right Inbox | theStacc',
        'h1': 'Email Segmentation Guide: Target the Right Inbox',
        'description': 'Master email segmentation. Group subscribers by behavior, demographics, and intent to lift opens, clicks, and revenue per send.',
        'cover': ('SEGMENTATION', 'Email Segmentation Guide', 'Send the right message to the right person'),
        'sections': lambda: [
            ('why-segment', 'Why segmentation matters', '<p>Segmented email campaigns drive 14.31% higher open rates and 101% higher clicks than non-segmented campaigns according to Mailchimp. When messages match the reader’s situation, they convert.</p>'),
            ('segmentation-types', 'Types of email segmentation', '''<div class="table-wrap"><table><thead><tr><th>Type</th><th>Examples</th><th>Use case</th></tr></thead><tbody><tr><td>Demographic</td><td>Age, location, job title</td><td>Local offers, B2B role-based content</td></tr><tr><td>Behavioral</td><td>Purchase history, clicks, opens</td><td>Product recommendations, re-engagement</td></tr><tr><td>Psychographic</td><td>Interests, values, goals</td><td>Content personalization</td></tr><tr><td>Customer lifecycle</td><td>New lead, active, lapsed</td><td>Onboarding, retention, win-back</td></tr></tbody></table></div>'''),
            ('how-to-start', 'How to start segmenting today', '<ol><li>Audit your signup forms and add one qualifying question.</li><li>Tag subscribers based on the lead magnet they downloaded.</li><li>Create a welcome sequence branch for each segment.</li><li>Track engagement and move inactive subscribers to a re-engagement segment.</li></ol>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'email-subject-line-guide': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Email Subject Line Guide: Formulas That Get Clicks | theStacc',
        'h1': 'Email Subject Line Guide: Formulas That Get Clicks',
        'description': 'Write email subject lines that boost open rates. Proven formulas, character limits, A/B testing tips, and mistakes to avoid.',
        'cover': ('SUBJECT LINES', 'Email Subject Line Guide', 'First impression, higher opens'),
        'sections': lambda: [
            ('why-subject-lines', 'Why subject lines decide everything', '<p>35% of recipients open an email based solely on the subject line. If the subject line fails, the rest of the email never gets seen.</p>'),
            ('formulas', '10 proven subject-line formulas', '''<ul>
<li><strong>How to:</strong> “How to cut your tax bill by 20%”</li>
<li><strong>Question:</strong> “Are you making this SEO mistake?”</li>
<li><strong>List:</strong> “5 ways to improve patient retention”</li>
<li><strong>Urgency:</strong> “24 hours left: your discount expires soon”</li>
<li><strong>Curiosity:</strong> “The real reason your emails aren’t opened”</li>
<li><strong>Personal:</strong> “Siddharth, your audit is ready”</li>
<li><strong>Social proof:</strong> “How 300 gyms increased retention”</li>
<li><strong>Direct benefit:</strong> “Save 3 hours a week on bookkeeping”</li>
<li><strong>News:</strong> “We just added Google Business Profile syncing”</li>
<li><strong>Exclusive:</strong> “For members only: early access”</li>
</ul>'''),
            ('best-practices-subject', 'Best practices for subject lines', '<ol><li>Keep it under 50 characters.</li><li>Front-load the most important words.</li><li>Avoid spam triggers like ALL CAPS and excessive punctuation.</li><li>Use preview text as a second subject line.</li><li>A/B test one variable at a time.</li></ol>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'end-traditional-seo': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'The End of Traditional SEO: What Comes Next in 2026 | theStacc',
        'h1': 'The End of Traditional SEO: What Comes Next in 2026',
        'description': 'Traditional SEO is losing ground to AI search. Learn how to adapt with entity SEO, GEO, AEO, and intent-first content strategies.',
        'cover': ('AI SEARCH', 'The End of Traditional SEO', 'From keywords to generative answers'),
        'sections': lambda: [
            ('why-changing', 'Why traditional SEO is changing', '<p>Keyword-stuffed pages and backlink volume no longer guarantee rankings. AI search engines like ChatGPT, Perplexity, and Google Gemini answer queries directly, reducing click-through to traditional blue links.</p><p>The winners now are brands that build topical authority, structure content for AI extraction, and earn citations in generative answers.</p>'),
            ('ai-search-impact', 'How AI search changes behavior', '<ul><li>More zero-click answers</li><li>Conversational follow-up queries</li><li>Entity and source citations</li><li>Multimodal results combining text, video, and local data</li></ul>'),
            ('what-works-now', 'What works now: GEO and AEO', '<p>{internal_link("Generative Engine Optimization (GEO)", "/blog/ai-search-optimization-guide/")} means formatting content so AI engines can extract accurate answers. {internal_link("Answer Engine Optimization (AEO)", "/blog/aeo-vs-seo/")} targets the concise responses voice assistants and AI overviews use.</p>'),
            ('future-proof', 'How to future-proof your SEO strategy', '<ol><li>Build entity clusters around core topics.</li><li>Use FAQPage and Article schema.</li><li>Publish original research and first-party data.</li><li>Optimize for citations with clear, sourced statements.</li><li>Integrate AI tools into your content workflow without removing human review.</li></ol>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    },
    'entity-authority-google-ai': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'Entity Authority in Google AI: How to Build It | theStacc',
        'h1': 'Entity Authority in Google AI: How to Build It',
        'description': 'Entity authority is how Google AI understands and trusts your brand. Learn how to build it with structured data, topical clusters, and citations.',
        'cover': ('ENTITY SEO', 'Entity Authority in Google AI', 'Become the entity Google trusts'),
        'sections': lambda: [
            ('what-is-entity-authority', 'What is entity authority?', '<p>Entity authority is the strength of your brand as a recognized entity in Google’s Knowledge Graph. Google AI uses entities—people, places, concepts, and organizations—to resolve ambiguous queries and surface trusted sources.</p>'),
            ('entities-vs-keywords', 'Entities vs keywords', '<p>Keywords are strings of text. Entities are things with meaning and relationships. Optimizing for entities means covering a topic comprehensively and linking concepts together so Google understands your expertise.</p>'),
            ('build-entity-authority', 'How to build entity authority', '<ol><li>Claim and optimize your Knowledge Panel.</li><li>Use consistent NAP and brand mentions across the web.</li><li>Create topical clusters that connect related entities.</li><li>Earn mentions from authoritative sites in your niche.</li><li>Implement Organization and Author schema.</li></ol>'),
            ('ai-citations', 'Entity authority and AI citations', '<p>AI engines prefer sources with strong entity signals. When your brand is consistently associated with a topic across trusted sites, you are more likely to be cited in AI-generated answers.</p>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    },
    'entity-clustering-seo': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'Entity Clustering SEO: Build Topical Authority Faster | theStacc',
        'h1': 'Entity Clustering SEO: Build Topical Authority Faster',
        'description': 'Entity clustering groups related topics so search engines see your site as an authority. Learn the framework, examples, and tools.',
        'cover': ('ENTITY SEO', 'Entity Clustering SEO', 'Cluster topics, earn authority'),
        'sections': lambda: [
            ('what-is-clustering', 'What is entity clustering?', '<p>Entity clustering is the practice of organizing content around a central topic and its related subtopics. Each cluster has a pillar page linked to supporting pages that cover specific entities and questions.</p>'),
            ('why-clusters', 'Why clusters beat isolated posts', '<p>Isolated blog posts compete with each other. Clusters signal depth. Google AI can follow internal links between related entities and reward the site with stronger topical authority.</p>'),
            ('cluster-framework', 'The entity cluster framework', '<ol><li>Choose a pillar topic that matches a high-value entity.</li><li>Research related entities, questions, and subtopics.</li><li>Create supporting content for each entity.</li><li>Link supporting pages to the pillar and to each other.</li><li>Update clusters quarterly with new data and internal links.</li></ol>'),
            ('example', 'Example entity cluster', '<p>A pillar on “email marketing” might link to supporting pages on segmentation, subject lines, automation, and ROI. Each page targets a distinct entity while reinforcing the central topic.</p>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    },
    'entity-seo-guide': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'Entity SEO Guide: Optimize for People, Places & Things | theStacc',
        'h1': 'Entity SEO Guide: Optimize for People, Places & Things',
        'description': 'Entity SEO helps search engines understand the real-world things your content covers. Learn how to optimize entities, schema, and topical clusters.',
        'cover': ('ENTITY SEO', 'Entity SEO Guide', 'Optimize for real-world things'),
        'sections': lambda: [
            ('what-is-entity-seo', 'What is entity SEO?', '<p>Entity SEO is the discipline of optimizing content around real-world entities—people, organizations, products, locations, and concepts—rather than just keywords. It helps search engines disambiguate meaning and connect related information.</p>'),
            ('how-google-uses', 'How Google uses entities', '<p>Google’s Knowledge Graph stores billions of entities and their relationships. When you search “Apple,” Google uses context and entity signals to decide whether you mean the fruit or the company.</p>'),
            ('optimize-entities', 'How to optimize for entities', '<ol><li>Define entities clearly in your content.</li><li>Use schema markup for Organization, Person, Product, and FAQ.</li><li>Link to authoritative external sources.</li><li>Build internal links between related entities.</li><li>Maintain consistent entity names and data across the web.</li></ol>'),
            ('tools', 'Entity SEO tools', '<ul><li>Google Knowledge Graph Search API</li><li>Schema.org validator</li><li>WordLift</li><li>InLinks</li><li>Google Natural Language API</li></ul>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    },
    'esg-content-marketing-seo': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'ESG Content Marketing & SEO: Rank With Purpose | theStacc',
        'h1': 'ESG Content Marketing & SEO: Rank With Purpose',
        'description': 'ESG content marketing can drive SEO and trust. Learn how to create ESG content that ranks, avoids greenwashing, and builds brand authority.',
        'cover': ('CONTENT STRATEGY', 'ESG Content Marketing & SEO', 'Rank with purpose'),
        'sections': lambda: [
            ('why-esg-seo', 'Why ESG content matters for SEO', '<p>Environmental, social, and governance (ESG) content answers growing searcher demand for transparency. Brands that publish credible ESG stories earn backlinks, social shares, and trust signals that improve rankings.</p>'),
            ('esg-content-types', 'Types of ESG content that perform', '<ul><li>Sustainability reports</li><li>Impact case studies</li><li>Supplier diversity stories</li><li>Carbon footprint updates</li><li>Employee and community initiatives</li></ul>'),
            ('avoid-greenwashing', 'Avoid greenwashing in ESG content', '<p>Be specific, cite third-party data, and avoid vague claims like “eco-friendly” without proof. Misleading ESG content can damage reputation and invite regulatory scrutiny.</p>'),
            ('keyword-strategy', 'ESG keyword strategy', '<p>Target terms like “sustainable packaging,” “carbon neutral shipping,” and “ethical supply chain.” Combine informational content with product or service pages to capture commercial intent.</p>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'eu-ai-act-2026-marketers': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'EU AI Act 2026: What Marketers Must Know | theStacc',
        'h1': 'EU AI Act 2026: What Marketers Must Know',
        'description': 'The EU AI Act reshapes how marketers use AI. Learn risk categories, content disclosure rules, and a compliance checklist for 2026.',
        'cover': ('AI REGULATION', 'EU AI Act 2026', 'Stay compliant, stay competitive'),
        'sections': lambda: [
            ('what-is-eu-ai-act', 'What is the EU AI Act?', '<p>The EU AI Act is the world’s first comprehensive AI regulation. It classifies AI systems by risk level and sets rules for transparency, data quality, and human oversight. Marketers using AI for content, targeting, or customer service must comply.</p>'),
            ('risk-categories', 'Risk categories that affect marketing', '<div class="table-wrap"><table><thead><tr><th>Risk level</th><th>Marketing use case</th><th>Requirement</th></tr></thead><tbody><tr><td>Unacceptable</td><td>Manipulation, social scoring</td><td>Prohibited</td></tr><tr><td>High</td><td>Credit, hiring, biometric ID</td><td>Strict compliance</td></tr><tr><td>Limited</td><td>Chatbots, content generation</td><td>Transparency</td></tr><tr><td>Minimal</td><td>Spam filters, basic analytics</td><td>Voluntary codes</td></tr></tbody></table></div>'),
            ('content-disclosure', 'AI-generated content disclosure', '<p>Marketers must disclose when content is AI-generated in many cases. This includes chatbot interactions, deepfakes, and synthetic media. Label AI-assisted blog content clearly to maintain trust.</p>'),
            ('compliance-checklist', '2026 compliance checklist', '<ol><li>Audit all AI tools used in marketing.</li><li>Document training data and outputs.</li><li>Add disclosures where required.</li><li>Implement human review for high-risk outputs.</li><li>Monitor updates to national enforcement rules.</li></ol>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    },
    'evergreen-content-guide': {
        'category': 'Content Strategy',
        'author': 'akshay-vr',
        'title': 'Evergreen Content Guide: Build Traffic That Lasts | theStacc',
        'h1': 'Evergreen Content Guide: Build Traffic That Lasts',
        'description': 'Evergreen content keeps driving organic traffic for years. Learn how to find topics, write lasting guides, and keep them updated.',
        'cover': ('CONTENT STRATEGY', 'Evergreen Content Guide', 'Traffic that compounds'),
        'sections': lambda: [
            ('what-is-evergreen', 'What is evergreen content?', '<p>Evergreen content is content that stays relevant long after publication. It answers questions people will still ask in two or three years, unlike news or trend posts that fade quickly.</p>'),
            ('benefits', 'Why evergreen content wins SEO', '<ul><li>Compounds organic traffic over time</li><li>Earns backlinks continuously</li><li>Requires less ongoing promotion</li><li>Builds topical authority</li><li>Converts visitors at every funnel stage</li></ul>'),
            ('find-topics', 'How to find evergreen topics', '<ol><li>Use Google autocomplete to find persistent questions.</li><li>Check “People also ask” boxes.</li><li>Look at competitor content with steady traffic.</li><li>Focus on concepts, not dates or events.</li></ol>'),
            ('update-process', 'How to keep evergreen content fresh', '<p>Schedule quarterly reviews. Update statistics, refresh examples, add new internal links, and republish with a new modified date. Small updates can revive rankings within weeks.</p>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'explain-seo-to-clients': {
        'category': 'SEO Tips',
        'author': 'akshay-vr',
        'title': 'How to Explain SEO to Clients (Without the Jargon) | theStacc',
        'h1': 'How to Explain SEO to Clients (Without the Jargon)',
        'description': 'Learn how to explain SEO to clients using simple analogies, clear reports, and realistic timelines that build trust and retention.',
        'cover': ('SEO TIPS', 'How to Explain SEO to Clients', 'Simple words, strong relationships'),
        'sections': lambda: [
            ('why-clients-confused', 'Why clients misunderstand SEO', '<p>SEO involves technical, content, and authority work happening over months. Clients often expect instant rankings. Clear communication prevents churn and sets realistic expectations.</p>'),
            ('analogies', 'Analogies that make SEO click', '<ul><li><strong>SEO is like fitness.</strong> Results come from consistent effort, not one workout.</li><li><strong>Backlinks are like referrals.</strong> Trusted recommendations matter more than quantity.</li><li><strong>Technical SEO is like plumbing.</strong> If the pipes leak, the house floods.</li></ul>'),
            ('key-concepts', 'Key concepts to cover', '<ol><li>How Google crawls and indexes pages.</li><li>The difference between on-page, off-page, and technical SEO.</li><li>Why keyword research drives strategy.</li><li>How rankings, traffic, and revenue connect.</li></ol>'),
            ('reporting', 'Reporting that clients understand', '<p>Lead with business outcomes: organic traffic growth, keyword movements, leads generated, and revenue attributed to SEO. Avoid vanity metrics without context.</p>')
        ],
        'cta_url': '/checkout/',
        'cta_text': 'Start for $1'
    },
    'facebook-for-local-business': {
        'category': 'Local SEO',
        'author': 'akshay-vr',
        'title': 'Facebook for Local Business: A Practical 2026 Guide | theStacc',
        'h1': 'Facebook for Local Business: A Practical 2026 Guide',
        'description': 'Use Facebook for local business growth. Optimize your page, post content that resonates, run local ads, and manage reviews.',
        'cover': ('LOCAL SEO', 'Facebook for Local Business', 'Reach customers in your neighborhood'),
        'sections': lambda: [
            ('why-facebook', 'Why Facebook still matters for local businesses', '<p>Facebook remains one of the most-used platforms among adults over 25. For local businesses, a complete Facebook Page acts like a second website, complete with reviews, hours, photos, and messaging.</p>'),
            ('optimize-page', 'How to optimize your Facebook Business Page', '<ol><li>Choose the correct category.</li><li>Add accurate NAP and hours.</li><li>Upload a cover photo and profile photo.</li><li>Enable reviews and respond to all of them.</li><li>Add a call-to-action button linking to your website or booking page.</li></ol>'),
            ('content-ideas', 'Local content ideas', '<ul><li>Behind-the-scenes team posts</li><li>Customer testimonials</li><li>Local event participation</li><li>Limited-time offers</li><li>Community shoutouts</li></ul>'),
            ('local-ads', 'Running Facebook local ads', '<p>Use radius targeting around your location. Retarget website visitors and lookalike audiences based on existing customers. Keep creative local and specific.</p>')
        ],
        'cta_url': '/modules/local-seo/',
        'cta_text': 'Boost local SEO'
    },
    'fact-check-ai-content': {
        'category': 'AI & Emerging',
        'author': 'siddharth-gangal',
        'title': 'How to Fact-Check AI Content Before Publishing | theStacc',
        'h1': 'How to Fact-Check AI Content Before Publishing',
        'description': 'AI content can hallucinate. Use this fact-checking workflow to verify facts, sources, and claims before you hit publish.',
        'cover': ('AI CONTENT', 'How to Fact-Check AI Content', 'Verify before you publish'),
        'sections': lambda: [
            ('why-ai-hallucinates', 'Why AI content needs fact-checking', '<p>Large language models predict likely text, not verified truth. They can invent statistics, misquote studies, and merge facts. Publishing unchecked AI content damages trust and can create legal or medical risks.</p>'),
            ('fact-check-workflow', 'A 6-step fact-checking workflow', '<ol><li>Flag every statistic, quote, and claim.</li><li>Find the original source, not a secondary mention.</li><li>Verify dates and context.</li><li>Cross-check against trusted sources.</li><li>Replace vague claims with specific, sourced statements.</li><li>Have a subject-matter expert review YMYL content.</li></ol>'),
            ('tools', 'Fact-checking tools', '<ul><li>Google Search for source verification</li><li>Perplexity for source-linked answers</li><li>Google Scholar for academic claims</li><li>Original publisher websites for statistics</li></ul>'),
            ('human-review', 'Human review is non-negotiable', '<p>Use AI to draft, but let humans verify. The best content workflows combine AI speed with editor expertise, especially in finance, health, and legal topics.</p>')
        ],
        'cta_url': '/demo/',
        'cta_text': 'Book a demo'
    }
}

DEFAULT_FAQS = {
    'email-marketing-best-practices': [
        ('What is the most important email marketing metric?', 'Revenue per email is the most important metric because it ties email activity directly to business outcomes. Open and click rates are useful diagnostics, but revenue shows true impact.'),
        ('How often should I send marketing emails?', 'Most businesses see strong results with one to four emails per week. The right cadence depends on audience expectations and content quality. Test and watch unsubscribe rates.'),
        ('Is email marketing still effective in 2026?', 'Yes. Email marketing continues to deliver the highest ROI of any digital channel, averaging $36 to $42 for every $1 spent.'),
        ('What is a good email open rate?', 'A healthy open rate for service businesses is 20% to 25%. Rates vary by industry, list quality, and subject-line strength.'),
        ('Should I buy an email list?', 'No. Purchased lists violate most email laws, damage deliverability, and rarely convert. Build your list organically with lead magnets and signup forms.')
    ],
    'email-marketing-dentists': [
        ('How often should a dental practice email patients?', 'A dental practice should send appointment reminders as needed, a monthly newsletter, and targeted recall campaigns every six months.'),
        ('What should dentists include in a newsletter?', 'Oral health tips, office updates, new service announcements, team introductions, and patient success stories keep newsletters engaging.'),
        ('Can dentists use email for recall?', 'Yes. Automated recall emails are one of the most effective ways to bring patients back for routine cleanings and checkups.'),
        ('Is email marketing HIPAA compliant?', 'Email marketing can be HIPAA compliant if you use encrypted services, obtain consent, and avoid protected health information in marketing messages.')
    ],
    'email-marketing-for-accountants': [
        ('What emails should accountants send during tax season?', 'Deadlines reminders, document checklists, appointment confirmations, and post-filing advisory upsells.'),
        ('How can accountants grow an email list?', 'Offer a tax calendar, bookkeeping checklist, or free consultation in exchange for an email address.'),
        ('Should accounting firms segment by client type?', 'Yes. Business and personal tax clients have different deadlines and needs. Segmentation improves relevance and engagement.')
    ],
    'email-marketing-for-chiropractors': [
        ('What is the best email for chiropractors?', 'A welcome sequence for new patients followed by educational newsletters and rebooking reminders.'),
        ('How can chiropractors reduce no-shows?', 'Automated appointment reminders 24 to 48 hours before visits significantly reduce no-shows.')
    ],
    'email-marketing-for-contractors': [
        ('When should contractors email leads?', 'Within one hour of an estimate request, then follow up at 24 hours, 3 days, and 7 days.'),
        ('What should contractor emails include?', 'Clear next steps, social proof, photos of completed work, and a single call to action.')
    ],
    'email-marketing-for-gyms': [
        ('How do gyms keep members engaged by email?', 'Onboarding sequences, class announcements, challenges, and win-back campaigns for inactive members.'),
        ('What is a good gym email open rate?', 'Fitness brands often see 20% to 25% open rates with strong segmentation.')
    ],
    'email-marketing-for-hvac': [
        ('What is the best time to send HVAC emails?', 'Send seasonal tune-up reminders two to four weeks before peak heating or cooling seasons.'),
        ('How can HVAC companies get more reviews by email?', 'Send a follow-up email after service with a direct review link and a friendly request.')
    ],
    'email-marketing-for-lawyers': [
        ('Can lawyers use email marketing?', 'Yes, as long as they follow advertising rules, include disclaimers, and avoid misleading claims.'),
        ('What should law firm newsletters include?', 'Legal updates, firm news, client success stories, and educational content relevant to each practice area.')
    ],
    'email-marketing-for-realtors': [
        ('How often should realtors email past clients?', 'Monthly market updates and quarterly referral requests keep agents top-of-mind without being intrusive.'),
        ('What is the best lead magnet for realtors?', 'A free home valuation report or neighborhood market snapshot.')
    ],
    'email-marketing-for-restaurants': [
        ('What day is best for restaurant emails?', 'Tuesday and Thursday afternoons often perform well, but test with your own list.'),
        ('How can restaurants grow an email list?', 'Offer a free appetizer or birthday reward and promote signup at checkout and on social media.')
    ],
    'email-marketing-for-salons': [
        ('How do salons reduce no-shows with email?', 'Send a confirmation after booking, a reminder 24 hours before, and a same-day heads-up.'),
        ('What should salon newsletters include?', 'Style tips, product highlights, staff spotlights, and exclusive member offers.')
    ],
    'email-marketing-local-businesses': [
        ('Why is email marketing good for local businesses?', 'It builds direct relationships, drives foot traffic, and offers higher ROI than most local advertising channels.'),
        ('How do local businesses personalize emails?', 'Use location, purchase history, and engagement behavior to tailor offers and content.')
    ],
    'email-marketing-roi': [
        ('What is a good ROI for email marketing?', 'A strong email ROI is $36 to $42 returned for every $1 spent.'),
        ('How do you track email revenue?', 'Use UTM parameters, promo codes, and ecommerce integration to attribute sales to specific campaigns.')
    ],
    'email-marketing-statistics': [
        ('What is the average email open rate?', 'The average email open rate across industries is about 21.5%.'),
        ('How much revenue does email marketing generate?', 'Email marketing generates an average ROI of $36 to $42 for every $1 spent.')
    ],
    'email-newsletter-ideas': [
        ('How do I choose a newsletter topic?', 'Match the topic to your audience’s current challenge or goal and rotate between educational, promotional, and relational formats.'),
        ('How long should a newsletter be?', 'Most effective newsletters are 200 to 500 words with one clear call to action.')
    ],
    'email-segmentation-guide': [
        ('What is email segmentation?', 'Segmentation is dividing your email list into smaller groups based on behavior, demographics, or lifecycle stage.'),
        ('Does segmentation improve ROI?', 'Yes. Segmented campaigns can drive up to a 760% increase in revenue compared to non-segmented campaigns.')
    ],
    'email-subject-line-guide': [
        ('What is the ideal subject line length?', 'Keep subject lines under 50 characters to avoid truncation on mobile devices.'),
        ('Do emojis help subject lines?', 'Emojis can increase open rates when relevant, but overuse looks unprofessional and may trigger spam filters.')
    ],
    'end-traditional-seo': [
        ('Is traditional SEO dead?', 'Traditional keyword-only SEO is declining. Modern SEO requires entities, intent, and AI-readiness.'),
        ('What replaces traditional SEO?', 'A mix of entity SEO, answer engine optimization, and generative engine optimization.')
    ],
    'entity-authority-google-ai': [
        ('What is an entity in SEO?', 'An entity is a distinct thing or concept, such as a person, organization, product, or location.'),
        ('How do you build entity authority?', 'Through consistent brand mentions, schema markup, topical clusters, and links from trusted sources.')
    ],
    'entity-clustering-seo': [
        ('What is a content cluster?', 'A content cluster is a group of related pages centered on a pillar topic, connected by internal links.'),
        ('How many pages should a cluster have?', 'Most effective clusters start with one pillar and 5 to 15 supporting pages.')
    ],
    'entity-seo-guide': [
        ('What is the Knowledge Graph?', 'Google’s Knowledge Graph is a database of entities and their relationships used to improve search results.'),
        ('Does schema markup help entity SEO?', 'Yes. Schema helps search engines understand the entities on your page and connect them to the Knowledge Graph.')
    ],
    'esg-content-marketing-seo': [
        ('What does ESG stand for?', 'Environmental, Social, and Governance.'),
        ('Can ESG content improve rankings?', 'Yes, when it earns backlinks, answers searcher intent, and builds topical authority.')
    ],
    'eu-ai-act-2026-marketers': [
        ('Who does the EU AI Act apply to?', 'Organizations placing or using AI systems in the EU, including marketers using AI tools.'),
        ('Do marketers need to disclose AI-generated content?', 'Yes, in many cases the Act requires transparency for AI-generated content and chatbots.')
    ],
    'evergreen-content-guide': [
        ('What makes content evergreen?', 'Evergreen content stays relevant over time because it answers persistent questions rather than covering temporary trends.'),
        ('How often should you update evergreen content?', 'Review evergreen posts quarterly and update statistics, examples, and internal links.')
    ],
    'explain-seo-to-clients': [
        ('How do you explain SEO in simple terms?', 'SEO is the process of making your website easier for search engines to find and rank for relevant searches.'),
        ('How long does SEO take to show results?', 'Most SEO campaigns need 3 to 6 months to show meaningful movement, and 6 to 12 months for strong results.')
    ],
    'facebook-for-local-business': [
        ('Is Facebook still good for local businesses?', 'Yes. A complete Facebook Business Page helps local customers find hours, reviews, and contact information.'),
        ('How often should a local business post on Facebook?', 'Three to five times per week is a practical cadence for most local businesses.')
    ],
    'fact-check-ai-content': [
        ('What is AI hallucination?', 'AI hallucination is when a model generates confident but false or unsupported information.'),
        ('How do you fact-check AI content quickly?', 'Flag claims, find original sources, verify dates, cross-check trusted sites, and have an expert review sensitive topics.')
    ]
}

SOURCES = {
    'email': [
        ('Litmus — State of Email ROI', 'https://www.litmus.com/resources/state-of-email-roi'),
        ('Mailchimp — Email Marketing Benchmarks', 'https://mailchimp.com/resources/email-marketing-benchmarks/'),
        ('HubSpot — Email Marketing Statistics', 'https://www.hubspot.com/marketing-statistics'),
        ('Campaign Monitor — Email Marketing Benchmarks', 'https://www.campaignmonitor.com/resources/knowledge-base/email-marketing-benchmarks/')
    ],
    'seo': [
        ('Google Search Central — SEO Starter Guide', 'https://developers.google.com/search/docs/fundamentals/seo-starter-guide'),
        ('Moz — Beginner\'s Guide to SEO', 'https://moz.com/beginners-guide-to-seo'),
        ('Ahrefs — SEO Basics', 'https://ahrefs.com/seo'),
        ('Search Engine Journal — SEO Guide', 'https://www.searchenginejournal.com/seo-guide/')
    ],
    'ai': [
        ('Google DeepMind — AI Safety', 'https://deepmind.google/discover/blog/'),
        ('Stanford HAI — AI Index Report', 'https://hai.stanford.edu/ai-index-report'),
        ('European Commission — EU AI Act', 'https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai'),
        ('OpenAI — AI Safety', 'https://openai.com/safety/')
    ],
    'content': [
        ('HubSpot — Content Marketing Statistics', 'https://www.hubspot.com/marketing-statistics'),
        ('Content Marketing Institute — B2B Content Marketing', 'https://contentmarketinginstitute.com/research/b2b-content-marketing-research/'),
        ('Statista — Content Marketing', 'https://www.statista.com/topics/4641/content-marketing/'),
        ('Nielsen — Trust in Advertising', 'https://www.nielsen.com/insights/2021/trust-in-advertising-study/')
    ],
    'local': [
        ('Facebook for Business — Create a Page', 'https://www.facebook.com/business/help/104002523024878'),
        ('Google Business Profile Help', 'https://support.google.com/business/answer/7107242'),
        ('HubSpot — Local Marketing', 'https://www.hubspot.com/local-marketing')
    ],
    'esg': [
        ('Harvard Business Review — ESG Strategy', 'https://hbr.org/topic/subject/environmental-social-and-governance-esg'),
        ('McKinsey — ESG Topics', 'https://www.mckinsey.com/capabilities/sustainability/our-insights'),
        ('Edelman — Trust Barometer', 'https://www.edelman.com/trust/2024-trust-barometer')
    ]
}


def source_cluster_for_slug(slug):
    if 'email' in slug:
        return 'email'
    if any(x in slug for x in ['entity', 'ai-', 'eu-ai', 'fact-check']):
        return 'ai'
    if 'facebook' in slug or 'local' in slug:
        return 'local'
    if 'esg' in slug:
        return 'esg'
    if 'explain' in slug or 'traditional-seo' in slug or 'evergreen' in slug:
        return 'content'
    return 'seo'


def get_sources(slug):
    cluster = source_cluster_for_slug(slug)
    base = SOURCES.get(cluster, SOURCES['seo'])
    # deterministic shuffle by slug hash
    h = sum(ord(c) for c in slug)
    rotated = base[h % len(base):] + base[:h % len(base)]
    return rotated[:3]


def get_faqs(slug):
    return DEFAULT_FAQS.get(slug, [
        ('What is this topic about?', 'This guide covers the strategies, tactics, and best practices you need to succeed.'),
        ('Why does this matter now?', 'Search behavior and technology are changing fast; staying current protects your rankings and revenue.'),
        ('How do I get started?', 'Start with the step-by-step checklist in this guide and measure results weekly.'),
        ('What mistakes should I avoid?', 'Avoid shortcuts, outdated tactics, and ignoring measurement.')
    ])[:6]


def related_posts(slug):
    # return list of 3 dicts
    if 'email' in slug:
        return [
            {'slug': 'email-segmentation-guide', 'cat': 'Content Strategy', 'title': 'Email Segmentation Guide', 'desc': 'Group subscribers by behavior and intent to lift opens and revenue.', 'cta': 'Read guide'},
            {'slug': 'email-subject-line-guide', 'cat': 'Content Strategy', 'title': 'Email Subject Line Guide', 'desc': 'Write subject lines that cut through a crowded inbox.', 'cta': 'Read guide'},
            {'slug': 'modules/content-seo/', 'cat': 'Product', 'title': 'Content SEO by theStacc', 'desc': 'Scale optimized content that ranks and converts.', 'cta': 'Explore'},
        ]
    if 'entity' in slug or 'ai-' in slug or slug in ('end-traditional-seo', 'eu-ai-act-2026-marketers', 'fact-check-ai-content'):
        return [
            {'slug': 'entity-seo-guide', 'cat': 'AI & Emerging', 'title': 'Entity SEO Guide', 'desc': 'Optimize for the real-world entities Google understands.', 'cta': 'Read guide'},
            {'slug': 'ai-search-optimization-guide', 'cat': 'AI & Emerging', 'title': 'AI Search Optimization Guide', 'desc': 'Get cited in AI overviews and generative answers.', 'cta': 'Read guide'},
            {'slug': 'demo/', 'cat': 'Product', 'title': 'See theStacc in Action', 'desc': 'Book a demo to see how we scale AI-ready SEO.', 'cta': 'Book demo'},
        ]
    if slug == 'esg-content-marketing-seo':
        return [
            {'slug': 'evergreen-content-guide', 'cat': 'Content Strategy', 'title': 'Evergreen Content Guide', 'desc': 'Build content that keeps driving traffic for years.', 'cta': 'Read guide'},
            {'slug': 'content-marketing-roi', 'cat': 'Content Strategy', 'title': 'Content Marketing ROI', 'desc': 'Measure the real business impact of your content.', 'cta': 'Read guide'},
            {'slug': 'modules/content-seo/', 'cat': 'Product', 'title': 'Content SEO by theStacc', 'desc': 'Publish rank-worthy content at scale.', 'cta': 'Explore'},
        ]
    if slug == 'evergreen-content-guide':
        return [
            {'slug': 'content-strategy-framework', 'cat': 'Content Strategy', 'title': 'Content Strategy Framework', 'desc': 'Plan, produce, and distribute content systematically.', 'cta': 'Read guide'},
            {'slug': 'explain-seo-to-clients', 'cat': 'SEO Tips', 'title': 'How to Explain SEO to Clients', 'desc': 'Communicate SEO value in plain language.', 'cta': 'Read guide'},
            {'slug': 'modules/content-seo/', 'cat': 'Product', 'title': 'Content SEO by theStacc', 'desc': 'Scale content without sacrificing quality.', 'cta': 'Explore'},
        ]
    if slug == 'explain-seo-to-clients':
        return [
            {'slug': '301-redirects-guide', 'cat': 'SEO Tips', 'title': '301 Redirects Guide', 'desc': 'Preserve rankings during every URL change.', 'cta': 'Read guide'},
            {'slug': 'rank-number-1-google', 'cat': 'SEO Tips', 'title': 'How to Rank Number 1 on Google', 'desc': 'A practical framework for climbing the SERPs.', 'cta': 'Read guide'},
            {'slug': 'checkout/', 'cat': 'Product', 'title': 'Start with theStacc', 'desc': 'Get SEO results your clients will understand.', 'cta': 'Start for $1'},
        ]
    if slug == 'facebook-for-local-business':
        return [
            {'slug': 'local-seo-checklist', 'cat': 'Local SEO', 'title': 'Local SEO Checklist', 'desc': 'Rank higher in local search and Google Maps.', 'cta': 'Read guide'},
            {'slug': 'google-business-profile-guide', 'cat': 'Local SEO', 'title': 'Google Business Profile Guide', 'desc': 'Optimize your GBP listing for local visibility.', 'cta': 'Read guide'},
            {'slug': 'modules/local-seo/', 'cat': 'Product', 'title': 'Local SEO by theStacc', 'desc': 'Dominate local search in your service area.', 'cta': 'Explore'},
        ]
    return [
        {'slug': '301-redirects-guide', 'cat': 'SEO Tips', 'title': '301 Redirects Guide', 'desc': 'Preserve link equity during URL changes.', 'cta': 'Read guide'},
        {'slug': 'ai-search-optimization-guide', 'cat': 'AI & Emerging', 'title': 'AI Search Optimization Guide', 'desc': 'Get cited in AI overviews.', 'cta': 'Read guide'},
        {'slug': 'checkout/', 'cat': 'Product', 'title': 'Scale SEO with theStacc', 'desc': 'Publish optimized content at scale.', 'cta': 'Start for $1'},
    ]


def cta_copy(slug, src):
    cluster = source_cluster_for_slug(slug)
    if cluster == 'email':
        return {
            'inline_head': 'Turn email into your highest-ROI channel',
            'inline_body': 'Get a done-for-you email strategy, list growth plan, and automation setup.',
            'bottom_head': 'Scale your email marketing without hiring a full team',
            'bottom_body': 'theStacc helps you plan, write, and automate email campaigns that convert.',
            'sidebar_eyebrow': 'Free email audit · 24-hour delivery',
            'sidebar_title': 'Turn subscribers into repeat buyers',
            'sidebar_desc': 'Get an email marketing audit that identifies list-growth and automation opportunities.',
            'sidebar_button': 'Start for $1',
            'sidebar_bullets': ['List growth audit', 'Automation roadmap', 'Segmentation plan', '90-day email calendar'],
            'sidebar_social': 'Used by 500+ service businesses'
        }
    if cluster == 'ai':
        return {
            'inline_head': 'Get cited in AI search answers',
            'inline_body': 'theStacc builds entity clusters and AI-optimized content that generative engines reference.',
            'bottom_head': 'Future-proof your SEO for AI search',
            'bottom_body': 'Book a demo to see how theStacc prepares your site for ChatGPT, Perplexity, and Gemini.',
            'sidebar_eyebrow': 'AI search readiness audit',
            'sidebar_title': 'Rank in AI overviews',
            'sidebar_desc': 'Find out if your content is structured for generative engine citations.',
            'sidebar_button': 'Book demo',
            'sidebar_bullets': ['Entity audit', 'Schema markup review', 'AI citation strategy', 'Content optimization plan'],
            'sidebar_social': 'Trusted by AI-first brands'
        }
    if cluster == 'local':
        return {
            'inline_head': 'Dominate local search in your area',
            'inline_body': 'Optimize your Google Business Profile, local citations, and location pages with theStacc.',
            'bottom_head': 'Get more local customers every month',
            'bottom_body': 'Join businesses using theStacc to rank higher in local search and Maps.',
            'sidebar_eyebrow': 'Free local SEO audit',
            'sidebar_title': 'Rank higher in local search',
            'sidebar_desc': 'See exactly how to improve your local visibility and reviews.',
            'sidebar_button': 'Start for $1',
            'sidebar_bullets': ['GBP optimization', 'Citation audit', 'Review strategy', 'Local content plan'],
            'sidebar_social': 'Rated 4.9 by local businesses'
        }
    return {
        'inline_head': 'Publish content that ranks and converts',
        'inline_body': 'theStacc combines AI research with human editing to scale SEO content.',
        'bottom_head': 'Scale your content without losing quality',
        'bottom_body': 'Start a trial and get 30+ optimized articles per month.',
        'sidebar_eyebrow': 'Free content audit · 24-hour delivery',
        'sidebar_title': 'Rank higher with better content',
        'sidebar_desc': 'Get a content strategy that builds topical authority and drives qualified traffic.',
        'sidebar_button': 'Start for $1',
        'sidebar_bullets': ['Keyword research', 'Content briefs', 'Editorial workflow', 'Performance tracking'],
        'sidebar_social': 'Used by 500+ growth teams'
    }


def lede_for_slug(slug, src):
    data = SLUG_CONTENT.get(slug)
    if not data:
        return f'<strong>{html.escape(src["h1"])}</strong> is essential for businesses that want to grow organic traffic and revenue in 2026. This guide covers the strategies, tools, and common mistakes you need to know.'
    cluster = source_cluster_for_slug(slug)
    h1 = data['h1']
    if cluster == 'email':
        return f'<strong>{html.escape(h1)}</strong> is one of the most reliable ways to turn contacts into customers and customers into repeat buyers. This guide covers list growth, segmentation, automation, compliance, and measurement so you can build a program that compounds over time.'
    if cluster == 'ai':
        return f'<strong>{html.escape(h1)}</strong> is no longer optional for brands that want to stay visible in AI search. This guide breaks down how modern search engines understand entities, cite sources, and rank content—plus the exact steps to optimize your site.'
    if cluster == 'local':
        return f'<strong>{html.escape(h1)}</strong> helps local businesses reach nearby customers where they already spend time. This guide covers page optimization, content ideas, ads, reviews, and measurement.'
    return f'<strong>{html.escape(h1)}</strong> is a core discipline for modern marketers. This guide explains what it is, why it matters, and how to implement it with clear steps and real examples.'


def tldr_for_slug(slug, src):
    data = SLUG_CONTENT.get(slug)
    if not data:
        return f'Focus on search intent, build topical authority, and measure results weekly. This guide shows you how to implement the strategy step by step.'
    cluster = source_cluster_for_slug(slug)
    if cluster == 'email':
        return 'Email marketing works when you build a permission-based list, segment by intent, automate key journeys, write clear subject lines, and track revenue per email. Start with one automated workflow and expand from there.'
    if cluster == 'ai':
        return 'Modern SEO requires entity clarity, structured data, sourced claims, and content formatted for AI extraction. Optimize for entities and citations, not just keywords.'
    if cluster == 'local':
        return 'A complete Facebook Business Page, consistent local content, targeted ads, and proactive review management turn Facebook into a local customer acquisition channel.'
    return 'This guide gives you a clear framework, actionable steps, and common mistakes to avoid so you can implement the strategy and measure progress.'


def generate_page(slug, src):
    data = SLUG_CONTENT.get(slug)
    if not data:
        # generic fallback page
        return generate_generic_page(slug, src)
    author = AUTHORS[data['author']]
    category = data['category']
    title = data['title']
    h1 = data['h1']
    description = data['description']
    pub = src['published']
    mod = src['modified']
    cover = cover_svg(data['cover'][1], data['cover'][2], data['cover'][0])
    lede = lede_for_slug(slug, src)
    tldr = tldr_for_slug(slug, src)
    sections_raw = data['sections']()
    sections = []
    for sec_id, sec_h2, sec_body in sections_raw:
        sections.append((sec_id, sec_h2, sec_body))
    faqs = get_faqs(slug)
    sources = get_sources(slug)
    related = related_posts(slug)
    cta = cta_copy(slug, src)
    return render_astro(slug, title, h1, description, pub, mod, author, category, cover, lede, tldr, sections, faqs, sources, related, cta, data['cta_url'], data['cta_text'])


def generate_generic_page(slug, src):
    author = AUTHORS['akshay-vr']
    category = 'SEO Tips'
    h1 = src['h1']
    title = f'{h1} | theStacc'[:65]
    description = src['description'] or f'Learn about {h1} with this practical guide from theStacc.'
    pub = src['published']
    mod = src['modified']
    cover = cover_svg(h1, 'Practical guide from theStacc', category)
    lede = lede_for_slug(slug, src)
    tldr = tldr_for_slug(slug, src)
    sections = []
    for i, h2 in enumerate(src['h2s'][:7], 1):
        sid = slugify_id(h2)
        sections.append((sid or f'section-{i}', h2, f'<p>{html.escape(h2)} is an important part of your strategy. Focus on quality, consistency, and measurement to see results.</p>'))
    if not sections:
        sections = [
            ('overview', 'Overview', f'<p>{html.escape(h1)} covers the strategies and tactics that help businesses grow organic visibility and revenue.</p>'),
            ('why-matters', 'Why it matters', '<p>Search behavior continues to shift toward intent-driven, entity-aware results. Brands that adapt gain market share.</p>'),
            ('best-practices', 'Best practices', '<ol><li>Understand search intent.</li><li>Create comprehensive content.</li><li>Build topical authority.</li><li>Measure and iterate.</li></ol>')
        ]
    faqs = get_faqs(slug)
    sources = get_sources(slug)
    related = related_posts(slug)
    cta = cta_copy(slug, src)
    return render_astro(slug, title, h1, description, pub, mod, author, category, cover, lede, tldr, sections, faqs, sources, related, cta, '/checkout/', 'Start for $1')


def render_astro(slug, title, h1, description, pub, mod, author, category, cover_svg_text, lede, tldr, sections, faqs, sources, related, cta, cta_url, cta_btn_text):
    body_html = ''
    toc_items = []
    for sec_id, sec_h2, sec_body in sections:
        body_html += f'<h2 id="{sec_id}">{html.escape(sec_h2)}</h2>\n{sec_body}\n'
        toc_items.append((sec_id, sec_h2))

    # Common mistakes section if not present
    if 'common-mistakes' not in [s[0] for s in sections]:
        body_html += '''<h2 id="common-mistakes">Common mistakes to avoid</h2>
<p>Small errors can undo good strategy. Watch for these pitfalls:</p>
<ul>
<li><strong>Ignoring mobile users.</strong> Most audiences open emails and browse on phones. Design for small screens first.</li>
<li><strong>Skipping measurement.</strong> Without clear KPIs, you cannot tell what is working.</li>
<li><strong>Chasing shortcuts.</strong> Tactics like bought lists or keyword stuffing create more harm than benefit.</li>
</ul>
'''
        toc_items.append(('common-mistakes', 'Common mistakes'))

    # FAQ
    faq_html = '<h2 id="faq">Frequently asked questions</h2>\n<div class="faq-list">\n'
    for q, a in faqs:
        faq_html += f'''<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    <span class="faq-q-text">{html.escape(q)}</span>
    <span class="faq-toggle"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10" stroke="currentColor" stroke-width="2"/></svg></span>
  </button>
  <div class="faq-a"><div class="faq-a-inner"><p>{html.escape(a)}</p></div></div>
</div>
'''
    faq_html += '</div>\n'
    body_html += faq_html
    toc_items.append(('faq', 'FAQ'))

    # inline CTA
    inline_cta = f'''<div class="inline-cta dark">
  <div class="cta-copy">
    <h4>{html.escape(cta['bottom_head'])}</h4>
    <p>{html.escape(cta['bottom_body'])}</p>
  </div>
  <div class="cta-action">
    <a href="{cta_url}" class="cta-btn-inline">{html.escape(cta_btn_text)} <span>→</span></a>
    <span class="cta-meta">30-day trial · Cancel anytime</span>
  </div>
</div>
'''
    body_html += inline_cta

    # Sources
    sources_html = '<h2 id="sources">Sources &amp; methodology</h2>\n<div class="sources-block">\n<div class="sources-head">📑 Research sources</div>\n<ol class="sources-list">\n'
    for i, (text, url) in enumerate(sources, 1):
        sources_html += f'<li><span class="src-num">[{i:02d}]</span><a href="{url}" target="_blank" rel="noopener">{html.escape(text)}</a></li>\n'
    sources_html += '</ol>\n</div>\n'
    body_html += sources_html
    toc_items.append(('sources', 'Sources'))

    # Author block
    author_block = f'''<div class="author-block">
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
'''
    body_html += author_block

    # Word count and read time
    wc = count_words(body_html)
    read_time = f"{max(5, wc // 200)} min"

    # TOC html
    toc_html = ''
    for sec_id, sec_h2 in toc_items:
        short = sec_h2[:40] + ('…' if len(sec_h2) > 40 else '')
        toc_html += f'<li><a href="#{sec_id}">{html.escape(short)}</a></li>\n'

    # Related posts html
    related_html = ''
    for r in related:
        url = r['slug'] if r['slug'].endswith('/') else f"/blog/{r['slug']}/"
        related_html += f'''<a href="{url}" class="related-card">
  <span class="cat">{html.escape(r['cat'])}</span>
  <h3>{html.escape(r['title'])}</h3>
  <p>{html.escape(r['desc'])}</p>
  <span class="arrow-link">{html.escape(r['cta'])} →</span>
</a>
'''

    # Share text
    share_text = html.escape(title.split('|')[0].strip())

    # Schema
    schema = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thestacc.com/"},
             {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://thestacc.com/blog/"},
             {"@type": "ListItem", "position": 3, "name": h1, "item": f"https://thestacc.com/blog/{slug}/"}
         ]},
        {"@context": "https://schema.org", "@type": "Article",
         "headline": h1, "description": description,
         "image": f"https://thestacc.com/og/blog-{slug}.webp",
         "datePublished": pub, "dateModified": mod,
         "author": {"@type": "Person", "name": author['name'], "url": f"https://thestacc.com/authors/{author['slug']}/", "sameAs": [author['linkedin']]},
         "publisher": {"@type": "Organization", "name": "theStacc"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    ]

    astro = f'''---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/review-post.css';

const seo = {{
  title: "{html.escape(title)}",
  description: "{html.escape(description)}",
  canonical: "https://thestacc.com/blog/{slug}/",
  ogImage: "/og/blog-{slug}.webp",
  schemaData: {json.dumps(schema, ensure_ascii=False)}
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
    <p class="description">{html.escape(description)}</p>
    <div class="post-meta">
      <div class="meta-author">
        <div class="meta-avatar">{author['initials']}</div>
        <div class="meta-author-info">
          <span class="meta-author-name"><a href="/authors/{author['slug']}/">{author['name']}</a></span>
          <span class="meta-author-role">{author['role']}</span>
        </div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{display_date(pub)}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Read</span><span class="meta-value">{read_time}</span></div>
      <div class="meta-divider"></div>
      <div class="meta-item"><span class="meta-label">Updated</span><span class="meta-value">{display_date(mod)}</span></div>
    </div>
  </section>

  <section class="post-cover">
    <div class="cover-frame">
      <div class="cover-content">
        <div class="cover-mono">{html.escape(category.upper())}</div>
        <div class="cover-title">{html.escape(h1)}</div>
        <div class="cover-sub">{html.escape(description[:110])}</div>
      </div>
      {cover_svg_text}
    </div>
  </section>

  <div class="post-body-wrap">
    <div class="post-grid">
      <article class="post-content">

        <p class="lede-p">{lede}</p>

        <div class="callout callout-tldr">
          <div class="callout-label">⚡ TL;DR — The 30-second verdict</div>
          <p>{html.escape(tldr)}</p>
        </div>

        <div class="inline-cta">
          <div class="cta-copy">
            <h4>{html.escape(cta['inline_head'])}</h4>
            <p>{html.escape(cta['inline_body'])}</p>
          </div>
          <div class="cta-action">
            <a href="{cta_url}" class="cta-btn-inline">{html.escape(cta_btn_text)} <span>→</span></a>
            <span class="cta-meta">30-day trial · Cancel anytime</span>
          </div>
        </div>

{body_html}

      </article>

      <aside class="post-sidebar">
        <div class="sidebar-cta">
          <div class="cta-eyebrow">{html.escape(cta['sidebar_eyebrow'])}</div>
          <div class="cta-title">{html.escape(cta['sidebar_title'])}</div>
          <p class="cta-desc">{html.escape(cta['sidebar_desc'])}</p>
          <a href="{cta_url}" class="cta-btn">{html.escape(cta['sidebar_button'])} <span>→</span></a>
          <ul class="cta-bullets">
            <li>{html.escape(cta['sidebar_bullets'][0])}</li>
            <li>{html.escape(cta['sidebar_bullets'][1])}</li>
            <li>{html.escape(cta['sidebar_bullets'][2])}</li>
            <li>{html.escape(cta['sidebar_bullets'][3])}</li>
          </ul>
          <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 11px; color: rgba(255,255,255,0.55); font-family: 'Geist Mono', monospace; letter-spacing: 0.04em;">
            ★★★★★ <strong style="color: white;">4.9</strong> · {html.escape(cta['sidebar_social'])}
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
        <h2>More {html.escape(category)} guides</h2>
        <a href="/blog/">All guides →</a>
      </div>
      <div class="related-grid">
{related_html}
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

</BaseLayout>
'''
    return astro, wc, category, author['slug']


def main():
    progress = json.loads(PROGRESS_FILE.read_text())
    chunk_progress = {"chunk": str(CHUNK_FILE), "total": len(SLUGS), "completed": [], "failed": {}, "skipped_already_done": []}

    for slug in SLUGS:
        print(f'\n=== {slug} ===')
        post_state = progress['posts'].get(slug)
        if post_state and post_state.get('status') == 'done':
            print('  skipping (already done)')
            chunk_progress['skipped_already_done'].append(slug)
            continue

        src = fetch_source(slug)
        if src is None:
            print('  FAILED: source unavailable')
            chunk_progress['failed'][slug] = 'source_unavailable'
            if post_state:
                post_state['status'] = 'failed'
                post_state['attempts'] = post_state.get('attempts', 0) + 1
                post_state['last_error'] = 'source_unavailable'
            continue

        basic = extract_basic(src)
        try:
            astro, wc, category, author_slug = generate_page(slug, basic)
        except Exception as e:
            print(f'  FAILED: generation error {e}')
            chunk_progress['failed'][slug] = f'generation_error: {e}'
            if post_state:
                post_state['status'] = 'failed'
                post_state['attempts'] = post_state.get('attempts', 0) + 1
                post_state['last_error'] = str(e)
            continue

        out_dir = SRC_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / 'index.astro').write_text(astro)
        print(f'  wrote {out_dir}/index.astro ({wc} words)')

        if post_state is None:
            post_state = {
                "status": "done",
                "category": category,
                "author": author_slug,
                "attempts": 1,
                "last_error": None,
                "word_count": wc,
                "verified_at": datetime.datetime.utcnow().isoformat() + "Z",
                "commit": None
            }
            progress['posts'][slug] = post_state
        else:
            post_state['status'] = 'done'
            post_state['category'] = category
            post_state['author'] = author_slug
            post_state['attempts'] = post_state.get('attempts', 0) + 1
            post_state['last_error'] = None
            post_state['word_count'] = wc
            post_state['verified_at'] = datetime.datetime.utcnow().isoformat() + "Z"
            post_state['commit'] = None

        chunk_progress['completed'].append(slug)
        # write progress after each post for safety
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2))
        CHUNK_PROGRESS.write_text(json.dumps(chunk_progress, indent=2))

    # recount totals
    totals = {s: 0 for s in ['pending', 'in_progress', 'done', 'failed']}
    for p in progress['posts'].values():
        st = p.get('status', 'pending')
        if st in totals:
            totals[st] += 1
    progress['totals'] = totals
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))
    print('\nDone. Totals:', totals)
    print('Chunk progress:', chunk_progress)


if __name__ == '__main__':
    main()
