#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调用微信公众平台 draft/add 保存草稿（不群发、不发布）。"""
import json, pathlib, urllib.request

ROOT = pathlib.Path("/home/user/Doubao/chats/38451969562668034/runze-daokedao")
token = pathlib.Path("/tmp/wx_token.txt").read_text().strip()
body = (ROOT / "dist/wechat-draft-body.html").read_text(encoding="utf-8")
thumb = pathlib.Path("/tmp/wx_thumb.txt").read_text().strip()

title = "花几年重读九部经典：一套把字放回源头的读本（免费在线读，有离线 APK）"
author = "润泽"
digest = ("《道德经》《易传》《心经》《庄子》《金刚经》《坛经》，加字学甲骨文与蒙学千字文、三字经。"
          "这套读本只做一件事：把每个关键字放回它造出来的那一刻，再看它怎么长成一句话、一部经。"
          "免费在线读，提供离线 APK。")

article = {
    "title": title,
    "author": author,
    "digest": digest,
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
print(json.dumps(out, ensure_ascii=False, indent=2))
if "media_id" in out:
    pathlib.Path("/tmp/wx_draft_id.txt").write_text(out["media_id"])
