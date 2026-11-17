"""Static checks for the story-engine plugin. Run: python3 tests/check_plugin.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"


def frontmatter(path):
    lines = Path(path).read_text().splitlines()
    assert lines[0] == "---", f"{path}: no frontmatter"
    end = lines.index("---", 1)
    out = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def index_ids():
    text = (KNOWLEDGE / "index.md").read_text()
    return set(re.findall(r"^\| ([FST]\d{3}) \|", text, re.M))


def check_manifests():
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    assert plugin["name"] == "story-engine"
    assert plugin["version"] == "0.1.0"
    assert plugin["license"] == "MIT"
    assert plugin["author"]["name"] == "sebdavila"
    assert plugin["description"]
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert market["name"] == "story-engine"
    assert market["owner"]["name"] == "sebdavila"
    assert len(market["plugins"]) == 1
    assert market["plugins"][0]["name"] == "story-engine"
    assert market["plugins"][0]["source"] == "./"


def check_skills():
    pass


def check_agents():
    pass


def check_ids():
    pass


def check_docs():
    pass


if __name__ == "__main__":
    check_manifests()
    check_skills()
    check_agents()
    check_ids()
    check_docs()
    print("OK")
