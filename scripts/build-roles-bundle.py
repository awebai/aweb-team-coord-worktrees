#!/usr/bin/env python3
"""Build an aw roles bundle from resources/roles/*.md."""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TITLES = {
    "coordinator": "Coordinator",
    "developer": "Developer",
    "reviewer": "Reviewer",
}

roles = {}
for path in sorted((ROOT / "resources" / "roles").glob("*.md")):
    name = path.stem
    roles[name] = {
        "title": TITLES.get(name, name.replace("-", " ").title()),
        "playbook_md": path.read_text(),
    }

print(json.dumps({"roles": roles}, indent=2))
