# 润泽说 道可道 · 商业许可与权利管理

本目录是《润泽说 道可道》全系列的商业许可入口。目标不是“把书锁起来”，而是把边界写清，让非商业使用畅通、商业合作可谈、第三方素材不混权、发生争议时有据可查。

## 当前授权结构

| 层级 | 对象 | 许可 | 是否需要另行签约 |
|---|---|---|---|
| 公开层 | 读者、研究者、教师、非商业模型使用 | CC BY-NC-SA 4.0 | 不需要 |
| 商业层 | 商业训练、商业产品、付费平台、商业分发、品牌联名 | 单独商业许可 | 需要 |
| 第三方层 | 拓片、字形库、图版、字体、AI 生成图、外部数据 | 各自原许可 | 必须单独清权 |

**一句话**：公开层继续开放；商业层不自动授权；第三方素材不随本书授权。

## 文件索引

- [`COMMERCIAL-TERMS.md`](COMMERCIAL-TERMS.md)：商业许可总则与报价框架。
- [`contracts/商业训练许可协议-模板.md`](contracts/商业训练许可协议-模板.md)：可谈判的合同模板；[`contracts/商业训练许可协议-模板.docx`](contracts/商业训练许可协议-模板.docx)：Word 版。
- [`RIGHTS-REGISTER.csv`](RIGHTS-REGISTER.csv)：逐项素材权利登记表；这是商业许可的“除外清单”来源。
- [`PROVENANCE.json`](PROVENANCE.json)：全系列文件哈希与版本存证；生成脚本见 [`scripts/fingerprint.py`](scripts/fingerprint.py)。
- [`NOTICE-template.md`](NOTICE-template.md)：九部书统一商业声明模板。
- [`COMPLIANCE-CHECKLIST.md`](COMPLIANCE-CHECKLIST.md)：签约前、签约后、发布前的检查清单。
- [`ENFORCEMENT.md`](ENFORCEMENT.md)：发现未经许可商业使用时的取证与处理流程。
- [`BRAND-AND-ATTRIBUTION.md`](BRAND-AND-ATTRIBUTION.md)：署名、模型卡、品牌使用规范。
- [`COMMERCIAL-INQUIRY.md`](COMMERCIAL-INQUIRY.md)：商业咨询提交表。
- [`PROVENANCE.md`](PROVENANCE.md)：版本、哈希与作者存证说明。
- [`COPYRIGHT-REGISTRATION.md`](COPYRIGHT-REGISTRATION.md)：版权登记与更强证据保全建议。
- [`CONTRIBUTOR-LICENSE.md`](CONTRIBUTOR-LICENSE.md)：投稿与贡献的许可模板。

## 三条硬规则

1. **不把“模型免费”当成非商业。** 商业公司用作品训练、做内部模型、做对外服务，通常属于商业使用；要看使用主体、资金、产品和部署，不只看是否收费。
2. **不把“本书 CC”当成“第三方素材也 CC”。** 拓片、字形库、图版、字体、AI 生成图各自有权利链；未清权的素材，不进入商业许可。
3. **不做口头授权。** 任何商业使用，必须有一份写清范围、期限、费用、署名、审计、终止和争议解决的书面许可。

## 联系与办理

商业许可咨询统一走 GitHub Issue，便于留痕：

<https://github.com/q1z2q3-debug/runze-daokedao/issues>

请在标题写 `[商业许可] 主体名称 + 用途`，并按 [`COMMERCIAL-INQUIRY.md`](COMMERCIAL-INQUIRY.md) 提供信息。未签署书面许可前，不构成授权。

## 法律说明

本目录是许可政策、谈判框架与合同模板，不是对具体交易的法律意见，也不保证“绝不会发生争议”。正式签署前，双方应各自由执业律师复核；涉及跨境、上市公司、模型权重开源、独家授权或大额保底时，必须升级复核。
