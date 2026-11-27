# 成果分类、编号与元数据

## 成果类型

| 代码 | 英文 | 中文及编目依据 |
| --- | --- | --- |
| P | Publications | 正式发表论文。必须核对出版方、期刊目录或有明确发表信息的正式记录。网页上线、仓库提交及预印本 DOI 各自只证明相应的公开行为。 |
| WP | Working Papers | 工作论文。已有相对完整的研究问题、材料和论证，尚未正式发表。 |
| RN | Research Notes | 研究手札。一个局部发现、短篇考证、理论辨析、思想实验、失败尝试或待解问题即可成篇。 |
| LN | Reading Notes | 阅读札记。以具体文献、段落或作者论证的细读为主要目的。 |
| MT | Methods & Tools | 研究方法与工具。记录方法、工作流、软件或他人可以复核的步骤与结果。 |

类型说明作品用途。证据质量、研究成熟度和评审状态分别判断。

## 永久编号、版本和演进

- 初次编目按当时类型领取递增序号，从 `0001` 开始，超过四位继续增长。示例格式为 `RN-0001`。首发日期另记，因此跨年无需换号。
- 新建私稿时给出的号是候选号。首次公开前与最新 `main` 及正在审阅的分支核对占号，解决并发冲突；正式占用后保留编号、首发日及路径。同一作品改题、换类、增译本或换版均沿用原记录。
- 同一作品从手札重新编为工作论文，可只改 `type`，即使当前类型与编号前缀不同。产生可单独引用的新论文时，保留两条记录，在新作登记 `develops` 指向前作；索引生成器也会在前作显示后续成果。
- 修正文献判断或论证时，更新正文、`version`、`last_revised` 并追加 `history`。旧版本须有可长期回读的文本链接，如带完整提交 SHA 的 GitHub blob。格式整理和档案页面改版不改变研究修订日。更正或撤回已公开成果时，保留编号与旧入口，并由研究者决定面向读者的说明。

## 研究领域

| 领域键 | 中文 | English |
| --- | --- | --- |
| `religious-studies` | 宗教学 | Religious Studies |
| `philosophy` | 哲学 | Philosophy |
| `artificial-intelligence` | 人工智能 | Artificial Intelligence |
| `chinese-intellectual-traditions` | 中国传统思想 | Chinese Intellectual Traditions |
| `interdisciplinary-studies` | 跨学科研究 | Interdisciplinary Studies |

同一成果可列多个领域。选择正文实际讨论的主题，研究者有兴趣的其他方向可以等到有作品时再编入。

## 字段字典

每项作品包含 `archive/works/<ID>/record.json` 与 `body.html.inc`。统一索引 `archive.json` 从所有公开条目生成。JSON 使用 UTF-8。

| 字段 | 格式与维护方法 |
| --- | --- |
| `id`、`path` | 稳定编号与正文公开相对路径。新条目默认使用小写编号加 `.html`，旧文沿用原文件名。 |
| `title`、`title_en` | 原文标题及可选英文标题。英文原作可填同一标题；没有经过核对的译题填 `null`。 |
| `abstract`、`abstract_en` | 主语言摘要；可另填供英文索引使用的摘要。不据此把正文标成双语。 |
| `type`、`areas`、`keywords` | 上表类型、一个或多个领域键、非空且无重复的关键词数组。 |
| `languages` | `["zh-CN"]`、`["en"]` 或包含两者的数组，第一项是页面主语言。双语正文用相应的 `lang` 标记两种文本。 |
| `first_published`、`last_revised` | ISO 日期 `YYYY-MM-DD`。分别指作品首次公开和最近的研究文本修订。档案迁移保留原日期。 |
| `version`、`history` | 如 `0.2`、`1.0`、`1.0.1`。修订数组从旧至新，每项有 `version`、`date`、`note`、`snapshot`。当前版本的固定链接可以稍后补记，旧版本均须能回读。 |
| `status` | `in-progress` 进行中，`working-note` 工作札记，`complete` 已完成，`published` 已正式发表。 |
| `peer_review` | `not-peer-reviewed`、`peer-reviewed`、`undocumented`。未正式发表一律显示 **Not peer reviewed / 未经同行评审**。正式发表作品按实际评审证据填写，无法核对时选 `undocumented`。 |
| `publication` | P 必填 `venue`、`date`、`url`。人工打开正式发表记录核对作者、题名、发表载体和日期；其他类型填 `null`。 |
| `related` | 数组，每项有目标 `id` 和 `kind`。`related` 为相关研究，`develops` 为发展自，`supersedes` 为接续并替代。没有真实关联时填 `[]`。 |
| `release` | `review` 仅用于私人候选，`public` 表示已准许公开的材料。实际授权在私人审阅记录中保存。 |
| `citation` | 自动生成于 `archive.json` 和作品页，含作者、原题、永久编号、版本、修订日及稳定网址。引用正式发表版时可沿出版记录查到出版方引文。 |

[已编目的中文实例](../archive/works/LN-0001/record.json) · [英文实例](../archive/works/MT-0001/record.json) · [机器可读档案](../archive.json)
