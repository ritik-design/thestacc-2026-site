---
title: "How to Connect GSC to Claude via MCP: Step-by-Step Guide"
description: "Connect Google Search Console to Claude via MCP in 15 minutes. OAuth and service account setup, 20 built-in tools, and real queries you can run today."
slug: "connect-gsc-claude-mcp"
keyword: "GSC MCP Claude"
author: "Sarah Chen"
authorRole: "Content Strategist"
reviewedBy: "Stacc Editorial Team"
reviewerRole: "Content Review Board"
expertise: "AI Content, SEO Analytics, Marketing Trends"
date: "2026-05-18"
lastUpdated: "2026-05-18"
factChecked: true
category: "Content Strategy"
image: "/blogs-preview-images/connect-gsc-claude-mcp.png"
---

# How to Connect GSC to Claude via MCP: Step-by-Step Guide

Connecting Google Search Console to Claude via MCP takes 15 minutes and replaces hours of manual data pulling. Once connected, you can ask Claude questions like "Which pages lost the most traffic last month?" or "What keywords have CTR below 2%?" and get answers drawn from live GSC data in seconds.

This guide covers the complete setup process for both OAuth and service account authentication. It works with Claude Desktop, Claude Code, and any MCP-compatible client. You do not need a paid Claude subscription for the basic integration, though some advanced features require Claude Pro or Team.

Stacc publishes 30+ articles per month on content strategy and search optimization. The workflow below is the same process our editorial team uses to monitor keyword movement, identify content gaps, and flag indexing issues without opening the GSC dashboard.

Here is what you will learn:

- What MCP is and why it matters for SEO workflows
- How to choose between OAuth and service account authentication
- The exact step-by-step setup for both methods
- How to configure Claude Desktop and Claude Code
- Twenty built-in tools you can use immediately
- Real prompts that save hours every week
- How to troubleshoot the five most common setup errors

## What You Need Before Starting

The setup requires four things. Most SEO professionals already have the first two.

| Requirement | Purpose | Cost |
|---|---|---|
| Google account with GSC access | Authenticate and pull data | Free |
| Claude Desktop or Claude Code | MCP client that connects to the server | Free plan works |
| Node.js 18+ installed | Run the MCP server package | Free |
| Google Cloud project | Create OAuth or service account credentials | Free |

