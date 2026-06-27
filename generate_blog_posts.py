import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / 'posts'
POSTS_DIR.mkdir(exist_ok=True)
POSTS_JSON = ROOT / 'posts.json'
INSIGHTS_HTML = ROOT / 'insights.html'
BRIEFINGS_DIR = ROOT / 'briefings'
BRIEFINGS_DIR.mkdir(exist_ok=True)
BRIEFINGS_JSON = ROOT / 'briefings.json'
BRIEFINGS_HTML = ROOT / 'briefings.html'

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title — Locke & Boole Solutions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy: #0D1F3C;
  --cream: #F0EDE8;
  --white: #FFFFFF;
  --text-muted: #8A94A6;
  --accent-line: #C8C0B4;
}
html { scroll-behavior: smooth; }
body { font-family: 'Inter', sans-serif; background: var(--cream); color: var(--navy); overflow-x: hidden; }
h1, h2, h3, h4, h5, h6 { font-weight: 700; }
nav { position: fixed; top: 0; left: 0; right: 0; z-index: 200; background: rgba(13, 31, 60, 0.97); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.06); padding: 0 48px; height: 68px; display: flex; align-items: center; justify-content: space-between; }
.nav-logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.nav-logo-mark { font-family: 'Times New Roman', serif; font-size: 26px; color: var(--cream); line-height: 1; }
.nav-logo-text { font-size: 13px; font-weight: 500; color: var(--cream); letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.85; }
.nav-links { display: flex; align-items: center; gap: 32px; list-style: none; }
.nav-links a { font-size: 13px; font-weight: 700; color: rgba(240,237,232,0.7); text-decoration: none; letter-spacing: 0.04em; }
.nav-links a:hover { color: var(--cream); }
.page-header { background: var(--navy); padding: 140px 48px 80px; position: relative; overflow: hidden; display: flex; flex-direction: column; align-items: center; text-align: center; }
.page-header h1 { font-family: 'Times New Roman', serif; font-size: clamp(40px, 5vw, 68px); color: var(--cream); line-height: 1.05; letter-spacing: -0.02em; max-width: 700px; }
.page-header p { margin-top: 20px; font-size: 15px; font-weight: 300; color: rgba(240,237,232,0.5); max-width: 520px; line-height: 1.75; }
.page-header .eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: rgba(240,237,232,0.35); margin-bottom: 20px; }
.article-section { padding: 88px 48px 120px; max-width: 940px; margin: 0 auto; background: var(--white); border-radius: 28px; box-shadow: 0 35px 90px rgba(13,31,60,0.08); }
.article-meta { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 32px; font-size: 13px; color: var(--navy); justify-content: center; }
.article-meta span { background: rgba(13,31,60,0.08); color: var(--navy); padding: 8px 12px; border-radius: 999px; letter-spacing: 0.12em; text-transform: uppercase; }
.article-content { color: var(--navy); line-height: 1.85; }
.article-content p { margin-bottom: 24px; }
.article-content h2 { font-family: 'Times New Roman', serif; font-size: clamp(28px, 4vw, 38px); margin-top: 52px; margin-bottom: 18px; color: var(--navy); }
.article-content ul { margin: 0 0 24px 22px; }
.article-content li { margin-bottom: 14px; }
.article-content blockquote { border-left: 3px solid rgba(13,31,60,0.2); margin: 32px 0; padding-left: 18px; color: rgba(13,31,60,0.85); font-style: italic; }
.article-footer { margin-top: 40px; display: flex; justify-content: center; }
.btn-ghost { background: transparent; color: var(--navy); padding: 13px 30px; font-size: 12px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; text-decoration: none; border: 1px solid rgba(13,31,60,0.25); transition: all 0.2s; }
.btn-ghost:hover { border-color: rgba(13,31,60,0.6); }
</style>
</head>
<body>
<nav>
  <a href="../index.html" class="nav-logo">
    <span class="nav-logo-mark">L&amp;B</span>
    <span class="nav-logo-text">Locke &amp; Boole</span>
  </a>
  <ul class="nav-links">
    <li><a href="../services.html">Services</a></li>
    <li><a href="../methodology.html">Methodology</a></li>
    <li><a href="../sectors.html">Sectors</a></li>
    <li><a href="../insights.html">Insights &amp; Blog</a></li>
    <li><a href="../about.html">About Us</a></li>
    <li><a href="../demo.html">Request a Demo</a></li>
  </ul>
</nav>
<div class="page-header">
  <div class="eyebrow">$eyebrow</div>
  <h1>$title</h1>
  <p>$subtitle</p>
</div>
<section class="article-section">
  <div class="article-meta">
    <span>$date</span>
    <span>$read_time</span>
    <span>Locke &amp; Boole Analyst Team</span>
  </div>
  <div class="article-content">
    <p>$excerpt</p>
$sections_html
  </div>
  <div class="article-footer">
    <a href="../insights.html" class="btn-ghost">Back to Insights</a>
