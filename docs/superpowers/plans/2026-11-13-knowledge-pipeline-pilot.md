# Knowledge Pipeline (Business Pilot) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the 11 business book cards into the first verified `knowledge/` files of story-engine (`frameworks.md`, `techniques.md`, `story-types.md`, `questions.md`, `rubric.md`, `business.md`), with stable IDs the skills and QA agents will cite.

**Architecture:** Two stdlib Python scripts do the mechanical work (index the cards; verify coverage, IDs, budget and copying). LLM agents do the judgment work from prompt files: one merges frameworks into clusters with IDs, then one agent per knowledge file writes it. A final agent traces a sample of entries back to the cards, then the user reviews.

**Tech Stack:** Python 3 stdlib only, run as `python3 -I`. Claude subagents for synthesis. Markdown.

**Spec:** `docs/superpowers/specs/2026-11-13-story-engine-design.md`

**Paths:**
- Story root: `/Users/sdavila/Desktop/Storytelling` (below: `$ROOT`)
- Books (never read by synthesis agents, only by the copy check): `$ROOT/md/`
- Pipeline workspace, local only, never pushed: `$ROOT/destilado/`
- Plugin repo: `$ROOT/story-engine/`

**Pilot cards** (all in `$ROOT/destilado/fichas-gemini/`):
1. `Stories That Stick - Kindra Hall.md`
2. `The Story Factor - Annette Simmons.md`
3. `Putting Stories to Work - Shawn Callahan.md`
4. `Better Selling Through Storytelling - John Livesay.md`
5. `Best Story Wins - Mark Edwards.md`
6. `Storytelling in Business - Janis Forman.md`
7. `Stories for Work - Gabrielle Dolan.md`
8. `The Elements of Persuasion - Richard Maxwell.md`
9. `Strategic Storytelling - Dave McKinsey.md`
10. `The Ultimate Guide to Storytelling in Business - Samir Parikh.md`
11. `Business Storytelling From Hype to Hack - Jyoti Guptara.md`

## Global Constraints

- All knowledge text in English.
- Each knowledge file at most 5,000 tokens, estimated as words × 1.35.
- Own words only. No sentence copied from a card or a book. No quotes. Examples are original, never taken from a book.
- Attribution by author surname in parentheses: "(Hall; Davis)".
- ID series: `F01…` frameworks, `S01…` story types, `T001…` techniques, `Q001…` questions, `R01…` rubric criteria. IDs are defined only in `clusters.md` (F, S, T) or in their own knowledge file (Q, R).
- Member and drop-log lines use the exact separator ` — ` (space, em dash, space) between item name and book stem.
- Book stem = card file name without `.md`, e.g. `Stories That Stick - Kindra Hall`.
- Python: stdlib only, run with `python3 -I`.
- Nothing under `$ROOT/destilado/` or `$ROOT/md/` is ever committed to the story-engine repo.

---

### Task 1: Card index

**Files:**
- Create: `$ROOT/destilado/indice.py`
- Create: `$ROOT/destilado/test_indice.py`
- Create (generated): `$ROOT/destilado/piloto/indice.md`, `$ROOT/destilado/piloto/secciones.md`

**Interfaces:**
- Produces: `python3 -I indice.py --out DIR CARD.md...` writes `DIR/indice.md` (one table row per framework: `| stem | domains | tasks | density | framework |`, then a `## By domain` list) and `DIR/secciones.md` (for each card: `# <stem>` followed by its Frameworks, Story types and Techniques sections). Functions `frontmatter(text) -> dict`, `section(text, name) -> str`, `frameworks(text) -> list[str]` (headings without the trailing chapter reference).

- [ ] **Step 1: Put the workspace under local git (never pushed)**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git init -q -b main && printf '*.log\n__pycache__/\n' > .gitignore && git add . && git commit -q -m "chore: snapshot cards and prompts" && git log --oneline
```
Expected: one commit listed.

- [ ] **Step 2: Write the failing test**

`$ROOT/destilado/test_indice.py`:
```python
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import indice

CARD = """---
title: "Stories That Stick: How Storytelling Works"
author: Kindra Hall
domains: [business, sales]   # comment
tasks: [mining, structure]
density: medium
---

## Core thesis
Thesis.

## Frameworks

### The Four Components of a Great Story (Ch. 3)
- Purpose: x

### Bridge Elements (Attention, Influence, Transformation) (Ch. 1)
- Purpose: y

## Techniques
- **Zoom**: one scene. (Ch. 3)

## Story types
- Value Story

## Questions and prompts
- Who is it for?
"""

