---
term: "Alt Text"
slug: "alt-text"
definition: "Alt text (alternative text) describes images for search engines and screen readers. Learn how to write effective alt text, examples, and why it matters for SEO."
category: "SEO"
difficulty: "Beginner"
keyword: "what is alt text"
date: "2026-03-22"
lastUpdated: "2026-03-22"
relatedTerms:
  - "image-seo"
  - "on-page-seo"
  - "accessibility-content"
  - "crawling"
  - "organic-traffic"
---

## What is Alt Text?

Alt text (alternative text) is an HTML attribute that provides a written description of an image. Used by screen readers for visually impaired users and by search engines to understand what an image shows.

You've probably seen it in code: `<img src="photo.jpg" alt="description here">`. That description is the alt text. It serves two audiences simultaneously. For people who can't see the image. Whether they use a screen reader, have a slow connection, or the image fails to load. Alt text tells them what's there. For Google, it's one of the primary signals used to index and rank images in Google Images.

WebAIM's 2024 accessibility analysis found that 54.5% of images on the web are missing alt text. Over half. That's both an [accessibility](/glossary/accessibility-content) failure and an SEO opportunity sitting right there for anyone willing to fill in a text field.

## Why Does Alt Text Matter?

Alt text sits at the intersection of accessibility, [SEO](/glossary/seo), and user experience. Ignore it, and you're losing on all three.

- **Accessibility compliance**. The ADA and WCAG 2.1 guidelines require alt text on meaningful images. Lawsuits over web accessibility have increased 300%+ since 2018. It's not optional.
- **Image search traffic**. Google Images drives significant [organic traffic](/glossary/organic-traffic). Without alt text, Google can't index your images properly, and you miss out on that traffic entirely.
- **[On-page SEO](/glossary/on-page-seo) signals**. Alt text gives Google additional context about your page's content. An article about kitchen remodeling with properly described images reinforces the page's topical relevance.
- **Fallback when images break**. If an image fails to load (slow connection, broken URL, email clients blocking images), alt text appears in its place. Users still understand what was supposed to be there.

Every image on your site should have alt text. Decorative images (borders, spacers) get an empty alt attribute (`alt=""`). Everything else gets a description.

## How Alt Text Works

Writing alt text is simple in concept. Doing it well requires understanding what different systems need from it.

### How Screen Readers Use It

When a screen reader encounters an image, it reads the alt text aloud. If the alt text says "stock photo of business meeting," that's what the user hears. Useless. If it says "5 team members reviewing a marketing report around a conference table," the user understands the context. Write for the person listening, not for a search engine.

### How Google Uses It

Googlebot can't "see" images the way humans do. It relies on alt text, surrounding text, file names, and structured data to understand image content. Google's own documentation states that alt text is "extremely useful" for Google Images ranking. It's one of the strongest [image SEO](/glossary/image-seo) signals you can control.

### The HTML Implementation

Alt text lives in the `alt` attribute of the `<img>` tag:

`<img src="dental-office-reception.jpg" alt="Modern dental office reception area with front desk staff greeting a patient">`

Most CMS platforms (WordPress, Webflow, Ghost) have dedicated alt text fields in their image upload interfaces. You don't need to edit HTML directly.

### What Happens Without Alt Text

If an image has no alt attribute at all, screen readers might read the file name instead. Something like "IMG_4392.jpg." Useless. If the alt attribute is present but empty (`alt=""`), screen readers skip the image entirely, which is correct behavior for decorative images but wrong for meaningful ones.

## Types of Alt Text

Not every image needs the same treatment:

- **Informative alt text**. Describes what the image shows and why it matters. Used for photos, illustrations, charts, and graphics that convey information. "Bar chart showing 40% increase in organic traffic from January to June 2025."
- **Functional alt text**. Describes what a clickable image does. Used for buttons, icons, and linked images. "Search button" or "Download PDF report."
- **Decorative alt text (empty)**. Used for purely decorative images that add no information. Set `alt=""` so screen readers skip them. Background patterns, divider lines, and decorative icons fall here.
- **Complex alt text**. Used for charts, graphs, and infographics that contain dense data. The alt text provides a summary, and a longer description goes in a `longdesc` attribute or nearby text.

Getting the type right matters. Over-describing decorative images clutters the screen reader experience. Under-describing informative images loses both accessibility and SEO value.