</section>
</body>
</html>
'''

BRIEFING_TEMPLATE = PAGE_TEMPLATE.replace('Back to Insights', 'Back to Briefings').replace('../insights.html', '../briefings.html')

def create_post_html(post, template=PAGE_TEMPLATE):
    sections_html = '\n'.join(f'    <h2>{section["heading"]}</h2>\n    <p>{section["body"]}</p>' for section in post['sections'])
    content = template.replace('$title', post['title'])
    content = content.replace('$eyebrow', post['eyebrow'])
    content = content.replace('$subtitle', post['subtitle'])
    content = content.replace('$date', post['date'])
    content = content.replace('$read_time', post['read_time'])
    content = content.replace('$excerpt', post['excerpt'])
    content = content.replace('$sections_html', sections_html)
    return content


def build_post_category(post):
    return post['eyebrow'].split(' · ')[0].strip()


def build_briefing_rows(briefings):
    lines = []
    for briefing in briefings:
        lines.append(f'    <a class="briefing-row" href="briefings/{briefing["filename"]}">')
        lines.append(f'      <div class="briefing-date">{briefing["date"]}</div>')
        lines.append('      <div class="briefing-content">')
        lines.append(f'        <div class="briefing-category">{briefing["eyebrow"]}</div>')
        lines.append(f'        <div class="briefing-title">{briefing["title"]}</div>')
        lines.append(f'        <div class="briefing-desc">{briefing["excerpt"]}</div>')
        lines.append('      </div>')
        if briefing.get('status', '').lower() == 'open':
            lines.append('      <div style="font-size:9px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:rgba(13,31,60,0.5);border:1px solid rgba(13,31,60,0.15);padding:4px 10px;white-space:nowrap;">Open</div>')
        else:
            lines.append('      <div>')
            lines.append('        <div class="briefing-restricted">Restricted</div>')
            lines.append('      </div>')
        lines.append('    </a>')
        lines.append('')
    return '\n'.join(lines).rstrip()


def rewrite_briefings_list_section(text, briefings):
    start = text.index('<!-- BRIEFINGS LIST -->')
    end = text.index('</section>', start) + len('</section>')
    replacement = '    <!-- BRIEFINGS LIST -->\n<section class="briefings-section">\n  <div class="section-eyebrow">Recent Briefings</div>\n  <div class="briefings-list">\n\n'
    replacement += build_briefing_rows(briefings)
    replacement += '\n\n  </div>\n</section>'
    return text[:start] + replacement + text[end:]


def build_insights_cards(posts):
    lines = []
    for post in posts[1:]:
        lines.append(f'    <a class="post-card" href="posts/{post["filename"]}">')
        lines.append(f'      <div class="post-card-category">{build_post_category(post)}</div>')
        lines.append(f'      <div class="post-card-title">{post["title"]}</div>')
        lines.append(f'      <div class="post-card-excerpt">{post["excerpt"]}</div>')
        lines.append('      <div class="post-card-footer">')
        lines.append(f'        <span class="post-card-date">{post["date"]}</span>')
        lines.append('        <span class="post-card-arrow">→</span>')
        lines.append('      </div>')
        lines.append('    </a>')
        lines.append('')
    return '\n'.join(lines).rstrip()


def rewrite_insights_posts_section(text, posts):
    start = text.index('<!-- POSTS -->')
    end = text.index('</section>', start) + len('</section>')
    replacement = '    <!-- POSTS -->\n<section class="posts-section">\n  <div class="posts-grid">\n\n'
    replacement += build_insights_cards(posts)
    replacement += '\n\n  </div>\n</section>'
    return text[:start] + replacement + text[end:]


def generate_posts(posts):
    for post in posts:
        path = POSTS_DIR / post['filename']
        path.write_text(create_post_html(post), encoding='utf-8')
        print(f'Generated {post["filename"]}')


def generate_briefings(briefings):
    for briefing in briefings:
        path = BRIEFINGS_DIR / briefing['filename']
        path.write_text(create_post_html(briefing, template=BRIEFING_TEMPLATE), encoding='utf-8')
        print(f'Generated {briefing["filename"]}')


def update_insights(posts):
    text = INSIGHTS_HTML.read_text(encoding='utf-8')
    featured_filename = f'posts/{posts[0]["filename"]}'
    text = re.sub(r'<a\s+href="[^"]*"\s+class="read-more"', f'<a href="{featured_filename}" class="read-more"', text, count=1)
    text = rewrite_insights_posts_section(text, posts)
    resource_pages = json.dumps(['insights.html', 'briefings.html'] + [f'posts/{post["filename"]}' for post in posts])
    text = re.sub(r'var resourcePages = \[.*?\];', f'var resourcePages = {resource_pages};', text, flags=re.S)
    INSIGHTS_HTML.write_text(text, encoding='utf-8')
    print('Updated insights.html links')


def update_briefings(briefings):
    text = BRIEFINGS_HTML.read_text(encoding='utf-8')
    text = rewrite_briefings_list_section(text, briefings)
    resource_pages = json.dumps(['insights.html', 'briefings.html'] + [f'briefings/{briefing["filename"]}' for briefing in briefings])
    text = re.sub(r'var resourcePages = \[.*?\];', f'var resourcePages = {resource_pages};', text, flags=re.S)
    BRIEFINGS_HTML.write_text(text, encoding='utf-8')
    print('Updated briefings.html links')


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    briefings = json.loads(BRIEFINGS_JSON.read_text(encoding='utf-8'))
    generate_posts(posts)
    generate_briefings(briefings)
    update_insights(posts)
    update_briefings(briefings)


if __name__ == '__main__':
    main()
