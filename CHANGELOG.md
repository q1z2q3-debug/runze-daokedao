## 2026-11-25 · 尚书 APK 换新版 0.3.8

- `docs/apk/shangshu-0.3.8.apk`（559 KB）：内含 1.34 MB 阅读版（58 篇 + 七附录，SVG 全内联）与 250 KB 校勘台，首页右下角固定入口；旧版 0.3.0 撤下，SHA256SUMS 重算（5ee2c827…）。
- `build.py` APK_BOOKS 尚书条目版本、体积、文件名同步；首页与 llms-books、ALL-BOOKS 的下载链一并换新。

# 变更记录

## 2026-11-27 · 《论语》入册第 09 部，APK 0.16.42 挂上总站

- 新书页 `docs/books/lunyu.html`：第九部，「润泽说 道可道之论语」，上下两论二十篇五百一十一章（另前言一篇，共 511 课、512 页），加专题八篇、论文三篇，合稿约 145 万字；底本朱熹《论语集注》，参校何晏《集解》、刘宝楠《正义》；总纲「一阴一阳之谓道」——学是受、习是发。右栏挂卷首与安卓安装包两链。
- APK：`docs/apk/lunyu-0.16.42.apk`（19,314,764 B，SHA256 `ebd4ca62…`），零权限、511 课插图内嵌、宋体两档字集内置，断网可读；`unzip -tqq` 通过。首页下载区增至第 10 张卡，`docs/assets/apk-qr/lunyu.svg` 生成后解码核验，指向 `…/apk/lunyu-0.16.42.apk`。
- 编号：论语取 09，原 `EXTRA_BOOKS` 顺延——甲骨文 10、千字文 11、三字经 12。
- 口径：全站「经典八部」改「经典九部」，「八部书」改「九部书」，合计字数 271 万改 416 万，APK 自「九部」改「十部」；llms、llms-books、ALL-BOOKS、README 同步，书页「同一系列的其他五部」改为按书目实数计数。
- SHA256SUMS 在 `docs/apk/` 内重算，10 个 APK、相对文件名。

## 2026-11-27 · 尚书 APK 换新图标 0.3.9，补全九张下载二维码

- `docs/apk/shangshu-0.3.9.apk`（643 KB）：新图标为暖纸底、墨色简尺、三枚刻度、赭红方印；包内仍是 58 篇 + 七附录 + 校勘台，`versionCode 9 / versionName 0.3.9`。旧 0.3.8 撤下。
- `build.py` 尚书条目 `v0.3.9`、APK 体积 643 KB、文件名同步；首页、书页、llms、ALL-BOOKS 的下载链一并换新。
- 补 `assets/apk-qr/shangshu.svg`、`mengzi.svg`：此前首页九张 APK 卡中有两张二维码缺图；现九张全部重生成并逐张解码核验，指向各自 APK。
- SHA256SUMS 重算（尚书 `43519b44…`）；README、ALL-BOOKS 补尚书、孟子两行，APK 口径改「经典八部＋《三字经》」。

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
