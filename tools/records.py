"""The public catalogue vocabulary and its integrity checks (standard library only)."""
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORKS = ROOT / "archive/works"
TEMPLATES = ROOT / "archive/templates"
SITE = "https://raylee-ai.github.io/"

TYPES = {
    "P": ("Publications", "正式发表论文"), "WP": ("Working Papers", "工作论文"),
    "RN": ("Research Notes", "研究手札"), "LN": ("Reading Notes", "阅读札记"),
    "MT": ("Methods & Tools", "研究方法与工具"),
}
AREAS = {
    "religious-studies": ("Religious Studies", "宗教学"), "philosophy": ("Philosophy", "哲学"),
    "artificial-intelligence": ("Artificial Intelligence", "人工智能"),
    "chinese-intellectual-traditions": ("Chinese Intellectual Traditions", "中国传统思想"),
    "interdisciplinary-studies": ("Interdisciplinary Studies", "跨学科研究"),
}
LANGUAGES = {"en": ("English", "英文"), "zh-CN": ("Chinese", "中文")}
STATES = {"in-progress": ("Work in progress", "进行中"), "working-note": ("Working note", "工作札记"),
          "complete": ("Complete", "已完成"), "published": ("Formally published", "已正式发表")}
PEER = {"not-peer-reviewed": ("Not peer reviewed", "未经同行评审"),
        "peer-reviewed": ("Peer reviewed", "已通过同行评审"),
        "undocumented": ("Review status unconfirmed", "评审状态待核")}
RELATIONS = {"related": ("Related work", "相关成果"), "develops": ("Develops", "发展自"),
             "supersedes": ("Supersedes", "接续并替代")}
INVERSE = {"related": ("Related work", "相关成果"), "develops": ("Developed into", "后续成果"),
           "supersedes": ("Superseded by", "由后作接续")}
RESERVED = {"index.html", "research.html", "about.html", "404.html"}
KEYS = set("""id type title title_en abstract abstract_en areas keywords languages first_published
last_revised version status peer_review related publication path release history""".split())
ID = re.compile(r"(P|WP|RN|LN|MT)-([0-9]{4,})")
VERSION = re.compile(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?")

def require(condition, message):
    if not condition:
        raise ValueError(message)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def string_list(values):
    return isinstance(values, list) and bool(values) and all(nonempty(v) for v in values) and len(set(values)) == len(values)

def iso(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), f"Expected ISO date, got {value!r}")
    dt.date.fromisoformat(value)
    return value

def web_url(value):
    return isinstance(value, str) and urlsplit(value).scheme == "https" and bool(urlsplit(value).netloc)

def version_key(value):
    require(isinstance(value, str) and VERSION.fullmatch(value), f"Invalid version {value!r}")
    return tuple(map(int, value.split(".")))

def validate(record, body, release):
    r = record
    require(set(r) == KEYS, f"Unexpected or missing record fields: {set(r) ^ KEYS}")
    match = ID.fullmatch(r["id"])
    require(match and int(match[2]) > 0 and match[2] == f"{int(match[2]):04d}", "Invalid stable ID")
    require(r["release"] == release, f"Expected release={release}")
    require(r["type"] in TYPES and r["status"] in STATES and r["peer_review"] in PEER, "Invalid type, status or review")
    require(re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", r["path"]) and r["path"] not in RESERVED, "Invalid or reserved public path")
    for key in ("title", "abstract"):
        require(nonempty(r[key]), f"Empty {key}")
    for key in ("title_en", "abstract_en"):
        require(r[key] is None or nonempty(r[key]), f"Use text or null for {key}")
    for key in ("areas", "keywords", "languages"):
        require(string_list(r[key]), f"Expected unique, nonempty {key}")
    require(set(r["areas"]) <= AREAS.keys() and set(r["languages"]) <= LANGUAGES.keys(), "Unknown area or language")
    require("[[" not in body + json.dumps(r, ensure_ascii=False), "Replace all writing prompts")
    require(nonempty(re.sub(r"<!--.*?-->|<[^>]*>", "", body, flags=re.S)), "Empty research text")
    if len(r["languages"]) > 1:
        for lang in r["languages"]:
            require(re.search(rf"""\blang=["']{lang}["']""", body), f"Mark the {lang} text with lang")
    require(iso(r["first_published"]) <= iso(r["last_revised"]), "Revision predates first publication")
    history = r["history"]
    require(isinstance(history, list) and history, "Revision history is required")
    versions, dates = [], []
    for entry in history:
        require(set(entry) == {"version", "date", "note", "snapshot"} and nonempty(entry["note"]), "Incomplete revision")
        versions.append(version_key(entry["version"]))
        dates.append(iso(entry["date"]))
        require(entry["snapshot"] is None or web_url(entry["snapshot"]), "Invalid revision link")
    require(all(e["snapshot"] for e in history[:-1]), "Link previous versions to their archived text")
    require(versions == sorted(set(versions)) and dates == sorted(dates), "History must be chronological with unique versions")
    require((dates[0], dates[-1], history[-1]["version"]) == (r["first_published"], r["last_revised"], r["version"]), "History and displayed dates/version disagree")
    pub = r["publication"]
    if r["type"] == "P":
        require(isinstance(pub, dict) and set(pub) == {"venue", "date", "url"} and nonempty(pub["venue"]) and web_url(pub["url"]), "Publications require a verifiable publication record")
        iso(pub["date"])
        require(r["status"] == "published", "Use published for a formal publication")
    else:
        require(pub is None and r["status"] != "published" and r["peer_review"] == "not-peer-reviewed", "Unpublished entries must use not-peer-reviewed")
    require(isinstance(r["related"], list), "Expected a related-work list")
    for link in r["related"]:
        require(set(link) == {"id", "kind"} and link["kind"] in RELATIONS and link["id"] != r["id"], "Invalid relationship")

def load(directory, release):
    require(not directory.is_symlink() and not any((directory / f).is_symlink() for f in ("record.json", "body.html.inc")), "Use normal source files inside the work directory")
    record = json.loads((directory / "record.json").read_text(encoding="utf-8"))
    body = (directory / "body.html.inc").read_text(encoding="utf-8")
    try:
        validate(record, body, release)
        if release == "public":
            require(directory.name == record["id"], "ID must match its directory")
            require({p.name for p in directory.iterdir() if p.name != ".DS_Store"} == {"record.json", "body.html.inc"}, "A public record contains an unexpected file")
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"{directory.name}: {error}") from error
    return record, body

def catalogue(candidate=None):
    entries = [load(p, "public") for p in sorted(WORKS.iterdir()) if p.is_dir() and not p.name.startswith(".")]
    if candidate:
        entries.append(load(candidate, "review"))
    ids = {r["id"] for r, _ in entries}
    require(len(ids) == len(entries) == len({r["path"] for r, _ in entries}), "Duplicate ID or URL")
    for r, _ in entries:
        require(all(link["id"] in ids for link in r["related"]), f"Unknown related work in {r['id']}")
    return sorted(entries, key=lambda item: (item[0]["first_published"], item[0]["id"]), reverse=True)

def citation(r):
    return f"Ray Lee. {r['title']} ({r['id']}, v{r['version']}). {r['last_revised']}. {SITE}{r['path']}"
