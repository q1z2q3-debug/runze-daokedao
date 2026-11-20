#!/usr/bin/env python3
"""Patch SEO head tags and JSON-LD into the 润泽说 道可道 sites.

Run from runze-daokedao after building the sites:
    python3 SEO/patch.py
"""
from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path
from urllib.parse import quote

BOOK_ROOT = Path(__file__).resolve().parents[2]
SEO_DIR = Path(__file__).resolve().parent
CONFIG = json.loads((SEO_DIR / "config.json").read_text(encoding="utf-8"))
AUTHOR = "润泽（润泽博士）"


def expected_url(base: str, rel: str) -> str:
    if rel in ("", ".", "index.html"):
        return base
    return base + quote(rel, safe="/")


def insert_before_head_close(html: str, block: str) -> str:
    if "</head>" not in html:
        return html
    return html.replace("</head>", block + "</head>", 1)


def set_meta(html: str, key: str, value: str, attr: str = "name") -> str:
    value = html_lib.escape(value, quote=True)
    pattern = re.compile(rf'<meta[^>]*{attr}=["\']{re.escape(key)}["\'][^>]*>', re.I)
    tag = f'<meta {attr}="{key}" content="{value}">'
    if pattern.search(html):
        return pattern.sub(tag, html, count=1)
    return insert_before_head_close(html, tag)


def set_link(html: str, rel: str, href: str) -> str:
    href = html_lib.escape(href, quote=True)
    pattern = re.compile(rf'<link[^>]*rel=["\']{re.escape(rel)}["\'][^>]*>', re.I)
    tag = f'<link rel="{rel}" href="{href}">'
    if pattern.search(html):
        return pattern.sub(tag, html, count=1)
    return insert_before_head_close(html, tag)


def ensure_robots(html: str) -> str:
    return set_meta(html, "robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")


def update_jsonld(html: str, site: dict, page_url: str, is_book: bool) -> str:
    """Update an existing Book object, otherwise add one."""
    scripts = list(re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I))
    found_book = False
    for match in reversed(scripts):
        try:
            obj = json.loads(match.group(1))
        except Exception:
            continue
        candidates = obj if isinstance(obj, list) else [obj]
        if not any(isinstance(x, dict) and x.get("@type") == "Book" for x in candidates):
            continue
        for x in candidates:
            if not isinstance(x, dict) or x.get("@type") != "Book":
                continue
            x.update({
                "@context": "https://schema.org",
                "@type": "Book",
                "@id": page_url + "#book",
                "name": site["title"].split("｜")[0],
                "alternateName": [site["name"], f"润泽说 道可道之{site['name']}"],
                "author": {"@type": "Person", "name": AUTHOR, "alternateName": ["润泽", "Runze", "#润泽博士"]},
                "publisher": {"@type": "Person", "name": AUTHOR},
                "inLanguage": "zh-CN",
                "bookEdition": f"v{site['version']}",
                "datePublished": "2026-11-20",
                "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
                "url": page_url,
                "description": site["description"],
                "keywords": ", ".join(site["keywords"]),
                "numberOfPages": site.get("number_of_pages"),
                "isAccessibleForFree": True,
            })
            if site.get("og_image"):
                x["image"] = site["og_image"]
        text = json.dumps(obj, ensure_ascii=False, indent=2)
        html = html[:match.start(1)] + "\n" + text + "\n" + html[match.end(1):]
        found_book = True
        break
    if not found_book:
        book = {
            "@context": "https://schema.org",
            "@type": "Book",
            "@id": page_url + "#book",
            "name": site["title"].split("｜")[0],
            "alternateName": [site["name"], f"润泽说 道可道之{site['name']}"],
            "author": {"@type": "Person", "name": AUTHOR, "alternateName": ["润泽", "Runze", "#润泽博士"]},
            "publisher": {"@type": "Person", "name": AUTHOR},
            "inLanguage": "zh-CN",
            "bookEdition": f"v{site['version']}",
            "datePublished": "2026-11-20",
            "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "url": page_url,
            "description": site["description"],
            "keywords": ", ".join(site["keywords"]),
            "numberOfPages": site.get("number_of_pages"),
            "isAccessibleForFree": True,
        }
        if site.get("og_image"):
            book["image"] = site["og_image"]
        block = '\n<script type="application/ld+json">\n' + json.dumps(book, ensure_ascii=False, indent=2) + '\n</script>\n'
        html = insert_before_head_close(html, block)
    return html