meta = indice.frontmatter(CARD)
assert meta["title"] == "Stories That Stick: How Storytelling Works", meta
assert meta["domains"] == ["business", "sales"], meta
assert meta["density"] == "medium"
assert indice.section(CARD, "Techniques") == "- **Zoom**: one scene. (Ch. 3)"
assert indice.section(CARD, "Exercises") == ""
assert indice.frameworks(CARD) == [
    "The Four Components of a Great Story",
    "Bridge Elements (Attention, Influence, Transformation)",
], indice.frameworks(CARD)

with tempfile.TemporaryDirectory() as d:
    card = Path(d, "Stories That Stick - Kindra Hall.md")
    card.write_text(CARD)
    indice.main(["--out", d, str(card)])
    idx = Path(d, "indice.md").read_text()
    assert "| Stories That Stick - Kindra Hall | business, sales | mining, structure | medium | The Four Components of a Great Story |" in idx, idx
    assert "- business: Stories That Stick - Kindra Hall" in idx, idx
    sec = Path(d, "secciones.md").read_text()
    assert sec.startswith("# Stories That Stick - Kindra Hall"), sec
    assert "## Techniques" in sec and "## Story types" in sec and "Who is it for?" not in sec, sec

print("ok")
```

- [ ] **Step 3: Run it to verify it fails**

Run: `cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I test_indice.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'indice'`

- [ ] **Step 4: Write the implementation**

`$ROOT/destilado/indice.py`:
```python
#!/usr/bin/env python3
"""Index book cards.
Usage: python3 -I indice.py --out DIR CARD.md [CARD.md ...]
Writes DIR/indice.md (one row per framework, plus cards by domain) and
DIR/secciones.md (Frameworks, Story types and Techniques of every card)."""
import re
import sys
from pathlib import Path

SECTIONS = ["Frameworks", "Story types", "Techniques"]


def frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    meta = {}
    for line in m.group(1).splitlines() if m else []:
        key, _, value = line.partition(":")
        value = value.split(" #")[0].strip().strip('"')
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        meta[key.strip()] = value
    return meta


