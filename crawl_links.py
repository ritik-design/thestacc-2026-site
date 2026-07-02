#!/usr/bin/env python3
"""Crawl the local preview and report broken internal links."""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import urlopen, Request

BASE = "http://localhost:7777"
MAX_PAGES = 2500
WORKERS = 20

visited = set()
to_visit = {BASE + "/", BASE + "/blog/"}
broken = []

class LinkExtractor(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base = base_url
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append(urljoin(self.base, attrs["href"]))
        if tag in ("img", "script", "source", "video", "audio", "iframe") and attrs.get("src"):
            self.links.append(urljoin(self.base, attrs["src"]))

def is_internal(url):
    parsed = urlparse(url)
    base_parsed = urlparse(BASE)
    return parsed.netloc in (base_parsed.netloc, "") and parsed.scheme in ("http", "https", "")

def check(url):
    url = urldefrag(url)[0]
    if url in visited:
        return None
    visited.add(url)
    req = Request(url, headers={"User-Agent": "audit-crawler/1.0"})
    try:
        with urlopen(req, timeout=20) as resp:
            ctype = resp.headers.get("Content-Type", "")
            body = resp.read()
            status = resp.status
            if status >= 400:
                broken.append((url, status))
            if "text/html" in ctype and len(visited) < MAX_PAGES:
                html = body.decode("utf-8", errors="replace")
                extractor = LinkExtractor(url)
                extractor.feed(html)
                for link in extractor.links:
                    link = urldefrag(link)[0]
                    if is_internal(link):
                        # skip static assets to reduce noise, but check them once if linked
                        if any(link.endswith(ext) for ext in [".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".pdf", ".woff", ".woff2"]):
                            if link not in visited:
                                visited.add(link)
                                try:
                                    with urlopen(Request(link, headers={"User-Agent":"audit-crawler/1.0"}), timeout=15) as r:
                                        if r.status >= 400:
                                            broken.append((link, r.status))
                                except Exception as e:
                                    broken.append((link, type(e).__name__))
                        else:
                            to_visit.add(link)
            return status
    except Exception as e:
        broken.append((url, type(e).__name__))
        return type(e).__name__

def main():
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {}
        while to_visit and len(visited) < MAX_PAGES:
            batch = []
            while to_visit and len(batch) < WORKERS:
                batch.append(to_visit.pop())
            for url in batch:
                futures[executor.submit(check, url)] = url
            # wait for the batch to finish before scheduling more
            for fut in as_completed(futures):
                del futures[fut]
                if not to_visit and not futures:
                    break
    print(f"Crawled {len(visited)} URLs")
    print(f"Broken: {len(broken)}")
    for url, status in broken[:50]:
        print(f"  {status} {url}")
    with open("broken_links.json", "w") as f:
        json.dump([{"url": u, "status": s} for u, s in broken], f, indent=2)

if __name__ == "__main__":
    main()
