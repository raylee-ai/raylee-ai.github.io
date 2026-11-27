"""Validate public routes, local anchors and changes to the permanent register."""
import json
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit

from records import ROOT, SITE, require


class PageLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1 = 0
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            require("alt" in values, "Image without alt attribute")
        for key in ("href", "src"):
            if key in values:
                self.links.append(values[key])


def check_links(pages):
    parsed = {p: PageLinks(text) for p, text in pages.items() if p.endswith(".html")}
    total = 0
    for path, page in parsed.items():
        require(page.h1 == 1 and "main" in page.ids, f"{path}: expected one H1 and a main anchor")
        require(all(n == 1 for n in Counter(page.ids).values()), f"{path}: duplicate HTML ID")
        for url in page.links:
            link = urlsplit(url)
            if link.scheme == "mailto" or (link.scheme in ("https", "http") and link.netloc != urlsplit(SITE).netloc):
                continue
            require(not link.scheme or link.scheme in ("https", "http"), f"{path}: unexpected URL scheme")
            require(not link.netloc or link.netloc == urlsplit(SITE).netloc, f"{path}: unexpected host")
            name = unquote(link.path)
            target = "index.html" if (link.netloc or name == "/") and name in ("", "/") else name.lstrip("/") or path
            require(".." not in PurePosixPath(target).parts and (target in pages or (ROOT / target).is_file()), f"{path}: missing target {url}")
            if link.fragment:
                require(target in parsed and unquote(link.fragment) in parsed[target].ids, f"{path}: missing anchor {url}")
            total += 1
    return len(parsed), total


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def history_since(base, entries):
    # Resolve a real commit once; paths below are relative to that immutable tree.
    commit = git("rev-parse", "--verify", base + "^{commit}").decode().strip()
    paths = git("ls-tree", "-r", "--name-only", commit, "--", "archive/works").decode().splitlines()
    current = {r["id"]: (r, body) for r, body in entries}
    old_ids = set()
    for path in paths:
        if not path.endswith("/record.json"):
            continue
        old = json.loads(git("show", f"{commit}:{path}"))
        key = old["id"]
        old_ids.add(key)
        require(key in current, f"Stable ID removed: {key}")
        r, body = current[key]
        for field in ("path", "first_published"):
            require(r[field] == old[field], f"{key}: {field} is permanent")
        require(len(r["history"]) >= len(old["history"]), f"{key}: lost an archived revision")
        for before, after in zip(old["history"], r["history"]):
            for field, value in before.items():
                if field != "snapshot" or value is not None:
                    require(after[field] == value, f"{key}: earlier revision changed")
        original = git("show", f"{commit}:{path.removesuffix('record.json')}body.html.inc").decode()
        require(original == body or old["version"] != r["version"], f"{key}: record the change to the text as a new version")
    for key in current.keys() - old_ids:
        require(key.split("-")[0] == current[key][0]["type"], f"{key}: allocate a new ID under its initial type")
