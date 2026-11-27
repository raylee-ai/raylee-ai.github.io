# Ray Lee — Research & Writing

个人开放研究档案。首页展示最近三项成果，完整索引支持按成果类型、研究领域和首次发布日期组合筛选。中文、英文及双语作品共用一个编号体系。

[首页](index.html) · [研究索引](research.html) · [关于](about.html) · [机器可读目录](archive.json)

## 本地预览

用浏览器打开本目录的 `index.html`，页面、文章、样式和筛选器都可离线使用。如需核对能复制或刷新的筛选网址，在仓库根目录运行以下命令，再访问终端所示端口的 `/research.html`。

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

## 内容维护

每项公开作品在 `archive/works/<ID>/` 中维护 `record.json` 和 `body.html.inc`。首页、研究索引、作品页、`archive.json` 和站点地图由 Python 3.9 或更新版本的标准库生成。Pages 直接分发提交好的静态文件。

```sh
python3 tools/archive.py build
python3 tools/archive.py check --base origin/main
```

| 文档 | 用途 |
| --- | --- |
| [现站与 Profile 审计](docs/audit.md) | 原站清单、部署证据、内容及迁移依据 |
| [分类、编号和元数据规范](docs/catalogue.md) | 编号、字段、版本、引用和演进关系 |
| [研究手札模板](archive/templates/research-note.html.inc) | 中文模板；同目录提供英文模板 |
| [发布流程](docs/publishing.md) | 私人研究、审阅预览、证据核对、确认与发布 |
| [Agent 维护说明](AGENTS.md) | 日常新增、修订、校验和提交方式 |
| [升级对照及验收](docs/acceptance.md) | 保真验证、筛选、视口、发布演练和预览图 |

生产 Pages 读取 `main` 根目录。首轮交付供研究者审阅，候选站名和简介见首页。
