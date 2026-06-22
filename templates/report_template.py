"""Render Markdown into warm-brown + gold industry-report HTML template."""

import re
import hashlib
import html as html_mod
from datetime import datetime
from typing import Optional

import markdown as md_lib

TEMPLATE_PATH = __file__.rsplit("/", 1)[0] + "/industry_report.html"

# Emoji → callout class mapping
CALLOUT_MAP = {
    "\u26a0\ufe0f": "warn",
    "\ud83d\udea8": "bad",
    "\u2757": "bad",
    "\u26a1": "warn",
    "\ud83d\udca1": "info",
    "\ud83d\udcdd": "info",
    "\u2705": "good",
    "\ud83d\udd12": "good",
    "\u274c": "bad",
}


def _preprocess_callouts(text: str) -> str:
    """Convert emoji-prefixed blockquotes to callout divs.

    > 🚨 ...  → <div class="callout-bad"><div class="callout-title">Critical</div>...
    > 💡 ...  → <div class="callout-info"><div class="callout-title">Note</div>...
    """
    lines = text.split("\n")
    out = []
    in_callout = False
    callout_type = ""
    callout_title = ""

    for line in lines:
        m = re.match(r"^>\s*([\U0001F300-\U0001F9FF\u2600-\u27BF\uFE0F])(.*)", line)
        if m:
            emoji = m.group(1)
            rest = m.group(2).strip()
            ctype = CALLOUT_MAP.get(emoji, "")
            if ctype:
                title_map = {"warn": "Warning", "bad": "Critical", "info": "Note", "good": "OK"}
                if not in_callout:
                    out.append(f'<div class="callout callout-{ctype}">')
                    out.append(f'<div class="callout-title">{title_map.get(ctype, "Note")}</div>')
                    in_callout = True
                    callout_type = ctype
                out.append(f"<p>{rest}</p>")
                continue
        # Plain blockquote (no emoji)
        bq = re.match(r"^>\s*(.*)", line)
        if bq and not in_callout:
            out.append(f"<blockquote><p>{bq.group(1)}</p></blockquote>")
            continue

        if in_callout:
            out.append("</div>")
            in_callout = False
        out.append(line)

    if in_callout:
        out.append("</div>")
    return "\n".join(out)


def _generate_toc(html_body: str) -> str:
    """Generate nested TOC list from h2/h3 headings in HTML body."""
    toc_items = []
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>')
    h3_pattern = re.compile(r'<h3[^>]*>(.*?)</h3>')

    for line in html_body.split("\n"):
        h2 = h2_pattern.search(line)
        if h2:
            text = re.sub(r"<[^>]+>", "", h2.group(1)).strip()
            anchor = text.lower().replace(" ", "-").replace(".", "")
            anchor = re.sub(r"[^\w\u4e00-\u9fff-]", "", anchor)
            toc_items.append(("h2", text, anchor))
        h3 = h3_pattern.search(line)
        if h3:
            text = re.sub(r"<[^>]+>", "", h3.group(1)).strip()
            anchor = text.lower().replace(" ", "-").replace(".", "")
            anchor = re.sub(r"[^\w\u4e00-\u9fff-]", "", anchor)
            toc_items.append(("h3", text, anchor))

    if not toc_items:
        return ""

    html = '<ol>\n'
    for level, text, anchor in toc_items:
        if level == "h3":
            html += f'  <li><a href="#{anchor}">{html_mod.escape(text)}</a></li>\n'
        else:
            html += f'<li><a href="#{anchor}">{html_mod.escape(text)}</a></li>\n'
    html += "</ol>\n"
    return html


def _add_anchors_to_headings(html_body: str) -> str:
    """Add id anchors to h2/h3 tags for TOC linking."""
    def _add_id(m):
        tag = m.group(1)
        text = re.sub(r"<[^>]+>", "", m.group(2))
        anchor = text.lower().replace(" ", "-").replace(".", "")
        anchor = re.sub(r"[^\w\u4e00-\u9fff-]", "", anchor)
        return f'<{tag} id="{anchor}">{m.group(2)}</{tag}>'
    html_body = re.sub(r"<h2>(.*?)</h2>", lambda m: _add_id(re.match(r"h2", "h2") or m), html_body)
    # More reliable approach
    html_body = re.sub(r"<(h[23])>(.*?)</\1>", _add_id, html_body)
    return html_body