If you do not have Node.js installed, download the LTS version from [nodejs.org](https://nodejs.org). Verify the installation by opening a terminal and running `node --version`. You should see a version number of 18.0.0 or higher.

Claude Desktop is the graphical application from Anthropic. Claude Code is the command-line version. Both support MCP. This guide covers both clients.

## Step 1: Choose Your Authentication Method

You have two options for connecting GSC to Claude via MCP: OAuth or service account. The right choice depends on your use case.

**OAuth** is best for individual users who manage one or a few properties. It uses your personal Google account credentials. You authenticate once through a browser popup, and the MCP server stores a refresh token locally. This is the fastest setup and requires no Google Cloud billing.

**Service account** is best for teams, agencies, and automation workflows. It uses a machine identity rather than a personal account. You create a service account in Google Cloud, download a JSON key file, and add that account as a user in Google Search Console. Multiple team members can share the same service account credentials, and the connection does not depend on any individual's Google session.

| Factor | OAuth | Service Account |
|---|---|---|
| Setup time | 5 minutes | 10 minutes |
| Best for | Individual users | Teams and agencies |
| Shared access | No | Yes |
| Automation friendly | Limited | Yes |
| Token expiration | Refreshs automatically | Never expires |
| Google Cloud billing | Not required | Not required |

If you are setting this up for the first time, start with OAuth. You can always switch to a service account later without losing data or configuration.

## Step 2: Create a Google Cloud Project

Whether you choose OAuth or service account, you need a Google Cloud project. This is where API access is managed.

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project selector at the top of the page
3. Click "New Project"
4. Name it "GSC MCP" or any descriptive name
5. Click "Create"

Wait for the project to finish creating. The page will refresh automatically. Make sure the new project is selected in the project selector before proceeding to the next step.

## Step 3: Enable the Google Search Console API

With your project selected, enable the API that the MCP server will use to pull data.

1. In the Google Cloud console, click the hamburger menu (three lines) in the top left
2. Work through to "APIs & Services" → "Library"
3. Search for "Google Search Console API"
4. Click on "Google Search Console API" in the results
5. Click the "Enable" button

The API is now active for your project. You do not need to enable billing for this API at standard usage levels.

Optionally, you can also enable the "Web Search Indexing API" if you want to submit URLs for indexing through Claude. This is not required for data analysis but is useful for active SEO management.

## Step 4A: Set Up OAuth Authentication

This section is for individual users. If you are setting up a service account, skip to Step 4B.

### 4A.1: Configure the OAuth Consent Screen

1. In Google Cloud, go to "APIs & Services" → "OAuth consent screen"
2. Select "External" as the user type
3. Click "Create"
4. Fill in the app name: "GSC MCP"
5. Add your email address as the user support email and developer contact email
6. Click "Save and Continue" three times to skip the optional scopes and test user screens
7. Click "Back to Dashboard"

### 4A.2: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. For application type, select "Desktop app"
4. Name it "GSC MCP Desktop"
5. Click "Create"
6. Click "Download JSON" and save the file to a secure location on your computer
7. Note the file path. You will need it in Step 5

The downloaded file contains your client ID and client secret. Do not share it or commit it to version control.

### 4A.3: Install the MCP Server

Open a terminal and run:

```bash
npx -y suganthan-gsc-mcp
```

This downloads and runs the MCP server package. The first run may take 30 to 60 seconds because npx downloads the package. Subsequent runs are instant.

If you see an error about `npx` not being found, verify that Node.js is installed correctly and that `npx` is in your system PATH.

## Step 4B: Set Up Service Account Authentication

This section is for teams and agencies. If you already completed OAuth setup, skip to Step 5.

### 4B.1: Create a Service Account

1. In Google Cloud, go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it "gsc-mcp-service"
4. Click "Create and Continue"
5. Skip the role assignment by clicking "Continue"
6. Click "Done"

### 4B.2: Create and Download a JSON Key

1. Find your new service account in the list and click on it
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" as the key type
5. Click "Create"
6. The JSON key file downloads automatically. Save it to a secure location
7. Note the file path. You will need it in Step 5

### 4B.3: Add the Service Account to Google Search Console

This is the critical step many people miss. The service account must have explicit permission to access your GSC data.

1. Open the downloaded JSON key file in a text editor
2. Copy the `client_email` value. It looks like `gsc-mcp-service@your-project.iam.gserviceaccount.com`
3. Go to [search.google.com/search-console](https://search.google.com/search-console)
4. Select the property you want to connect
5. Click the gear icon → "Users and permissions"
6. Click "Add user"
7. Paste the service account email address
8. Set permission level to "Full"
9. Click "Add"

Repeat steps 4 through 9 for every GSC property you want Claude to access.

### 4B.4: Install the MCP Server

Open a terminal and run:

```bash
npx -y suganthan-gsc-mcp
```

## Step 5: Configure Claude Desktop

With authentication credentials ready, you now tell Claude Desktop how to connect to the MCP server.

### 5.1: Open the Configuration File

1. Open Claude Desktop
2. Click "Claude" in the menu bar (Mac) or the hamburger menu (Windows)
3. Select "Settings" → "Developer"
4. Click "Edit Config"

This opens the `claude_desktop_config.json` file in your default text editor.

### 5.2: Add the MCP Server Configuration

For **OAuth** authentication, paste this configuration into the JSON file. Replace the placeholder paths with your actual file locations:

```json
{
  "mcpServers": {
    "gsc": {
      "command": "npx",
      "args": ["-y", "suganthan-gsc-mcp"],
      "env": {
        "GSC_AUTH_MODE": "oauth",
        "GSC_OAUTH_SECRETS_FILE": "/Users/yourname/gsc-oauth-secrets.json",
        "GSC_SITE_URL": "sc-domain:yourdomain.com"
      }
    }
  }
}
```

For **service account** authentication, use this configuration instead:

```json
{
  "mcpServers": {
    "gsc": {
      "command": "npx",
      "args": ["-y", "suganthan-gsc-mcp"],
      "env": {
        "GSC_AUTH_MODE": "service_account",
        "GSC_KEY_FILE": "/Users/yourname/gsc-service-key.json",
        "GSC_SITE_URL": "sc-domain:yourdomain.com"
      }
    }
  }
}
```

### Critical Formatting Notes

The `GSC_SITE_URL` value must match exactly how your property is registered in Google Search Console:

| Property Type | Correct Format | Incorrect Format |
|---|---|---|
| Domain property | `sc-domain:yourdomain.com` | `https://yourdomain.com` |
| URL-prefix property | `https://www.yourdomain.com/` | `yourdomain.com` |

For **multiple properties**, add the `GSC_SITE_URLS` environment variable as a comma-separated list:

```json
"GSC_SITE_URLS": "sc-domain:site1.com,sc-domain:site2.com,https://www.site3.com/"
```

### 5.3: Save and Restart Claude Desktop

Save the configuration file. Then **fully quit** Claude Desktop. On Mac, press Cmd+Q. On Windows, right-click the Claude icon in the system tray and select "Quit." Do not just close the window. The configuration only loads on a full restart.

Reopen Claude Desktop. Go to Settings → Developer. You should see "gsc" listed under MCP servers with a green "Running" indicator.

## Step 6: Configure Claude Code

If you use Claude Code (the command-line version), the setup is similar but uses a different configuration file.

### 6.1: Add the MCP Server

Run this command in your terminal:

```bash
claude mcp add gsc -- npx -y suganthan-gsc-mcp
```

Then set the required environment variables:

For **OAuth**:
```bash
claude mcp env gsc GSC_AUTH_MODE=oauth
claude mcp env gsc GSC_OAUTH_SECRETS_FILE=/Users/yourname/gsc-oauth-secrets.json
claude mcp env gsc GSC_SITE_URL=sc-domain:yourdomain.com
```

For **service account**:
```bash
claude mcp env gsc GSC_AUTH_MODE=service_account
claude mcp env gsc GSC_KEY_FILE=/Users/yourname/gsc-service-key.json
claude mcp env gsc GSC_SITE_URL=sc-domain:yourdomain.com
```

### 6.2: Verify the Connection

Start a new Claude Code session and type:

```
/mcp
```

You should see "gsc" listed with a "connected" status. If you see "error" or "disconnected," check the troubleshooting section below.

## Step 7: Authenticate and Test

The first time you use the MCP server, it needs to authenticate with Google.

### For OAuth Users

1. Start a new conversation in Claude Desktop
2. Type: "List all my Search Console properties"
3. Claude will call the GSC MCP tool
4. A browser window opens asking you to sign in to Google
5. Sign in with the Google account that has GSC access
6. Grant permission for the app to access Search Console data
7. Return to Claude. The response will list your properties

The authentication token is stored locally and refreshes automatically. You only need to complete this flow once.

### For Service Account Users

No additional authentication step is required. The service account JSON key contains all the credentials needed. Start a new conversation and ask:

```
Show me a site snapshot for the last 28 days
```

If the service account was added to GSC correctly, Claude will return a summary of clicks, impressions, CTR, and position data.

## What You Can Do With GSC Connected to Claude

The suganthan-gsc-mcp package includes 20 built-in tools organized into four categories. Here is the complete list:

### Analysis Tools (11)

| Tool | What It Does |
|---|---|
| Site snapshot | Summary of clicks, impressions, CTR, and position for any date range |
| Quick wins | Keywords ranking on page 2 with high impressions but low CTR |
| Content gaps | Queries where you appear but do not have dedicated content |
| Traffic drops | Pages or queries with significant impression or click declines |
| CTR opportunities | Keywords with below-average CTR for their position |
| Cannibalization check | Multiple pages competing for the same query |
| Content decay | Pages that ranked well but are losing traffic over time |
| URL inspection | Live index status, last crawl, and any issues for a specific URL |
| Topic clusters | Group related queries into thematic clusters |
| CTR vs benchmarks | Compare your CTR to industry averages by position |
| Advanced search analytics | Custom filtering by query, page, country, device, and date |

### Monitoring Tools (2)

| Tool | What It Does |
|---|---|
| Check alerts | Any manual actions, security issues, or coverage problems |
| Verify claim | Confirm that a specific claim is supported by your GSC data |

### Reporting Tools (3)

| Tool | What It Does |
|---|---|
| Content recommendations | Suggest content updates based on performance data |
| Generate report | Create a formatted performance report for any date range |
| Multi-site dashboard | Aggregate data across multiple GSC properties |

### Indexing Tools (4)

| Tool | What It Does |
|---|---|
| Submit URL | Request indexing for a single URL |
| Batch submit | Request indexing for multiple URLs at once |
| Submit sitemap | Submit or resubmit a sitemap URL |
| List sitemaps | Show all submitted sitemaps and their status |

## Real Prompts That Save Hours Every Week

Here are prompts you can use immediately after setup. Each replaces a manual task that typically takes 15 to 60 minutes.

**Prompt 1: Find quick-win keywords**

```
Show me keywords ranking on page 2 with more than 1,000 impressions in the last 28 days but CTR below 2%. Sort by impression volume descending.
```

This replaces 20 minutes of manual filtering in the GSC Performance tab.

**Prompt 2: Detect traffic drops**

```
Compare the last 28 days to the previous 28 days. Which pages lost more than 20% of clicks? Show the page URL, previous clicks, current clicks, and percentage change.
```

This replaces 30 minutes of date-range comparison and spreadsheet work.

**Prompt 3: Find content gaps**

```
What queries am I showing up for where I do not have a dedicated page? Filter for queries with more than 500 impressions and average position worse than 15.
```

This replaces 45 minutes of query-by-query analysis and cross-referencing with your content inventory.

**Prompt 4: Check for cannibalization**

```
Are multiple pages on my site competing for the same query? Show any query where more than 2 pages received impressions, along with each page's average position.
```

This replaces 60 minutes of manual cross-referencing across multiple GSC exports.

**Prompt 5: Monitor indexing health**

```
Check the index coverage for my site. How many pages are excluded, and what are the top reasons? Compare to the previous month.
```

This replaces the need to open the GSC Index Coverage report and manually count categories.

## Troubleshooting Common Setup Errors

Even with clear instructions, five errors come up repeatedly. Here is how to fix each one.

### Error 1: "spawn npx ENOENT" (Windows)

**Symptom:** Claude shows an error about not finding `npx` when trying to start the MCP server.

**Cause:** On Windows, the `npx` command is `npx.cmd`, and Claude cannot resolve it directly.

**Fix:** Change your configuration to use the `cmd /c` wrapper:

```json
{
  "mcpServers": {
    "gsc": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "suganthan-gsc-mcp"],
      "env": {
        "GSC_AUTH_MODE": "oauth",
        "GSC_OAUTH_SECRETS_FILE": "C:\\Users\\YourName\\gsc-oauth-secrets.json",
        "GSC_SITE_URL": "sc-domain:yourdomain.com"
      }
    }
  }
}
```

### Error 2: "Property not found" or "User does not have permission"

**Symptom:** Claude returns an error saying the site URL is not found or the user lacks permission.

**Cause:** The `GSC_SITE_URL` format does not match how the property is registered in Search Console, or the service account was not added as a user.

**Fix:**
- For domain properties, use `sc-domain:yourdomain.com` with no protocol
- For URL-prefix properties, use the exact URL including `https://` and trailing slash
- For service accounts, verify the client_email was added to GSC with "Full" permission

### Error 3: MCP Server Shows "Error" After Restart

**Symptom:** The GSC server shows a red "Error" status in Claude Desktop settings.

**Cause:** The JSON configuration has a syntax error, or the credential file path is incorrect.

**Fix:**
- Validate your JSON at [jsonlint.com](https://jsonlint.com)
- Ensure all paths are absolute, not relative
- Verify the credential file exists at the specified path
- Check that there are no trailing commas in the JSON

### Error 4: OAuth Token Expires or Prompts Repeatedly

**Symptom:** You have to re-authenticate through Google every time you start Claude.

**Cause:** The OAuth refresh token is not being stored or read correctly.

**Fix:** Update to `suganthan-gsc-mcp` version 2.2.1 or later. Earlier versions had a bug where concurrent tool calls triggered duplicate authentication flows, causing token storage to fail. The latest version reuses active auth sessions.

### Error 5: "Rate limit exceeded"

**Symptom:** Claude returns an error about exceeding API quotas after running several queries.

**Cause:** Google Search Console API has quota limits. The default is 200 queries per 100 seconds per user.

**Fix:** Space out your queries. If you are running batch analysis across multiple date ranges, break the work into smaller chunks. For high-volume use, request a quota increase in the Google Cloud console under APIs & Services → Quotas.

## What About Hallucinations?

A common concern with AI-driven data analysis is hallucination, where the AI makes up data or draws incorrect conclusions. The suganthan-gsc-mcp server includes three guardrails against this:

1. **Data provenance metadata:** Every tool response includes a `_meta` field showing the exact GSC API endpoint called, the parameters used, and the timestamp of the request. You can verify any number by checking the raw API response.

2. **Verify claim tool:** A dedicated tool that cross-checks a specific claim against your live GSC data. If Claude says "Your CTR improved 15%," you can ask it to verify that claim, and it will re-query the data to confirm.

3. **Structured output:** The tools return structured JSON rather than free text, which reduces the opportunity for the AI to embellish or misinterpret.

These measures do not eliminate the need for human review, but they reduce the risk of acting on fabricated data.

## Frequently Asked Questions

**What is MCP?**

MCP stands for Model Context Protocol. It is an open standard created by Anthropic that lets AI assistants connect to external tools and data sources. Think of it as a USB-C port for AI applications. One protocol, many devices. For a deeper explanation, see our [guide to what MCP is](/blog/what-is-mcp/).

**Do I need a paid Claude subscription?**

No. The MCP integration works on Claude's free plan. However, Claude Pro and Team plans offer higher usage limits and longer context windows, which are helpful when analyzing large GSC datasets.

**Is my GSC data secure?**

With OAuth, your data flows directly from Google's API to Claude on your local machine. The MCP server does not send data to third-party servers. With service accounts, the same direct API connection applies. The credential files are stored locally. Do not share them or commit them to version control.

**Can I connect multiple GSC properties?**

Yes. Use the `GSC_SITE_URLS` environment variable with a comma-separated list of properties. Claude can then query any property in the list and even compare data across properties.

**Does this work with other AI assistants?**

The suganthan-gsc-mcp package works with any MCP-compatible client, including Claude Desktop, Claude Code, Cursor, and VS Code with the appropriate extensions. The configuration syntax may vary slightly by client.

**What is the difference between this and just exporting GSC data to CSV?**

Exporting to CSV is a one-time snapshot. The MCP connection gives Claude live access to your data. You can ask follow-up questions, compare date ranges dynamically, and get recommendations based on the full dataset without manual exports or spreadsheet work.

**Can I use this to modify my GSC data?**

No. The MCP server has read-only access to your search analytics data. The only write operations available are URL indexing requests and sitemap submissions, which are standard GSC functions.

**What if I already use a paid SEO tool?**

Paid SEO tools like Ahrefs, Semrush, and Screaming Frog offer broader data sources and competitive analysis. The GSC MCP connection does not replace them. It complements them by giving you instant, conversational access to your own first-party search data without opening another dashboard.

## Key Takeaways

- Connecting GSC to Claude via MCP takes 15 minutes and replaces hours of manual data work each week
- OAuth is fastest for individuals. Service accounts are best for teams and automation
- The `GSC_SITE_URL` format must exactly match your property type in Search Console
- Twenty built-in tools cover analysis, monitoring, reporting, and indexing
- Common errors involve path formatting, JSON syntax, and Windows command resolution
- Hallucination guardrails include data provenance metadata, a verify claim tool, and structured output
- The integration is read-only and does not replace dedicated SEO tools, but it dramatically speeds up first-party data analysis

If you have not connected GSC to Claude yet, the 15-minute setup is one of the highest-ROI technical tasks you can complete this week. The ability to ask questions in plain English and get answers from live search data changes how you approach SEO analysis.

> **Get more from your search data.** Stacc helps brands turn GSC insights into content strategies that rank. From quick-win keyword identification to full content gap analysis, we build the editorial calendar from your actual search performance. [See how we use GSC data →](/blog/mcp-content-marketing/)
