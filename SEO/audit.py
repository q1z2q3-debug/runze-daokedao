#!/usr/bin/env python3
"""Audit SEO basics for the 润泽说 道可道 sites.

Run from runze-daokedao:
    python3 SEO/audit.py
"""
from __future__ import annotations

import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

BOOK_ROOT = Path(__file__).resolve().parents[2]
SEO_DIR = Path(__file__).resolve().parent
CONFIG = json.loads((SEO_DIR / "config.json").read_text(encoding="utf-8"))


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.ldjson = 0
        self.h1 = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "h1":
            self.h1 += 1
        elif tag == "script" and a.get("type") == "application/ld+json":
            self.ldjson += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def expected_url(base: str, rel: str) -> str:
    if rel in ("", ".", "index.html"):
        return base
    return base + quote(rel, safe="/")


def read_page(path: Path) -> dict:
    html = path.read_text(errors="ignore")
    p = HeadParser()
    p.feed(html)
    desc = next((m.get("content", "") for m in p.metas if m.get("name") == "description" or m.get("property") == "og:description"), "")
    canonical = next((l.get("href", "") for l in p.links if l.get("rel") == "canonical"), "")
    og = [m for m in p.metas if m.get("property", "").startswith("og:")]
    tw = [m for m in p.metas if m.get("name", "").startswith("twitter:")]
    return {
        "exists": True,
        "bytes": len(html),
        "title": p.title.strip(),
        "description": desc.strip(),
        "canonical": canonical,
        "og": len(og),
        "twitter": len(tw),
        "ldjson": p.ldjson,
        "h1": p.h1,
        "text_len": len(re.sub(r"<[^>]+>", "", html)),
    }


def main() -> None:
    rows = []
    for site in CONFIG["sites"]:
        root = BOOK_ROOT / site["repo"] / site["site_dir"]
        pages = {}
        for key in ("index", "book", "preface"):
            rel = site.get(key)
            if not rel:
                continue
            path = root / rel
            pages[key] = read_page(path) if path.exists() else {"exists": False}
        index = pages.get("index", {})
        book = pages.get("book", {})
        expected_index = expected_url(site["base"], site["index"])
        expected_book = expected_url(site["base"], site["book"])
        checks = {
            "index_exists": bool(index.get("exists")),
            "book_exists": bool(book.get("exists")),
            "title": bool(index.get("title")),
            "description": bool(index.get("description")),
            "canonical_index": index.get("canonical") == expected_index,
            "canonical_book": book.get("canonical") == expected_book,
            "og": index.get("og", 0) >= 4,
            "twitter": index.get("twitter", 0) >= 3,
            "ldjson": index.get("ldjson", 0) >= 1,
            "h1": index.get("h1", 0) == 1,
            "sitemap": (root / "sitemap.xml").exists(),
            "robots": (root / "robots.txt").exists(),
            "llms": (root / "llms.txt").exists(),
            "ai_txt": (root / "ai.txt").exists(),
        }
        # 0-5: technical / social / structured / discoverability / content
        score = sum(1 for k in ("title", "description", "canonical_index", "canonical_book", "og", "twitter", "ldjson", "h1", "sitemap", "robots", "llms") if checks[k])
        rows.append({
            "key": site["key"],
            "name": site["name"],
            "version": site["version"],
            "index_bytes": index.get("bytes", 0),
            "book_bytes": book.get("bytes", 0),
            **checks,
            "score_11": score,
        })
    out = SEO_DIR / "audit-report.json"
    out.write_text(json.dumps({"generated_at": "2026-11-20", "sites": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (SEO_DIR / "audit-report.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f"{r['name']:<5} score={r['score_11']}/11 index={r['index_bytes']} book={r['book_bytes']} title={r['title']} desc={r['description']} canon={r['canonical_index']}/{r['canonical_book']} ld={r['ldjson']} sitemap={r['sitemap']} robots={r['robots']} llms={r['llms']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