def render_html_report(
    markdown_text: str,
    title: str,
    industry: str = "",
    subtitle: str = "",
    byline: str = "",
) -> str:
    """Convert Markdown report text to full HTML using the industry-report template."""
    source_sha256 = hashlib.sha256(markdown_text.encode()).hexdigest()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Step 1: preprocess callouts
    processed = _preprocess_callouts(markdown_text)

    # Step 2: convert to HTML with extensions
    body_html = md_lib.markdown(
        processed,
        extensions=["extra", "codehilite", "toc"],
    )

    # Step 3: add anchors to headings
    body_html = _add_anchors_to_headings(body_html)

    # Step 4: generate TOC
    toc_html = _generate_toc(body_html)

    # Step 5: build CDN scripts block
    cdn_scripts = """
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true,theme:'neutral'});</script>
""".strip()

    # Step 6: read template and substitute
    try:
        with open(TEMPLATE_PATH, encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback: embed template directly
        template = _get_embedded_template()

    eyebrow_block = f'<div class="eyebrow">{html_mod.escape(industry or "行业研报")}</div>' if industry else ""
    subtitle_block = f'<p class="subtitle">{html_mod.escape(subtitle)}</p>' if subtitle else ""
    byline_block = f'<p class="byline">{html_mod.escape(byline)}</p>' if byline else ""

    html = template
    html = html.replace("{{LANG}}", "zh-CN")
    html = html.replace("{{TITLE}}", html_mod.escape(title))
    html = html.replace("{{SOURCE_PATH}}", f"industry: {html_mod.escape(industry or title)}")
    html = html.replace("{{SOURCE_SHA256}}", source_sha256)
    html = html.replace("{{SOURCE_SHA256_SHORT}}", source_sha256[:12])
    html = html.replace("{{GENERATED_AT}}", now)
    html = html.replace("{{HEAD_CDN}}", cdn_scripts)
    html = html.replace("{{TOC_LABEL}}", "目录")
    html = html.replace("{{TOC_HTML}}", toc_html)
    html = html.replace("{{EYEBROW_BLOCK}}", eyebrow_block)
    html = html.replace("{{SUBTITLE_BLOCK}}", subtitle_block)
    html = html.replace("{{BYLINE_BLOCK}}", byline_block)
    html = html.replace("{{EXTRA_META}}", "")
    html = html.replace("{{BODY_HTML}}", body_html)

    return html


def _get_embedded_template() -> str:
    """Fallback embedded template when template file not found."""
    return """<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
{{HEAD_CDN}}
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&display=swap');
:root {
  --bg: #0b0f19; --bg-soft: #141b2d; --bg-card: #141b2d; --bg-code: #0b0f19;
  --ink: #cbd5e1; --ink-soft: #94a3b8; --ink-muted: #64748b;
  --primary: #f8fafc; --primary-soft: #e2e8f0; --accent: #3b82f6;
  --accent-soft: #1d4ed8; --accent-text: #60a5fa;
  --border: #1e293b; --border-soft: #141b2d;
  --font-sans: 'Inter', sans-serif; --font-serif: 'Merriweather', serif;
}
* { box-sizing: border-box; }
body {
  font-family: var(--font-sans);
  line-height: 1.7; color: var(--ink); background: var(--bg); margin: 0; padding: 0; font-size: 16px;
}
.layout { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 280px 1fr; gap: 64px; padding: 0 40px; }
nav.toc { position: sticky; top: 40px; align-self: start; font-size: 14px; max-height: calc(100vh - 80px); overflow-y: auto; padding-right: 24px; padding-top: 40px; }
nav.toc h3 { color: var(--ink-muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em; }
nav.toc a { color: var(--ink-soft); text-decoration: none; font-size: 14px; }
header.hero { background: linear-gradient(135deg, #020617 0%, #0f172a 100%); margin: 0 0 56px; padding: 64px 48px; border-radius: 20px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3); border: 1px solid var(--border); }
header.hero h1 { font-family: var(--font-serif); font-size: 42px; color: #ffffff; max-width: 800px; margin: 0 0 20px; }
header.hero .eyebrow { color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 16px; }
h2 { font-size: 28px; border-bottom: 1px solid var(--border); color: var(--primary); font-weight: 800; padding-bottom: 16px; margin: 64px 0 24px; }
.callout { margin: 24px 0; padding: 20px 24px; border-radius: 12px; border-left: 4px solid; background: var(--bg-card); box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid var(--border); border-radius: 12px; background: var(--bg-card); }
thead { background: var(--bg-soft); color: var(--primary); }
th, td { padding: 16px 20px; border-bottom: 1px solid var(--border); }
pre { background: #0f172a; padding: 24px; overflow-x: auto; border-radius: 12px; color: #e2e8f0; }
@media (max-width: 900px) { .layout { grid-template-columns: 1fr; padding: 0 20px; } header.hero { margin: 0 0 32px; padding: 40px 24px; } header.hero h1 { font-size: 32px; } }
</style>
</head>
<body><div class="layout">
<nav class="toc"><h3>{{TOC_LABEL}}</h3>{{TOC_HTML}}</nav>
<main>
<header class="hero">{{EYEBROW_BLOCK}}<h1>{{TITLE}}</h1>{{SUBTITLE_BLOCK}}{{BYLINE_BLOCK}}</header>
{{BODY_HTML}}
</main>
</div></body></html>"""
