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


BRIEF_LABELS = ["- Audience:", "- Objective:", "- Domain:", "- Goal map row:",
                "- Format:", "- Length:", "- Material:"]
TRACE_LABELS = ["Knowledge trace", "- Read:", "- Framework:", "- Techniques:", "- Deviation:"]

# Text each skill must contain. Tasks 3-7 add their skill here.
SKILL_NEEDLES = {
    "story-coach": BRIEF_LABELS + ["story-mining", "story-structure", "story-draft",
                                   "story-review", "When to use", "Goal map"],
    "story-mining": ["../../knowledge/questions/", "founder-and-origin", "customer-and-buyer",
                     "personal-memory", "story-structure", "index.md"],
}
KNOWLEDGE_REF = re.compile(r"\.\./\.\./knowledge/([\w./*<>-]*)")


def check_skills():
    for name, needles in SKILL_NEEDLES.items():
        path = ROOT / "skills" / name / "SKILL.md"
        meta = frontmatter(path)
        assert meta.get("name") == name, path
        assert 0 < len(meta.get("description", "")) <= 1024, f"{path}: description length"
        text = path.read_text()
        assert len(text.splitlines()) < 500, f"{path}: too long"
        for needle in needles:
            assert needle in text, f"{name} lacks {needle!r}"
        for ref in KNOWLEDGE_REF.findall(text):
            ref = ref.rstrip(".")
            if "<" in ref or "*" in ref:
                continue
            assert (KNOWLEDGE / ref).exists(), f"{name}: missing knowledge/{ref}"


AUDITOR_LABELS = [
    "Auditor verdict:",
    "1. IDs exist:",
    "2. Framework steps present:",
    "3. Techniques placed:",
    "4. Framework fits Goal map:",
    "Ungrounded advice:",
    "no knowledge trace",
]


def check_agents():
    for stem in ("knowledge-auditor", "story-reviewer"):
        path = ROOT / "agents" / f"{stem}.md"
        meta = frontmatter(path)
        assert meta.get("name") == stem, path
        assert meta.get("description"), path
    auditor = ROOT / "agents/knowledge-auditor.md"
    meta = frontmatter(auditor)
    assert meta.get("model") == "sonnet"
    assert meta.get("tools") == "Read, Grep, Glob"
    body = auditor.read_text()
    for label in AUDITOR_LABELS:
        assert label in body, f"auditor lacks {label!r}"
    reviewer = ROOT / "agents/story-reviewer.md"
    meta = frontmatter(reviewer)
    assert "model" not in meta
    assert meta.get("tools") == "Read"
    body = reviewer.read_text()
    for needle in ("Reviewer score:", "rubric.md", "only `rubric.md`"):
        assert needle in body, f"reviewer lacks {needle!r}"


def check_ids():
    known = index_ids()
    questions = "".join(p.read_text() for p in (KNOWLEDGE / "questions").glob("*.md"))
    files = list((ROOT / "skills").rglob("*.md")) + list((ROOT / "agents").glob("*.md"))
    if (ROOT / "README.md").exists():
        files.append(ROOT / "README.md")
    for path in files:
        text = path.read_text()
        for found in re.findall(r"\b[FST]\d{3}\b", text):
            assert found in known, f"{path}: unknown {found}"
        for found in re.findall(r"\bR\d{2}\b", text):
            assert 1 <= int(found[1:]) <= 10, f"{path}: unknown {found}"
        for found in re.findall(r"\bQ\d{3}\b", text):
            assert f"**{found}**" in questions, f"{path}: unknown {found}"


def check_docs():
    pass


if __name__ == "__main__":
    check_manifests()
    check_skills()
    check_agents()
    check_ids()
    check_docs()
    print("OK")
