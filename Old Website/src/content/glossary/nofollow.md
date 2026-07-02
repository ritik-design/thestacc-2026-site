---
term: "Nofollow Link"
slug: "nofollow"
definition: "A nofollow link is a hyperlink with a rel=\"nofollow\" attribute that tells search engines not to pass SEO authority (link equity) to the target page, though Google may still use it as a ranking hint."
category: "SEO"
difficulty: "Beginner"
keyword: "what is a nofollow link"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "dofollow"
  - "backlinks"
  - "link-building"
  - "sponsored-link"
  - "ugc-link"
---

## What Is a Nofollow Link?

A nofollow link is a hyperlink that contains a `rel="nofollow"` attribute in its HTML. This attribute was introduced by Google in 2005 as a way for webmasters to tell search engines: "I do not endorse this link, and I do not want to pass my page's authority to the destination."

Originally, nofollow was a directive — Google would not follow the link and would not pass any ranking authority. In March 2020, Google changed this behavior. Nofollow became a "hint," meaning Google may choose to count some nofollow links for ranking purposes, crawling, and indexing, depending on the context and quality of the link.

**The HTML looks like this:**

```html
<a href="https://example.com" rel="nofollow">Link text</a>
```

## Why Nofollow Links Matter

Nofollow links serve three critical purposes in the modern web ecosystem:

**1. Spam Prevention**

Before nofollow existed, comment sections, forums, and user-generated content areas were flooded with spam links. Spammers would drop links to their sites knowing that every link passed authority. Nofollow gave webmasters a tool to stop this abuse without removing links entirely.

**2. Advertising Transparency**

Google requires that paid links, sponsored content, and advertisements use nofollow or sponsored attributes. This prevents websites from buying their way to higher rankings and ensures that editorial links (true votes of confidence) carry more weight than paid placements.

**3. Natural Link Profile Building**

A website with 100% dofollow backlinks looks unnatural to Google. Major websites like Wikipedia, Reddit, Medium, and most social media platforms use nofollow on outbound links. Earning links from these platforms is normal, expected, and beneficial even without direct authority transfer.

**Key statistics:**
- The average website's backlink profile contains 20-40% nofollow links (Ahrefs)
- Wikipedia, one of the most authoritative sites on the web, uses nofollow on all external links — yet links from Wikipedia are still highly prized
- Google explicitly states that nofollow links from high-quality sites can indirectly improve rankings by driving traffic, building brand awareness, and leading to future dofollow links

## How Nofollow Links Work

### The March 2020 Change

Before March 2020, nofollow was a hard rule. Google's crawlers would not follow nofollow links for crawling or ranking purposes.

After March 2020, nofollow became a "hint." This means:

- Google *may* crawl nofollow links if they appear valuable
- Google *may* use nofollow links for ranking in some cases
- Google *may* discover new pages through nofollow links

However, for practical SEO purposes, nofollow links still do not pass the same authority as dofollow links. The change simply gave Google flexibility to make exceptions.

### When to Use Nofollow

Google recommends using nofollow (or its newer variants) in these situations:

| Situation | Recommended Attribute | Reason |
|---|---|---|
| Paid links and advertisements | `rel="sponsored"` | Prevents paid link manipulation |
| User-generated content (comments, forums) | `rel="ugc"` | Prevents spam abuse |
| Untrusted or unverified links | `rel="nofollow"` | Protects your site's reputation |
| Sitewide links (footer, sidebar) | `rel="nofollow"` | Prevents over-optimization |
| Links to competitors | `rel="nofollow"` | Avoids passing authority to rivals |
| Affiliate links | `rel="sponsored"` | Required by Google's guidelines |

### Nofollow vs. Sponsored vs. UGC

Google introduced two new link attributes in September 2019 alongside the nofollow update:

| Attribute | Use Case | Example |
|---|---|---|
| `rel="nofollow"` | Untrusted links you don't endorse | Random comment links |
| `rel="sponsored"` | Paid links, ads, affiliate links | Sponsored blog post links |
| `rel="ugc"` | User-generated content links | Forum posts, comment signatures |
| Multiple attributes | Combined situations | `rel="nofollow ugc"` for untrusted user content |

## Do Nofollow Links Help SEO?

**Direct answer:** Nofollow links do not pass direct ranking authority the way dofollow links do.

**Complete answer:** Nofollow links provide several indirect SEO benefits:

**1. Referral Traffic**

A nofollow link from a high-traffic page can send hundreds or thousands of visitors to your site. If those visitors engage with your content, share it, or link to it from their own sites, you gain dofollow links organically.

**2. Brand Building and Awareness**

Being mentioned on major publications — even with nofollow links — builds brand recognition. When people search for your brand later, Google sees this as a positive signal.

**3. Diversified Link Profile**

Google expects natural backlink profiles to include both dofollow and nofollow links. A site with only dofollow links looks manipulated. Nofollow links from legitimate sources make your profile look natural.

**4. Indexing and Discovery**

Google may follow nofollow links to discover new pages. If a nofollow link is the only way Google finds your new page, it can still get indexed and ranked.

**5. Future Dofollow Conversions**

A nofollow link today can lead to a dofollow link tomorrow. A journalist who discovers you through a nofollow mention may later write an article with a dofollow link. A blogger who finds you via a nofollow guest post may reference you in their own dofollow content.

## Where Nofollow Links Come From

These platforms and situations typically produce nofollow links:

- **Social media platforms** (Facebook, Twitter, LinkedIn, Instagram, Pinterest)
- **Wikipedia** (all external links are nofollow)
- **Reddit** (all user-posted links are nofollow)
- **Medium** (some links are nofollow)
- **Quora** (user links are nofollow)
- **YouTube descriptions** (links are nofollow)
- **Most blog comments** (WordPress defaults to nofollow)
- **Press release distribution services** (nofollow by default)
- **Paid directory listings** (nofollow or sponsored)
- **Guest post author bios** (sometimes nofollow, sometimes dofollow)

## Common Nofollow Mistakes

**Mistake 1: Ignoring nofollow links entirely.**

Some SEOs focus exclusively on dofollow links and ignore nofollow opportunities. This is a mistake. Nofollow links from major sites drive traffic, build authority, and create pathways to future dofollow links.

**Mistake 2: Using nofollow on internal links.**

There is rarely a good reason to use nofollow on internal links. Nofollow on internal links prevents Google from distributing authority throughout your site effectively. Use nofollow internally only in specific cases like login pages or duplicate content you don't want indexed.

**Mistake 3: Not using sponsored on paid links.**

Google can detect paid links algorithmically. Failing to mark them as sponsored puts you at risk of manual penalties. When in doubt, mark paid links as sponsored.

**Mistake 4: Adding nofollow to all outbound links.**

Some webmasters add nofollow to every external link out of fear. This is unnecessary and can make your site look suspicious. Use nofollow selectively, not universally.

## How to Check If a Link Is Nofollow

**Method 1: Browser Inspect**
Right-click the link → Inspect Element → Look for `rel="nofollow"` or `rel="sponsored"` or `rel="ugc"` in the `<a>` tag.

**Method 2: SEO Tools**
Ahrefs, Semrush, and Moz all show which of your backlinks are nofollow vs. dofollow in their backlink reports.

**Method 3: Browser Extensions**
Extensions like NoFollow or SEOquake highlight nofollow links on any page you visit.

## Related Terms

- [Dofollow](/glossary/dofollow/)
- [Backlinks](/glossary/backlinks/)
- [Link Building](/glossary/link-building/)
- [Sponsored Link](/glossary/sponsored-link/)
- [UGC Link](/glossary/ugc-link/)
