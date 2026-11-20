#!/usr/bin/env python3
"""Build the public 甲骨文 landing page + 77 volume pages.

This is intentionally separate from the generic SEO patch: it creates pages
that did not exist before, then the generic patch can re-run safely.
"""
from __future__ import annotations

import html as H
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "daokedao-jiaguwen"
BOOK = REPO / "book"
DOCS = REPO / "docs"
VOL = DOCS / "volumes"
BASE = "https://q1z2q3-debug.github.io/daokedao-jiaguwen/"
AUTHOR = "润泽（润泽博士）"
CN = "零一二三四五六七八九"


def cn_num(s: str) -> int:
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十", 1)
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s)


def text_of(html: str) -> str:
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = H.unescape(re.sub(r"\s+", " ", body)).strip()
    return body


def inject(page: str, title: str, desc: str, url: str) -> str:
    def before(block: str) -> str:
        return page.replace("</head>", block + "</head>", 1) if "</head>" in page else page

    def meta(name: str, content: str, prop: bool = False) -> str:
        nonlocal page
        key = "property" if prop else "name"
        pat = re.compile(rf'<meta[^>]*{key}=["\']{re.escape(name)}["\'][^>]*>', re.I)
        tag = f'<meta {key}="{name}" content="{H.escape(content, quote=True)}">'
        page = pat.sub(tag, page, count=1) if pat.search(page) else before(tag)
        return page

    def link(rel: str, href: str) -> str:
        nonlocal page
        pat = re.compile(rf'<link[^>]*rel=["\']{re.escape(rel)}["\'][^>]*>', re.I)
        tag = f'<link rel="{rel}" href="{H.escape(href, quote=True)}">'
        page = pat.sub(tag, page, count=1) if pat.search(page) else before(tag)
        return page

    page = link("canonical", url)
    page = meta("description", desc)
    page = meta("robots", "index,follow,max-image-preview:large,max-snippet:-1")
    page = meta("author", AUTHOR)
    page = meta("og:type", "article", True)
    page = meta("og:site_name", "润泽说 道可道", True)
    page = meta("og:locale", "zh_CN", True)
    page = meta("og:title", title, True)
    page = meta("og:description", desc, True)
    page = meta("og:url", url, True)
    page = meta("twitter:card", "summary_large_image")
    page = meta("twitter:title", title)
    page = meta("twitter:description", desc)
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Person", "name": AUTHOR},
        "inLanguage": "zh-CN",
        "url": url,
        "isPartOf": {"@type": "Book", "name": "润泽说 道可道之甲骨文", "url": BASE},
        "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    }
    page = before('\n<script type="application/ld+json">\n' + json.dumps(article, ensure_ascii=False, indent=2) + '\n</script>\n') if '"@type": "Article"' not in page else page
    return page


def main() -> None:
    VOL.mkdir(parents=True, exist_ok=True)
    items = []
    for src in BOOK.glob("*阅读版.html"):
        if "前言" in src.name:
            continue
        text = src.read_text(errors="ignore")
        m = re.search(r"<title>(.*?)</title>", text, re.S)
        title = H.unescape(m.group(1).strip()) if m else src.stem
        m2 = re.search(r"卷([一二三四五六七八九十]+)", title)
        if not m2:
            continue
        num = cn_num(m2.group(1))
        items.append((num, title, src, text))
    items.sort(key=lambda x: x[0])
    assert len(items) == 77, len(items)

    cards = []
    for num, title, src, text in items:
        dst = VOL / f"v{num:02d}.html"
        body = text_of(text)
        desc = re.sub(r"\s+", " ", body)[:120]
        shutil.copyfile(src, dst)
        page = dst.read_text(errors="ignore")
        page = inject(page, title, desc, f"{BASE}volumes/v{num:02d}.html")
        dst.write_text(page, encoding="utf-8")
        cards.append((num, title, f"volumes/v{num:02d}.html", desc[:45]))

    # 77 card grid
    grid = "\n".join(
        f'<a class="vol" href="{href}"><b>卷{num:02d}</b><span>{H.escape(re.sub(r"^.*?·\s*", "", title))}</span></a>'
        for num, title, href, _ in cards
    ) + '\n<a class="vol" href="volumes/v01.html"><b>从卷一</b><span>开始通读</span></a>'
    # sample chips
    samples = ["文", "化", "地", "风", "岁", "寒", "暑", "霜", "露", "冰", "夜", "早", "晚", "手", "病", "马", "鸟", "鱼", "龟", "蛇", "龙", "凤", "鸡", "兽", "车", "门", "户", "壶", "贝", "丝", "来", "见"]
    chips = "\n".join(f"<span>{c}</span>" for c in samples)

    index = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%238c3b25'/%3E%3Cpath d='M12 18h40M12 32h40M12 46h40' stroke='%23f3ede1' stroke-width='5'/%3E%3C/svg%3E">
