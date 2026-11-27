#!/usr/bin/env python3
"""Build the public archive, or work on a review copy outside the public repository."""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from checks import check_links, history_since
from records import LANGUAGES, ROOT, TEMPLATES, TYPES, catalogue, require
from render import outputs

ASSETS = ("style.css", "filters.js", "favicon.svg")


def outside_repo(path):
    path = path.expanduser().resolve()
    require(path != ROOT and ROOT not in path.parents and path not in ROOT.parents,
            "Choose a private directory outside this repository")
    return path


def draft(path, kind, language):
    path = outside_repo(path)
    existing = [int(r["id"].split("-")[1]) for r, _ in catalogue() if r["id"].startswith(kind + "-")]
    key = f"{kind}-{max(existing, default=0) + 1:04d}"
    today = dt.date.today().isoformat()
    langs = ["zh-CN", "en"] if language == "both" else [language]
    record = {"id": key, "type": kind, "title": "[[Title]]", "title_en": None, "abstract": "[[Abstract]]",
              "abstract_en": None, "areas": [], "keywords": [], "languages": langs,
              "first_published": today, "last_revised": today, "version": "0.1", "status": "in-progress",
              "peer_review": "not-peer-reviewed", "related": [], "publication": None,
              "path": key.lower() + ".html", "release": "review",
              "history": [{"version": "0.1", "date": today, "note": "[[Revision note]]", "snapshot": None}]}
    parts = []
    for lang in langs:
        name = "research-note.en.html.inc" if lang == "en" else "research-note.html.inc"
        part = (TEMPLATES / name).read_text(encoding="utf-8")
        parts.append(f'<section lang="{lang}">\n{part}</section>\n' if len(langs) > 1 else part)
    path.mkdir(parents=True, exist_ok=False)
    (path / "record.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (path / "body.html.inc").write_text("".join(parts), encoding="utf-8")
    print(f"{key} — private writing files: {path}")


def save(directory, files):
    # Prepare all files before swapping them into place. Every output can be rebuilt.
    with tempfile.TemporaryDirectory(dir=directory) as staging:
        for name, content in files.items():
            (Path(staging) / name).write_text(content, encoding="utf-8")
        for name in files:
            os.replace(Path(staging) / name, directory / name)


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="command", required=True)
    actions.add_parser("build", help="write ready-to-serve pages for the public records")
    check = actions.add_parser("check", help="check metadata, generated files and internal links")
    check.add_argument("--base", help="also check stable IDs, routes and prior versions against this Git ref")
    start = actions.add_parser("draft", help="create a new private candidate directory")
    start.add_argument("directory", type=Path)
    start.add_argument("--type", choices=TYPES, default="RN")
    start.add_argument("--lang", choices=[*LANGUAGES, "both"], default="zh-CN")
    preview = actions.add_parser("preview", help="render a private candidate with the public archive beside it")
    preview.add_argument("directory", type=Path)
    args = parser.parse_args()
    if args.command == "draft":
        draft(args.directory, args.type, args.lang)
        return
    candidate = outside_repo(args.directory) if args.command == "preview" else None
    entries = catalogue(candidate)
    pages = outputs(entries, review=bool(candidate))
    page_count, link_count = check_links(pages)
    if args.command == "check":
        if args.base:
            history_since(args.base, entries)
        for path, content in pages.items():
            target = ROOT / path
            require(target.is_file() and target.read_bytes() == content.encode(), f"Rebuild stale or missing {path}")
        print(f"Verified {len(entries)} works, {page_count} pages and {link_count} internal links/anchors.")
        return
    if candidate:
        dest = candidate / "preview"
        require(not dest.is_symlink(), "Choose a local preview directory without symlinks")
        dest.mkdir(exist_ok=True)
        for asset in ASSETS:
            pages[asset] = (ROOT / asset).read_text(encoding="utf-8")
        save(dest, pages)
        print(dest / "index.html")
    else:
        save(ROOT, pages)
        print(f"Built {page_count} static pages from {len(entries)} public works.")


if __name__ == "__main__":
    try:
        run()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
