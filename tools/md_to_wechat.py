#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用 Markdown → 公众号草稿正文 HTML（内联样式，兼容微信编辑器）。
用法：python3 tools/md_to_wechat.py <src.md> <out.html>
"""
import markdown, pathlib, re, sys

STYLE = {
    "h2": "font-size:19px;font-weight:700;color:#1B1917;margin:28px 0 14px;padding-left:10px;border-left:4px solid #8C3A2E;line-height:1.5;",
    "h3": "font-size:17px;font-weight:700;color:#1B1917;margin:22px 0 10px;line-height:1.5;",
    "p": "font-size:16px;color:#3A342C;line-height:1.9;margin:14px 0;letter-spacing:.3px;",
    "blockquote": "margin:18px 0;padding:12px 16px;background:#F1ECE2;border-left:3px solid #DCD3C4;color:#6B6152;font-size:15px;line-height:1.8;",
    "ul": "margin:14px 0;padding-left:22px;color:#3A342C;",
    "ol": "margin:14px 0;padding-left:22px;color:#3A342C;",
    "li": "font-size:16px;line-height:1.9;margin:8px 0;",
    "table": "width:100%;border-collapse:collapse;margin:18px 0;font-size:14px;",
    "th": "border:1px solid #DCD3C4;background:#F1ECE2;padding:9px 10px;text-align:left;color:#1B1917;font-weight:600;",
    "td": "border:1px solid #DCD3C4;padding:9px 10px;color:#3A342C;line-height:1.7;",
    "a": "color:#8C3A2E;text-decoration:none;border-bottom:1px solid rgba(140,58,46,.28);",
    "strong": "color:#1B1917;",
    "pre": "margin:16px 0;padding:14px 14px;background:#F5F1E8;border-radius:6px;overflow-x:auto;",
    "code": "font-family:Menlo,Consolas,monospace;font-size:13px;line-height:1.7;color:#2B2620;",
}

def convert(md_text: str) -> str:
    md = markdown.Markdown(extensions=["tables", "sane_lists", "fenced_code"])
    raw = md.convert(md_text)

    def add_style(tag, text):
        return re.sub(rf"<{tag}>", f'<{tag} style="{STYLE[tag]}">', text)

    for tag in ["h2", "h3", "p", "blockquote", "ul", "ol", "li", "table", "th", "td", "strong"]:
        raw = add_style(tag, raw)

    # 代码块：pre 与 code 加样式（code 在 pre 内与行内分别处理）
    raw = re.sub(r"<pre>", f'<pre style="{STYLE["pre"]}">', raw)
    raw = re.sub(r"<code>", f'<code style="{STYLE["code"]}">', raw)

    # 先保护 <img>，避免裸链接正则把 src 包进 <a>
    imgs = []
    def _stash_img(m):
        imgs.append(m.group(0)); return f"\x00IMG{len(imgs)-1}\x00"
    raw = re.sub(r'<img[^>]*>', _stash_img, raw)

    # 链接补内联样式
    raw = re.sub(r'<a href="([^"]+)">', rf'<a href="\1" style="{STYLE["a"]}">', raw)

    # 裸 URL 补成 <a>（跳过已在 href/标签内）
    def _linkify(m):
        url = m.group(0)
        return f'<a href="{url}" style="{STYLE["a"]}">{url}</a>'
    raw = re.sub(r'(?<!href=")(?<!">)https?://[^\s<]+', _linkify, raw)

    # 还原 img，补内联样式（宽度自适应）
    def _restore_img(m):
        tag = imgs[int(m.group(1))]
        if "style=" not in tag:
            tag = tag.replace("<img", '<img style="max-width:100%;height:auto;margin:10px 0;"')
        return tag
    raw = re.sub(r"\x00IMG(\d+)\x00", _restore_img, raw)

    # 去掉首个 H1（标题单独传 title）
    raw = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", raw, count=1, flags=re.S)
    return raw

if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    body_md = src.read_text(encoding="utf-8")
    raw = convert(body_md)
    out.write_text(raw, encoding="utf-8")
    print("body chars:", len(raw), "| tables:", raw.count("<table"),
          "| links:", raw.count("<a "), "| pre:", raw.count("<pre"))
