#!/usr/bin/env python3
"""dev.to 发布队列：读 jobs.json（[title, ch, file, tags, description]），逐篇 POST，自带重试与限速。
用法：python3 tools/pub_queue.py tools/pub_jobs.json
"""
import json, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "tools" / "pub_jobs.json")
TOK = subprocess.run(["bash", "-lc", "~/.daokedao-vault/cred devto"], capture_output=True, text=True).stdout.strip()

def post(j):
    if isinstance(j, dict):
        title, f, tags, desc = j["title"], j["file"], j["tags"], j["desc"]
        canonical, key = j["canonical"], j.get("key", j["file"])
    else:
        title, ch, f, tags, desc = j
        canonical = f"https://q1z2q3-debug.github.io/runze-daokedao/chapters/yizhuan/{ch}.html"
        key = ch
    body = (ROOT / "dist" / f).read_text(encoding="utf-8")
    payload = json.dumps({"article": {
        "title": title, "published": True, "body_markdown": body, "tags": tags,
        "canonical_url": canonical,
        "description": desc}}).encode()
    req = urllib.request.Request("https://dev.to/api/articles", data=payload, method="POST",
        headers={"api-key": TOK, "Content-Type": "application/json",
                 "Accept": "application/vnd.api+json", "User-Agent": "Mozilla/5.0 Chrome/126.0"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))["url"], None
    except urllib.error.HTTPError as e:
        return None, f"{e.code} {e.read()[:200]}"

jobs = json.loads(JOBS.read_text(encoding="utf-8"))
done = []
for j in jobs:
    key = j.get("key") if isinstance(j, dict) else j[1]
    for _ in range(6):
        url, err = post(j)
        if url:
            done.append([key, url]); print("OK", key, url, flush=True); break
        print("FAIL", key, err, flush=True); time.sleep(40)
    time.sleep(35)
print(json.dumps(done))
