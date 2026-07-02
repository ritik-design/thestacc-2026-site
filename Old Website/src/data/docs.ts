export type DocsPage = {
  title: string;
  slug: string;
  description: string;
  popular?: boolean;
  content: string;
};

export type DocsCategory = {
  name: string;
  slug: string;
  items: DocsPage[];
};

export const docsCategories: DocsCategory[] = [
  {
    name: 'Getting started',
    slug: 'getting-started',
    items: [
      {
        title: 'Introduction',
        slug: 'introduction',
        description: 'Learn what theStacc does, how it helps local businesses grow organically with AI-powered SEO, and how to get started.',
        popular: true,
        content: `theStacc is an AI-powered marketing automation platform that helps small businesses get found online. It handles SEO content creation, local search optimization, and social media management - all on autopilot.

## Three core modules

### Content SEO

Generates AI-written, SEO-optimized blog posts and publishes them to your website daily. Includes keyword research, content planning, image generation, SEO scoring, and automatic publishing to WordPress, Webflow, Ghost, and Zepio - or any custom site via webhook.

### Local SEO

Optimizes your Google Business Profile, manages customer reviews with AI-generated responses, publishes local posts, and tracks your visibility in "near me" searches and the Google Map Pack.

### Social Media

Creates and publishes AI-generated posts across Instagram, Facebook, LinkedIn, and X (Twitter). Includes brand style customization, content pillars, multi-language support, and platform-specific formatting.

## How it works

1. **Connect** - Link your website, Google Business Profile, and social accounts
2. **Configure** - Set your business details, target audience, keywords, and brand style
3. **Generate** - AI creates optimized content across all your channels
4. **Publish** - Content publishes automatically or waits for your approval
5. **Track** - Monitor rankings, reviews, and engagement from your dashboard

## Who it's for

theStacc is built for small businesses, agencies, and marketers who want consistent online presence without the manual effort. Each module works independently - use one or all three.

## Next steps

- [Quick Start](/docs/getting-started/quick-start) to get set up in minutes
- [Key Concepts](/docs/getting-started/key-concepts) to understand the platform
- Explore [Content SEO](/docs/content-seo/overview), [Local SEO](/docs/local-seo/overview), or [Social Media](/docs/social-media/overview)`,
      },
      {
        title: 'Quick Start',
        slug: 'quick-start',
        description: 'Get from signup to your first AI-generated blog post, local SEO update, or social media post in under 10 minutes.',
        popular: true,
        content: `This guide walks you through setting up theStacc and generating your first content. The onboarding flow guides you through each step.

## Create your account

Sign up at [app.thestacc.com/signup](https://app.thestacc.com/signup) with email/password or Google OAuth. You'll need to verify your email before accessing the dashboard.

## Choose your modules

During onboarding, select which modules to activate:

- **Content SEO** - Blog content generation and publishing
- **Local SEO** - Google Business Profile optimization
- **Social Media** - Social post creation and scheduling

You can enable additional modules anytime from your dashboard.

## Content SEO setup

1. **Enter your website URL** - theStacc analyzes your site content and SEO
2. **Review target audience** - AI generates buyer personas (ICPs) based on your business
3. **Set target locations** - Choose global reach or specific geographic areas
4. **Connect publishing** - Link WordPress, or set up a webhook for custom sites
5. **Start your trial** - Begin generating content immediately

## Local SEO setup

1. **Search for your business** - Find your business listing on Google
2. **Confirm your business** - Select the correct listing from results
3. **Add business context** - Services offered, customer pain points, business hours
4. **Start your trial** - Begin optimizing your local presence

## Social Media setup

1. **Connect platforms** - Link Instagram, Facebook, LinkedIn, and/or X accounts
2. **Set brand style** - Upload logo, choose colors, fonts, and brand voice
3. **Define content pillars** - Select topics like Educational, Behind the Scenes, etc.
4. **Generate content plan** - AI creates your first batch of social posts

## Monitor your progress

Your dashboard shows an overview of all active modules with progress indicators, pending actions, and milestone notifications.`,
      },
      {
        title: 'Key Concepts',
        slug: 'key-concepts',
        description: "Understand theStacc's modules, content plans, publishing modes, and automation features before you get started.",
        content: `Core concepts that the platform is built around.

## Modules

Modules are the three feature areas of theStacc. Each module operates independently with its own settings, content plans, and publishing options:

- **Content SEO** - Blog generation and website publishing
- **Local SEO** - Google Business Profile and local search
- **Social Media** - Multi-platform social posting

Each module has its own subscription and trial period.

## Content plans

A content plan tells theStacc what to create. For Content SEO, this means keywords to target and blog frequency. For Social Media, this means content pillars, platforms, and posting schedule. Plans can run simultaneously.

## Publishing modes

Every module supports three publishing modes:

- **No Auto Publish** - Content saved as drafts. You publish manually when ready.
- **Requires Approval** - Content enters a "Pending Review" state. You approve, edit, or reject before it goes live.
- **Auto Publish** - Content publishes automatically after generation. No review step.

You can change your publishing mode anytime in module settings.

## SEO scoring

Every generated blog post receives an SEO score from 0-100. The score evaluates keyword optimization, content length, heading structure, image usage, and link distribution. Posts below your quality threshold are automatically regenerated.

## Target audience (ICP)

Ideal Customer Profiles define who your content is written for. theStacc generates audience segments based on your business and lets you enable or disable segments. This shapes the tone, topics, and focus of all generated content.

## Integrations

Integrations connect theStacc to external platforms for publishing and data. Current integrations include WordPress.com, WordPress.org (self-hosted), Webflow, Ghost, Zepio, custom webhooks, Google Business Profile, Instagram, Facebook, LinkedIn, and X.

## Team roles

- **Owner** - Full access including billing and project deletion
- **Admin** - Full access except billing and deletion
- **Editor** - Can create, edit, and publish content
- **Viewer** - Read-only access`,
      },
    ],
  },
  {
    name: 'How it works',
    slug: 'how-it-works',
    items: [
      {
        title: 'The content engine',
        slug: 'content-engine',
        description: 'How theStacc turns your business details into publish-ready blog posts, local posts, and social content - the full generation pipeline, stage by stage.',
        popular: true,
        content: `theStacc is not a single "write me a post" button. Behind every piece of content is a multi-stage engine that researches, plans, writes, illustrates, scores, and publishes - so the output reads like a strategist wrote it, not a chatbot.

This page explains what actually happens each time content is created.

![How the content engine turns your inputs into a published post, in six stages](/images/docs/content-engine-pipeline.svg)

## The blog pipeline

When theStacc creates a blog post, it moves through six stages:

1. **Content plan** - Before any writing happens, theStacc builds a rolling content calendar from your keywords, your business, and what you have already published. It rotates keywords so you never get two posts chasing the same term back-to-back, and spaces topics out across the month.
2. **Plan the post** - For each topic, the engine first designs the article: an SEO-focused title, a meta description, the full H2/H3 outline, where images should go, and the secondary terms to weave in. Planning first is what keeps posts well-structured instead of rambling.
3. **Write the post** - The engine then writes the full article in clean HTML - proper heading hierarchy, your target keyword used naturally, internal-link markers, and image placeholders. It writes grounded in your uploaded sources and in your brand voice (see [Quality & safety](/docs/how-it-works/quality-safety)).
4. **Generate images** - Original hero and in-content visuals are generated to match the article and your brand, then attached automatically. No stock photos, no hunting for images.
5. **SEO scoring** - Every finished post gets a 0-100 score across keyword placement, length, structure, images, and links. Posts that fall below your quality bar are regenerated automatically.
6. **Review and publish** - The draft is saved instantly so you can read it while images finish. From there it follows your publishing mode - straight to your site, into a review queue, or held as a draft (see [Publishing](/docs/content-seo/publishing)).

The result: a complete, on-brand, SEO-ready article with images and metadata - in one pass, on a schedule.

## The local SEO pipeline

Local posts follow the same plan-first philosophy, tuned for Google Business Profile:

- theStacc builds a monthly plan of Google Business Profile posts and rotates the "hook" of each one (a result, a question, a seasonal angle, a trust signal) so your profile never looks repetitive.
- Posts are written to the length Google actually shows before the "Read more" fold, with built-in guardrails that strip things that violate Google's rules - fabricated discount codes, stuffed phone numbers, spammy openers.
- Offers and events get their own short, card-friendly titles.

## The social pipeline

Social content is generated as a coordinated monthly plan rather than one-off posts:

- The engine selects a balanced mix of **content pillars** (education, authority, social proof, brand personality, community, conversion) and **post formats** so your feed has variety instead of the same template every day.
- Each caption is written natively for its platform - the right length, hashtag count, and link placement for Instagram, Facebook, LinkedIn, or X. A caption is never just copy-pasted across networks.
- Matching visuals are generated for each post, including multi-slide carousels, sized correctly per platform.

## What feeds the engine

The quality of the output comes from what the engine is given to work with:

- **Your business profile** - what you do, who you serve, your locations and services.
- **Your keywords and topics** - what you want to rank for, plus a "topics to avoid" list.
- **Your sources** - documents or pasted text the engine treats as ground truth.
- **Your brand voice** - learned from writing samples so the output sounds like you.

Garbage in, garbage out works in reverse here: the more context you give theStacc, the sharper every post becomes. See [Business Setup](/docs/content-seo/business-setup) and [How the AI works](/docs/how-it-works/how-the-ai-works).`,
      },
      {
        title: 'How the AI works',
        slug: 'how-the-ai-works',
        description: 'theStacc orchestrates several purpose-built AI engines - one for writing, a fast one for quick tasks, and one for images - so content is high quality, fast, and affordable.',
        content: `theStacc is not a thin wrapper around one chatbot. It orchestrates several specialised AI engines, each picked for the job it is best at. You never choose or configure them - the platform routes every task to the right engine automatically.

![How theStacc routes each task to the writing, fast, or image engine - plus live data](/images/docs/ai-engines.svg)

## A multi-engine approach

### The writing engine

The heavy lifting - planning and writing long-form blog posts, monthly content plans, and structured social captions - runs on a top-tier writing engine. It works in two steps (plan, then write) using a structured, guided process, which is why posts come out well-organised and on-topic rather than meandering.

### The fast engine

Not every task needs the most powerful model. Quick jobs - learning your brand voice from writing samples, running safety and compliance checks, and drafting the first preview post so you see results instantly - run on a faster, lighter engine. This is what keeps the app feeling responsive and keeps generation affordable.

### The image engine

Hero images, in-article illustrations, and social graphics (including carousels) are produced by a dedicated image engine, sized correctly for each placement and styled to your brand. Every image is original - there is no stock-photo library involved.

### Live data

Planning and tracking are grounded in live data, not guesses: real keyword and search-volume signals shape your content plan, and local ranking data powers your "near me" and Map Pack tracking.

## Why more than one engine

Using several engines instead of one means theStacc can:

- **Go deep where it matters** - full reasoning power for writing and planning, where quality shows.
- **Stay fast where it counts** - lightweight processing for quick tasks, so the dashboard never feels slow.
- **Keep costs sane** - matching each task to the right-sized engine is what lets theStacc generate content at volume without the price ballooning.

## Always improving, nothing for you to manage

The engines behind theStacc are upgraded continuously as the technology improves. Because everything is abstracted behind the platform, your content quality goes up over time with zero work on your side - no settings to change, no migrations, no re-learning. You focus on your business; theStacc handles the rest.`,
      },
      {
        title: 'Quality & safety',
        slug: 'quality-safety',
        description: 'The systems that keep theStacc content on-brand, non-repetitive, accurate, and compliant - brand voice, grounding, anti-repetition, SEO scoring, and the compliance layer.',
        content: `Automated content is only useful if it is good, consistent, and safe to publish. Several systems run on every generation to make sure of that.

## Brand voice

Upload a few of your existing articles or posts and theStacc learns how you write - tone, vocabulary, sentence rhythm, and the words you avoid - then applies that voice to everything it generates. Your automated content sounds like you, not like generic AI.

## Grounding in your sources

Upload documents (PDF, Word, text) or paste in material, and the engine treats it as ground truth while writing. This keeps facts, product details, and claims accurate instead of invented.

## Anti-repetition

Publishing on a schedule only works if the content stays fresh. theStacc actively prevents repetition:

- **Keyword rotation** - it will not target the same keyword twice in a rolling window.
- **Hook and opening diversity** - openings and angles are varied so posts do not all start the same way.
- **Statistic and topic de-duplication** - it tracks what it has already used and steers around it.

## SEO scoring

Every blog post is scored 0-100 on keyword placement, length, heading structure, image usage, and links. Anything below your quality threshold is regenerated automatically, so weak posts never reach your site.

## Topics to avoid

Set a per-project "do not write about" list and theStacc steers clear of those subjects entirely - useful for competitors, sensitive topics, or off-brand themes.

## Compliance (for regulated businesses)

Businesses in regulated fields (legal, healthcare, financial, real estate, and similar) can turn on an optional compliance layer. When enabled, theStacc:

- Injects the disclosures and language your field requires into generated content.
- Routes posts through a review gate before they can publish, flagging anything that needs a human check.

Compliance is opt-in and acts as an assistant, not a guarantee - the licensed professional stays responsible for what is published. See [Publishing](/docs/content-seo/publishing) for how the review gate works.

## Built-in platform guardrails

Beyond your settings, theStacc enforces the rules of each destination automatically - for example, stripping fabricated promo codes and phone numbers from Google Business Profile posts (which Google prohibits) and keeping captions within each social network's limits.`,
      },
    ],
  },
  {
    name: 'Content SEO',
    slug: 'content-seo',
    items: [
      {
        title: 'Overview',
        slug: 'overview',
        description: 'Overview of the Content SEO dashboard, calendar view, blog statuses, and the full content generation pipeline.',
        popular: true,
        content: `The Content SEO module generates AI-powered blog posts and publishes them to your website on autopilot.

## Dashboard

Your Content SEO dashboard shows everything at a glance:

### Calendar view

A monthly calendar displaying all your blogs with color-coded status indicators:

- **Scheduled** (slate) - Not yet generated
- **Generating** (blue) - AI generation in progress
- **Pending Review** (amber) - Awaiting your approval
- **Approved** (emerald) - Ready to publish
- **Published** (green) - Live on your website
- **Rejected** (rose) - Declined by you
- **Paused** (violet) - Generation paused

Navigate between months and expand the calendar to see the full picture.

### Stats bar

Quick metrics showing total blogs generated, scheduled vs published ratio, and pending review count.

### Blog list view

A sortable table view with columns for title, keyword, difficulty score, search volume, status, and scheduled date. Supports bulk selection and per-blog dropdown actions.

## Content generation pipeline

When generation is active, a real-time progress panel shows:

- Current progress (Day X of Y)
- Rotating status messages during generation
- Preview of recently generated blogs
- Animated processing state

Generation is resumable - if you leave and come back, it picks up where it left off.

## Blog detail page

Click any blog to open the full editor with:

- **Tiptap WYSIWYG editor** - Rich text editing with bold, italic, headings, lists, blockquotes, code blocks, links, and images
- **Blog metadata** - Title, slug, meta title, meta description, featured image, category, and tags
- **Section management** - Regenerate specific sections or images individually
- **SEO analysis panel** - Live SEO score with category-by-category breakdown and specific improvement suggestions
- **Timeline** - Key dates, associated keywords, and integration sync status`,
      },
      {
        title: 'Business Setup',
        slug: 'business-setup',
        description: 'Configure your website URL, define your target audience, add competitors, and set your service locations for AI content.',
        content: `Before generating content, theStacc needs to understand your business. These settings shape every piece of content the AI creates.

## Website information

Navigate to **Content SEO > Settings > Business Details**. Enter:

- **Website name** and **URL**
- **Business description** - A brief overview of what you do
- **Website logo** - Upload your logo for branded content

## Features and pain points

Add your key business features and customer pain points as tags. These tell the AI what to emphasize and what problems to address in generated content.

- **Features** - What your product/service offers (e.g., "24/7 support", "Free shipping")
- **Pain points** - Problems your customers face (e.g., "Slow delivery times", "Complicated setup")

## Target audience (ICP)

theStacc generates Ideal Customer Profiles based on your business. Each segment includes a name and description. You can:

- Enable or disable segments to control who content targets
- Edit segment descriptions for more accuracy
- Add new custom segments
- Delete irrelevant segments

## Business location

Set whether your business is online or has a physical location:

- **Online** - Choose Global or Specific Locations
- **Offline/Physical** - Specify your locations (required)

For specific locations, select countries and states/regions. This affects keyword targeting and local content relevance.

## Competitors

Add competitors by their website URL under **Settings > Competitors**. For each competitor:

- theStacc auto-fetches their favicon
- Add a "How we differ" description explaining your advantage
- The AI uses competitor info to differentiate your content

## Sitemap configuration

Under **Settings > Content Details**, configure:

- **Sitemap URL** - Enter or auto-discover your sitemap
- **Blog address** - The URL path where blogs live on your site
- **Example articles** - Up to 3 example blog URLs to help the AI match your content style`,
      },
      {
        title: 'Content Plans & Keywords',
        slug: 'content-plans',
        description: 'Manage your target keywords, create structured content plans, and control your AI-driven blog publishing strategy.',
        content: `Content plans and keywords drive your blog strategy. They determine what topics the AI writes about and which search terms you target.

## Keyword management

Navigate to **Content SEO > Settings > Keywords** to manage your keyword list.

### Active vs inactive

Keywords are split into two sections:

- **Active keywords** (max 30) - Currently being targeted in content generation
- **Inactive keywords** - Paused, not being used for new content

Toggle keywords between active and inactive at any time. You can also edit keyword names or delete them.

### Adding keywords

Click **Add Keywords** to open the keyword modal. Each keyword shows:

- **Search volume** - Monthly search count
- **Difficulty** - How competitive the keyword is (0-100)
- **Relevance** - How well it matches your business

We recommend starting with 20-30 keywords that have moderate difficulty and clear relevance to your services.

## Content plan generation

When you activate your Content SEO module, theStacc creates a content plan that maps keywords to blog posts across your calendar. The plan considers:

- Your active keyword list
- Target audience segments
- Business features and differentiators
- Competitor landscape
- Publishing frequency

## Publishing schedule

Configure how many blogs to generate and when:

- **Posts per week** - How many blog posts to generate
- **Publishing days** - Which days to publish on
- **Publishing time** - What time posts go live (timezone-aware)

## Promotions

Under **Settings > Promotions**, theStacc can detect location-based events and festivals to create timely promotional content:

- Automatic event detection based on your target locations
- Categories: National Holidays, Cultural Festivals, Commercial Events, Awareness Days, and more
- Monthly calendar view of detected events
- Generate promotional content ideas tied to events
- Save promotion plans to your content calendar`,
      },
      {
        title: 'Blog Generation',
        slug: 'blog-generation',
        description: 'How theStacc AI generates blog posts, quality controls content, calculates SEO scores, and uses the built-in editor.',
        content: `theStacc uses a multi-step AI pipeline to generate each blog post. Every article goes through research, writing, image generation, and quality checks.

## The generation pipeline

### Outline creation

The AI researches your target keyword by analyzing search intent and top-ranking content. It builds a structured outline with headings, key points, internal linking opportunities, and FAQ suggestions.

### Content writing

Using the outline, the AI generates a complete blog post. The process prioritizes:

- **Accuracy** - Factual, well-researched information
- **Readability** - Clear language with varied sentence structure
- **SEO structure** - Proper heading hierarchy, keyword placement, and meta data
- **Brand voice** - Matches your configured writing style

### Image generation

Each blog post includes AI-generated images:

- A featured image for the post header
- Section images where visual content adds value
- Images match your selected image style (Photorealistic, Flat Illustration, Cinematic, Watercolor, Sketch, or Brand & Text)

## SEO scoring

Every post receives an SEO score (0-100) evaluating:

- **Keyword optimization** - Keyword placement and density
- **Content length** - Whether the article is comprehensive enough
- **Heading structure** - Proper H1/H2/H3 hierarchy
- **Image usage** - Alt text, placement, and relevance
- **Link distribution** - Internal and external links

Posts below your quality threshold are automatically regenerated.

## Blog editor

Click any blog to open the Tiptap WYSIWYG editor:

- Full formatting toolbar: bold, italic, strikethrough, headings (H1-H3), bullet/numbered lists, blockquotes, code blocks, links, and images
- Edit title, slug, meta title, and meta description
- Replace or regenerate the featured image
- Regenerate individual sections or images
- Undo/redo support

## Content regeneration

You can regenerate content at multiple levels:

- **Entire blog** - Fully regenerate from scratch
- **Specific section** - Regenerate just one section while keeping the rest
- **Images only** - Regenerate images without changing text
- Previous versions are not kept, so review before regenerating.`,
      },
      {
        title: 'Publishing',
        slug: 'publishing',
        description: 'Configure publishing modes, set up WordPress integration, use webhooks for custom sites, and manage content sync settings.',
        popular: true,
        content: `Once content is generated, theStacc handles publishing to your website. Configure your publishing mode and integrations under **Content SEO > Settings > Publishing**.

![How a generated post reaches your site: your publishing mode decides whether it auto-publishes, waits for approval, or stays a draft](/images/docs/publishing-flow.svg)

## Publishing modes

### No auto publish

Blogs are saved as drafts. You manually review, edit, and publish each one when ready. Best for maximum control over every piece of content.

### Requires approval

Blogs enter a "Pending Review" state. You receive a notification, review the post, make edits if needed, then approve or reject. Rejected posts can be regenerated. Best balance of control and convenience.

### Auto publish

Blogs publish automatically after generation and SEO scoring. No review step required - but you can still unpublish or edit after it goes live. Requires an active publishing integration. Best for hands-off operation.

## Publishing integrations

### WordPress.com

Connect via OAuth authentication:

1. Go to **Settings > Publishing > Integrations**
2. Click **Connect WordPress.com**
3. Authorize theStacc to access your WordPress site
4. Select your target site

Posts are created as standard WordPress posts with title, body, featured image, categories, tags, and SEO meta data (compatible with Yoast and RankMath).

### WordPress.org (self-hosted)

Connect using Application Passwords:

1. In your WordPress admin, go to **Users > Profile > Application Passwords**
2. Create a new application password for theStacc
3. In theStacc, enter your site URL and application password
4. Test the connection

### Webhook

For custom websites or CMS platforms not directly supported:

1. Enter your custom endpoint URL
2. Add any required custom headers (key-value pairs)
3. Click **Test Connection** to verify reachability
4. Click **Sample Payload** to send the real publish-shape JSON and validate your parser

Your receiver must handle **two events**: \`test.ping\` (no blog fields, returned by Test Connection) and \`blog.published\` (full blog payload). Respond to publish events with \`{"ok": true, "url": "<live-post-url>", "id": "<your-cms-id>"}\` so theStacc can show a clickable **View live post** link.

See [Connect Platforms → Custom Webhook](/docs/content-seo/connect-platforms/) for the full request/response contract and a minimal receiver example.

### Ghost

Connect your Ghost blog for direct publishing via the Ghost Admin API. Enter your Ghost site URL and API key to get started.

### Webflow

Publish blog content directly to your Webflow CMS. theStacc uses a Webflow API token — generated in Site Settings → Apps & Integrations → API Access — with **CMS: Read and write** and **Sites: Read and publish** permissions. After connecting, theStacc creates each new blog as a CMS item, optionally publishes the site so it goes live immediately, and stores the live URL on the post. See [Connect Platforms → Webflow](/docs/content-seo/connect-platforms/) for the full setup walkthrough including permission selection.

### Zepio

Publish directly to your Zepio site. Generate a developer API token in Zepio, paste it into theStacc, and each new blog is created on your Zepio site automatically.

### Shopify

Publish blog posts to your Shopify store's blog. Connect your Shopify store and theStacc handles publishing to your store's built-in blog.

## Integration management

Each connected integration shows:

- Connection status (Active/Inactive)
- Last sync timestamp
- Connection details
- Test button to verify the connection
- Toggle to activate or deactivate
- Disconnect option`,
      },
      {
        title: 'Preferences',
        slug: 'preferences',
        description: 'Set your writing style, image style, CTA links, and other content preferences to match your brand standards.',
        content: `Customize how theStacc generates content under **Content SEO > Settings > Preferences**.

## Writing style

Choose from 12 writing styles that shape the tone of every generated blog:

- Informative, Simple & Clear, Formal, Casual
- Enthusiastic, Persuasive, Professional, Friendly
- Entertaining, Inspirational, Analytical, Narrative

The selected style is applied consistently across all generated content.

## Image style

Choose from 6 image generation styles:

- **Photorealistic** - Lifelike photography style
- **Flat Illustration** - Clean, modern vector illustrations
- **Cinematic** - Dramatic, film-quality visuals
- **Watercolor** - Artistic, hand-painted look
- **Sketch** - Hand-drawn, pencil illustration style
- **Brand & Text** - Uses your brand logo and colors

## Internal links (CTA)

Configure Call-to-Action links that get woven into generated content:

- **Primary link** - Your main CTA (e.g., product page, signup)
- **Secondary link** - Supporting CTA (e.g., pricing, demo)
- **Tertiary link** - Additional link (e.g., contact, resources)

Each link includes a label, URL, and optional notes for context.

## Content toggles

Enable or disable specific content features:

- **Image inclusion** - Whether to generate and include images
- **Call-to-actions** - Whether to include CTA blocks in posts
- **Internal links** - Whether to weave in your configured links
- **YouTube integration** - Add your YouTube channel URL to auto-link relevant videos in blog content`,
      },
      {
        title: 'Connect Platforms',
        slug: 'connect-platforms',
        description: 'Set up all publishing integrations including WordPress, Ghost, Webflow, Shopify, and custom Webhook endpoints.',
        content: `theStacc supports 6 publishing integrations for Content SEO. Connect one or more to automatically publish blog content to your website. Manage all integrations under **Content SEO > Settings > Publishing**.

## WordPress.com

Hosted WordPress sites. Recommended for WordPress.com users.

1. Click **Connect WordPress.com**
2. Authorize via secure OAuth connection
3. Sign in and grant theStacc access
4. Select your target site if you have multiple

Each published blog includes title, body content (HTML), featured image, categories, tags, SEO meta data (Yoast/RankMath compatible), and post slug.

## WordPress.org

Self-hosted WordPress sites. Connect with an application password.

1. In your WordPress admin, go to **Users > Profile > Application Passwords**
2. Create a new password with the name "theStacc"
3. Copy the generated password
4. In theStacc, enter your site URL and the application password
5. Click **Test Connection** to verify

Requires WordPress 5.6+ with REST API enabled (on by default). HTTPS recommended.

## Custom Webhook

Send blog posts to any platform via HTTP. Works with any system that accepts HTTP POST requests.

> **Building the receiver?** See the [Webhook Reference](/docs/developers/webhook-reference) for the full developer guide — handshake, signing, every event, every field, response contract, database schemas, and ready-to-paste receiver examples in 6 languages.

1. Enter your **endpoint URL**
2. Add **custom headers** (optional) — for authentication tokens, API keys, or routing
3. Click **Test Connection** to verify the URL is reachable
4. Click **Sample Payload** to send the real publish-shape JSON and validate your parser

### Two events your receiver must handle

theStacc sends a different payload shape for each button. Branch on the \`event\` field — your receiver should handle both, or it will fail Test Connection even when the publish path works.

**\`event: "test.ping"\`** — fired by **Test Connection**. Liveness probe only. No blog fields.

\`\`\`json
{
  "event": "test.ping",
  "message": "This is a test from theStacc",
  "timestamp": "2026-04-30T12:00:00Z"
}
\`\`\`

Respond \`200 {"ok": true}\`. Do **not** require \`title\`, \`slug\`, or \`content\` for this event — there are none.

**\`event: "blog.published"\`** — fired on every real publish (and by **Sample Payload** with a \`preview-\` prefixed \`blog_id\` for receiver validation).

\`\`\`json
{
  "event": "blog.published",
  "blog_id": "8f3e...",
  "title": "10 SEO mistakes to avoid in 2026",
  "slug": "10-seo-mistakes-to-avoid-in-2026",
  "content": "<h2>Introduction</h2><p>...</p>",
  "excerpt": "Short description...",
  "excerpt_short": "Short description... (≤256 chars, word-boundary trimmed)",
  "meta_title": "10 SEO mistakes to avoid in 2026",
  "meta_description": "...",
  "featured_image_url": "https://cdn.thestacc.com/blogs/...jpg",
  "categories": ["SEO"],
  "tags": ["seo", "2026"],
  "keyword": "seo mistakes 2026",
  "published_at": "2026-04-30T12:00:00Z"
}
\`\`\`

If \`blog_id\` starts with \`preview-\`, it's a sample call — accept it but skip your CMS write so test runs don't pollute your database.

### What to return so the live URL appears in theStacc

Respond with \`200\` (or \`201\`) and a JSON body containing the live post URL. theStacc reads the response and stores both fields against the blog so the dashboard shows a clickable **View live post** link.

\`\`\`json
{
  "ok": true,
  "url": "https://your-cms.com/blog/10-seo-mistakes-to-avoid-in-2026",
  "id": "internal-cms-post-id"
}
\`\`\`

- **\`url\`** (or \`published_url\`) — the public URL of the blog on your site. If omitted, theStacc shows a *"Sent to webhook — your receiver didn't return a public URL"* warning.
- **\`id\`** — your internal CMS post id. Stored as \`external_post_id\` so future updates / unpublishes can target the right record.

For preview calls (\`blog_id\` starts with \`preview-\`), it's fine to skip both fields and return \`{"ok": true, "skipped": true}\`.

### Minimal receiver example (Next.js / Vercel)

\`\`\`js
export async function POST(request) {
  const body = await request.json();

  if (body.event === "test.ping") {
    return Response.json({ ok: true });
  }

  if (body.event === "blog.published") {
    if (body.blog_id?.startsWith("preview-")) {
      return Response.json({ ok: true, skipped: true });
    }
    const post = await cms.posts.create({
      title: body.title,
      slug: body.slug,
      content: body.content,
      // ...
    });
    return Response.json({
      ok: true,
      url: \`https://your-cms.com/blog/\${post.slug}\`,
      id: post.id,
    });
  }

  return Response.json({ error: "Unknown event" }, { status: 400 });
}
\`\`\`

### Verify webhook signatures (recommended)

When you configure a webhook secret, theStacc signs every request with HMAC-SHA256 and sends the hex digest in the \`X-Webhook-Signature\` header. Verify it on every request — without verification, anyone who guesses your endpoint URL can post fake blogs to your CMS.

**Critical:** the signature is computed over the **raw request body** that theStacc sent, which is JSON serialized in compact form (\`json.dumps(payload, separators=(',', ':'))\` — no whitespace between keys and values). If you re-serialize the parsed JSON before hashing, the byte-for-byte representation will differ and the hashes won't match. **Always hash the raw bytes you receive over the wire.**

**Node.js / Next.js:**

\`\`\`js
import crypto from 'crypto';

export async function POST(request) {
  const rawBody = await request.text();           // raw bytes — do NOT parse first
  const sigHeader = request.headers.get('x-webhook-signature') || '';
  const expected = crypto
    .createHmac('sha256', process.env.STACC_WEBHOOK_SECRET)
    .update(rawBody)
    .digest('hex');

  // Length-check before timingSafeEqual — Node throws RangeError on
  // mismatched buffer lengths (e.g. when a probe sends a short or
  // empty X-Webhook-Signature). Crashing the receiver on every
  // garbage probe is a worse failure mode than 401-rejecting.
  const sigBuf = Buffer.from(sigHeader, 'utf8');
  const expBuf = Buffer.from(expected, 'utf8');
  if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) {
    return new Response('Invalid signature', { status: 401 });
  }

  const body = JSON.parse(rawBody);
  // ... handle event
}
\`\`\`

**Python / FastAPI:**

\`\`\`python
import hmac, hashlib, os
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
SECRET = os.environ["STACC_WEBHOOK_SECRET"].encode()

@app.post("/stacc-webhook")
async def receive(request: Request):
    raw = await request.body()
    sig = request.headers.get("x-webhook-signature", "")
    expected = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(401, "Invalid signature")
    body = await request.json()
    # ... handle event
\`\`\`

**Python / Flask:**

\`\`\`python
import hmac, hashlib, os
from flask import Flask, request, abort

app = Flask(__name__)
SECRET = os.environ["STACC_WEBHOOK_SECRET"].encode()

@app.post("/stacc-webhook")
def receive():
    raw = request.get_data()
    sig = request.headers.get("X-Webhook-Signature", "")
    expected = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        abort(401)
    body = request.get_json()
    # ... handle event
\`\`\`

**PHP:**

\`\`\`php
<?php
$raw = file_get_contents('php://input');
$sig = $_SERVER['HTTP_X_WEBHOOK_SIGNATURE'] ?? '';
$expected = hash_hmac('sha256', $raw, getenv('STACC_WEBHOOK_SECRET'));
if (!hash_equals($expected, $sig)) {
    http_response_code(401);
    exit('Invalid signature');
}
$body = json_decode($raw, true);
// ... handle event
\`\`\`

If no webhook secret is configured, the \`X-Webhook-Signature\` header is omitted and your receiver must trust the URL alone — fine for development, **not** recommended in production.

### All event types

theStacc emits five different events on the same webhook URL. Branch on \`event\`.

| Event | When fired | Payload |
|---|---|---|
| \`test.ping\` | Test Connection button | \`{event, message, timestamp}\` |
| \`blog.published\` | First successful publish | full blog payload (see above) |
| \`blog.updated\` | Re-publish of an existing blog | full blog payload — same shape as \`blog.published\` |
| \`blog.unpublished\` | User unpublishes from theStacc | \`{event, blog_id, title}\` |
| \`blog.deleted\` | User deletes a published blog | \`{event, blog_id, title}\` |

For \`blog.updated\` / \`blog.unpublished\` / \`blog.deleted\`, look up the post in your CMS using the \`external_post_id\` you returned from \`blog.published\` (theStacc stores it and sends \`blog_id\` so you can map back).

### Operational details

- **Timeout:** theStacc waits up to **15 seconds** for a 2xx response. Slow CMS writes (image uploads, search indexing) will time out — return 2xx fast and do heavy work async.
- **No automatic retries.** A 5xx or timeout fails the publish in theStacc and the user sees a "Failed to publish" toast. If your endpoint is occasionally slow, queue the actual CMS write internally and return 2xx immediately.
- **Redirects rejected.** A 3xx response is treated as failure (anti-SSRF guardrail; a public webhook receiver that 302s to an internal address would otherwise bypass URL safety checks).
- **HTTPS only.** \`http://\` URLs and internal/private IP ranges are rejected at save time.
- **Idempotency.** Use \`blog_id\` as a dedupe key. If theStacc ever resends (manual user retry), you'll see the same \`blog_id\`.
- **Test before writing receiver code.** Point your webhook at [webhook.site](https://webhook.site) or [requestbin.com](https://requestbin.com) first to inspect the actual request body and headers, then build your receiver against the real shape.

### Best practices

- Use HTTPS — theStacc rejects \`http://\` and internal addresses.
- Return a 2xx status code. Redirects (3xx) are rejected.
- Verify the \`X-Webhook-Signature\` header on every request when a secret is set.
- Idempotency — use \`blog_id\` as a dedupe key in case of retries.
- Set up error alerting on your endpoint so silent 4xx/5xx responses don't go unnoticed.

## Ghost

Publish directly to your Ghost blog via the Ghost Admin API.

1. Click **Connect Ghost**
2. Enter your Ghost site URL
3. Enter your Ghost Admin API key (found in Ghost Admin > Settings > Integrations)
4. Test the connection

Posts are created with full content, featured images, tags, and meta data.

## Webflow

Publish blog content to your Webflow CMS collections via a Webflow API token.

### Before you start

- Your Webflow workspace must be on a plan that includes the CMS API (Workspace plans with CMS hosting). Free workspaces can read but cannot create CMS items.
- The Webflow site must have been **published at least once from the Designer**. Webflow rejects live CMS publishes if the site has never been published.
- A CMS Collection for blog posts must exist on the site. If you don't have one, create it in Webflow Designer → CMS → New Collection (recommended fields below).

### Step 1 — Generate a Webflow API token

1. In Webflow, open the site you want to connect.
2. Go to **Site Settings → Apps & Integrations → API Access**. You'll see this:

![Webflow Site Settings → Apps & Integrations → API access section](/images/integrations/webflow/api-access-page.webp)

3. **Click the blue "Generate API token" button on the right — NOT "Generate V1 token".** V1 tokens use Webflow's legacy API which theStacc doesn't support.
4. On the next screen, name the token \`theStacc\` and set permissions exactly like this — Webflow shows a dropdown for each scope. The two scopes that need access are CMS and Sites; everything else stays on None.

| Scope | Permission | Underlying API scope | Why |
|---|---|---|---|
| **CMS** | Read and write | \`cms:read\` + \`cms:write\` | Create and update blog items in your collection |
| **Sites** | Read and write | \`sites:read\` + \`sites:write\` | Read site info (for the live URL) and re-publish the site so new posts appear live |
| **Custom code** | None | — | Not used |
| **Pages** | None | — | Not used |
| **Users** | None | — | Not used |
| **Forms** | None | — | Not used |
| **Components** | None | — | Not used |
| **Ecommerce** | None | — | Not used |
| **Authorized user** | Read only | \`authorized_user:read\` | Default — leave as-is |

> Webflow's UI labels (e.g. "Read and publish") are friendlier names for the underlying scopes. The token Stacc actually receives carries the API scopes shown in the right column. Source: [Webflow Data API scopes reference](https://developers.webflow.com/data/reference/scopes).

5. Click **Generate token** and **copy it immediately** — Webflow won't show it again.

### Step 2 — Connect in theStacc

1. In theStacc, open **Content SEO → Settings → Publishing** and toggle Webflow on.
2. Paste the token, give the integration a friendly name, and click Continue.
3. Select your Webflow site from the dropdown.
4. Select the CMS collection where blog posts should land.
5. Map theStacc fields to your Webflow collection fields:
   - **Required:** Title, Content, Slug
   - **Optional:** Featured Image, Meta Description, Excerpt, Tags, Author, Category, Published Date, Is Featured
   - Auto-mapping fills most of these based on field-name matches — review and adjust.
6. Choose a publishing behavior:
   - **Publish Immediately** — items go live the moment theStacc publishes them; theStacc also re-publishes the site so they appear on the live URL.
   - **Save as Draft** — items appear in Webflow as drafts; you publish manually.
   - **Stage for Review** — items are created and ready to publish; you press Publish in Webflow Designer.
7. Click **Create Integration**.

### Recommended CMS collection fields

| Field | Webflow type |
|---|---|
| Name | Plain text (auto-created — title goes here) |
| Slug | URL slug (auto-created) |
| Post Content | Rich text |
| Featured Image | Image |
| Excerpt | Plain text |
| Meta Title | Plain text |
| Meta Description | Plain text |
| Tags | Plain text (comma-separated) |
| Author | Plain text |

> Webflow blog templates often use **Reference / Multi-reference** fields for Categories, Tags, and Authors. theStacc cannot yet auto-create the referenced items, so use **Plain text** fields for these for now.

### Verify

After saving the integration, click **Test Connection**. A green check confirms the token works and the collection is reachable.

### Troubleshooting

- **"Invalid API token"** — token wrong, expired, or revoked. Generate a new one and update the integration.
- **"No CMS collections found"** — the site has no CMS collections. Create one in Designer first.
- **"Item with this slug already exists"** — a post with that slug was already published. Edit the slug or delete the existing item in Webflow.
- **Post published but URL returns 404** — most often the site has never been published from the Designer, or you're using a custom domain whose DNS hasn't propagated. Open Webflow Designer and click Publish at least once.
- **"409 Site not published" on first publish** — Webflow rejects live CMS publishes on un-published sites. theStacc automatically falls back to staged item creation. Publish your site once in Designer; future live publishes work directly.
- **403 Forbidden when creating items** — the workspace plan doesn't include CMS API access. Upgrade to a Workspace plan with CMS hosting.

### What gets sent to Webflow

theStacc sends \`POST https://api.webflow.com/v2/collections/{id}/items/live\` (or \`/items\` for staged) with your mapped fields plus the required \`name\` and \`slug\`. No source code, design changes, or custom integrations are needed on the Webflow side.

## Shopify

Publish blog posts to your Shopify store's built-in blog.

1. Click **Connect Shopify**
2. Authorize theStacc to access your Shopify store
3. Select the blog to publish to (if you have multiple)
4. Posts are published as Shopify blog articles with content, images, and tags

## Managing connections

Each connected integration shows:

- **Status** - Active, inactive, or disconnected
- **Last sync** - When the last successful publish happened
- **Test button** - Verify the connection works
- **Active/Inactive toggle** - Pause publishing without disconnecting
- **Disconnect** - Remove the integration entirely

## Troubleshooting

- **Connection failed** - Verify your site URL includes https:// and the API is accessible
- **Authentication error** - Regenerate your application password or API key
- **Publishing failed** - Check user permissions (Author or Editor role minimum)
- **Images not uploading** - Verify your CMS media library has available storage`,
      },
    ],
  },
  {
    name: 'Local SEO',
    slug: 'local-seo',
    items: [
      {
        title: 'Overview',
        slug: 'overview',
        description: 'Overview of the Local SEO dashboard, key performance metrics, GBP management, and core module features.',
        content: `The Local SEO module helps your business dominate local search results - the map pack and "near me" searches that drive foot traffic and calls.

![How Local SEO plans posts, applies safety guardrails, and tracks reviews and rankings on your Google Business Profile](/images/docs/local-seo-flow.svg)

## Dashboard

Your Local SEO dashboard provides an overview of your local search performance:

### Key metrics

- **GBP Score** - Overall health score of your Google Business Profile
- **Review count and rating** - Total reviews and average star rating
- **Visibility index** - How visible your business is in local search
- **Citation count** - Number of directory listings
- **Review response rate** - Percentage of reviews you've responded to
- **Traffic comparison** - Month-over-month local traffic changes

### Location performance

View your current business location details, service area coverage, Google Business Profile verification status, review metrics, and photo gallery performance.

## Module features

### Google Business Profile

Connect your GBP and optimize it continuously. theStacc analyzes your profile completeness, category selection, and attributes to maximize your local ranking.

### Local posts

Generate and publish 300-500 word local SEO posts directly to your Google Business Profile to keep it active and improve ranking signals.

### Review management

Monitor all your Google reviews, filter by rating, generate AI responses, and track response metrics - all from one dashboard.

### Business setup

Configure your business details including services offered, customer pain points, business hours, and service area under **Local SEO > Settings > Businesses**.

### Keywords

Manage local SEO keywords organized by type: Service + Location, Best/Top, Near Me, Emergency, Brand, and Service keywords. Up to 30 active keywords.

## Getting started

To use Local SEO, go through the onboarding flow:

1. Search for your business on Google
2. Select the correct listing from results
3. Add your services, pain points, and business hours
4. Start your trial`,
      },
      {
        title: 'Google Business Profile',
        slug: 'google-business-profile',
        description: 'Connect, optimize, and manage your Google Business Profile directly from theStacc to improve local search visibility.',
        content: `Your Google Business Profile (GBP) is the most important asset for local search visibility. theStacc connects to your GBP and optimizes it continuously.

## Connecting your profile

During Local SEO onboarding:

1. Search for your business by name and location
2. theStacc searches for matching business listings
3. Select your business from the results (shows name, address, rating)
4. Confirm your business details

theStacc requires your GBP to be claimed and verified.

## Profile optimization

Once connected, theStacc analyzes your profile and generates an optimization score covering:

### Business information

- Business name accuracy
- Address and service area configuration
- Phone number and website URL
- Business hours (including holiday hours)
- Business description with keyword optimization

### Categories

Your primary category is the most important ranking factor for local search. theStacc analyzes your competitors and suggests optimal primary and secondary categories.

### Attributes

Google supports dozens of attributes (wheelchair accessible, free Wi-Fi, outdoor seating, etc.). theStacc identifies which are relevant and helps you fill them in.

## Google Posts

theStacc generates and publishes local posts (300-500 words) to your Google Business Profile:

- Posts keep your profile active (a ranking signal)
- Content targets your local keywords
- Monthly calendar view shows all scheduled and published posts
- Filter posts by "Upcoming" or "Published"
- Edit posts inline before publishing
- Copy post content to clipboard
- Regenerate posts that need improvement

Configure posting frequency in **Local SEO > Settings > Preferences**.

## Performance tracking

Track your local SEO performance:

- **GBP score** - Overall profile health
- **Map pack appearances** - How often you show in the local 3-pack
- **Search queries** - What searches trigger your listing
- **Customer actions** - Calls, direction requests, and website visits
- **Photo views** - How your gallery performs vs competitors`,
      },
      {
        title: 'Reviews',
        slug: 'reviews',
        description: 'Monitor customer reviews across platforms, generate AI-powered review responses, and track your review metrics over time.',
        content: `theStacc's review management lets you monitor, respond to, and analyze all your Google reviews from one place.

## Review dashboard

Navigate to **Local SEO > Reviews** to see all your Google Business Profile reviews.

### Filtering

- **By star rating** - Filter to show only 1-star, 2-star, etc.
- **Needs attention** - Show only unanswered reviews
- **All reviews** - Complete review history

### Review details

Each review shows:

- Customer name and profile
- Star rating
- Review text
- Date posted
- Your reply (if any)
- Reply status

## AI-generated responses

For each review, theStacc can generate a professional response:

1. Click on a review that needs a response
2. Click **Generate Response** to get an AI-drafted reply
3. Review and edit the suggested response
4. Post the response directly to Google

AI responses are tailored to:

- The review's sentiment (positive, neutral, negative)
- Specific points mentioned by the reviewer
- Your business details and services
- Professional, brand-appropriate tone

## Review metrics

Track your review health over time:

- **Total review count** - How many reviews you have
- **Average rating** - Your overall star rating
- **Rating distribution** - Breakdown by star level (1-5)
- **Response rate** - Percentage of reviews with replies
- **Average response time** - How quickly you typically respond

## Best practices

- Respond to every review, positive or negative
- Reply within 24-48 hours for best impact on local rankings
- Use AI-generated responses as a starting point, then personalize
- Thank positive reviewers and address concerns in negative reviews
- Quick, thoughtful responses build customer trust and improve your local ranking`,
      },
    ],
  },
  {
    name: 'Social Media',
    slug: 'social-media',
    items: [
      {
        title: 'Overview',
        slug: 'overview',
        description: 'Overview of the Social Media module dashboard, content calendar, post management, and scheduling workflow.',
        content: `The Social Media module creates and publishes AI-generated posts across Instagram, Facebook, LinkedIn, and X (Twitter).

![How a monthly social plan becomes native captions and visuals for each platform](/images/docs/social-plan.svg)

## Dashboard

### Stats bar

Quick metrics at the top:

- Total posts scheduled
- Total posts published
- Drafts pending review
- Total posts count

### Calendar view

A monthly calendar showing all scheduled posts across platforms. Each date shows platform icons for the posts scheduled that day. Navigate between months and expand the calendar for a full view.

### Post list view

A table of all posts with:

- **Platform icons** - Which platforms the post targets
- **Post title/preview** - Content preview
- **Format** - Text-Image or Carousel
- **Status** - Current state of the post
- **Scheduled date and time** - When it will publish
- **Hashtags** - Tags for the post
- **Actions** - Edit, delete, regenerate via dropdown

Filter posts by tab: **Upcoming**, **Published**, or **Failed**.

## Post statuses

Posts move through these states:

- **To Be Generated** - Queued for AI generation
- **Generating** - AI is creating the content
- **Generated** - Content created, awaiting action
- **Pending Review** - Waiting for your approval
- **Approved** - Ready to publish
- **Published** - Live on social platforms
- **Failed** - Publishing failed (retry available)

## Supported platforms

- **Instagram** - Feed posts, Carousels (up to 10 images), Stories, Reels
- **Facebook** - Text, Images (up to 10), Videos, Stories, Reels
- **LinkedIn** - Text, Images (up to 20), Videos, Documents/PDFs
- **X (Twitter)** - Tweets, Threads, Images (up to 4), Videos, GIFs`,
      },
      {
        title: 'Connecting Platforms',
        slug: 'connecting-platforms',
        description: 'Connect your Instagram, Facebook, LinkedIn, and X (Twitter) accounts to theStacc for automated social media publishing.',
        popular: true,
        content: `Connect your social accounts to publish content directly from theStacc.

## Instagram

1. Go to **Social Media > Settings > Connections**
2. Click **Connect Instagram**
3. Authorize via OAuth
4. **Requires** a Business or Creator account (personal accounts not supported)

Supports: Feed Posts, Carousels (up to 10 images), Stories, Reels.

## Facebook

1. Click **Connect Facebook**
2. Authorize via OAuth
3. Grant access to your Facebook Page

Supports: Text posts, Images (up to 10), Videos, Stories, Reels.

## LinkedIn

1. Click **Connect LinkedIn**
2. Authorize via OAuth
3. Select Personal Profile or Company Page

Supports: Text posts, Images (up to 20), Videos, Documents/PDFs.

## X (Twitter)

1. Click **Connect X**
2. Authorize via OAuth

Supports: Tweets, Threads, Images (up to 4), Videos, GIFs. Character limits apply (280 free tier, 25k premium).

## Connection status

Each platform shows:

- **Connected** - Active and ready to publish
- **Not Connected** - Needs OAuth authorization
- **Expired** - Token expired, needs re-authentication

You can disconnect or reconnect any platform at any time. Expired connections show a **Re-authenticate** button.

## Requirements

- Instagram requires a Business or Creator account linked to a Facebook Page
- Facebook requires Page admin access
- LinkedIn company page posting requires admin permissions
- All connections use OAuth - theStacc never stores your social media passwords`,
      },
      {
        title: 'Brand & Style',
        slug: 'brand-style',
        description: 'Configure brand colors, logo, fonts, voice settings, and image style to keep your AI-generated social posts on-brand.',
        content: `Customize the look and feel of all generated social content under **Social Media > Settings > Brand & Style**.

## Brand color

Set your primary brand color using the color picker. This color is applied to all generated social post graphics and templates.

## Brand logo

Upload your logo to include in branded social posts. Used especially with the "Brand & Text" image style.

## Image style

Choose from 6 styles for social post visuals:

- **Photorealistic** - Lifelike photography
- **Flat Illustration** - Clean vector graphics
- **Cinematic** - Dramatic, film-quality
- **Watercolor** - Artistic, painted look
- **Sketch** - Hand-drawn style
- **Brand & Text** - Your logo and brand colors as the visual

## Font pairing

Select from pre-defined font combinations applied to social post graphics. Options include serif, sans-serif, and monospace pairings.

## Brand voice

Set the tone for all generated captions:

- **Professional** - Polished and authoritative
- **Casual** - Relaxed and conversational
- **Witty** - Clever and humorous
- **Inspirational** - Motivational and uplifting
- **Educational** - Informative and teaching-oriented
- **Bold** - Direct and confident

## Content language

theStacc supports 30+ languages for social post generation:

- English (US/UK), Spanish, French, German, Portuguese, Italian, Dutch
- Japanese, Korean, Chinese, Thai, Vietnamese, Indonesian, Malay, Filipino
- Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu
- Arabic, Turkish, Russian, Polish, Swedish, Danish, Norwegian, Finnish

## Words to avoid

Add a custom blocklist of words or phrases that should never appear in generated content. Useful for brand safety and avoiding sensitive terms.`,
      },
      {
        title: 'Content & Scheduling',
        slug: 'content-scheduling',
        description: 'Set up content pillars, create and edit social posts, schedule publishing times, and manage platform-specific formatting.',
        content: `Manage your social content strategy with content pillars, the post editor, and scheduling controls.

## Content pillars

Content pillars organize your social strategy into themed categories. Choose up to 6:

- **Educational** - Tips, how-tos, industry insights
- **Thought Leadership** - Opinions, trends, expert takes
- **Product Highlights** - Feature spotlights, use cases
- **Industry News** - Current events, market updates
- **Behind the Scenes** - Team culture, process, company life
- **Engagement** - Questions, polls, community interaction

Set a distribution percentage for each pillar and posts-per-week frequency.

## Content plan generation

theStacc generates a content plan based on your pillars, audience, and platforms:

- Select the planning period (1-30 days)
- Choose target platforms
- AI creates multiple post variations across your pillars
- Each post gets platform-optimized captions, hashtags, and images
- First comment suggestions (for Instagram)

## Post editor

Click any post to open the full editor:

### Caption editing

- Main caption editor (expandable)
- Platform-specific caption overrides for each connected platform
- Character limit indicators per platform
- Hashtag management (add/remove tags)
- First comment drafts per platform

### Image management

- Multi-image gallery view
- Image preview with lightbox
- Delete, upload, or regenerate images
- Manage image order for carousels

### Platform preview

See exactly how your post will look on each platform before publishing. Platform-specific rendering shows caption, images, and hashtags.

### Post metadata

- Content pillar assignment
- Scheduled date and time pickers
- Format type (Text-Image or Carousel)
- Platform selection (multi-select)

## Scheduling

Posts publish at their scheduled date and time using your workspace timezone. You can:

- Edit the scheduled date and time from the post editor
- Filter posts by Upcoming, Published, or Failed
- Reschedule failed posts
- Bulk manage posts from the calendar view`,
      },
    ],
  },
  {
    name: 'Account',
    slug: 'account',
    items: [
      {
        title: 'Workspace & Team',
        slug: 'workspace-team',
        description: 'Manage your workspace settings, invite team members, assign roles, and control access permissions across your account.',
        content: `Your workspace is the central hub for managing your theStacc account. Access settings by clicking **Settings** in the sidebar.

## General settings

### Workspace name

Your workspace name appears in the dashboard and email notifications. Change it under **Settings > General**.

### Timezone

Your workspace timezone controls when scheduled content publishes and when reports are sent.

### Website URL

The primary website connected to your workspace for content publishing and SEO tracking.

## Project management

theStacc supports multiple projects. Use the project selector in the sidebar to switch between them. Each project has:

- Its own module configurations
- Independent content plans and keywords
- Separate team member access
- Individual billing

Create new projects from the project selector dropdown.

## Team members

### Inviting members

1. Go to **Settings > Team**
2. Click **Invite Member**
3. Enter their email address
4. Select their role
5. Send the invitation

Invited members receive an email with a link to join. Track pending invitations and resend or cancel them.

### Roles and permissions

- **Owner** - Full access to everything including billing, project deletion, and team management
- **Admin** - Full access to all features except billing management and project deletion
- **Editor** - Can create, edit, approve, and publish content. Cannot modify settings or billing.
- **Viewer** - Read-only access to all content and dashboards

### Managing members

- Change member roles from the team list
- Remove members (they immediately lose access)
- View member status (Active or Pending Invitation)

## Notifications

Configure notifications for each team member:

- **Approval notifications** - Blog or post ready for review
- **Blog issue alerts** - Generation failures or SEO concerns
- **Milestone celebrations** - Publishing milestones reached
- **Warning notifications** - Action required (integration issues, etc.)

Notifications appear in the dashboard and are sent via email.`,
      },
      {
        title: 'Billing & Plans',
        slug: 'billing',
        description: 'Manage module subscriptions, start or extend trials, change plans, and access billing history and invoices.',
        content: `theStacc uses module-based subscriptions. Each module (Content SEO, Local SEO, Social Media) is priced separately, so you only pay for what you use - run one module or all three.

## Plans

Pick the modules you need:

- **Content SEO - $99/month** - 30 AI-written, SEO-scored articles published to your site every month.
- **Local SEO - $49/month** - Google Business Profile optimization, posts, reviews, and rank tracking.
- **Social Media - $49/month** - automated posts across your connected social platforms.
- **All three (bundle) - $167/month** - every module, about 15% cheaper than buying separately.

Each plan includes a set monthly content volume that refreshes at the start of every billing cycle. For current pricing and exactly what each plan includes, see the [pricing page](/pricing).

## Trial

Every module starts with a **$1 trial** so you can see real output before committing. During the trial:

- Full access to all module features
- Days remaining shown on your dashboard
- Cancel anytime - no contract
- Upgrade to a paid plan whenever you are ready

## Subscription status

Your subscription can be in one of these states:

- **Trialing** - Free trial period active
- **Active** - Paid subscription running
- **Past Due** - Payment failed, action needed
- **Cancelled** - Subscription ended

Track all module subscriptions and their status under **Settings > Billing**.

## Managing your subscription

### Upgrading

Upgrade from trial to paid, or move to a higher plan from **Settings > Billing > Change Plan**. Upgrades take effect immediately with prorated billing.

### Cancellation

Cancel any module's subscription from **Settings > Billing**. Your access continues until the end of the current billing period. Published content stays on your website - theStacc never removes it.

### Billing portal

Access your billing portal to:

- Update your payment method
- View payment history
- Download invoices
- Update billing address

## Invoices

Invoices are generated on your billing date and sent to the workspace owner's email. View and download past invoices from the billing portal.

## Payment methods

theStacc accepts all major credit cards through our secure payment processor. Your card details are handled entirely by the processor - theStacc never sees or stores your full card number.

## Project deletion

Under **Settings > Billing** you'll find the danger zone for project deletion. This permanently removes:

- All project data and content
- Team member access
- Active subscriptions (cancelled immediately)

This action cannot be undone.`,
      },
    ],
  },
  {
    name: 'Developers',
    slug: 'developers',
    items: [
      {
        title: 'Public Blog API',
        slug: 'public-blog-api',
        description: 'API reference for fetching published blog posts on static sites, custom frontends, and third-party integrations.',
        popular: true,
        content: `The Public Blog API lets you fetch your published blog content from theStacc and display it on any website — including static sites hosted on Cloudflare Pages, Vercel, Netlify, or any other platform. No CMS required.

## When to use this

Use the Public Blog API when:

- Your site runs on **Cloudflare Pages**, **Vercel**, **Netlify**, or **GitHub Pages**
- You don't use a CMS like WordPress, Ghost, or Webflow
- Your site is built with a static site generator (Astro, Next.js, Hugo, Gatsby, 11ty, etc.)
- You want full control over how blog content is rendered on your site

If you use WordPress, Ghost, or Webflow, you don't need this — use the [direct publishing integrations](/docs/content-seo/publishing) instead.

## How it works

theStacc generates and stores your blog content. The Public Blog API exposes that content as JSON. Your static site fetches it at **build time** and generates static HTML pages.

\`\`\`
theStacc generates blog → stored in theStacc database
                                    ↓
Your site rebuilds → fetches blogs from Public Blog API
                                    ↓
Static HTML pages generated → deployed to your CDN
                                    ↓
Google crawls → sees full static HTML → indexes and ranks normally
\`\`\`

Because content is fetched at build time (not in the browser), Google sees fully rendered HTML pages. **SEO is identical to any other static site** — Google has no idea the content came from an API.

## Authentication

Every project gets a unique **API key** for public access. Find it under **Settings > Publishing > API Access**.

Include the API key in every request as a query parameter or header:

\`\`\`
# Query parameter
GET https://api.thestacc.com/blog/api/v1/public/blogs?api_key=YOUR_API_KEY

# Or as a header
GET https://api.thestacc.com/blog/api/v1/public/blogs
Authorization: Bearer YOUR_API_KEY
\`\`\`

Keep your API key private. Use environment variables in your build process — never commit it to your repository.

## Endpoints

### List all published blogs

\`\`\`
GET /blog/api/v1/public/blogs?api_key=YOUR_API_KEY
\`\`\`

Returns all blogs with \`status: published\`, sorted by \`published_at\` (newest first). By default returns metadata only (no content). Pass \`include_content=true\` to get full HTML content.

**Query parameters:**

- \`api_key\` (required) — your project API key
- \`limit\` (optional) — number of blogs to return (default: 50, max: 100)
- \`offset\` (optional) — pagination offset (default: 0)
- \`category\` (optional) — filter by category name
- \`include_content\` (optional) — set to \`true\` to include full blog HTML content (default: false)

**Response (default — without content):**

\`\`\`json
{
  "blogs": [
    {
      "id": "abc-123",
      "title": "10 SEO Tips for Small Businesses",
      "slug": "seo-tips-small-businesses",
      "excerpt": "Discover actionable SEO strategies that...",
      "meta_title": "10 SEO Tips for Small Businesses | Your Brand",
      "meta_description": "Discover 10 actionable SEO strategies...",
      "featured_image_url": "https://storage.thestacc.com/images/seo-tips.webp",
      "categories": ["SEO", "Marketing"],
      "tags": ["seo", "small-business", "organic-traffic"],
      "published_at": "2026-03-28T10:00:00Z"
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
\`\`\`

When \`include_content=true\` is passed, each blog also includes a \`content\` field with the full HTML body.

### Get a single blog by slug

\`\`\`
GET /blog/api/v1/public/blogs/:slug?api_key=YOUR_API_KEY
\`\`\`

Returns the full blog content for a specific slug (always includes content).

**Response:**

\`\`\`json
{
  "id": "abc-123",
  "title": "10 SEO Tips for Small Businesses",
  "slug": "seo-tips-small-businesses",
  "excerpt": "Discover actionable SEO strategies that...",
  "content": "<h2>Why SEO matters</h2><p>Search engine optimization...</p>",
  "meta_title": "10 SEO Tips for Small Businesses | Your Brand",
  "meta_description": "Discover 10 actionable SEO strategies...",
  "featured_image_url": "https://storage.thestacc.com/images/seo-tips.webp",
  "categories": ["SEO", "Marketing"],
  "tags": ["seo", "small-business", "organic-traffic"],
  "published_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-29T14:30:00Z",
  "word_count": 1850
}
\`\`\`

Returns \`404\` if the slug doesn't exist or the blog isn't published.

### Get blog sitemap data

\`\`\`
GET /blog/api/v1/public/blogs/sitemap?api_key=YOUR_API_KEY
\`\`\`

Returns a lightweight list of all published blogs for generating your XML sitemap. Only includes \`slug\`, \`published_at\`, and \`updated_at\`.

**Response:**

\`\`\`json
{
  "blogs": [
    {
      "slug": "seo-tips-small-businesses",
      "published_at": "2026-03-28T10:00:00Z",
      "updated_at": "2026-03-29T14:30:00Z"
    }
  ],
  "total": 42
}
\`\`\`

## Content format

The \`content\` field contains **HTML** — the same HTML that gets published to WordPress or Ghost. It includes:

- Headings (\`h2\`, \`h3\`, \`h4\`)
- Paragraphs, lists, blockquotes
- Links (internal and external)
- Images with alt text
- Inline styles for formatting

You can render it directly with \`set:html\` (Astro), \`dangerouslySetInnerHTML\` (React/Next.js), or \`| safe\` (Hugo). Apply your own CSS to match your site's design.

## Rate limits

The Public Blog API is designed for build-time fetching, not real-time client requests. A typical static site build makes 1-3 requests total. Avoid calling the API from client-side browser code — use it at build time only.

## Error handling

All errors return a JSON object with a \`detail\` field:

\`\`\`json
{
  "detail": "Invalid API key. Check that your key is correct and hasn't been revoked."
}
\`\`\`

**Common HTTP status codes:**

- \`401\` — Invalid or missing API key
- \`404\` — Blog not found or not published
- \`500\` — Server error (retry after a few seconds)

## Next steps

- Follow the [Static Site Integration](/docs/developers/static-site-integration) guide for framework-specific setup
- Set up [Deploy Hooks](/docs/developers/deploy-hooks) so your site rebuilds automatically when new content is published`,
      },
      {
        title: 'Static Site Integration',
        slug: 'static-site-integration',
        description: 'Step-by-step guide to display theStacc blogs on Astro, Next.js, Hugo, and other static site generators.',
        popular: true,
        content: `This guide walks you through connecting theStacc to your static site. By the end, your site will automatically display AI-generated blog posts — fully rendered as static HTML for perfect SEO.

## Prerequisites

Before starting, make sure you have:

1. A theStacc project with **Content SEO** enabled and at least one published blog
2. Your **Public Blog API key** from **Settings > Publishing > API Access**
3. A static site built with Astro, Next.js, Hugo, or any other SSG
4. Your site deployed on Cloudflare Pages, Vercel, Netlify, or similar

## Overview

The integration has three parts:

1. **Fetch** — Your site calls the theStacc API at build time to get blog data
2. **Render** — Your SSG generates static HTML pages from the API response
3. **Rebuild** — A deploy hook triggers a new build whenever content is published

This guide covers the first two parts. See [Deploy Hooks](/docs/developers/deploy-hooks) for automatic rebuilds.

## Environment setup

Store your API key as an environment variable. **Never hardcode it in your source files.**

Create or update your \`.env\` file:

\`\`\`
THESTACC_API_KEY=your_api_key_here
THESTACC_API_URL=https://api.thestacc.com/blog/api/v1/public
\`\`\`

Add \`.env\` to your \`.gitignore\` if it's not already there.

For your hosting platform, add the same variables in the dashboard:

- **Cloudflare Pages** — Settings > Environment variables
- **Vercel** — Settings > Environment Variables
- **Netlify** — Site configuration > Environment variables

## Astro

Astro is the most straightforward integration since it supports static and server-rendered pages natively.

### Create the API helper

Create \`src/lib/thestacc.ts\`:

\`\`\`typescript
const API_KEY = import.meta.env.THESTACC_API_KEY;
const API_URL = import.meta.env.THESTACC_API_URL;

export async function getAllBlogs() {
  const res = await fetch(\`\${API_URL}/blogs?api_key=\${API_KEY}\`);
  if (!res.ok) throw new Error(\`Failed to fetch blogs: \${res.status}\`);
  const data = await res.json();
  return data.blogs;
}

export async function getBlogBySlug(slug: string) {
  const res = await fetch(\`\${API_URL}/blogs/\${slug}?api_key=\${API_KEY}\`);
  if (!res.ok) return null;
  return await res.json();
}
\`\`\`

### Create the blog listing page

Create \`src/pages/blog/index.astro\`:

\`\`\`astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getAllBlogs } from '../../lib/thestacc';

const blogs = await getAllBlogs();
---

<BaseLayout title="Blog">
  <h1>Blog</h1>
  <div class="blog-grid">
    {blogs.map((blog) => (
      <a href={\`/blog/\${blog.slug}\`}>
        <img src={blog.featured_image_url} alt={blog.title} />
        <h2>{blog.title}</h2>
        <p>{blog.excerpt}</p>
        <time>{new Date(blog.published_at).toLocaleDateString()}</time>
      </a>
    ))}
  </div>
</BaseLayout>
\`\`\`

### Create the blog detail page

Create \`src/pages/blog/[slug].astro\`:

\`\`\`astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getAllBlogs, getBlogBySlug } from '../../lib/thestacc';

export async function getStaticPaths() {
  const blogs = await getAllBlogs();
  return blogs.map((blog) => ({
    params: { slug: blog.slug },
  }));
}

const { slug } = Astro.params;
const blog = await getBlogBySlug(slug);

if (!blog) return Astro.redirect('/404');
---

<BaseLayout title={blog.meta_title} description={blog.meta_description}>
  <article>
    <img src={blog.featured_image_url} alt={blog.title} />
    <h1>{blog.title}</h1>
    <time>{new Date(blog.published_at).toLocaleDateString()}</time>
    <div class="blog-content" set:html={blog.content} />
  </article>
</BaseLayout>
\`\`\`

\`set:html\` renders the HTML content directly. Style the \`.blog-content\` class in your CSS to match your site's design.

### Generate the sitemap

If you use \`@astrojs/sitemap\`, the blog pages are automatically included since they're generated as static routes.

## Next.js (App Router)

### Create the API helper

Create \`lib/thestacc.ts\`:

\`\`\`typescript
const API_KEY = process.env.THESTACC_API_KEY;
const API_URL = process.env.THESTACC_API_URL;

export async function getAllBlogs() {
  const res = await fetch(\`\${API_URL}/blogs?api_key=\${API_KEY}\`, {
    next: { revalidate: false },
  });
  if (!res.ok) throw new Error('Failed to fetch blogs');
  const data = await res.json();
  return data.blogs;
}

export async function getBlogBySlug(slug: string) {
  const res = await fetch(\`\${API_URL}/blogs/\${slug}?api_key=\${API_KEY}\`, {
    next: { revalidate: false },
  });
  if (!res.ok) return null;
  return await res.json();
}
\`\`\`

### Create the blog listing page

Create \`app/blog/page.tsx\`:

\`\`\`tsx
import { getAllBlogs } from '@/lib/thestacc';
import Link from 'next/link';
import Image from 'next/image';

export default async function BlogPage() {
  const blogs = await getAllBlogs();

  return (
    <main>
      <h1>Blog</h1>
      <div className="blog-grid">
        {blogs.map((blog) => (
          <Link key={blog.id} href={\`/blog/\${blog.slug}\`}>
            <Image src={blog.featured_image_url} alt={blog.title} width={800} height={400} />
            <h2>{blog.title}</h2>
            <p>{blog.excerpt}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
\`\`\`

### Create the blog detail page

Create \`app/blog/[slug]/page.tsx\`:

\`\`\`tsx
import { getAllBlogs, getBlogBySlug } from '@/lib/thestacc';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  const blogs = await getAllBlogs();
  return blogs.map((blog) => ({ slug: blog.slug }));
}

export async function generateMetadata({ params }) {
  const blog = await getBlogBySlug(params.slug);
  if (!blog) return {};
  return {
    title: blog.meta_title,
    description: blog.meta_description,
    openGraph: { images: [blog.featured_image_url] },
  };
}

export default async function BlogPost({ params }) {
  const blog = await getBlogBySlug(params.slug);
  if (!blog) notFound();

  return (
    <article>
      <img src={blog.featured_image_url} alt={blog.title} />
      <h1>{blog.title}</h1>
      <time>{new Date(blog.published_at).toLocaleDateString()}</time>
      <div
        className="blog-content"
        dangerouslySetInnerHTML={{ __html: blog.content }}
      />
    </article>
  );
}
\`\`\`

For static export, add \`output: 'export'\` to your \`next.config.js\` and use \`generateStaticParams\` as shown above.

## Hugo

### Create the data fetch script

Hugo doesn't fetch API data natively. Use a build script that runs before Hugo.

Create \`fetch-blogs.sh\`:

\`\`\`bash
#!/bin/bash
mkdir -p content/blog

# Fetch all blogs
RESPONSE=$(curl -s "$THESTACC_API_URL/blogs?api_key=$THESTACC_API_KEY")

# Generate a markdown file for each blog
echo "$RESPONSE" | jq -c '.blogs[]' | while read -r blog; do
  SLUG=$(echo "$blog" | jq -r '.slug')
  TITLE=$(echo "$blog" | jq -r '.title')
  DESC=$(echo "$blog" | jq -r '.meta_description')
  DATE=$(echo "$blog" | jq -r '.published_at')
  IMAGE=$(echo "$blog" | jq -r '.featured_image_url')
  CONTENT=$(echo "$blog" | jq -r '.content')

  cat > "content/blog/$SLUG.html" <<EOF
---
title: "$TITLE"
description: "$DESC"
date: "$DATE"
featured_image: "$IMAGE"
markup: html
---

$CONTENT
EOF
done
\`\`\`

The script uses \`.html\` extension and \`markup: html\` frontmatter so Hugo renders the API's HTML content as-is instead of processing it as markdown. In your Hugo template, use \`{{ .Content | safeHTML }}\` to output the content without escaping.

Update your build command on Cloudflare Pages (or wherever you deploy):

\`\`\`
bash fetch-blogs.sh && hugo
\`\`\`

## Nuxt 3 (Vue.js)

### Create the API composable

Create \`composables/useThestacc.ts\`:

\`\`\`typescript
export async function getAllBlogs() {
  const config = useRuntimeConfig()
  const data = await $fetch(\`\${config.public.thestaccApiUrl}/blogs\`, {
    query: { api_key: config.thestaccApiKey },
  })
  return data.blogs
}

export async function getBlogBySlug(slug: string) {
  const config = useRuntimeConfig()
  return await $fetch(\`\${config.public.thestaccApiUrl}/blogs/\${slug}\`, {
    query: { api_key: config.thestaccApiKey },
  })
}
\`\`\`

### Add runtime config

In your \`nuxt.config.ts\`:

\`\`\`typescript
export default defineNuxtConfig({
  runtimeConfig: {
    thestaccApiKey: process.env.THESTACC_API_KEY,
    public: {
      thestaccApiUrl: process.env.THESTACC_API_URL,
    },
  },
})
\`\`\`

### Create the blog listing page

Create \`pages/blog/index.vue\`:

\`\`\`vue
<script setup>
const blogs = await getAllBlogs()
</script>

<template>
  <div>
    <h1>Blog</h1>
    <div class="blog-grid">
      <NuxtLink v-for="blog in blogs" :key="blog.id" :to="\`/blog/\${blog.slug}\`">
        <img :src="blog.featured_image_url" :alt="blog.title" />
        <h2>{{ blog.title }}</h2>
        <p>{{ blog.excerpt }}</p>
        <time>{{ new Date(blog.published_at).toLocaleDateString() }}</time>
      </NuxtLink>
    </div>
  </div>
</template>
\`\`\`

### Create the blog detail page

Create \`pages/blog/[slug].vue\`:

\`\`\`vue
<script setup>
const route = useRoute()
const blog = await getBlogBySlug(route.params.slug as string)

useHead({
  title: blog?.meta_title,
  meta: [
    { name: 'description', content: blog?.meta_description },
  ],
})
</script>

<template>
  <article v-if="blog">
    <img :src="blog.featured_image_url" :alt="blog.title" />
    <h1>{{ blog.title }}</h1>
    <time>{{ new Date(blog.published_at).toLocaleDateString() }}</time>
    <div class="blog-content" v-html="blog.content" />
  </article>
</template>
\`\`\`

\`v-html\` renders the HTML content directly. Style the \`.blog-content\` class in your CSS to match your site's design.

### Static generation

For static export on Cloudflare Pages, Vercel, or Netlify, run:

\`\`\`
npx nuxi generate
\`\`\`

Nuxt pre-renders all pages at build time — the output is pure static HTML with the same SEO as any other static site generator.

## Styling the content

The API returns HTML content. Add CSS to style it within your site's design:

\`\`\`css
.blog-content h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
}

.blog-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.blog-content p {
  line-height: 1.75;
  margin-bottom: 1rem;
}

.blog-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1.5rem 0;
}

.blog-content a {
  color: var(--color-primary);
  text-decoration: underline;
}

.blog-content ul, .blog-content ol {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.blog-content blockquote {
  border-left: 3px solid var(--color-primary);
  padding-left: 1rem;
  font-style: italic;
  color: #6b7280;
}
\`\`\`

If you use Tailwind CSS, apply the [\`@tailwindcss/typography\`](https://tailwindcss.com/docs/typography-plugin) plugin and wrap the content in a \`prose\` class:

\`\`\`html
<div class="prose prose-lg" set:html={blog.content} />
\`\`\`

## Testing locally

Run your site locally and verify:

1. Blog listing page shows all published blogs
2. Each blog detail page renders content correctly
3. Images load properly
4. Meta tags are set (check with View Source)
5. Internal links within blog content work

## Next steps

- Set up [Deploy Hooks](/docs/developers/deploy-hooks) so your site rebuilds automatically when blogs are published
- Add an XML sitemap for SEO using the [sitemap endpoint](/docs/developers/public-blog-api#get-blog-sitemap-data)`,
      },
      {
        title: 'Deploy Hooks',
        slug: 'deploy-hooks',
        description: 'Set up deploy hooks to automatically rebuild your static site whenever theStacc publishes new AI-generated content.',
        content: `Deploy hooks let your static site rebuild automatically whenever theStacc publishes, updates, or unpublishes a blog post. Without deploy hooks, you'd need to manually trigger a rebuild every time content changes.

## How deploy hooks work

\`\`\`
1. You publish a blog in theStacc
2. theStacc sends a POST request to your deploy hook URL
3. Your hosting platform receives the request and starts a new build
4. During the build, your site fetches the latest content from the Public Blog API
5. New static HTML pages are generated and deployed
\`\`\`

The entire process takes 1-3 minutes depending on your site's build time.

## Events that trigger a rebuild

theStacc fires a deploy hook when:

- A new blog is **published**
- A published blog is **updated** (content edited, then synced)
- A published blog is **unpublished** (removed from your site)

Draft changes, generation, or approval steps do **not** trigger a rebuild.

## Setting up deploy hooks

### Step 1: Get your deploy hook URL

#### Cloudflare Pages

1. Go to your project in the Cloudflare dashboard
2. Navigate to **Settings > Builds & deployments > Deploy hooks**
3. Click **Add deploy hook**
4. Name it "theStacc" and select your production branch
5. Copy the generated URL (looks like \`https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/...\`)

#### Vercel

1. Go to your project in the Vercel dashboard
2. Navigate to **Settings > Git > Deploy Hooks**
3. Create a hook named "theStacc" for your main branch
4. Copy the generated URL (looks like \`https://api.vercel.com/v1/integrations/deploy/...\`)

#### Netlify

1. Go to your site in the Netlify dashboard
2. Navigate to **Site configuration > Build & deploy > Build hooks**
3. Click **Add build hook**
4. Name it "theStacc" and select your production branch
5. Copy the generated URL (looks like \`https://api.netlify.com/build_hooks/...\`)

#### GitHub Pages

GitHub Pages doesn't have built-in deploy hooks. Use a GitHub Actions workflow instead:

1. Create a repository dispatch workflow in \`.github/workflows/rebuild.yml\`:

\`\`\`yaml
name: Rebuild site
on:
  repository_dispatch:
    types: [thestacc-publish]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and deploy
        run: |
          npm install
          npm run build
\`\`\`

2. Use a webhook-to-dispatch service, or set up a simple Cloudflare Worker that converts the theStacc webhook into a GitHub repository dispatch event.

### Step 2: Add the URL to theStacc

1. Go to **Settings > Publishing > API Access** in your theStacc dashboard
2. Find the **Deploy Hook** section
3. Paste your deploy hook URL
4. Click **Test** to verify the connection — this triggers a test build on your hosting platform
5. Save

## Build optimization

Each deploy hook triggers a full site rebuild. Keep builds fast:

- **Cache API responses** — If your framework supports build caching, the theStacc API returns \`Cache-Control\` and \`ETag\` headers
- **Incremental builds** — Frameworks like Next.js and Astro support incremental static regeneration. Only new or changed pages get rebuilt
- **Limit unnecessary rebuilds** — theStacc only triggers hooks for published content changes, not drafts or internal edits

## Monitoring builds

After setting up deploy hooks:

1. Publish a test blog in theStacc
2. Check your hosting platform's build logs — you should see a new build triggered within seconds
3. Once the build completes, verify the new blog appears on your site
4. Check the published URL in your browser and confirm content renders correctly

If the build doesn't trigger, verify:

- The deploy hook URL is correct and active
- Your hosting platform hasn't disabled automatic builds
- Your API key is configured in the hosting platform's environment variables

## Debouncing

If you publish multiple blogs at once (e.g., approving a batch), theStacc waits **30 seconds** after the last publish event before firing the deploy hook. This prevents multiple redundant builds and keeps your hosting platform's build queue clean.

## Security

Deploy hook URLs are stored securely and never exposed in the frontend. The URLs themselves act as authentication — anyone with the URL can trigger a build. If you suspect your URL has been compromised:

1. Delete the current hook on your hosting platform
2. Create a new one
3. Update the URL in theStacc settings

## Next steps

- Review the [Public Blog API](/docs/developers/public-blog-api) reference for all available endpoints
- Follow the [Static Site Integration](/docs/developers/static-site-integration) guide if you haven't set up your site yet`,
      },
      {
        title: 'Webhook Reference',
        slug: 'webhook-reference',
        description: 'Production reference for the Custom Webhook integration — handshake, signing, every event, every field, response contract, database schemas, and receiver examples in 6 languages.',
        popular: true,
        content: `This is the **end-to-end reference** for theStacc's Custom Webhook integration. It covers everything a developer needs to ship a production receiver: how authentication works, every event we send, every field we put in the payload, what to return, and ready-to-paste receiver + database schema examples.

> **Quick orientation:** if you're configuring this from theStacc's dashboard, start at [Connect Platforms → Custom Webhook](/docs/content-seo/connect-platforms). This page is for the developer who needs to build (or audit) the receiving endpoint.

## When to use a webhook

Choose the Custom Webhook integration when:

- Your site is built on a **custom stack** — Next.js, Astro, Remix, SvelteKit, Rails, Django, Laravel, etc. (anything that's not WordPress / Ghost / Webflow / Shopify).
- You want **full control** over what happens when a blog publishes — write to your own DB, trigger a rebuild, push to a CDN, fan out to other systems.
- You already have a CMS but want **theStacc to write into it via your own API**, not theStacc's direct integrations.

If you use WordPress, Ghost, Webflow, or Shopify, use those integrations instead — they handle authentication, image uploads, and field mapping for you.

## How the handshake works

theStacc uses **stateless per-request authentication** via a shared secret — the same model as Stripe, GitHub, and Slack webhooks. There is **no OAuth dance, no token exchange, no TLS-mutual-auth**. The "handshake" happens once during setup: both sides record the same secret, then every subsequent request is independently signed and verified.

### Step 1 — One-time setup

The developer pastes a Webhook URL + Secret Key into the **Settings → Publishing → Add Webhook** dialog. theStacc stores the secret encrypted; the developer keeps a copy in an env var on their server. After this, both sides hold the same secret.

![Webhook one-time setup — developer pastes URL + Secret Key into theStacc dashboard, theStacc stores it encrypted](/images/docs/webhook-setup.webp)

### Step 2 — Per request (every blog publish, sync, unpublish, delete)

theStacc serializes the payload to JSON, computes \`sig = HMAC-SHA256(secret, body)\`, and POSTs the body to your webhook URL with the signature in the \`X-Webhook-Signature\` header. Your receiver reads the **raw body bytes** (not the parsed JSON), recomputes the same HMAC with its own copy of the secret, and compares. If the two signatures match, the request is authentic — process it and respond 200 with the live URL + your CMS id. If they don't, return 401.

![Webhook per-request signing flow — theStacc signs body with HMAC-SHA256 and sends X-Webhook-Signature header; receiver verifies and returns 200 OK with url and id](/images/docs/webhook-signing.webp)

Both sides compute the same signature independently. If they match, the receiver knows the request **really came from theStacc** and **wasn't modified in transit**. That's the entire authentication mechanism.

> **The shared secret is the entire defense.** Anyone who guesses your webhook URL but doesn't know the secret cannot forge a request. Treat it like a database password — store in env vars, rotate if leaked, never commit to git.

## 30-minute production setup

A field-tested path from "we picked Webhook" to "first blog publishes live":

1. **Generate a secret** — \`openssl rand -hex 32\` (or any 32+ char random string).
2. **Add an env var** to your hosting platform: \`STACC_WEBHOOK_SECRET=<the secret>\`.
3. **Add a database table** for incoming blogs ([schema templates below](#database-schema-templates)).
4. **Add a receiver route** at e.g. \`POST /api/stacc-webhook\` ([examples in 6 languages below](#receiver-examples)).
5. **Deploy.** Note the public URL.
6. **In theStacc:** Settings → Publishing → Custom Webhook → enter URL + secret + click **Test Connection**. Green check = working.
7. **Click Sample Payload** to validate your full publish handler with a fake blog (\`blog_id\` will start with \`preview-\`).
8. **Approve any blog and publish.** First real blog should land in your DB within a few seconds.

If anything fails, the [Troubleshooting](#troubleshooting) section below covers every error we've seen.

## Authentication: HMAC-SHA256 signing

When you configure a webhook secret in theStacc, every request includes a signature in the \`X-Webhook-Signature\` header.

### How theStacc generates the signature

\`\`\`python
# Exactly what runs in production (services/blog/.../api/v1/blogs.py)
import hmac, hashlib, json

payload_bytes = json.dumps(payload, separators=(',', ':')).encode()
signature = hmac.new(
    secret.encode(),
    payload_bytes,
    hashlib.sha256,
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Webhook-Signature": signature,  # 64-char hex string
}
\`\`\`

**Critical detail:** the JSON is serialized with **\`separators=(',', ':')\`** — compact, no whitespace. This produces a different byte stream than \`json.dumps(payload)\` (which adds spaces). Your receiver MUST hash the **raw bytes received over the wire**, not parse-and-re-serialize the JSON, or signatures won't match.

### Properties of the signature

| Property | Behavior |
|---|---|
| Deterministic | Same secret + same body bytes → always the same signature |
| Body-bound | Even one byte different in body → completely different signature |
| Length | Always 64 hex characters (256 bits) |
| Format | Lowercase hex, no \`sha256=\` prefix |

### Replay-attack note

HMAC alone doesn't prevent replay — if an attacker captures a signed request, the signature still validates if they replay the exact same bytes. theStacc embeds a fresh \`published_at\` UTC timestamp in every blog event, so receivers can defend by rejecting requests older than ~5 minutes:

\`\`\`js
const sentAt = new Date(body.published_at);
const ageSec = (Date.now() - sentAt.getTime()) / 1000;
if (ageSec > 300) return new Response('Too old, possible replay', { status: 401 });
\`\`\`

For most receivers this isn't necessary — the dominant threat is "someone guessed our webhook URL" and HMAC fully defends against that.

## All events theStacc emits

Five event types. **Branch on the \`event\` field at the top of your handler.**

| Event | When it fires | Idempotent? | Body shape |
|---|---|---|---|
| \`test.ping\` | User clicks Test Connection | ✅ | \`{ event, message, timestamp }\` |
| \`blog.published\` | First successful publish of a blog | ✅ via \`blog_id\` | Full blog payload (see below) |
| \`blog.updated\` | Re-publish or content sync of an existing blog | ✅ via \`blog_id\` | Full blog payload — same shape as \`blog.published\` |
| \`blog.unpublished\` | User unpublishes from theStacc | ✅ | \`{ event, blog_id, title }\` |
| \`blog.deleted\` | User deletes a published blog | ✅ | \`{ event, blog_id, title }\` |

A note on \`preview-\` prefixed \`blog_id\`s: when the user clicks **Sample Payload** in the dashboard, theStacc fires a real-shaped \`blog.published\` event but with \`blog_id: "preview-00000000-0000-0000-0000-000000000000"\`. Your handler should detect the prefix and skip the actual database write so test runs don't pollute production data.

### \`test.ping\` payload

\`\`\`json
{
  "event": "test.ping",
  "message": "This is a test from theStacc",
  "timestamp": "2026-04-30T12:00:00Z"
}
\`\`\`

Respond \`200 {"ok": true}\`. **Do not** require \`title\`, \`slug\`, or \`content\` for this event — there are none.

### \`blog.published\` / \`blog.updated\` payload

\`\`\`json
{
  "event": "blog.published",
  "blog_id": "8f3e1d2c-49ab-4d10-9e7f-7c0bf298faa4",
  "title": "10 SEO mistakes to avoid in 2026",
  "slug": "10-seo-mistakes-to-avoid-in-2026",
  "content": "<h2>Introduction</h2><p>If you've been running SEO...</p>",
  "excerpt": "A short summary of the blog post.",
  "excerpt_short": "A short summary of the blog post.",
  "meta_title": "10 SEO mistakes to avoid in 2026",
  "meta_description": "Avoid these 10 common SEO pitfalls...",
  "featured_image_url": "https://cdn.thestacc.com/blogs/abc123.jpg",
  "categories": ["SEO"],
  "tags": ["seo", "2026", "marketing"],
  "keyword": "seo mistakes 2026",
  "published_at": "2026-04-30T12:00:00Z",
  "images": [
    { "url": "https://cdn.thestacc.com/blog_images/proj-x/blog-y/illustration-1.png", "alt": "How keyword cannibalization happens" },
    { "url": "https://cdn.thestacc.com/blog_images/proj-x/blog-y/illustration-2.png", "alt": "Site audit checklist diagram" }
  ]
}
\`\`\`

### \`blog.unpublished\` / \`blog.deleted\` payload

\`\`\`json
{
  "event": "blog.unpublished",
  "blog_id": "8f3e1d2c-49ab-4d10-9e7f-7c0bf298faa4",
  "title": "10 SEO mistakes to avoid in 2026"
}
\`\`\`

For these events, look up the post in your CMS using the \`blog_id\` (which you should have stored when handling the original \`blog.published\`) and delete or hide it.

## Field reference

Every field theStacc sends in a \`blog.published\` / \`blog.updated\` event:

| Field | Type | Always sent? | Practical limits | What it is |
|---|---|---|---|---|
| \`event\` | string | ✅ | enum: \`blog.published\` \\| \`blog.updated\` \\| \`blog.unpublished\` \\| \`blog.deleted\` \\| \`test.ping\` | Use this to route in your handler. |
| \`blog_id\` | string (UUID) | ✅ | 36 chars, or 44 chars if \`preview-\` prefixed | theStacc's stable identifier. Use as your dedup / foreign key. |
| \`title\` | string | ✅ | typically 50–120 chars | Blog title. Not HTML-escaped — receiver renders it. |
| \`slug\` | string | ✅ | up to 50 chars, lowercase, hyphenated | URL-safe identifier. Stable across re-publishes unless user edits it. |
| \`content\` | string (HTML) | ✅ | typically 4 000–15 000 chars | Full blog HTML. Includes \`<h2>\`, \`<p>\`, \`<ul>\`, \`<a>\`, \`<img>\`, etc. |
| \`excerpt\` | string \\| \`""\` | ✅ (may be empty) | typically 100–300 chars | Short summary, plain text. |
| \`excerpt_short\` | string \\| \`""\` | ✅ (may be empty) | hard cap **≤ 256 chars** | Truncated copy of \`excerpt\` (word-boundary trimmed, ellipsis appended when shorter). Use this when forwarding to a CMS with a strict Excerpt cap — notably Webflow's default 256-char Excerpt collection field. Falls back to \`meta_description\` when \`excerpt\` is empty. |
| \`meta_title\` | string \\| \`null\` | ✅ | up to 70 chars (SEO best practice) | Optimized SEO title. May equal \`title\`. |
| \`meta_description\` | string \\| \`null\` | ✅ | up to 160 chars (SEO best practice) | Optimized SEO description. |
| \`featured_image_url\` | string (URL) \\| \`null\` | ✅ | https://cdn.thestacc.com/... or your uploaded image | Public CDN URL. Always reachable. |
| \`categories\` | string[] | ✅ (may be \`[]\`) | typically 0–3 items, each ≤ 50 chars | One blog can have multiple categories. |
| \`tags\` | string[] | ✅ (may be \`[]\`) | typically 0–10 items, each ≤ 30 chars | Loose keywords. |
| \`keyword\` | string \\| \`null\` | ✅ | typically 1–8 words | Focus keyword the blog targets. |
| \`published_at\` | string (ISO 8601 UTC) | ✅ | always Z-suffixed UTC | When theStacc finalized this publish. |
| \`images\` | \`{url, alt}[]\` | ✅ (may be \`[]\`) | typically 0–4 items | **New — May 2026.** Every \`<img>\` URL embedded in \`content\` body, in document order, deduped. Use to self-host body images: iterate, download from \`url\`, upload to your storage, then \`content.replaceAll('src="{url}"', 'src="{new_url}"')\`. Does **not** include \`featured_image_url\` — that's a separate top-level field and most CMSes already have a dedicated hero slot for it. See [Self-hosting images](#self-hosting-images-recommended-for-production) below. |

> **Field length is not enforced at the API level.** Postgres \`TEXT\` columns are unbounded, and theStacc-generated content stays well within the practical limits above. If you want hard caps in your DB schema, the limits in the table are safe defaults.

## Response contract

Your receiver MUST return a JSON body. theStacc reads two fields:

\`\`\`json
{
  "ok": true,
  "url": "https://your-cms.com/blog/10-seo-mistakes-to-avoid-in-2026",
  "id": "your-internal-cms-post-id"
}
\`\`\`

| Field | Required for | What theStacc does with it |
|---|---|---|
| HTTP status \`2xx\` | every request | Anything else (4xx, 5xx, 3xx) marks the publish as failed and surfaces an error toast in theStacc. |
| \`url\` (or \`published_url\`) | a clickable "View live post" link to appear in theStacc | Stored against the blog. If omitted, theStacc shows a *"Sent to webhook — your receiver didn't return a public URL"* warning. |
| \`id\` | future updates / unpublishes to target the right CMS record | Stored as \`external_post_id\`. Sent back unchanged on subsequent \`blog.updated\` / \`blog.unpublished\` events. |

For preview / test calls (\`test.ping\` or \`blog_id\` starts with \`preview-\`), it's fine to skip both fields and return \`{"ok": true, "skipped": true}\`.

## Self-hosting images (optional)

> **New — May 18, 2026.** The payload now carries an additive \`images\` array listing every image URL in \`content\`, making it straightforward to mirror blog body images into your own storage as part of your CMS-side processing. Backward compatible: receivers that don't read \`images\` are unaffected; every other field is byte-for-byte identical to before this addition. **This entire section is what's new on the page** — if you've integrated previously, this is the only change you need to read.

By default, every \`<img>\` inside \`content\` and the \`featured_image_url\` point at theStacc's CDN, served to your visitors directly. That's the simplest setup and works out of the box.

For deeper CMS integration, many sites prefer to host blog images on their own storage alongside the rest of their media library — the \`images\` array makes that mirror in one pass, with no HTML parsing required.

### When self-hosting helps

- **Same origin as the rest of your site.** Images load from your CDN / domain, sharing the same caching, latency, and edge-rules as the surrounding page.
- **Cleaner CMS integration.** Images live inside your media library — searchable, taggable, and re-usable in other content the same way as any other asset.
- **Self-contained CMS records.** Once mirrored, each post is wholly owned by your CMS with no external image references to track in your asset audits.

### How it works

The \`images\` field is a list of \`{url, alt}\` objects — one per \`<img>\` in the \`content\` body, in document order, with duplicates collapsed. Each \`url\` is byte-for-byte identical to what's in the corresponding \`src=\` attribute inside \`content\`, so a plain string find/replace handles the swap reliably.

\`\`\`js
let content = body.content;

// 1. Mirror every body image.
for (const img of body.images || []) {
  const bytes = await fetch(img.url).then(r => r.arrayBuffer());
  const newUrl = await uploadToMyStorage(bytes, suggestFilename(img.url));
  // The URL string IS the stable identifier — find/replace by full src=.
  content = content.replaceAll(\`src="\${img.url}"\`, \`src="\${newUrl}"\`);
}

// 2. Mirror the featured image separately. It's a top-level field, not
//    in images[] — most CMSes have a dedicated featured-image slot.
let featuredUrl = body.featured_image_url;
if (featuredUrl) {
  const bytes = await fetch(featuredUrl).then(r => r.arrayBuffer());
  featuredUrl = await uploadToMyStorage(bytes, suggestFilename(featuredUrl));
}

// 3. Store \`content\` (with rewritten src=) and \`featuredUrl\` in your CMS.
\`\`\`

That's the entire pattern. No HTML parser, no DOM library, no positional tracking — the URL is the identifier.

### Python receiver

\`\`\`python
content = body["content"]

# 1. Mirror body images.
for img in body.get("images", []):
    blob = httpx.get(img["url"]).content
    new_url = upload_to_my_storage(blob, suggest_filename(img["url"]))
    content = content.replace(f'src="{img["url"]}"', f'src="{new_url}"')

# 2. Mirror the featured image separately.
featured_url = body.get("featured_image_url")
if featured_url:
    blob = httpx.get(featured_url).content
    featured_url = upload_to_my_storage(blob, suggest_filename(featured_url))

# 3. Persist content + featured_url to your CMS.
\`\`\`

### Security: allowlist your fetch host

Whenever a server-side handler downloads URLs from any external source, standard practice is to allowlist trusted hosts before issuing the request. For theStacc images, the trusted host is \`cdn.thestacc.com\`:

\`\`\`js
const ALLOWED_HOSTS = new Set(['cdn.thestacc.com']);

async function safeFetch(url) {
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:') throw new Error(\`Refusing non-HTTPS URL: \${url}\`);
  if (!ALLOWED_HOSTS.has(parsed.hostname)) throw new Error(\`Untrusted host: \${parsed.hostname}\`);
  return fetch(url);
}

for (const img of body.images || []) {
  const bytes = await safeFetch(img.url).then(r => r.arrayBuffer());
  // …then upload + find/replace as before.
}
\`\`\`

Same shape in Python:

\`\`\`python
from urllib.parse import urlparse

ALLOWED_HOSTS = {"cdn.thestacc.com"}

def safe_fetch(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Refusing non-HTTPS URL: {url}")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Untrusted host: {parsed.hostname}")
    return httpx.get(url).content
\`\`\`

Apply the same allowlist to \`featured_image_url\`. With it in place, every body and featured image fetches through a single auditable choke point.

### Notes

- **Featured image is NOT in \`images[]\`.** It's a separate top-level field (\`featured_image_url\`). theStacc strips the inline duplicate from \`content\` before sending so the page doesn't render the same image twice.
- **Duplicate URLs are deduped.** If the same body image appears twice, the array lists it once. Your \`content.replaceAll(…)\` swaps every occurrence in one pass anyway.
- **\`alt\` may be empty.** Decorative images and images the generator didn't caption ship with \`alt: ""\`. Pass it through verbatim to preserve accessibility on your re-hosted copy.
- **Backward compatible.** Receivers that ignore \`images\` continue working unchanged — every other field is byte-for-byte identical to before this field was added.
- **\`data-image-id\` is not used.** We intentionally do **not** inject any per-image identifier attribute into the \`<img>\` tags inside \`content\` — the existing HTML shape is preserved exactly. The URL itself is the stable identifier.
- **\`images[]\` mirrors \`content\` verbatim.** URLs reflect exactly what's in each \`src=\` attribute, so a one-to-one find/replace works without any normalization step. The host allowlist above handles any unusual value (relative path, \`data:\` URI, etc.) uniformly without per-shape special-casing.
- **SEO-friendly, globally unique basenames — flat storage works.** Body images use slug-based basenames like \`{slug}-{blog_id_short8}-{uuid8}.png\` — e.g. \`solar-installation-rajasthan-rooftop-5d0035a4-2c857f8b.png\`. The \`slug\` portion is derived from the image's alt text (capped at 60 chars, lowercase, ASCII-only) so receivers that use the URL as their CDN-facing filename get SEO value for free. \`blog_id_short8\` is the first 8 hex chars of the blog UUID and \`uuid8\` is a random 8-hex suffix — together 64 bits of entropy, so the basename alone is guaranteed unique across every blog you ever receive. If your CMS or storage layer prefers a flat directory (no per-blog subfolders), \`url.split('/').pop()\` gives you a collision-free key directly. Images uploaded before each naming-convention change keep their original basenames — receivers handle all formats transparently because the find/replace mirror loop operates on the full URL string regardless of basename shape. Historical formats you may encounter on older blogs: \`{blog_id}_{YYYYMMDD_HHMMSS}_{8-hex}.png\` (May 18 – May 20 2026) and \`{YYYYMMDD_HHMMSS}_{8-hex}.png\` (pre-May 18 2026, Gemini-era).

### Migrating blogs already published with theStacc's URLs

If you have blogs already in your CMS with theStacc CDN URLs and you want to switch them to self-hosted images:

1. Open each blog in theStacc → click **Publish** to re-publish.
2. The webhook fires as \`blog.updated\` with the new \`images\` array.
3. Your receiver runs the mirror loop above and updates the post (same \`blog_id\` → same CMS record).
4. The CMS post now stores your URLs instead of theStacc's.

There's no bulk-republish API — for most accounts this is a one-shot migration of a handful of posts.

## Database schema templates

Pick the database you already use. Each schema below maps directly to the webhook payload — no transformation needed.

### Postgres

\`\`\`sql
CREATE TABLE thestacc_blogs (
    blog_id           UUID PRIMARY KEY,
    title             TEXT NOT NULL,
    slug              TEXT NOT NULL UNIQUE,
    content           TEXT NOT NULL,
    excerpt           TEXT,
    meta_title        TEXT,
    meta_description  TEXT,
    featured_image_url TEXT,
    keyword           TEXT,
    categories        TEXT[] NOT NULL DEFAULT '{}',
    tags              TEXT[] NOT NULL DEFAULT '{}',
    published_at      TIMESTAMPTZ NOT NULL,
    last_event        TEXT NOT NULL,
    received_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    cms_post_id       TEXT,
    is_unpublished    BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_thestacc_blogs_slug ON thestacc_blogs(slug);
CREATE INDEX idx_thestacc_blogs_published_at ON thestacc_blogs(published_at DESC);
CREATE INDEX idx_thestacc_blogs_active ON thestacc_blogs(published_at DESC) WHERE is_unpublished = FALSE;
\`\`\`

### MySQL / MariaDB

\`\`\`sql
CREATE TABLE thestacc_blogs (
    blog_id            CHAR(36) PRIMARY KEY,
    title              VARCHAR(255) NOT NULL,
    slug               VARCHAR(255) NOT NULL UNIQUE,
    content            LONGTEXT NOT NULL,
    excerpt            TEXT,
    meta_title         VARCHAR(255),
    meta_description   VARCHAR(500),
    featured_image_url VARCHAR(2048),
    keyword            VARCHAR(255),
    categories         JSON NOT NULL,
    tags               JSON NOT NULL,
    published_at       DATETIME(3) NOT NULL,
    last_event         VARCHAR(50) NOT NULL,
    received_at        DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at         DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    cms_post_id        VARCHAR(255),
    is_unpublished     BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX idx_slug (slug),
    INDEX idx_published_at (published_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
\`\`\`

### Prisma (Postgres-flavored)

\`\`\`prisma
model ThestaccBlog {
  blogId            String    @id @map("blog_id") @db.Uuid
  title             String
  slug              String    @unique
  content           String
  excerpt           String?
  metaTitle         String?   @map("meta_title")
  metaDescription   String?   @map("meta_description")
  featuredImageUrl  String?   @map("featured_image_url")
  keyword           String?
  categories        String[]
  tags              String[]
  publishedAt       DateTime  @map("published_at")
  lastEvent         String    @map("last_event")
  receivedAt        DateTime  @default(now()) @map("received_at")
  updatedAt         DateTime  @updatedAt @map("updated_at")
  cmsPostId         String?   @map("cms_post_id")
  isUnpublished     Boolean   @default(false) @map("is_unpublished")

  @@index([slug])
  @@index([publishedAt(sort: Desc)])
  @@map("thestacc_blogs")
}
\`\`\`

### MongoDB

\`\`\`js
db.createCollection("thestaccBlogs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["blog_id", "title", "slug", "content", "published_at", "last_event"],
      properties: {
        blog_id:            { bsonType: "string" },
        title:              { bsonType: "string" },
        slug:               { bsonType: "string" },
        content:            { bsonType: "string" },
        excerpt:            { bsonType: ["string", "null"] },
        meta_title:         { bsonType: ["string", "null"] },
        meta_description:   { bsonType: ["string", "null"] },
        featured_image_url: { bsonType: ["string", "null"] },
        keyword:            { bsonType: ["string", "null"] },
        categories:         { bsonType: "array", items: { bsonType: "string" } },
        tags:               { bsonType: "array", items: { bsonType: "string" } },
        published_at:       { bsonType: "date" },
        last_event:         { bsonType: "string" },
        cms_post_id:        { bsonType: ["string", "null"] },
        is_unpublished:     { bsonType: "bool" }
      }
    }
  }
});
db.thestaccBlogs.createIndex({ blog_id: 1 }, { unique: true });
db.thestaccBlogs.createIndex({ slug: 1 }, { unique: true });
db.thestaccBlogs.createIndex({ published_at: -1 });
\`\`\`

## Receiver examples

Each example is **production-ready** — handles every event type, verifies the HMAC signature, dedupes via \`blog_id\`, and returns the response shape theStacc expects.

### Next.js (App Router)

\`\`\`typescript
// app/api/stacc-webhook/route.ts
import crypto from 'crypto';

const SECRET = process.env.STACC_WEBHOOK_SECRET!;

export async function POST(request: Request) {
  // CRITICAL: read raw bytes BEFORE parsing JSON.
  // request.json() consumes the stream and re-serializing
  // would change byte order/whitespace → signature mismatch.
  const rawBody = await request.text();

  const sig = request.headers.get('x-webhook-signature') || '';
  const expected = crypto.createHmac('sha256', SECRET).update(rawBody).digest('hex');

  // Decode both before comparing. Buffer.from with invalid hex returns
  // a shorter buffer (Node stops at the first non-hex char) which would
  // make timingSafeEqual throw RangeError instead of returning false —
  // crashing the receiver on any garbage probe.
  const sigBuf = Buffer.from(sig, 'hex');
  const expBuf = Buffer.from(expected, 'hex');
  const valid =
    sigBuf.length === expBuf.length
    && crypto.timingSafeEqual(sigBuf, expBuf);

  if (!valid) {
    return new Response('Invalid signature', { status: 401 });
  }

  const body = JSON.parse(rawBody);

  if (body.event === 'test.ping') {
    return Response.json({ ok: true });
  }

  if (body.event === 'blog.published' || body.event === 'blog.updated') {
    if (body.blog_id?.startsWith('preview-')) {
      return Response.json({ ok: true, skipped: true });
    }
    const post = await db.thestaccBlog.upsert({
      where: { blogId: body.blog_id },
      create: {
        blogId: body.blog_id,
        title: body.title,
        slug: body.slug,
        content: body.content,
        excerpt: body.excerpt || null,
        metaTitle: body.meta_title || null,
        metaDescription: body.meta_description || null,
        featuredImageUrl: body.featured_image_url || null,
        keyword: body.keyword || null,
        categories: body.categories || [],
        tags: body.tags || [],
        publishedAt: new Date(body.published_at),
        lastEvent: body.event,
      },
      update: {
        title: body.title,
        slug: body.slug,
        content: body.content,
        excerpt: body.excerpt || null,
        metaTitle: body.meta_title || null,
        metaDescription: body.meta_description || null,
        featuredImageUrl: body.featured_image_url || null,
        keyword: body.keyword || null,
        categories: body.categories || [],
        tags: body.tags || [],
        publishedAt: new Date(body.published_at),
        lastEvent: body.event,
        isUnpublished: false,
      },
    });
    return Response.json({
      ok: true,
      url: \`https://example.com/blog/\${post.slug}\`,
      id: post.blogId,
    });
  }

  if (body.event === 'blog.unpublished' || body.event === 'blog.deleted') {
    await db.thestaccBlog.update({
      where: { blogId: body.blog_id },
      data: { isUnpublished: true, lastEvent: body.event },
    });
    return Response.json({ ok: true });
  }

  return Response.json({ error: 'Unknown event' }, { status: 400 });
}
\`\`\`

### Express

\`\`\`javascript
import express from 'express';
import crypto from 'crypto';

const app = express();
const SECRET = process.env.STACC_WEBHOOK_SECRET;

// CRITICAL: capture raw body BEFORE express.json() parses it.
app.post('/api/stacc-webhook',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const raw = req.body; // Buffer
    const sig = req.get('x-webhook-signature') || '';
    const expected = crypto.createHmac('sha256', SECRET).update(raw).digest('hex');

    // Length-check the decoded buffers BEFORE timingSafeEqual —
    // invalid hex produces a short buffer and timingSafeEqual throws
    // on mismatched lengths.
    const sigBuf = Buffer.from(sig, 'hex');
    const expBuf = Buffer.from(expected, 'hex');
    if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) {
      return res.status(401).send('Invalid signature');
    }

    const body = JSON.parse(raw.toString('utf8'));
    // ... handle body.event as in the Next.js example
    res.json({ ok: true });
  }
);
\`\`\`

### Astro (server endpoint)

\`\`\`typescript
// src/pages/api/stacc-webhook.ts
import type { APIRoute } from 'astro';
import crypto from 'crypto';

export const prerender = false; // server-rendered, not static

const SECRET = import.meta.env.STACC_WEBHOOK_SECRET;

export const POST: APIRoute = async ({ request }) => {
  const raw = await request.text();
  const sig = request.headers.get('x-webhook-signature') || '';
  const expected = crypto.createHmac('sha256', SECRET).update(raw).digest('hex');

  // Length-check decoded buffers before timingSafeEqual — invalid hex
  // produces a short buffer and timingSafeEqual throws on length mismatch.
  const sigBuf = Buffer.from(sig, 'hex');
  const expBuf = Buffer.from(expected, 'hex');
  if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) {
    return new Response('Invalid signature', { status: 401 });
  }

  const body = JSON.parse(raw);
  // ... handle events as in Next.js example
  return new Response(JSON.stringify({ ok: true }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
\`\`\`

### Python / FastAPI

\`\`\`python
import hmac, hashlib, os
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
SECRET = os.environ["STACC_WEBHOOK_SECRET"].encode()

@app.post("/api/stacc-webhook")
async def receive(request: Request):
    raw = await request.body()  # bytes — DON'T re-serialize
    sig = request.headers.get("x-webhook-signature", "")
    expected = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected, sig):
        raise HTTPException(401, "Invalid signature")

    import json
    body = json.loads(raw)

    if body["event"] == "test.ping":
        return {"ok": True}

    if body["event"] in ("blog.published", "blog.updated"):
        if body.get("blog_id", "").startswith("preview-"):
            return {"ok": True, "skipped": True}
        # ... upsert into your DB
        return {
            "ok": True,
            "url": f"https://example.com/blog/{body['slug']}",
            "id": body["blog_id"],
        }

    if body["event"] in ("blog.unpublished", "blog.deleted"):
        # ... soft-delete by blog_id
        return {"ok": True}

    raise HTTPException(400, "Unknown event")
\`\`\`

### Python / Flask

\`\`\`python
import hmac, hashlib, os
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
SECRET = os.environ["STACC_WEBHOOK_SECRET"].encode()

@app.post("/api/stacc-webhook")
def receive():
    raw = request.get_data()
    sig = request.headers.get("X-Webhook-Signature", "")
    expected = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected, sig):
        abort(401)

    body = request.get_json(force=True)
    # ... same event branching as FastAPI example
    return jsonify({"ok": True})
\`\`\`

### PHP

\`\`\`php
<?php
$raw = file_get_contents('php://input');
$sig = $_SERVER['HTTP_X_WEBHOOK_SIGNATURE'] ?? '';
$expected = hash_hmac('sha256', $raw, getenv('STACC_WEBHOOK_SECRET'));

if (!hash_equals($expected, $sig)) {
    http_response_code(401);
    exit('Invalid signature');
}

$body = json_decode($raw, true);

switch ($body['event']) {
    case 'test.ping':
        echo json_encode(['ok' => true]);
        break;
    case 'blog.published':
    case 'blog.updated':
        if (str_starts_with($body['blog_id'] ?? '', 'preview-')) {
            echo json_encode(['ok' => true, 'skipped' => true]);
            break;
        }
        // ... upsert into DB
        echo json_encode([
            'ok'  => true,
            'url' => "https://example.com/blog/{$body['slug']}",
            'id'  => $body['blog_id'],
        ]);
        break;
    case 'blog.unpublished':
    case 'blog.deleted':
        // ... soft-delete
        echo json_encode(['ok' => true]);
        break;
    default:
        http_response_code(400);
        echo json_encode(['error' => 'Unknown event']);
}
\`\`\`

## Idempotency & retries

theStacc retries are **manual only**. If your endpoint times out (15s) or returns 5xx, the publish fails immediately and the user sees a "Failed to publish" toast — the user clicks Republish to retry.

Two practical implications:

1. **Use \`blog_id\` as a dedup key.** Even though theStacc doesn't auto-retry, the *user* might click Republish multiple times. UPSERT on \`blog_id\` so duplicate clicks converge on the same row instead of creating two posts.

2. **Return 2xx fast, do heavy work async.** If your CMS write involves image processing, search re-indexing, or CDN purging, run those in a background job after responding. A 15-second sync write will time out theStacc's call.

\`\`\`typescript
// Example: respond fast, queue the heavy work
export async function POST(request: Request) {
  // ... verify signature, parse body ...

  await db.thestaccBlog.upsert({ /* ... */ }); // fast — just writes the row

  // Fire-and-forget: image upload, ISR revalidate, search index, etc.
  enqueueBackgroundJob('process-blog', body.blog_id);

  return Response.json({ ok: true, url, id });
}
\`\`\`

## Limits & operational rules

| Rule | Value | Why |
|---|---|---|
| **Response timeout** | 15 seconds | Slow CMS writes will fail. Return 2xx fast. |
| **HTTP status accepted** | 2xx (200, 201, 202) | 3xx, 4xx, 5xx all fail the publish. |
| **Redirects** | Rejected | Anti-SSRF: a public webhook receiver could 302 to internal addresses. |
| **HTTPS required** | Yes | \`http://\` URLs and private IP ranges rejected at save time. |
| **Custom headers** | Up to 20 key/value pairs | For bearer tokens / API keys. Keys ≤ 100 chars, values ≤ 1000. |
| **Webhook secret length** | 16+ characters recommended | We don't enforce a minimum, but anything shorter is brute-forceable. |
| **Auto-retries** | None | A failed publish stays failed until the user clicks Republish. |
| **Concurrent publishes** | Possible | If a user bulk-publishes, your endpoint may receive multiple requests in parallel. Use UPSERT, not INSERT. |
| **Payload size** | Typically < 50 KB | Driven by \`content\` length. Hard cap is 1 MB on theStacc side. |

## Troubleshooting

Concrete error → cause → fix:

| What you see in theStacc | Cause | Fix |
|---|---|---|
| "Could not reach the URL" on Test Connection | Receiver not deployed, wrong URL, or blocked by firewall | curl your URL from outside your network. Check hosting platform logs. |
| "Webhook returned redirect 301/302" | Your route redirects (e.g., HTTP→HTTPS, or trailing-slash redirect) | Configure theStacc with the FINAL URL. Receivers must respond directly with 2xx. |
| "Webhook returned 401" on Test Connection | Signature verification failing on your side | Likely re-serialization bug. Hash the **raw body bytes**, not parsed JSON. |
| "Webhook returned 4xx" on real publish but 2xx on Test | Your handler errors on \`blog.published\` but not on \`test.ping\` | Run **Sample Payload** in theStacc — it sends the real shape with \`preview-\` prefix so your full handler runs without writing real data. |
| "Sent to webhook — your receiver didn't return a public URL" | You returned 2xx but no \`url\` field in the response | Add \`url\` to your response JSON. theStacc displays it in the dashboard. |
| Publish "succeeds" but post never appears on site | You returned 2xx without actually writing to your DB | Check your server logs — your handler probably threw an error after the response was sent. |
| "Webhook URL must be HTTPS" at save time | URL starts with \`http://\` or points to localhost / 127.0.0.1 / 192.168.x | Deploy publicly with HTTPS. For local dev, use ngrok or a similar tunnel. |
| Some publishes succeed, others time out | Your handler is slow under load | Move the heavy work (image upload, search reindex) to a background queue. Respond 2xx in < 1s. |

## Security best practices

1. **Always set a webhook secret.** Without one, anyone who guesses your URL can post fake blogs.
2. **Use \`crypto.timingSafeEqual\` / \`hmac.compare_digest\`** when comparing signatures — plain \`===\` is timing-attack vulnerable.
3. **Hash the raw body, not the parsed JSON.** Re-serialization changes whitespace and breaks signatures.
4. **Store the secret in env vars only.** Never commit to git, never include in client-side code.
5. **Rotate the secret on suspected leak.** Generate a new one, update both your env var and theStacc's integration settings, redeploy. theStacc starts using the new secret on the next request.
6. **Run your receiver behind HTTPS-only.** Add HSTS if you control the domain.
7. **Rate-limit the receiver.** Even with HMAC, a flood of unauthenticated requests can DoS your endpoint while you reject them. Cloudflare / your hosting platform usually does this automatically.

## FAQ — questions clients ask

**How does the handshake work?**
There's no traditional handshake — it's stateless per-request authentication. The "handshake" is just storing a shared secret on both sides, once, during setup. Every subsequent request is independently authenticated via HMAC. See [How the handshake works](#how-the-handshake-works) above.

**What identifies a request as coming from theStacc?**
The \`X-Webhook-Signature\` header verified against your secret. Nothing else is reliable — anyone can fake the body content, the User-Agent, or the source IP.

**Does the signature change over time?**
The signature is deterministic — same secret + same body bytes = same signature, every time. In practice every request has a unique signature because every payload contains a unique \`blog_id\` and \`published_at\` timestamp. See [Properties of the signature](#properties-of-the-signature).

**What's the maximum title / slug / content length?**
We don't enforce length limits at the API level — theStacc-generated content stays well within reasonable bounds (titles ~120 chars, slugs ~50 chars, content ~15 000 chars). If your CMS or DB needs hard caps, the [Field reference](#field-reference) table lists safe defaults.

**What if my receiver is slow / down when a publish happens?**
The publish fails for that specific blog. The user sees a "Failed to publish" toast and can click Republish once your endpoint is healthy. There's no automatic retry queue.

**Can I get historical blogs through the webhook?**
No — webhooks are forward-only. For backfills, use the [Public Blog API](/docs/developers/public-blog-api) which lets you fetch all your published blogs.

**Do I need to handle \`test.ping\` separately?**
Yes — it has no blog fields. If your handler tries to read \`title\` or \`content\` from a \`test.ping\` event, it'll error out and Test Connection will fail. Branch on \`event\` first.

**Can I receive webhooks from staging and production into the same endpoint?**
Yes. theStacc doesn't tag the source. If you need to differentiate, set different \`Authorization\` custom headers in each integration, or use different webhook URLs.

**How do I rotate the webhook secret?**
Generate a new secret, update your env var, redeploy, then update theStacc's integration. There's a brief window (< 30s) where one publish could fail if it lands between updates — schedule rotation during quiet hours, or use a temporary "accept either secret" check during the transition.

**Can theStacc post to multiple webhook URLs?**
Yes — set up multiple Custom Webhook integrations on the same project. Each gets its own URL, secret, and headers. theStacc fires every published blog at every active integration.

**What happens if I delete a blog in theStacc?**
We send \`event: "blog.deleted"\` with the \`blog_id\` and \`title\`. Your handler should remove or hide the post in your CMS. If the receiver fails, the blog stays deleted in theStacc but lingers on your site — periodic reconciliation via the [Public Blog API](/docs/developers/public-blog-api) is a defensive option.

## Next steps

- Set up the integration in [Connect Platforms → Custom Webhook](/docs/content-seo/connect-platforms)
- Reference the [Public Blog API](/docs/developers/public-blog-api) if you also want to backfill historical content
- See the [Static Site Integration](/docs/developers/static-site-integration) guide for static-site-specific patterns`,
      },
    ],
  },
];

