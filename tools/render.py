"""Render static pages and indices; readers never need Python or a data request."""
import json
from html import escape
from string import Template
from xml.etree import ElementTree as ET

from records import AREAS, INVERSE, LANGUAGES, PEER, RELATIONS, SITE, STATES, TEMPLATES, TYPES, citation


def template(name, **values):
    return Template((TEMPLATES / (name + ".html.inc")).read_text(encoding="utf-8")).substitute(values)


def anchor(url, label):
    return f'<a href="{escape(url)}">{escape(label)}</a>'


def time(value):
    return f'<time datetime="{value}">{value}</time>'


def peer_label(record):
    english, chinese = PEER[record["peer_review"]]
    return f'<span lang="en">{english}</span> / <span lang="zh-CN">{chinese}</span>'


def page(path, title, description, content, *, lang="en", nav_item="", review=False):
    zh = lang == "zh-CN"
    nav = []
    for url, label in zip(("index.html", "research.html", "about.html"),
                          ("首页", "研究索引", "关于") if zh else ("Home", "Research", "About (中文)")):
        current = ' aria-current="page"' if url == nav_item else ""
        nav.append(f'<a href="{url}"{current}>{label}</a>')
    canonical = SITE if path == "index.html" else SITE + path
    discovery = '<meta name="robots" content="noindex,nofollow">' if review else f'<link rel="canonical" href="{canonical}">'
    return template("layout", lang=lang, description=escape(description), title=escape(title),
                    discovery=discovery, nav="".join(nav), navigation="主导航" if zh else "Main navigation",
                    skip="跳至正文" if zh else "Skip to content", contact="联系" if zh else "Contact",
                    script='<script src="filters.js" defer></script>' if path == "research.html" else "",
                    review_notice='<p class="notice">Local review / 本地审阅 · 候选条目的发布日期为拟定日期。</p>' if review else "",
                    content=content)


def card(r, heading):
    area_names = " · ".join(AREAS[a][0] for a in r["areas"])
    abstract = r["abstract_en"] or r["abstract"]
    abstract_lang = "en" if r["abstract_en"] else r["languages"][0]
    languages = " / ".join(LANGUAGES[lang][0] for lang in r["languages"])
    return f'''<article class="writing-item" data-type="{r['type']}" data-areas="{' '.join(r['areas'])}" data-date="{r['first_published']}">
  <div class="work-status"><span>{r['id']} · {escape(TYPES[r['type']][0])}</span><span>{languages} · v{r['version']}</span></div>
  <h{heading} lang="{r['languages'][0]}">{anchor(r['path'], r['title'])}</h{heading}>
  <p lang="{abstract_lang}">{escape(abstract)}</p>
  <div class="work-details"><span>{time(r['first_published'])}</span><span>{area_names}</span><span>{peer_label(r)}</span></div>
</article>'''


def work(r, body, records):
    column = int(r["languages"][0] == "zh-CN")
    def label(en, zh):
        return (en, zh)[column]
    def field(name, value):
        return f'<dt>{name}</dt><dd>{value}</dd>'
    fields = [
        field(label("Fields", "研究领域"), " · ".join(AREAS[key][column] for key in r["areas"])),
        field(label("Keywords", "关键词"), " · ".join(map(escape, r["keywords"]))),
        field(label("Text language", "正文语言"), " / ".join(LANGUAGES[key][column] for key in r["languages"])),
    ]
    if r["publication"]:
        pub = r["publication"]
        fields.append(field(label("Publication record", "正式发表记录"), anchor(pub["url"], pub["venue"]) + " · " + time(pub["date"])))
    related = {(link["id"], RELATIONS[link["kind"]][column]) for link in r["related"]}
    for other in records.values():
        for link in other["related"]:
            if link["id"] == r["id"]:
                related.add((other["id"], INVERSE[link["kind"]][column]))
    if related:
        links = [escape(kind) + " · " + anchor(records[key]["path"], key + " · " + records[key]["title"]) for key, kind in sorted(related)]
        fields.append(field(label("Related works", "关联研究"), "<br>".join(links)))
    history = []
    for version in reversed(r["history"]):
        ref = " · " + anchor(version["snapshot"], label("Version source", "此版本原文")) if version["snapshot"] else ""
        history.append(f'<li>v{version["version"]} · {time(version["date"])} · {escape(version["note"])}{ref}</li>')
    dates = label("First posted", "首次发布") + " " + time(r["first_published"]) + " · " + label("Last research revision", "最近研究修订") + " " + time(r["last_revised"])
    other_title = ""
    if r["title_en"] and r["title_en"] != r["title"]:
        other_title = f'<p lang="en">{escape(r["title_en"])}</p>'
    return template("work", title=escape(r["title"]), other_title=other_title, abstract=escape(r["abstract"]),
                    id=r["id"], back=label("Research index", "研究索引"), kind=escape(TYPES[r["type"]][column]),
                    status=STATES[r["status"]][column], version=r["version"], peer=peer_label(r), dates=dates,
                    details_label=label("Citation, fields & version history", "引用方式、研究领域与版本记录"),
                    fields="".join(fields), cite_label=label("How to cite", "引用方式"), citation=escape(citation(r)),
                    history_label=label("Version history", "版本记录"), history="".join(history), body=body)


def outputs(entries, review=False):
    records = {r["id"]: r for r, _ in entries}
    ordered = list(records.values())
    def options(choices):
        return "".join(f'<option value="{key}">{escape(value[0])}</option>' for key, value in choices.items())
    home = template("home", entries="\n".join(card(r, 3) for r in ordered[:3]))
    research = template("research", entries="\n".join(card(r, 3) for r in ordered),
                        types=options(TYPES), areas=options(AREAS),
                        count=f"{len(ordered)} {'work' if len(ordered) == 1 else 'works'}")
    pages = {}
    for path, title, description, content, lang in [
        ("index.html", "Ray Lee — Research & Writing", "Ray Lee’s research and writing on religious epistemology and research methods.", home, "en"),
        ("research.html", "Research · Ray Lee", "Browse Ray Lee’s research archive by type, field and date.", research, "en"),
        ("about.html", "关于 Ray Lee · Research & Writing", "Ray Lee 的研究背景、方法与个人开放研究档案说明。", template("about"), "zh-CN"),
    ]:
        pages[path] = page(path, title, description, content, lang=lang, nav_item=path, review=review)
    for r, body in entries:
        pages[r["path"]] = page(r["path"], r["title"] + " · Ray Lee", r["abstract"], work(r, body, records),
                                lang=r["languages"][0], review=review)
    public_index = [dict(r, citation=citation(r)) for r in ordered]
    pages["archive.json"] = json.dumps(public_index, ensure_ascii=False, indent=2) + "\n"
    if not review:
        sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for path in pages:
            if path.endswith(".html"):
                ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = SITE if path == "index.html" else SITE + path
        ET.indent(sitemap)
        pages["sitemap.xml"] = ET.tostring(sitemap, encoding="unicode") + "\n"
    return pages