def section(text, name):
    m = re.search(rf"^## {re.escape(name)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def frameworks(text):
    heads = re.findall(r"^### (.+)$", section(text, "Frameworks"), re.M)
    return [re.sub(r"\s*\((Ch\.|Intro|Appendix)[^()]*\)\s*$", "", h).strip() for h in heads]


def main(argv):
    out = Path(argv[argv.index("--out") + 1])
    cards = [Path(a) for a in argv if a.endswith(".md")]
    out.mkdir(parents=True, exist_ok=True)
    rows = ["| Book | Domains | Tasks | Density | Framework |", "|---|---|---|---|---|"]
    by_domain, bundle = {}, []
    for card in sorted(cards):
        text, stem = card.read_text(), card.stem
        meta = frontmatter(text)
        doms, tasks = meta.get("domains", []), meta.get("tasks", [])
        for d in doms:
            by_domain.setdefault(d, []).append(stem)
        for fw in frameworks(text) or ["(none)"]:
            rows.append(f"| {stem} | {', '.join(doms)} | {', '.join(tasks)} | {meta.get('density', '')} | {fw} |")
        bundle.append(f"# {stem}\n\n" + "\n\n".join(f"## {s}\n\n{section(text, s)}" for s in SECTIONS))
    domains = [f"- {d}: {'; '.join(stems)}" for d, stems in sorted(by_domain.items())]
    (out / "indice.md").write_text("\n".join(rows + ["", "## By domain", ""] + domains) + "\n")
    (out / "secciones.md").write_text("\n\n".join(bundle) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I test_indice.py`
Expected: `ok`

- [ ] **Step 6: Generate the pilot index and check it**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado/fichas-gemini && python3 -I ../indice.py --out ../piloto \
 "Stories That Stick - Kindra Hall.md" "The Story Factor - Annette Simmons.md" \
 "Putting Stories to Work - Shawn Callahan.md" "Better Selling Through Storytelling - John Livesay.md" \
 "Best Story Wins - Mark Edwards.md" "Storytelling in Business - Janis Forman.md" \
 "Stories for Work - Gabrielle Dolan.md" "The Elements of Persuasion - Richard Maxwell.md" \
 "Strategic Storytelling - Dave McKinsey.md" "The Ultimate Guide to Storytelling in Business - Samir Parikh.md" \
 "Business Storytelling From Hype to Hack - Jyoti Guptara.md" \
 && grep -c '^| [A-Z]' ../piloto/indice.md && grep -c '^# ' ../piloto/secciones.md && grep '(none)' ../piloto/indice.md
```
Expected: first count = number of frameworks (roughly 60–100, header row excluded); second count = `11`; the `(none)` grep prints nothing (every card has frameworks). If a card shows `(none)`, open it and check its Frameworks heading spelling before continuing.

- [ ] **Step 7: Commit**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git add indice.py test_indice.py piloto && git commit -q -m "feat: card index for business pilot"
```

---

### Task 2: Pipeline verifier

**Files:**
- Create: `$ROOT/destilado/verificar.py`
- Create: `$ROOT/destilado/test_verificar.py`

**Interfaces:**
- Consumes: `indice.frameworks(text)` from Task 1.
- Produces: `python3 -I verificar.py --cards DIR --clusters FILE --droplog FILE [--knowledge DIR] [--books DIR] CARD.md...` prints one line per problem and exits 1 if any, else prints `ok` and exits 0. Checks: (1) coverage: every framework of every given card appears as `<name> — <stem>` in clusters or drop-log; (2) IDs: every `F\d\d`, `S\d\d`, `T\d\d\d` cited in knowledge files is defined as a `## <ID> ·` heading in clusters; (3) budget: each knowledge `.md` ≤ 5,000 estimated tokens; (4) quotes: no quoted run of 40+ characters in knowledge files; (5) copying: no 12-word run shared between a knowledge file and any card or book. Functions: `coverage(cards, ref_text) -> list[str]`, `ids(knowledge_files, clusters_text) -> list[str]`, `budget(files) -> list[str]`, `quotes(files) -> list[str]`, `copied(files, sources) -> list[str]`.

- [ ] **Step 1: Write the failing test**

`$ROOT/destilado/test_verificar.py`:
```python
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import verificar as v

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    card = d / "Book - Author.md"
    card.write_text("## Frameworks\n\n### Alpha Arc (Ch. 1)\n\n### Beta Loop (Ch. 2)\n\n## Techniques\n")
    clusters = "## F01 · Arc\n- Members: Alpha Arc — Book - Author\n\n## T001 · Zoom\n"
    droplog = "- Beta Loop — Book - Author: anecdote, not a method\n"

    assert v.coverage([card], clusters + droplog) == []
    assert v.coverage([card], clusters) == ["coverage: 'Beta Loop — Book - Author' not in clusters or drop-log"]

    good = d / "frameworks.md"
    good.write_text("## F01 · Arc\nUse with T001. Sources: (Author)\n")
    assert v.ids([good], clusters) == []
    bad = d / "business.md"
    bad.write_text("Use F02 and S03.\n")
    assert v.ids([bad], clusters) == ["ids: business.md cites F02, S03, not defined in clusters"]

    big = d / "big.md"
    big.write_text("word " * 3800)
    assert v.budget([good]) == []
    assert v.budget([big]) == ["budget: big.md ~5130 tokens > 5000"]

    quoted = d / "quoted.md"
    quoted.write_text('As one author put it, "the normal is the part most people leave out of their story".\n')
    assert v.quotes([good]) == []
    assert len(v.quotes([quoted])) == 1

    src = d / "source.md"
    src.write_text("The normal is the part most people leave out which is why their stories never stick at all.")
    copy = d / "copy.md"
    copy.write_text("Remember: the normal is the part most people leave out, which is why their stories never stick.")
    assert v.copied([good], [src]) == []
    hits = v.copied([copy], [src])
    assert len(hits) == 1 and hits[0].startswith("copied: copy.md shares 12+ words with source.md: '"), hits

print("ok")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I test_verificar.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'verificar'`

- [ ] **Step 3: Write the implementation**

`$ROOT/destilado/verificar.py`:
```python
#!/usr/bin/env python3
"""Verify the knowledge pipeline.
Usage: python3 -I verificar.py --cards DIR --clusters FILE --droplog FILE
                               [--knowledge DIR] [--books DIR] CARD.md [CARD.md ...]
Prints one line per problem and exits 1, or prints ok."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from indice import frameworks

N = 12  # words in a run that counts as copying
MAX_TOKENS = 5000
ID_RE = r"\b(?:F\d\d|S\d\d|T\d\d\d)\b"


def coverage(cards, ref_text):
    return [f"coverage: '{fw} — {c.stem}' not in clusters or drop-log"
            for c in cards for fw in frameworks(c.read_text())
            if f"{fw} — {c.stem}" not in ref_text]


def ids(files, clusters_text):
    defined = set(re.findall(rf"^## ({ID_RE}) ·", clusters_text, re.M))
    out = []
    for f in files:
        missing = sorted(set(re.findall(ID_RE, f.read_text())) - defined)
        if missing:
            out.append(f"ids: {f.name} cites {', '.join(missing)}, not defined in clusters")
    return out


def budget(files):
    out = []
    for f in files:
        tokens = round(len(f.read_text().split()) * 1.35)
        if tokens > MAX_TOKENS:
            out.append(f"budget: {f.name} ~{tokens} tokens > {MAX_TOKENS}")
    return out


def quotes(files):
    return [f"quotes: {f.name}: {m.group(0)[:60]}"
            for f in files for m in re.finditer(r"[\"“][^\"”\n]{40,}[\"”]", f.read_text())]


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def shingles(text):
    w = words(text)
    return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}


def copied(files, sources):
    # ponytail: exact 12-word runs only; paraphrase with one word changed passes. Add fuzzy matching if review finds near-copies.
    mine = {s: f for f in files for s in shingles(f.read_text())}
    out, seen = [], set()
    for src in sources:
        for s in sorted(shingles(src.read_text(errors="ignore")) & mine.keys()):
            key = (mine[s].name, src.name)
            if key not in seen:
                seen.add(key)
                out.append(f"copied: {mine[s].name} shares 12+ words with {src.name}: '{s}'")
    return out


def arg(argv, name):
    return Path(argv[argv.index(name) + 1]) if name in argv else None


def main(argv):
    cards_dir = arg(argv, "--cards")
    cards = [cards_dir / a for a in argv if a.endswith(".md") and not a.startswith("-")
             and (cards_dir / a).exists()]
    clusters = arg(argv, "--clusters").read_text()
    droplog = arg(argv, "--droplog").read_text()
    problems = coverage(cards, clusters + droplog)
    kdir = arg(argv, "--knowledge")
    if kdir:
        kfiles = sorted(kdir.rglob("*.md"))
        books = sorted(arg(argv, "--books").glob("*.md")) if arg(argv, "--books") else []
        problems += ids(kfiles, clusters) + budget(kfiles) + quotes(kfiles) + copied(kfiles, cards + books)
    print("\n".join(problems) or "ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I test_verificar.py`
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git add verificar.py test_verificar.py && git commit -q -m "feat: pipeline verifier (coverage, ids, budget, quotes, copying)"
```

---

### Task 3: Clusters (merge frameworks, assign IDs)

**Files:**
- Create: `$ROOT/destilado/prompts/clusters.md`
- Create (agent output): `$ROOT/destilado/piloto/clusters.md`, `$ROOT/destilado/piloto/drop-log.md`

**Interfaces:**
- Consumes: `piloto/indice.md`, `piloto/secciones.md` (Task 1); `verificar.py` coverage check (Task 2).
- Produces: `clusters.md` with headings `## <ID> · <Canonical name>` for F, S and T IDs, each with `- Kind:`, `- Family:`, `- Members:`, `- Core:`, `- Differences worth keeping:` lines. `drop-log.md` with lines `- <name> — <stem>: <reason>`.

- [ ] **Step 1: Write the prompt**

`$ROOT/destilado/prompts/clusters.md`:
````markdown
# Merge book-card items into clusters

You merge what 11 storytelling books teach into one list of distinct ideas, so the story-engine plugin teaches each idea once, with all its sources.

## Inputs
- INDEX: /Users/sdavila/Desktop/Storytelling/destilado/piloto/indice.md (every framework, by book stem)
- SECTIONS: /Users/sdavila/Desktop/Storytelling/destilado/piloto/secciones.md (Frameworks, Story types and Techniques of each card)
Read both completely before writing.

## Rules
- Merge items that share the same mechanism, even under different names (for example a three-part before/turn/after arc taught by several authors). Keep items apart when their steps or purpose would make a writer act differently.
- Three kinds, three ID series: frameworks (multi-step models) F01, F02…; story types S01…; techniques (single tactics) T001…
- Number in a useful reading order: within each kind, group by family.
- Family is one of: structure, finding, selection, data, delivery, persuasion, brand, review.
- Members: copy each item's name exactly as it appears in INDEX (frameworks) or as the bold label or bullet name in SECTIONS (story types, techniques), then " — " (space, em dash, space), then the book stem. Separate members with "; ".
- Every framework row in INDEX must appear in exactly one cluster's Members line, or in the drop log with a reason. A framework that is really a story type or a technique goes in that kind's cluster.
- Write Core in your own words. Never copy a sentence from SECTIONS.

## Output 1: /Users/sdavila/Desktop/Storytelling/destilado/piloto/clusters.md

```markdown
# Clusters — business pilot

## F01 · <Canonical name>
- Kind: framework
- Family: structure
- Members: <name> — <stem>; <name> — <stem>
- Core: 2–3 sentences: the shared mechanism.
- Differences worth keeping: bullets naming which author adds what, or "None".
```
Story types (S) and techniques (T) use the same fields. For techniques, Core is one sentence.

## Output 2: /Users/sdavila/Desktop/Storytelling/destilado/piloto/drop-log.md

One line per dropped framework: `- <name> — <stem>: <reason>` (reasons: too book-specific, anecdote not method, restates a cluster without adding steps).

Reply with the count of F, S and T clusters and the count of dropped items.
````

- [ ] **Step 2: Dispatch the clusters agent**

Dispatch one general-purpose subagent with the prompt: `Follow the instructions in /Users/sdavila/Desktop/Storytelling/destilado/prompts/clusters.md exactly.`
Expected reply: counts, for example "F: 18, S: 9, T: 120, dropped: 7".

- [ ] **Step 3: Run the coverage check**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I verificar.py --cards fichas-gemini --clusters piloto/clusters.md --droplog piloto/drop-log.md \
 "Stories That Stick - Kindra Hall.md" "The Story Factor - Annette Simmons.md" \
 "Putting Stories to Work - Shawn Callahan.md" "Better Selling Through Storytelling - John Livesay.md" \
 "Best Story Wins - Mark Edwards.md" "Storytelling in Business - Janis Forman.md" \
 "Stories for Work - Gabrielle Dolan.md" "The Elements of Persuasion - Richard Maxwell.md" \
 "Strategic Storytelling - Dave McKinsey.md" "The Ultimate Guide to Storytelling in Business - Samir Parikh.md" \
 "Business Storytelling From Hype to Hack - Jyoti Guptara.md"
```
Expected: `ok`. If `coverage:` lines appear, send them to the same agent (SendMessage) and ask it to place each item in a cluster or the drop log; rerun until `ok`.

- [ ] **Step 4: Commit**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git add prompts/clusters.md piloto/clusters.md piloto/drop-log.md && git commit -q -m "feat: business pilot clusters with IDs"
```

---

### Task 4: Knowledge files

**Files:**
- Create: `$ROOT/destilado/prompts/knowledge.md`
- Create (agent output): `$ROOT/story-engine/knowledge/frameworks.md`, `techniques.md`, `story-types.md`, `questions.md`, `rubric.md`, `business.md`

**Interfaces:**
- Consumes: `piloto/clusters.md` (Task 3), `piloto/secciones.md` (Task 1), the 11 pilot cards, `verificar.py` (Task 2).
- Produces (format later read by the skills and QA agents of plan 2):
  - `frameworks.md`: `## Fxx · Name` entries with **Also known as**, **Use when**, **Avoid when**, **Steps** (numbered), **Common mistakes**, **Example**, **Sources**.
  - `techniques.md`: `## <Family>` groups of `- **Txxx · Name** — how. When. (Surnames)`.
  - `story-types.md`: `## Sxx · Name` entries (**Purpose**, **Audience**, **Teller**, **Choose when**, **Shape**, **Sources**) and a final `## Selection rules` table: goal → S, F.
  - `questions.md`: `## <Purpose>` groups of `- **Q001** question — what it surfaces (Surname)`.
  - `rubric.md`: `## Rxx · Criterion` entries with **Check**, **0 / 1 / 2** descriptors, **Typical failure**, **Fix** (citing F/T IDs).
  - `business.md`: domain guide citing IDs only: `## When to use story in business`, `## Goal map` table (goal → S, F, T), `## Principles` (claim, evidence type, surnames), `## Mistakes`, `## Formats` (pitch, sales conversation, keynote, email, data presentation).

- [ ] **Step 1: Write the prompt**

`$ROOT/destilado/prompts/knowledge.md`:
````markdown
# Write one story-engine knowledge file

You write TARGET, one knowledge file of story-engine, an open-source storytelling plugin. Skills load this file before helping a user, and a QA agent checks drafts against it, so it must be precise, actionable and citable by ID.

## Inputs
- CLUSTERS: /Users/sdavila/Desktop/Storytelling/destilado/piloto/clusters.md — the only source of F, S and T IDs. Never invent an ID.
- SECTIONS: /Users/sdavila/Desktop/Storytelling/destilado/piloto/secciones.md
- CARDS: the 11 pilot cards in /Users/sdavila/Desktop/Storytelling/destilado/fichas-gemini/ listed in CLUSTERS member lines.

## Rules
- English. Own words only: never copy a sentence from a card. No quotes.
- Examples are original (invent a new short scenario); never reuse a book's example.
- Attribute by surname in parentheses: (Hall; Simmons).
- Cite F, S and T by ID exactly as in CLUSTERS.
- Hard limit: 3,700 words (about 5,000 tokens). Cut low-value items before going over.
- Be concrete: every step and technique must say what to do, not what to value.

## Targets

**frameworks.md** — one entry per F cluster, in ID order. Read CLUSTERS, then the member frameworks in CARDS for their steps.
```markdown
## F01 · Name
**Also known as:** Member name (Surname); Member name (Surname)
**Use when:** …
**Avoid when:** …
**Steps:**
1. …
**Common mistakes:** …
**Example:** 3–5 sentences, original.
**Sources:** Surname; Surname
```

**techniques.md** — every T cluster, grouped by family (`## Structure`, `## Finding`, …): `- **T001 · Name** — how to do it. When to use it. (Surname; Surname)`.

**story-types.md** — one entry per S cluster:
```markdown
## S01 · Name
**Purpose:** … **Audience:** … **Teller:** …
**Choose when:** …
**Shape:** which F to use and how the beats map.
**Sources:** …
```
End with `## Selection rules`: a table `| Goal | Story type | Framework |` (sell, raise money, align a team, recruit, build credibility, explain data, handle an objection).

**questions.md** — every mining, testing and diagnostic question from the Questions and prompts sections of CARDS, merged and deduplicated, grouped by purpose (`## Personal memory`, `## Founder`, `## Customer`, `## Objections`, `## Leadership lesson`, `## Data`, `## Diagnose a draft`). Format: `- **Q001** question — what it surfaces (Surname)`. Number continuously across groups.

**rubric.md** — 8–10 criteria a reviewer scores a story draft with, built from the Principles and Mistakes sections of CARDS. Must include: character, emotion, specific moment, concrete detail, tension or change, ending and takeaway, fit to the brief's objective (what the audience should think, feel, know or do), and audience fit.
```markdown
## R01 · Criterion
**Check:** what to look at in the draft.
**0:** … **1:** … **2:** …
**Typical failure:** …
**Fix:** what to change, citing F/T IDs.
```

**business.md** — the domain guide. Do not re-explain frameworks: cite IDs.
```markdown
## When to use story in business
## Goal map
| Goal | Story type | Framework | Key techniques |
## Principles
- Claim. Evidence: study | author experience | anecdote. (Surname)
## Mistakes
- Mistake → fix (IDs). (Surname)
## Formats
### Pitch  ### Sales conversation  ### Keynote  ### Email  ### Data presentation
```

Write the file to /Users/sdavila/Desktop/Storytelling/story-engine/knowledge/TARGET. Reply with the path and word count.
````

- [ ] **Step 2: Dispatch six agents in parallel**

Dispatch six general-purpose subagents in one message, one per target, each with the prompt: `Follow /Users/sdavila/Desktop/Storytelling/destilado/prompts/knowledge.md exactly. TARGET = <file>` for `frameworks.md`, `techniques.md`, `story-types.md`, `questions.md`, `rubric.md`, `business.md`.
Expected: six replies with paths and word counts, each under 3,700 words.

- [ ] **Step 3: Run the full verifier**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && python3 -I verificar.py --cards fichas-gemini --clusters piloto/clusters.md --droplog piloto/drop-log.md \
 --knowledge ../story-engine/knowledge --books ../md \
 "Stories That Stick - Kindra Hall.md" "The Story Factor - Annette Simmons.md" \
 "Putting Stories to Work - Shawn Callahan.md" "Better Selling Through Storytelling - John Livesay.md" \
 "Best Story Wins - Mark Edwards.md" "Storytelling in Business - Janis Forman.md" \
 "Stories for Work - Gabrielle Dolan.md" "The Elements of Persuasion - Richard Maxwell.md" \
 "Strategic Storytelling - Dave McKinsey.md" "The Ultimate Guide to Storytelling in Business - Samir Parikh.md" \
 "Business Storytelling From Hype to Hack - Jyoti Guptara.md"
```
Expected: `ok`. For each problem line, SendMessage the agent that wrote that file with the exact line and ask for a fix; rerun until `ok`. At most 2 fix rounds; anything left goes to Task 5 as a known issue.

- [ ] **Step 4: Commit the knowledge files to the plugin repo**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git add prompts/knowledge.md && git commit -q -m "feat: knowledge-file prompt"
cd /Users/sdavila/Desktop/Storytelling/story-engine && git add knowledge && git commit -q -m "feat: business pilot knowledge files

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Fidelity check and user review

**Files:**
- Create: `$ROOT/destilado/prompts/fidelidad.md`
- Create (agent output): `$ROOT/destilado/piloto/fidelidad.md`

**Interfaces:**
- Consumes: knowledge files (Task 4), `clusters.md` (Task 3), the 11 cards.
- Produces: `fidelidad.md`, a table of sampled entries with verdict `supported | partly | unsupported` and the card evidence. Gate for extending the pipeline to all 55 books.

- [ ] **Step 1: Write the prompt**

`$ROOT/destilado/prompts/fidelidad.md`:
````markdown
# Fidelity check of story-engine knowledge files

You did not write these files. Check that they say only what the source cards support.

Inputs: /Users/sdavila/Desktop/Storytelling/story-engine/knowledge/*.md, /Users/sdavila/Desktop/Storytelling/destilado/piloto/clusters.md, and the cards in /Users/sdavila/Desktop/Storytelling/destilado/fichas-gemini/ named in the clusters' Members lines.

1. Sample 20 entries: 6 from frameworks.md, 4 from story-types.md, 4 from techniques.md, 3 from business.md (principles), 3 from rubric.md.
2. For each, find its sources' card sections and decide: supported (every step or claim appears in at least one source card), partly (some step or claim has no source), unsupported.
3. Also flag any example that retells a book's example instead of an original one.

Write /Users/sdavila/Desktop/Storytelling/destilado/piloto/fidelidad.md:

| ID / entry | File | Verdict | Unsupported part | Card evidence (stem, section) |

End with a one-line total: supported / partly / unsupported. Reply with that line.
````

- [ ] **Step 2: Dispatch the fidelity agent**

Dispatch one general-purpose subagent: `Follow /Users/sdavila/Desktop/Storytelling/destilado/prompts/fidelidad.md exactly.`
Expected: a total line. Pass threshold: at least 18 of 20 supported and 0 unsupported. Below that, fix the flagged entries (SendMessage the writing agents from Task 4 or edit directly), rerun `verificar.py`, and recheck only the failed entries.

- [ ] **Step 3: Commit**

```bash
cd /Users/sdavila/Desktop/Storytelling/destilado && git add prompts/fidelidad.md piloto/fidelidad.md && git commit -q -m "chore: fidelity check of business pilot"
cd /Users/sdavila/Desktop/Storytelling/story-engine && git add knowledge && git commit -q -m "fix: knowledge corrections from fidelity check

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || true
```

- [ ] **Step 4: User review gate**

Show the user: cluster counts, verifier result, fidelity total, and links to `knowledge/frameworks.md` and `knowledge/business.md`. Ask for approval to (a) extend the pipeline to all 55 cards (rerun Tasks 1–5 with every card and the remaining domain files `brand.md`, `personal.md`, `craft.md`, `data.md`, `science.md`), and (b) start plan 2 (skills, QA agents, evals, publication). Do not proceed without that approval.