<title>润泽说 道可道之甲骨文｜一字一世界，一字一智慧</title>
<style>
:root{{--ink:#171512;--paper:#f3ede1;--muted:#6b6253;--line:#d8cbb6;--accent:#8c3b25}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.85 "Noto Serif CJK SC","Songti SC",serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:38px 22px 70px}}
.hero{{border-bottom:1px solid var(--line);padding-bottom:26px}}
.kicker{{letter-spacing:.18em;color:var(--accent);font-size:14px}}
h1{{font-size:clamp(30px,5vw,58px);line-height:1.18;margin:10px 0 14px;letter-spacing:.03em}}
.lead{{max-width:760px;color:#37322b;margin:0 0 18px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}
.stat{{border:1px solid var(--line);padding:8px 13px;background:#fbf7ee}}
.stat b{{font-size:20px;margin-right:6px}}
.actions a{{display:inline-block;margin:6px 8px 6px 0;padding:12px 14px;min-height:44px;border:1px solid var(--ink);text-decoration:none;color:var(--ink)}}
.actions a.primary{{background:var(--ink);color:var(--paper)}}
section{{padding:34px 0;border-bottom:1px solid var(--line)}}
h2{{font-size:25px;margin:0 0 8px}}
.note{{color:var(--muted);font-size:14px;max-width:820px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}}
.chips span{{border:1px solid var(--line);background:#fbf7ee;padding:7px 10px;font-size:15px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:8px;margin-top:18px}}
.vol{{display:block;border:1px solid var(--line);background:#fbf7ee;padding:10px 12px;text-decoration:none;color:var(--ink)}}
.vol b{{display:block;font-size:12px;color:var(--accent);letter-spacing:.08em}}
.vol span{{display:block;font-size:14px;line-height:1.45}}
.links{{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px}}
.links a{{color:var(--accent);display:inline-block;padding:8px 0;min-height:44px}}
footer{{padding-top:24px;color:var(--muted);font-size:13px}}
</style>
</head>
<body>
<main class="wrap">
<div class="hero">
<div class="kicker">润泽说 · 道可道 · 甲骨文</div>
<h1>一字一世界<br>一字一智慧</h1>
<p class="lead">七十七卷、九百二十四字位、九百零五唯一字。每字保留“字形 · 复写 / 字源 / 同片释文 / 一字一世界 / 一字一智慧”五件；有本字的列本字，只有借字的列借字，后起的标后起，未见拓片的照实标“待核”。</p>
<div class="stats"><span class="stat"><b>77</b>卷</span><span class="stat"><b>924</b>字位</span><span class="stat"><b>905</b>唯一字</span><span class="stat"><b>v0.77.0</b></span></div>
<div class="actions"><a class="primary" href="volumes/v77.html">读卷七十七 · 补遗与借字</a><a href="preface.html">前言 · 文与化</a><a href="research/甲骨文证据校验器.html">证据与置信度</a><a href="https://github.com/q1z2q3-debug/daokedao-jiaguwen">GitHub 仓库</a></div>
</div>

<section>
<h2>为什么是“一图一字一详解”</h2>
<p class="note">甲骨文不是“看图猜字”。一个字要同时过四道关：字形是否有拓片或摹本依据、字源是否能落到先秦构形、同片释文是否能读通、后世字义如何层累。四关都过，才写“已核”；只过部分，就写“中”或“待核”。这一套写法，是把字放回它出生的那片甲骨、那顿饭、那场雨、那次战争里。</p>
</section>

<section>
<h2>十二字补遗与三十字</h2>
<p class="note">卷七十七补“地、寒、暑、霜、露、冰、夜、早、晚、手、病、蛇”；另收“风、岁、马、鸟、鱼、龟、龙、凤、鸡、兽、车、门、户、壶、贝、丝、来、见”等常用字。点开卷页，能看到每一字的证据状态，而不是一句“据说”。</p>
<div class="chips">{chips}</div>
</section>

<section>
<h2>七十七卷 · 全书目录</h2>
<p class="note">按“天地人—身体心—动作生活—关系共同体—器物制度—自然动物……”一路展开。每一卷都可单独阅读，也可从卷一顺着读。</p>
<div class="grid">{grid}</div>
</section>

<section>
<h2>证据、引用与许可</h2>
<p class="note">本书原创正文、注释、编排及作者自绘部分采用 CC BY-NC-SA 4.0：署名、非商业、相同方式共享。第三方拓片、字形库、AI 图、图版与字体不随本书授权。商业训练与商业分发需事先书面许可。</p>
<div class="links"><a href="https://github.com/q1z2q3-debug/runze-daokedao/blob/main/LICENSING/README.md">商业许可入口</a><a href="https://github.com/q1z2q3-debug/daokedao-jiaguwen/blob/main/CITATION.cff">CITATION.cff</a><a href="llms.txt">llms.txt · 模型入口</a><a href="sitemap.xml">sitemap</a></div>
</section>
<footer>润泽说 道可道之甲骨文 · v0.77.0 · 2026-11-20 · 上海</footer>
</main>
</body>
</html>
"""
    (DOCS / "index.html").write_text(index, encoding="utf-8")

    # sitemap: all public HTML, excluding internal shot dirs
    urls = []
    for p in sorted(DOCS.rglob("*.html")):
        if "_shots" in p.parts:
            continue
        rel = p.relative_to(DOCS).as_posix()
        urls.append(BASE + quote(rel, safe="/"))
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append(f"  <url><loc>{H.escape(u)}</loc><lastmod>2026-11-20</lastmod></url>")
    body.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"volumes={len(items)} urls={len(urls)}")


if __name__ == "__main__":
    main()