// Helper functions
export function getDocBySlug(
  categorySlug: string,
  pageSlug: string
): { category: DocsCategory; page: DocsPage } | undefined {
  const category = docsCategories.find((c) => c.slug === categorySlug);
  if (!category) return undefined;
  const page = category.items.find((p) => p.slug === pageSlug);
  if (!page) return undefined;
  return { category, page };
}

export function getAllDocPaths() {
  return docsCategories.flatMap((category) =>
    category.items.map((page) => ({
      params: { slug: `${category.slug}/${page.slug}` },
      props: { category, page },
    }))
  );
}

export function getPopularDocs(): { category: DocsCategory; page: DocsPage }[] {
  const popular: { category: DocsCategory; page: DocsPage }[] = [];
  for (const category of docsCategories) {
    for (const page of category.items) {
      if (page.popular) {
        popular.push({ category, page });
      }
    }
  }
  return popular;
}

export function getNextDoc(
  categorySlug: string,
  pageSlug: string
): { category: DocsCategory; page: DocsPage } | undefined {
  const allPages = docsCategories.flatMap((c) =>
    c.items.map((p) => ({ category: c, page: p }))
  );
  const currentIndex = allPages.findIndex(
    (p) => p.category.slug === categorySlug && p.page.slug === pageSlug
  );
  if (currentIndex === -1 || currentIndex >= allPages.length - 1) return undefined;
  return allPages[currentIndex + 1];
}

export function getPrevDoc(
  categorySlug: string,
  pageSlug: string
): { category: DocsCategory; page: DocsPage } | undefined {
  const allPages = docsCategories.flatMap((c) =>
    c.items.map((p) => ({ category: c, page: p }))
  );
  const currentIndex = allPages.findIndex(
    (p) => p.category.slug === categorySlug && p.page.slug === pageSlug
  );
  if (currentIndex <= 0) return undefined;
  return allPages[currentIndex - 1];
}
