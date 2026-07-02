#!/usr/bin/env python3
import os
import re
import glob

OLD_DIR = '/home/ritik/thestacc.com-astro/thestacc-2026-site/Old Website/src/pages/for'
NEW_DIR = '/home/ritik/thestacc.com-astro/thestacc-2026-site/src/pages/for'

def extract_frontmatter(text):
    if not text.startswith('---'):
        return '', text
    m = re.search(r'^---\n(.*?)\n---\n(.*)$', text, re.DOTALL)
    if not m:
        return '', text
    return m.group(1), m.group(2)

def clean_frontmatter(fm):
    lines = fm.splitlines()
    cleaned = []
    for line in lines:
        s = line.strip()
        if s.startswith('import BaseLayout from'):
            continue
        if s.startswith('import Header from'):
            continue
        if s.startswith('import Footer from'):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

def extract_title_desc(opening_tag):
    title = ''
    desc = ''
    m = re.search(r'title\s*=\s*"([^"]*)"', opening_tag)
    if m:
        title = m.group(1)
    else:
        m = re.search(r"title\s*=\s*'([^']*)'", opening_tag)
        if m:
            title = m.group(1)
    m = re.search(r'description\s*=\s*"([^"]*)"', opening_tag)
    if m:
        desc = m.group(1)
    else:
        m = re.search(r"description\s*=\s*'([^']*)'", opening_tag)
        if m:
            desc = m.group(1)
    return title, desc

def add_is_inline(body):
    def repl(match):
        opening = match.group(1)
        content = match.group(2)
        if re.search(r'\b(document|window)\b', content):
            if 'is:inline' not in opening:
                opening = opening.rstrip() + ' is:inline'
        return f'<script{opening}>{content}</script>'
    return re.sub(r'<script([^>]*)>(.*?)</script>', repl, body, flags=re.DOTALL)

def escape_title_tags(body):
    # Escape literal <title> and </title> that aren't already escaped
    body = re.sub(r'(?<!&lt;)<title>', '&lt;title&gt;', body)
    body = re.sub(r'(?<!&lt;)</title>', '&lt;/title&gt;', body)
    return body

def process_file(old_path, slug):
    with open(old_path, 'r', encoding='utf-8') as f:
        text = f.read()

    fm, rest = extract_frontmatter(text)
    fm = clean_frontmatter(fm)
    rest = rest.strip()

    # Extract BaseLayout wrapper
    m = re.search(r'^(<BaseLayout\b[^>]*>)(.*)</BaseLayout>\s*$', rest, re.DOTALL)
    if not m:
        return None, 'Could not find BaseLayout wrapper'
    opening_tag = m.group(1)
    body = m.group(2)

    title, desc = extract_title_desc(opening_tag)

    # Remove Header/Footer tags
    body = re.sub(r'<Header\s*/?>', '', body)
    body = re.sub(r'<Footer\s*/?>', '', body)

    # Clean up empty lines left around removed header/footer
    body = re.sub(r'\n{3,}', '\n\n', body)

    # Add is:inline to scripts using document/window
    body = add_is_inline(body)

    # Escape literal title tags in body
    body = escape_title_tags(body)

    canonical = f'https://thestacc.com/for/{slug}/'
    og_image = f'/og/for-{slug}.webp'

    seo_block = f"""const seo = {{
  title: {repr(title)},
  description: {repr(desc)},
  canonical: '{canonical}',
  ogImage: '{og_image}'
}};"""

    new_fm = "---\n"
    new_fm += "import BaseLayout from '../../../layouts/BaseLayout.astro';\n"
    if fm.strip():
        new_fm += "\n" + seo_block + "\n\n" + fm.strip() + "\n"
    else:
        new_fm += "\n" + seo_block + "\n"
    new_fm += "---\n"

    new_text = new_fm + "<BaseLayout seo={seo}>\n" + body.rstrip() + "\n</BaseLayout>\n"
    return new_text, None

def main():
    created = []
    skipped = []
    errors = []
    for old_path in sorted(glob.glob(os.path.join(OLD_DIR, '*.astro'))):
        fname = os.path.basename(old_path)
        if fname.endswith('.bak'):
            continue
        if fname == 'index.astro':
            continue
        slug = fname[:-6]
        new_dir = os.path.join(NEW_DIR, slug)
        new_path = os.path.join(new_dir, 'index.astro')
        if os.path.exists(new_path):
            skipped.append(slug)
            continue
        new_text, err = process_file(old_path, slug)
        if err:
            errors.append((slug, err))
            continue
        os.makedirs(new_dir, exist_ok=True)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        created.append(slug)
    print(f"Created: {len(created)}")
    print(', '.join(created))
    if skipped:
        print(f"Skipped (already exist): {len(skipped)}")
        print(', '.join(skipped))
    if errors:
        print(f"Errors: {len(errors)}")
        for slug, err in errors:
            print(f"  {slug}: {err}")

if __name__ == '__main__':
    main()
