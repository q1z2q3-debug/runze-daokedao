#!/usr/bin/env python3
"""Generate a provenance manifest for the 润泽说 道可道 book repositories.

Only tracked files are hashed. Run from the runze-daokedao repository root:
    python3 LICENSING/scripts/fingerprint.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK_ROOT = ROOT.parent
BOOKS = {
    "runze-daodejing": "润泽说 道可道之道德经心法读本",
    "daokedao-yijing-pub": "润泽说 道可道之易传",
    "daokedao-xinjing": "润泽说 道可道之心经通释",
    "daokedao-tanjing": "润泽说 道可道之坛经",
    "daokedao-jingang": "润泽说 道可道之金刚经",
    "daokedao-qianziwen": "润泽说 蒙学之千字文",
    "daokedao-jiaguwen": "润泽说 道可道之甲骨文",
    "daokedao-zhuangzi": "润泽说 道可道之庄子",
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True
    ).stdout.strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def version(repo: Path) -> str:
    p = repo / "VERSION"
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""


def main() -> None:
    repos: dict[str, dict] = {}
    for dirname, title in BOOKS.items():
        repo = BOOK_ROOT / dirname
        if not repo.exists():
            repos[dirname] = {"title": title, "error": "repository not found"}
            continue
        try:
            commit = git(repo, "rev-parse", "HEAD")
            branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
            remote = git(repo, "config", "--get", "remote.origin.url") or ""
            files = git(repo, "ls-files", "-z").split("\0")
            entries = []
            total = 0
            aggregate = hashlib.sha256()
            for rel in sorted(x for x in files if x):
                path = repo / rel
                if not path.is_file():
                    continue
                size = path.stat().st_size
                digest = sha256(path)
                total += size
                entries.append({"path": rel, "bytes": size, "sha256": digest})
                aggregate.update(f"{rel}\0{digest}\n".encode("utf-8"))
            repos[dirname] = {
                "title": title,
                "version": version(repo),
                "branch": branch,
                "commit": commit,
                "remote": remote,
                "file_count": len(entries),
                "bytes": total,
                "aggregate_sha256": aggregate.hexdigest(),
                "files": entries,
            }
        except Exception as exc:  # keep a usable manifest even if one repo fails
            repos[dirname] = {"title": title, "error": f"{type(exc).__name__}: {exc}"}

    out = {
        "schema": "runze-daokedao-provenance-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "author": "润泽（润泽博士）",
        "license": "CC BY-NC-SA 4.0; commercial use requires a separate written license",
        "note": "Hashes cover tracked files only. This is technical evidence, not copyright registration.",
        "books": repos,
    }
    out_path = ROOT / "LICENSING" / "PROVENANCE.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