def add_site_schema(html: str, site: dict, page_url: str, is_book: bool) -> str:
    if '"@type": "WebSite"' in html:
        return html
    site_obj = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site["title"].split("｜")[0],
        "alternateName": f"润泽说 道可道之{site['name']}",
        "url": site["base"],
        "inLanguage": "zh-CN",
        "publisher": {"@type": "Person", "name": AUTHOR},
    }
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "润泽说 道可道", "item": CONFIG["series"]["site"]},
        {"@type": "ListItem", "position": 2, "name": site["title"].split("｜")[0], "item": site["base"]},
    ]
    if is_book:
        crumbs.append({"@type": "ListItem", "position": 3, "name": "全书阅读", "item": page_url})
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}
    block = '\n<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": [site_obj, breadcrumb]}, ensure_ascii=False, indent=2) + '\n</script>\n'
    return insert_before_head_close(html, block)


def patch_page(path: Path, site: dict, rel: str, is_book: bool) -> bool:
    if not path.exists():
        return False
    original = path.read_text(errors="ignore")
    html = original
    page_url = expected_url(site["base"], rel)
    html = set_link(html, "canonical", page_url)
    html = set_meta(html, "description", site["description"])
    html = set_meta(html, "author", AUTHOR)
    html = set_meta(html, "keywords", ", ".join(site["keywords"]))
    html = ensure_robots(html)
    html = set_meta(html, "og:type", "book", "property")
    html = set_meta(html, "og:site_name", CONFIG["series"]["name"], "property")
    html = set_meta(html, "og:locale", "zh_CN", "property")
    html = set_meta(html, "og:title", site["title"], "property")
    html = set_meta(html, "og:description", site["description"], "property")
    html = set_meta(html, "og:url", page_url, "property")
    if site.get("og_image"):
        html = set_meta(html, "og:image", site["og_image"], "property")
    html = set_meta(html, "twitter:card", "summary_large_image")
    html = set_meta(html, "twitter:title", site["title"])
    html = set_meta(html, "twitter:description", site["description"])
    if site.get("og_image"):
        html = set_meta(html, "twitter:image", site["og_image"])
    html = set_meta(html, "citation_title", site["title"])
    html = set_meta(html, "citation_author", AUTHOR)
    html = set_meta(html, "citation_publication_date", "2026-11-20")
    html = set_meta(html, "citation_language", "zh")
    html = set_meta(html, "citation_abstract", site["description"])
    html = set_meta(html, "citation_fulltext_html_url", page_url)
    html = update_jsonld(html, site, page_url, is_book)
    html = add_site_schema(html, site, page_url, is_book)
    if html == original:
        return False
    path.write_text(html, encoding="utf-8")
    return True


def write_discovery(site: dict) -> None:
    root = BOOK_ROOT / site["repo"] / site["site_dir"]
    root.mkdir(parents=True, exist_ok=True)
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        urls = []
        for p in sorted(root.rglob("*.html")):
            if "_shots" in p.parts:
                continue
            rel = p.relative_to(root).as_posix()
            urls.append(expected_url(site["base"], rel))
        body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in urls:
            body.append(f"  <url><loc>{html_lib.escape(u)}</loc><lastmod>2026-11-20</lastmod></url>")
        body.append("</urlset>")
        sitemap.write_text("\n".join(body) + "\n", encoding="utf-8")
    robots = root / "robots.txt"
    content = f"""User-agent: *
Allow: /

# Search and retrieval crawlers are welcome.
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

# Commercial training is not authorized by robots alone.
# See https://github.com/q1z2q3-debug/runze-daokedao/blob/main/LICENSING/README.md

Sitemap: {site['base']}sitemap.xml
"""
    if not robots.exists():
        robots.write_text(content, encoding="utf-8")
    ai = root / "ai.txt"
    ai.write_text(f"""# AI usage policy for {site['title'].split('｜')[0]}
# Author: {AUTHOR}
# License: CC BY-NC-SA 4.0
Allow: search, index, retrieval, citation, non-commercial research
Commercial training: prior written license required
License: https://github.com/q1z2q3-debug/runze-daokedao/blob/main/LICENSING/README.md
Sitemap: {site['base']}sitemap.xml
""", encoding="utf-8")


def main() -> None:
    for site in CONFIG["sites"]:
        root = BOOK_ROOT / site["repo"] / site["site_dir"]
        changed = []
        for key in ("index", "book", "preface"):
            rel = site.get(key)
            if not rel:
                continue
            if patch_page(root / rel, site, rel, key != "index"):
                changed.append(rel)
        write_discovery(site)
        print(f"{site['name']}: {', '.join(changed) if changed else 'no page change'}")


if __name__ == "__main__":
    main()
