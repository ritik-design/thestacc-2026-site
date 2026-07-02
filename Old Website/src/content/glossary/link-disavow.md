---
term: "Link Disavow"
slug: "link-disavow"
definition: "The link disavow process is using Google's Disavow Links Tool to tell Google to ignore specific backlinks when assessing your site's ranking, typically used to neutralize toxic or manipulative links."
category: "SEO"
difficulty: "Intermediate"
keyword: "what is link disavow"
date: "2026-06-08"
lastUpdated: "2026-06-08"
relatedTerms:
  - "toxic-links"
  - "backlinks"
  - "google-penalty"
  - "manual-action"
  - "pbn"
---

## What Is Link Disavow?

Link disavow is the process of telling Google to ignore specific backlinks pointing to your website. You do this by creating a disavow file — a text file listing URLs or domains you want Google to disregard — and uploading it through Google's Disavow Links Tool.

Google uses your backlink profile as a major ranking factor. When spammy, low-quality, or manipulative sites link to you, those links can harm your rankings. The disavow tool gives you a way to say: "I did not create these links. I do not want them counted against me."

**Critical warning:** The disavow tool is an advanced feature. Using it incorrectly can harm your site's performance. Google explicitly states that most sites do not need to use this tool.

## When to Use the Disavow Tool

### You SHOULD Disavow If:

- You have a manual action for "unnatural links" in Google Search Console
- You participated in link schemes, PBNs, or paid links in the past
- Your site was hit by a negative SEO attack (someone built spammy links to harm you)
- You have a significant number of toxic links you cannot remove through outreach

### You Should NOT Disavow If:

- You have a few random low-quality links (Google ignores these automatically)
- You are trying to disavow links from legitimate sites you simply do not like
- You have not attempted to remove the links manually first (required for manual actions)
- You are not confident the links are actually harmful

**Google's guidance:** "You should disavow backlinks only if you believe you have a considerable number of spammy, artificial, or low-quality links pointing to your site, and you are confident that the links are causing issues for you."

## How to Create a Disavow File

### File Format

The disavow file is a simple text file (.txt) with one entry per line:

```
# Domain-level disavow — ignores ALL links from this domain
domain:spammy-site.com
domain:another-spam-site.net

# URL-level disavow — ignores only this specific link
https://spammy-site.com/bad-page/
https://forum-spam.org/links-section/specific-post
```

### Best Practices

**1. Use domain-level disavow for clear spam.**

If an entire domain is spammy, disavow the whole domain rather than individual URLs. This catches links you might have missed.

**2. Be specific with URL-level disavow.**

Use URL-level disavow only when a domain is mostly legitimate but has one bad page linking to you.

**3. Include comments for documentation.**

Lines starting with `#` are comments. Use them to document why you disavowed each entry:

```
# PBN network — 50 spam sites with identical templates
domain:pbnsite1.com
domain:pbnsite2.com

# Negative SEO attack — foreign language site, no relevance
domain:foreign-spam-site.ru
```

**4. Upload the file to the correct property.**

If you have both HTTP and HTTPS versions, or www and non-www versions, upload the disavow file to the canonical version in Google Search Console.

## The Disavow Process

### Step 1: Identify Toxic Links

Export your backlink profile from:
- Google Search Console (Links report)
- Ahrefs Site Explorer
- Semrush Backlink Analytics
- Moz Link Explorer

Analyze links for toxicity signals:
- Links from PBNs or link farms
- Sitewide footer/sidebar links
- Exact-match anchor text from irrelevant sites
- Links from foreign language sites with no topical relevance
- Links from sites with zero organic traffic

### Step 2: Attempt Removal (Required for Manual Actions)

If you have a manual action, Google requires proof that you attempted to remove the links:

1. Contact site owners requesting link removal
2. Document your outreach attempts (dates, emails, responses)
3. Keep a spreadsheet of all contacts and outcomes

**Tip:** Use a dedicated email address for removal requests. Some site owners may try to charge you for removal — Google advises against paying for link removal.

### Step 3: Create the Disavow File

List all remaining toxic links that could not be removed:

```
# Links from PBN network discovered March 2026
domain:badlink1.com
domain:badlink2.com
domain:badlink3.com

# Negative SEO — auto-generated comment spam
https://spam-forum.net/comments/12345/
https://blog-comments-spam.org/post/98765/
```

### Step 4: Upload to Google

1. Go to [Google Search Console Disavow Tool](https://search.google.com/search-console/disavow-links)
2. Select your property
3. Click "Disavow Links"
4. Click "Choose File" and select your .txt file
5. Click "Submit"

### Step 5: Submit Reconsideration Request (If Manual Action)

If you received a manual action:
1. Document your cleanup efforts
2. Include your disavow file
3. Submit a reconsideration request through Google Search Console
4. Wait 2-4 weeks for a response

## How Long Does Disavow Take?

- **Algorithmic impact:** 2-6 weeks for Google to process the disavow file
- **Manual action recovery:** 2-4 weeks after reconsideration request
- **No notification:** Google does not confirm when your disavow file is processed

**Important:** Disavowing links does not instantly restore rankings. It simply stops the harmful links from counting against you. Recovery depends on how strong your remaining backlink profile is.

## Common Disavow Mistakes

**Mistake 1: Disavowing good links.**

Some SEOs panic and disavow links from legitimate sites that happen to have low domain authority. This can remove valuable link equity and hurt rankings.

**Mistake 2: Disavowing entire domains too aggressively.**

A site with DR 20 that links to you naturally is not toxic. Save domain-level disavow for clear spam, PBNs, and link farms.

**Mistake 3: Not documenting removal attempts.**

For manual actions, Google requires evidence of outreach. Without documentation, your reconsideration request will be denied.

**Mistake 4: Disavowing and then immediately building more bad links.**

Disavowing past toxic links while continuing to build new ones is futile. Stop the behavior that created the problem.

**Mistake 5: Uploading a poorly formatted file.**

The disavow tool accepts only .txt files with specific formatting. URLs must be complete (including http:// or https://). One entry per line.

## Related Terms

- [Toxic Links](/glossary/toxic-links/)
- [Backlinks](/glossary/backlinks/)
- [Google Penalty](/glossary/google-penalty/)
- [Manual Action](/glossary/manual-action/)
- [PBN](/glossary/pbn/)
