# 润泽说 道可道 · SEO 工作台

本目录是八部书站点的 SEO 单一配置源与可复现脚本。目标不是“堆关键词”，而是让搜索引擎与模型能正确理解、正确引用每一部书。

## 目录

- `config.json`：八站路径、站点根 URL、首页/全书页/前言页、版本、标题、描述、关键词、OG 图。
- `audit.py`：11 项静态检查；输出 `audit-report.json` 与 `audit-report.csv`。
- `patch.py`：按配置注入 canonical、description、OG/Twitter、citation 元标签；更新/新增 Book、WebSite、BreadcrumbList。
- `build_jiaguwen.py`：甲骨文专用构建；把 77 卷阅读版复制为 `docs/volumes/v01.html` … `v77.html`，生成新版首页与 sitemap。先跑它，再跑 `patch.py`。
- `overview.html`：基线 → 修补后 → 竞品对照 → 超越路径的可视化总览。
- `COMPARISON.md`：竞品取样与逐项对照。
- `ROADMAP.md`：四层超越路径与验收标准。
- `KEYWORDS.csv`：八书关键词簇与落地页，不是“关键词堆”，是内容缺口清单。

## 复现顺序

```bash
cd runze-daokedao
python3 SEO/build_jiaguwen.py   # 只在需要重建甲骨文首页/77卷时跑
python3 SEO/patch.py            # 幂等；重复跑不会重复注入
python3 SEO/audit.py            # 复核
```

## 当前结果（2026-11-20）

| 书目 | 修补前 | 修补后 | 站点 |
|---|---:|---:|---|
| 道德经 | 8/11 | 11/11 | https://q1z2q3-debug.github.io/runze-daodejing/ |
| 易传 | 10/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-yijing/ |
| 心经 | 11/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-xinjing/ |
| 坛经 | 11/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-tanjing/ |
| 金刚经 | 11/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-jingang/ |
| 千字文 | 6/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-qianziwen/ |
| 甲骨文 | 3/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-jiaguwen/ |
| 庄子 | 9/11 | 11/11 | https://q1z2q3-debug.github.io/daokedao-zhuangzi/ |

甲骨文站点另有：77 个独立卷页、85 个 sitemap URL、首页 13.9KB（原 785B）。

## 线上验证（2026-11-20）

已 push 到八站仓库，Pages 生效后抽查：

| 页面 | 状态 | canonical | 说明 |
|---|---|---|---|
| 道德经首页 | 200 | 正确 | — |
| 易传首页 | 200 | 正确 | JSON-LD 2 段 |
| 心经首页 | 200 | 正确 | — |
| 坛经首页 | 200 | 正确 | — |
| 金刚经首页 | 200 | 正确 | — |
| 千字文首页 | 200 | 正确 | 全书页 9.4MB，下载会被截断 |
| 甲骨文首页 | 200 | 正确 | 新版首页 |
| 庄子首页 | 200 | 正确 | — |
| 甲骨文 v01 | 200 | 正确 | 134KB，含内嵌图 |
| 甲骨文 v77 | 200 | 正确 | 18KB |

千字文 `book.html` 仍是大单页：HTTP 200，但 9.4MB 传输在中途被关闭；这是性能问题，不是标签问题，已列入 P1。

## 口径与边界

1. **这是静态本地审计**：检查标签是否存在、canonical 是否指向站点而不是 GitHub。不等于线上 HTTP 抓取、收录量、排名或富结果验证。
2. **分数不等于质量**：11/11 只说明基础项齐全。内容是否值得引用，取决于证据、版本、断句与注释。
3. **robots 与 ai.txt 的边界**：robots 允许索引与检索；ai.txt 说明商业训练需书面许可。两者不矛盾：允许“读”，不等于允许“商用训练”。
4. **第三方素材不随书授权**：拓片、字形库、AI 图、图版、字体各自有权利状态，见 `LICENSING/RIGHTS-REGISTER.csv`。
5. **构建覆盖风险**：`patch.py` 是后处理脚本；若某站重跑构建，可能覆盖已注入的 head。长期方案是把 SEO 注入并入模板/构建脚本。

## 下一步（按优先级）

1. 线上复验：对八站 `curl -I`、`curl -s` 复核 canonical/OG/JSON-LD；已抽查首页，后续每次发布都复验。
2. 七部书补 `cite/`；八站补 `feed.xml`。
3. 千字文 9.4MB、心经 1.7MB 全书页拆分或懒加载。
4. 甲骨文 905 个唯一字逐字页（字—卷—书三级内链）。
5. 八站统一 `llms.txt` 与 JSONL 分卷入口，让模型按卷取用。

## 相关文件

- 总站许可入口：`../LICENSING/README.md`
- 全书面板：`../ALL-BOOKS.md`
- 模型入口：`../docs/llms.txt`、`../docs/llms-books.txt`
