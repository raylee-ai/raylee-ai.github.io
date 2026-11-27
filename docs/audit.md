# 现有个人网站与 GitHub Profile 审计

核对日期为 2026 年 11 月 27 日。网站基线为 `487334ef36f8c7f1043ccd8e81284cca4605365a`，Profile 基线为 `83d4d252c4eaee6c6a2724d9cec6532cdf2f1e9f`。两个本地检出分别与远端 `main` 对齐。已阅读源码、两篇原文及 Profile README，并在 Chrome 实际打开线上四个页面。[网站基线](https://github.com/raylee-ai/raylee-ai.github.io/tree/487334ef36f8c7f1043ccd8e81284cca4605365a) · [Profile 基线](https://github.com/raylee-ai/raylee-ai/tree/83d4d252c4eaee6c6a2724d9cec6532cdf2f1e9f)

## 文件与导航

| 基线文件 | 线上用途及可复用部分 |
| --- | --- |
| `index.html` | 英文首页。作者简介、宗教学本科身份、联系方式、最新写作。Writing 指向 `index.html#notes`，条目直接链接两篇原文。 |
| `about.html` | 中文介绍、研究兴趣、阅读方法、个人立场说明和公开联系邮箱。 |
| `ghazali.html` | 中文札记，含来源范围、六个参考文献锚点、修订说明。 |
| `citation-audit.html` | 英文方法札记。用两项书目判断及四条引文演示版本匹配与转换损失，附两个 OpenAlex 条目和离线工具。 |
| `style.css` | 白底、蓝灰链接、Georgia 和系统中文字体、单栏阅读、600px 移动断点、跳转到正文、键盘聚焦和减少动画偏好。 |
| `favicon.svg` | 已有 R 字站标。 |
| `.nojekyll` | 以静态文件分发。 |
| `README.md` | 旧说明记录了从 main 更新 Pages 的方式，文件目录遗漏了后来增加的英文方法札记。 |

原站共四个 HTML 文件。旧站用首页承担索引，作品状态和版本散落在各页。新索引沿用现有阅读宽度、字形、颜色、站标和原文路径。首页旧锚点、正文锚点继续可达。[原首页](https://raylee-ai.github.io/) · [原关于页](https://raylee-ai.github.io/about.html)

## 两篇作品的归档依据

| 原文及自述 | 首次公开与修订证据 | 首轮编目 |
| --- | --- | --- |
| 《教导有效，何以识别先知？》。旧正文用“研究札记”作泛称，旧首页明确标为 Reading note。文章逐段读取安萨里原典并讨论既有解释。 | 2026-11-16 首发；同日可追溯 v0.1 和 v0.2。v0.2 的正文有详细修订说明，标明进行中、未经同行评审。 | LN-0001 阅读札记。宗教学、哲学。 |
| *Which edition did I match, and which citations survived?*。原页面标 Methods note、Working note v1.0。文中保留可复现样例的公开仓库入口。 | 2026-11-23 首发 v1.0。当天首页和文章导航的调整没有形成新的研究版本。 | MT-0001 研究方法与工具。宗教学。按未发表工作札记展示评审提示。 |

未见正式发表记录或另一份可单列的工作论文。开放工具继续由英文文章链接，首轮没有把同一个方法案例拆成第二项成果。[安萨里 v0.1 原页](https://github.com/raylee-ai/raylee-ai.github.io/blob/9e42f230eba072b1f481a7ecc5a3677550308fcb/ghazali.html) · [v0.2 原页](https://github.com/raylee-ai/raylee-ai.github.io/blob/68a4c63bbb17b49d3ad88f01c319cebf09c1a49e/ghazali.html) · [方法札记 v1.0](https://github.com/raylee-ai/raylee-ai.github.io/blob/54b5547b9429d8690eeb9d733bd23116e7981243/citation-audit.html)

## GitHub Profile

Profile 基线有三个文件。README 使用 `assets/intro.svg` 标题图，另有未被这个 README 引用的 `banner.png`。简介提到宗教学、哲学、中央民族大学，以及 Lancer、文献元数据审计和 AI 界面设计工具。网站链接仍指向正确的首页，其文字只写宗教方向的中文札记，与已经存在的英文方法札记范围有出入。关联仓库本轮作为身份与导航来源，档案升级在网站仓库中完成。[Profile README](https://github.com/raylee-ai/raylee-ai/blob/83d4d252c4eaee6c6a2724d9cec6532cdf2f1e9f/README.md)

## 部署与技术取舍

GitHub Pages 设置实际显示 **Deploy from a branch**、`main`、`/ (root)`。第 7 次 Pages 运行从网站基线完成 build、report-build-status 和 deploy。根目录有 `.nojekyll`，仓库没有自定义发布工作流或前端包管理配置。[Pages 运行记录](https://github.com/raylee-ai/raylee-ai.github.io/actions/runs/45141072957)

两篇作品的信息会同时出现在首页、完整索引和文章页。一个离线生成命令使这些位置共用同一份元数据，并可在提交前发现陈旧输出。浏览器只加载静态 HTML、原有 CSS 和索引上的筛选脚本。正文渲染、链接和部署均沿用 GitHub Pages 原有机制。
