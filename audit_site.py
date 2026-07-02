#!/usr/bin/env python3
"""Quick automated audit of the built/previewed site."""
import re
import subprocess
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from html.parser import HTMLParser

BASE = "http://localhost:7777"
ROOT = "/home/ritik/thestacc.com-astro/thestacc-2026-site"

class LinkExtractor(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base = base_url
        self.links = []
        self.srcs = []
        self.alts = []
        self.h1s = []
        self.h2s = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append(urljoin(self.base, attrs["href"]))
        if tag in ("img", "script", "source", "video", "audio") and attrs.get("src"):
            self.srcs.append(urljoin(self.base, attrs["src"]))
        if tag == "img" and "alt" in attrs:
            self.alts.append(attrs["alt"])
        if tag in ("h1", "h2"):
            self.current_heading = tag
            self.heading_buf = ""

    def handle_data(self, data):
        if getattr(self, "current_heading", None):
            self.heading_buf += data

    def handle_endtag(self, tag):
        if getattr(self, "current_heading", None) == tag:
            text = re.sub(r"\s+", " ", self.heading_buf).strip()
            if tag == "h1":
                self.h1s.append(text)
            else:
                self.h2s.append(text)
            self.current_heading = None

def fetch(url):
    req = Request(url, headers={"User-Agent": "audit-bot/1.0"})
    try:
        with urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return type(e).__name__, str(e)

def is_internal(url):
    parsed = urlparse(url)
    base_parsed = urlparse(BASE)
    return parsed.netloc in (base_parsed.netloc, "") and parsed.scheme in ("http", "https", "")

def check_page(path):
    url = urljoin(BASE, path)
    status, html = fetch(url)
    if status != 200:
        print(f"FAIL {status} {url}")
        return None
    extractor = LinkExtractor(url)
    extractor.feed(html)
    return extractor

def main():
    print("=== Sharp corners in dist ===")
    proc = subprocess.run(
        ["grep", "-r", "-o", "-E", r"border-radius\s*:\s*[^;{}]+;", f"{ROOT}/dist/"],
        capture_output=True, text=True
    )
    if proc.stdout.strip():
        lines = proc.stdout.strip().splitlines()
        print(f"FOUND {len(lines)} border-radius declarations:")
        for line in lines[:20]:
            print("  ", line)
    else:
        print("OK — no border-radius declarations in dist/")

    print("\n=== FAQ markup in dist ===")
    proc = subprocess.run(
        ["grep", "-r", "-l", "faq-question", f"{ROOT}/dist/"],
        capture_output=True, text=True
    )
    old_faq = proc.stdout.strip().splitlines()
    proc = subprocess.run(
        ["grep", "-r", "-l", "tool-faq", f"{ROOT}/dist/"],
        capture_output=True, text=True
    )
    tool_faq = proc.stdout.strip().splitlines()
    print(f"Old .faq-question pages: {len(old_faq)}")
    print(f"Old .tool-faq pages: {len(tool_faq)}")

    print("\n=== /blog/ index link check ===")
    extractor = check_page("/blog/")
    if not extractor:
        return
    links = [l for l in extractor.links if is_internal(l) and not l.endswith((".css", ".js", ".svg", ".png", ".jpg", ".webp"))]
    broken = []
    for link in sorted(set(links)):
        status, _ = fetch(link)
        if status != 200:
            broken.append((link, status))
    print(f"Internal links found on /blog/: {len(set(links))}")
    if broken:
        print(f"BROKEN ({len(broken)}):")
        for link, status in broken[:30]:
            print(f"  {status} {link}")
    else:
        print("OK — all internal /blog/ links return 200")

    print("\n=== Key pages smoke test ===")
    key_pages = ["/", "/pricing/", "/reviews/rankmath/", "/tools/ai-humanizer/", "/case-studies/", "/compare/", "/glossary/schema-markup/", "/tools/ai-content-detector/"]
    for path in key_pages:
        status, html = fetch(urljoin(BASE, path))
        ok = status == 200
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        h1_text = re.sub(r"\s+", " ", h1s[0]).strip() if h1s else "NO H1"
        print(f"{'OK' if ok else 'FAIL'} {status} {path} — H1: {h1_text[:70]}")

    print("\n=== /blog/ index headings ===")
    print("H1s:", extractor.h1s)
    print("First 5 H2s:", extractor.h2s[:5])

if __name__ == "__main__":
    main()
