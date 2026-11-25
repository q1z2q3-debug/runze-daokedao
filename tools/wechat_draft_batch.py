#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量提交公众号草稿（draft/add，仅存草稿，不群发）。"""
import json, pathlib, urllib.request

ROOT = pathlib.Path("/home/user/Doubao/chats/38451969562668034/runze-daokedao")
token = pathlib.Path("/tmp/wx_token.txt").read_text().strip()
thumb = pathlib.Path("/tmp/wx_thumb.txt").read_text().strip()

JOBS = [
    {
        "title": "《道德经》的三层解读境界：指月三境",
        "author": "润泽",
        "digest": "文字只是路标与符号，解读经文说到底是借着经文映照自己。这里分三层循序渐进：初时教授授课、学生听课；继而好友交谈、心心相印；终而水溶于水，泯除对立，直契实相。目的从来不是守住手指，而是看见月亮。",
        "body": "dist/wx-zh-zhiyue.html",
    },
    {
        "title": "把 50 万字古籍做成 3 MB 安卓阅读器：一条从 Markdown 到 APK 的流水线",
        "author": "润泽",
        "digest": "一部 72 卷、50.5 万字、704 页的《周易》读本，如何在地铁上、断网时、手机上被读到。以 HTML 为唯一成品派生阅读页、PDF、离线 APK 与检索站；字体子集内嵌、零权限 WebView 壳、长文拆页，并补 DOI 存档与数据集可被引用。",
        "body": "dist/wx-zh-apk-pipeline.html",
    },
]

results = []
for j in JOBS:
    body = (ROOT / j["body"]).read_text(encoding="utf-8")
    article = {
        "title": j["title"],
        "author": j["author"],
        "digest": j["digest"],
        "content": body,
        "thumb_media_id": thumb,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    payload = {"articles": [article]}
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    req = urllib.request.Request(
        url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    out = json.loads(resp)
    print(j["title"], "->", json.dumps(out, ensure_ascii=False))
    results.append({"title": j["title"], "media_id": out.get("media_id"), "err": out.get("errcode")})

(ROOT / "dist/wechat-drafts.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