## Alt Text Examples

**Example 1: A restaurant's menu page**
Bad alt text: "food" or "dish photo" or no alt text at all. Good alt text: "Grilled salmon with roasted vegetables and lemon butter sauce served on a white plate." The descriptive version helps Google rank the image for "grilled salmon" searches and helps visually impaired users understand the menu item.

**Example 2: A real estate listing**
Bad: "house exterior." Good: "Two-story colonial home with red brick facade, white columns, and landscaped front yard at 123 Main Street." A [local SEO](/glossary/local-seo) win. The detailed description includes property features that match what homebuyers search for in Google Images.

**Example 3: An ecommerce product page**
Bad: "product image 1." Good: "Nike Air Max 90 running shoe in white and grey, side view." This alt text includes the brand, product name, color, and angle. Exactly what Google needs to surface it in Shopping and Image search results. Using theStacc-published blog content alongside properly optimized product images creates a strong [on-page SEO](/glossary/on-page-seo) foundation.

## Alt Text vs. Title Text

These get confused constantly, but they serve completely different purposes.

| | Alt Text | Title Text |
|---|---|---|
| **Purpose** | Describes the image for accessibility and SEO | Provides supplementary info on hover |
| **Required** | Yes (WCAG compliance) | No |
| **SEO impact** | Strong (primary image ranking signal) | Minimal |
| **Screen reader** | Read aloud automatically | Sometimes read, depends on settings |
| **Visibility** | Shown when image fails to load | Shown as tooltip on mouse hover |

Alt text is mandatory. Title text is optional and mostly cosmetic. Focus your effort on alt text.

## Alt Text Best Practices

- **Be specific and concise**. Describe what's in the image in 125 characters or fewer. Screen readers may cut off longer descriptions. "Golden retriever catching a frisbee in a park" beats "dog" every time.
- **Include keywords naturally, not forcefully**. If the image is on a page about [keyword research](/glossary/keyword-research), and the image shows a keyword analysis tool, mention that. But don't stuff: "keyword research keyword tool best keyword research SEO keywords" is spam.
- **Don't start with "image of" or "photo of"**. Screen readers already announce it's an image. Starting with "image of" is redundant. Jump straight to the description.
- **Describe function for clickable images**. If an image is a link or button, the alt text should describe the action, not the image. A magnifying glass icon that triggers search should have `alt="Search"`. Not `alt="magnifying glass."
- **Automate where possible**. When publishing at scale, maintaining consistent alt text gets hard. theStacc includes optimized alt text in every article it publishes, so images are accessible and SEO-ready from day one.

## Frequently Asked Questions

### How long should alt text be?

Keep it under 125 characters. Most screen readers cut off alt text around that length. For complex images like infographics, provide a brief alt text summary and add a longer description in the surrounding page content.

### Does alt text affect Google rankings?

Yes. Alt text is a confirmed ranking factor for Google Images and provides supporting context for web search rankings. Google's Search Central documentation explicitly recommends writing descriptive alt text for [on-page SEO](/glossary/on-page-seo).

### Should every image have alt text?

Every meaningful image needs alt text. Decorative images (spacers, background patterns, visual flourishes) should have empty alt attributes (`alt=""`) so screen readers skip them. The key question: does this image convey information? If yes, describe it.

### Can alt text be too long?

Yes. Excessively long alt text is frustrating for screen reader users and can look like [keyword stuffing](/glossary/keyword-stuffing) to Google. Keep descriptions focused. If an image needs a paragraph of explanation, put that in the body text near the image. Not in the alt attribute.

---

Want every blog post published with proper alt text, [heading tags](/glossary/heading-tags), and on-page SEO built in? theStacc publishes 30 SEO-optimized articles to your site every month. Automatically. [Start for $1 →](https://app.thestacc.com)

## Sources

- [Google Search Central: Image SEO Best Practices](https://developers.google.com/search/docs/appearance/google-images)
- [WebAIM: Alternative Text Guide](https://webaim.org/techniques/alttext/)
- [WebAIM: The WebAIM Million (Annual Accessibility Report)](https://webaim.org/projects/million/)
- [W3C: WCAG 2.1 Image Requirements](https://www.w3.org/WAI/tutorials/images/)
- [Moz: Image SEO Guide](https://moz.com/learn/seo/image-seo)
