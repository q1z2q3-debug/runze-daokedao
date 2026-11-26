## 2026-11-25 · 尚书 APK 换新版 0.3.8

- `docs/apk/shangshu-0.3.8.apk`（559 KB）：内含 1.34 MB 阅读版（58 篇 + 七附录，SVG 全内联）与 250 KB 校勘台，首页右下角固定入口；旧版 0.3.0 撤下，SHA256SUMS 重算（5ee2c827…）。
- `build.py` APK_BOOKS 尚书条目版本、体积、文件名同步；首页与 llms-books、ALL-BOOKS 的下载链一并换新。

# 变更记录

## 2026-11-26 · 《孟子》入册，经典七部扩为八部

- 书目：`build.py` BOOKS 增《润泽说 道可道之孟子》（no.08，v0.37.0，57.1 万字，261 页 + 261 图），字学、蒙学编号顺延为 09–11。
- 文案：全站「经典七部」改「经典八部」，合计字数约 214 万 → 约 271 万；一句话定义、问答、书页 lede、llms、页面标题与 JSON-LD 同步；书页右栏挂「全本离线版」「体检报告 v0.37.0」两链。
- DOI：孟子未送 Zenodo，书页存档栏标「未送存」，引用页排除无 DOI 条目。
- APK：`docs/apk/mengzi-0.37.0.apk`（3.1 MB，GitHub Actions 构建，assets 含 261 章页与 261 图）入库，APK_BOOKS 增条目，SHA256SUMS 重算（a2bbaade…）。
- 总表：README、ALL-BOOKS.md、docs/llms-books.txt 增孟子行。

## 2026-11-25 · 《尚书》入册，经典六部扩为七部

- 书目：`build.py` BOOKS 增《润泽说 道可道之尚书》（no.07，v0.3.8，26.0 万字，58 篇 + 7 附录 + 校勘台 511 条账目），字学、蒙学编号顺延为 08–10。
- 文案：全站「经典六部」改「经典七部」，合计字数 188.0 万 → 约 214 万；一句话定义、问答、书页 lede、llms、页面标题与 JSON-LD 同步。
- DOI：尚书尚在校勘正编，未送 Zenodo。书页存档栏写「未送存」，引用页表格与 BibTeX 排除无 DOI 条目，schema `sameAs` 与 llms 不再强行拼 DOI 链接。
- 入口：书页右栏增「校勘台（可筛可勾可导出）」「校勘记·正编·底账」两链；无英文稿者不再挂指向自身的「英文稿索引」死链。
- APK：`docs/apk/shangshu-0.3.0.apk`（510 KB）入库，APK_BOOKS 增条目，SHA256SUMS 重算（d5abf2a7…）。
- 总表：README、ALL-BOOKS.md、docs/llms-books.txt 增尚书行；顺手对齐 llms-books 中道德经（2.9.25→3.0.1）、心经（1.1.0→1.0.0）的版本口径。

## 更早

见 `git log`。
