# Pre-Scale Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the knowledge pipeline safe to run on all 55 book cards. Every gap the pilot's final review found must fail loudly, not pass silently.

**Architecture:** The same two stdlib scripts (`indice.py`, `verificar.py`) gain the missing checks. One new script, `fuentes.py`, collects the exact card text behind each cluster, so writers and fidelity agents work from source text, not from cluster summaries. Clustering becomes map-reduce: 5 lot agents of 11 cards each, then one merge agent per kind. Prompts move from `piloto/` to a run directory given as `RUN`.

**Tech Stack:** Python 3 stdlib only, run as `python3 -I`. Markdown prompts for Claude subagents.

**Spec:** `docs/superpowers/specs/2026-11-13-story-engine-design.md`. Inputs for this plan: the final review in `.superpowers/sdd/2026-11-13-knowledge-pipeline-pilot/progress.md` (entry "Final review") and the list in `docs/superpowers/HANDOFF.md`.

**Paths:**
- `$ROOT` = `/Users/sdavila/Desktop/Storytelling`
- Pipeline workspace (local only, never pushed): `$ROOT/destilado/`. Tasks 1–6 commit there.
- Plugin repo: `$ROOT/story-engine/`. Task 7 commits there.
- Scale run directory (used by the prompts, created in the scale run, not here): `$ROOT/destilado/escala/`

## Global Constraints

- Python stdlib only. Run every script and test as `python3 -I <file>`. Tests are plain `assert` scripts that print `ok`.
- ID widths for the scale run: `F001`, `S001`, `T001` (3 digits), `Q001` (3 digits), `R01` (2 digits).
- Member and drop-log lines use the exact separator ` — ` (space, em dash, space) between item name and book stem.
- Knowledge files: English, own words only, no quotes, original examples, attribution by surname in parentheses, at most 5,000 tokens each (words × 1.35).
- Domain guides: one per domain, in `knowledge/domains/<domain>.md`, for all 10 domains: business, sales, leadership, marketing, brand, personal, oral, craft, data, science (decided by Sebastián 2026-11-17).
- Nothing is published. No push, no public repo, no remote changes.
- Never modify `fichas-gemini/` or `../md/`.

## File map

- Modify `destilado/indice.py`: `heading()` (chapter strip, shared), `items()` (story-type and technique names), domain and question bundles.
- Modify `destilado/verificar.py`: ID width, one-home check, path labels, coverage of all three kinds, `--allow`, `--books` required.
- Create `destilado/fuentes.py`: card text per cluster, one bundle per kind and family.
- Modify the tests `destilado/test_indice.py` and `destilado/test_verificar.py`, and create `destilado/test_fuentes.py`.
- Create `destilado/prompts/lote.md` and `destilado/prompts/fusion.md`. Delete `destilado/prompts/clusters.md`. Rewrite `destilado/prompts/knowledge.md` and `destilado/prompts/fidelidad.md`.
- Modify `story-engine/docs/superpowers/specs/2026-11-13-story-engine-design.md`, `story-engine/docs/superpowers/HANDOFF.md`, and the ledger.

---

### Task 1: indice.py, shared name parsing and bundles

**Files:**
- Modify: `destilado/indice.py`
- Test: `destilado/test_indice.py`

**Interfaces:**
- Produces: `heading(h: str) -> str` (removes a trailing chapter reference). `items(text: str) -> list[str]` (bold bullet names in the Story types and Techniques sections, without group labels). `main` also writes `DIR/dominios/<domain>.md` (Principles and Mistakes of every card tagged with that domain) and `DIR/preguntas.md` (Questions and prompts of every card). `frameworks(text)` keeps its signature.

- [ ] **Step 1: Write the failing tests.** Add before `print("ok")` in `test_indice.py`:

```python
assert indice.heading('Scenes (Part II, "A Recipe")') == "Scenes"
assert indice.heading("Kano Model (JTBD)") == "Kano Model (JTBD)"

ITEMS = """## Story types
The book proposes **Four Stories**:
- **Value Story** (Ch. 4):
  - *Purpose*: sell.
- **Founder Story:** origin.

## Techniques
- **Group label**:
  - **Zoom In**: one scene. (Ch. 3)
  - **Open Late**: start mid-action.
- **Plain Tip**: do it.

## Quotes
- **Not an item**: quote.
"""
assert indice.items(ITEMS) == ["Value Story", "Founder Story", "Zoom In", "Open Late", "Plain Tip"], indice.items(ITEMS)

with tempfile.TemporaryDirectory() as d:
    c1 = Path(d, "A - One.md")
    c1.write_text("---\ndomains: [sales, oral]\n---\n\n## Principles\n- P1\n\n## Mistakes\n- M1\n\n## Questions and prompts\n- Q1\n")
    c2 = Path(d, "B - Two.md")
    c2.write_text("---\ndomains: [sales]\n---\n\n## Principles\n- P2\n\n## Mistakes\n- M2\n\n## Questions and prompts\n- Q2\n")
    out = Path(d, "out")
    indice.main(["--out", str(out), str(c1), str(c2)])
    sales = (out / "dominios" / "sales.md").read_text()
    assert "# A - One" in sales and "# B - Two" in sales and "- P2" in sales and "- M1" in sales, sales
    assert "# B - Two" not in (out / "dominios" / "oral.md").read_text()
    q = (out / "preguntas.md").read_text()
    assert "- Q1" in q and "- Q2" in q and "- P1" not in q, q
```

- [ ] **Step 2: Run and confirm failure.** Run `cd $ROOT/destilado && python3 -I test_indice.py`. Expected: `AttributeError: module 'indice' has no attribute 'heading'`.

- [ ] **Step 3: Implement.** In `indice.py`, replace `frameworks()` and add the new functions:

```python
def heading(h):
    """Framework heading without its trailing chapter reference."""
    return re.sub(r"\s*\((Ch\.|Intro|Appendix|Part [IVXLC\d]+)[^()]*\)\s*$", "", h).strip()


def frameworks(text):
    return [heading(h) for h in re.findall(r"^### (.+)$", section(text, "Frameworks"), re.M)]


BULLET = re.compile(r"(\s*)- \*\*(.+?)\*\*")


def items(text):
    """Bold bullet names in Story types and Techniques. A bullet followed by a deeper bold bullet is a group label, not an item."""
    out = []
    for name in ("Story types", "Techniques"):
        lines = section(text, name).splitlines()
        for i, line in enumerate(lines):
            m = BULLET.match(line)
            if not m:
                continue
            nxt = BULLET.match(lines[i + 1]) if i + 1 < len(lines) else None
            if nxt and len(nxt.group(1)) > len(m.group(1)):
                continue
            out.append(m.group(2).strip().rstrip(":").strip())
    return out
```

In `main`, after `bundle.append(...)`, collect the domain and question bundles, and write them after `secciones.md`:

```python
        pm = "\n\n".join(f"## {s}\n\n{section(text, s)}" for s in ("Principles", "Mistakes"))
        for d in doms:
            domain_bundle.setdefault(d, []).append(f"# {stem}\n\n{pm}")
        questions.append(f"# {stem}\n\n{section(text, 'Questions and prompts')}")
```

```python
    (out / "dominios").mkdir(exist_ok=True)
    for d, parts in domain_bundle.items():
        (out / "dominios" / f"{d}.md").write_text("\n\n".join(parts) + "\n")
    (out / "preguntas.md").write_text("\n\n".join(questions) + "\n")
```

Initialize them next to `by_domain`: `by_domain, bundle, domain_bundle, questions = {}, [], {}, []`. Update the module docstring to list the new outputs.

- [ ] **Step 4: Run tests.** Run `python3 -I test_indice.py && python3 -I test_verificar.py`. Expected: `ok` twice.

- [ ] **Step 5: Commit.**

```bash
cd $ROOT/destilado && git add indice.py test_indice.py && git commit -m "feat: indice item names, domain and question bundles"
```

---

### Task 2: verificar.py, IDs, one home per ID, coverage of all kinds

**Files:**
- Modify: `destilado/verificar.py`
- Test: `destilado/test_verificar.py`

**Interfaces:**
- Consumes: `indice.frameworks`, `indice.items` (Task 1).
- Produces: `ids(files, clusters_text)` now reports (a) cited IDs of any width not defined in clusters and (b) every cluster ID whose number of definition lines across knowledge files is not exactly 1. `coverage(cards, ref_text)` checks frameworks, story types and techniques. Messages name files by their path relative to `--knowledge` (`frameworks/data.md`), through the module-level `BASE`.

- [ ] **Step 1: Write the failing tests.** In `test_verificar.py`, replace the block from `card.write_text(` down to (but not including) `big = d / "big.md"` with:

```python
    card.write_text("## Frameworks\n\n### Alpha Arc (Ch. 1)\n\n### Beta Loop (Ch. 2)\n\n"
                    "## Story types\n- **Value Story** (Ch. 4):\n  - *Purpose*: sell.\n\n"
                    "## Techniques\n- **Zoom In**: one scene.\n")
    clusters = ("## F001 · Arc\n- Members: Alpha Arc — Book - Author\n\n"
                "## S001 · Value\n- Members: Value Story — Book - Author\n\n"
                "## T001 · Zoom\n- Members: Zoom In — Book - Author\n")
    droplog = "- Beta Loop — Book - Author: anecdote, not a method\n"

    assert v.coverage([card], clusters + droplog) == []
    assert v.coverage([card], clusters) == ["coverage: 'Beta Loop — Book - Author' not in clusters or drop-log"]
    no_tech = clusters.replace("Zoom In — Book - Author", "")
    assert v.coverage([card], no_tech + droplog) == ["coverage: 'Zoom In — Book - Author' not in clusters or drop-log"]

    good = d / "frameworks.md"
    good.write_text("## F001 · Arc\nUse with T001.\n\n## S001 · Value\nShape: F001.\n\n- **T001 · Zoom** — one scene.\n")
    assert v.ids([good], clusters) == []
    bad = d / "business.md"
    bad.write_text("Use F02, F1000 and S003.\n")
    assert v.ids([good, bad], clusters) == ["ids: business.md cites F02, F1000, S003, not defined in clusters"]
    twice = d / "twice.md"
    twice.write_text("## F001 · Arc again\n")
    assert v.ids([good, twice], clusters) == ["ids: F001 defined in 2 knowledge entries (frameworks.md, twice.md)"]
    partial = d / "partial.md"
    partial.write_text("## F001 · Arc\n")
    assert v.ids([partial], clusters) == ["ids: S001 defined in 0 knowledge entries (none)",
                                          "ids: T001 defined in 0 knowledge entries (none)"]
    v.BASE = d
    sub = d / "frameworks"
    sub.mkdir()
    (sub / "data.md").write_text("Cites F999.\n")
    assert v.ids([good, sub / "data.md"], clusters) == ["ids: frameworks/data.md cites F999, not defined in clusters"]
    v.BASE = None
```

In the CLI block further down, change `cl.write_text("## F01 · Arc\n...` so the cluster ID is `F001`.

- [ ] **Step 2: Run and confirm failure.** Run `python3 -I test_verificar.py`. Expected: an `AssertionError` on the `no_tech` coverage line, because techniques are not checked yet.

- [ ] **Step 3: Implement.** In `verificar.py`:

```python
from indice import frameworks, items

ID_RE = r"\b[FST]\d+\b"  # any width: F01 or F1000 shows up as undefined instead of being skipped
DEF_RE = r"^(?:## |- \*\*)([FST]\d{3}) ·"  # where a knowledge file defines an entry
BASE = None  # main sets this to --knowledge so messages say frameworks/data.md, not data.md


def label(f):
    return f.relative_to(BASE).as_posix() if BASE and f.is_relative_to(BASE) else f.name
```

In `coverage()`, change `for fw in frameworks(c.read_text())` to `for fw in frameworks(c.read_text()) + items(c.read_text())`. Read the card text once:

```python
    out = []
    for c in cards:
        text = c.read_text()
        out += [f"coverage: '{fw} — {c.stem}' not in clusters or drop-log"
                for fw in frameworks(text) + items(text) if f"{fw} — {c.stem}" not in covered]
    return out
```

Replace `ids()`:

```python
def ids(files, clusters_text):
    defined = set(re.findall(r"^## ([FST]\d{3}) ·", clusters_text, re.M))
    out, homes = [], {}
    for f in files:
        text = f.read_text()
        missing = sorted(set(re.findall(ID_RE, text)) - defined)
        if missing:
            out.append(f"ids: {label(f)} cites {', '.join(missing)}, not defined in clusters")
        for i in re.findall(DEF_RE, text, re.M):
            homes.setdefault(i, []).append(label(f))
    for i in sorted(defined):
        where = homes.get(i, [])
        if len(where) != 1:
            out.append(f"ids: {i} defined in {len(where)} knowledge entries ({', '.join(where) or 'none'})")
    return out
```

In `budget()`, `quotes()` and `copied()`, replace `f.name` and `mine[s].name` with `label(f)` and `label(mine[s])`. In `main`, after reading `--knowledge`, set `global BASE` and then `BASE = Path(opts["--knowledge"])`. Declare `global BASE` as the first line of `main`.

- [ ] **Step 4: Run tests.** Run `python3 -I test_verificar.py && python3 -I test_indice.py`. Expected: `ok` twice.

- [ ] **Step 5: Commit.**

```bash
git add verificar.py test_verificar.py && git commit -m "feat: verifier checks ID width, one home per ID, all three kinds"
```

---

### Task 3: verificar.py, allowlist and required books

**Files:**
- Modify: `destilado/verificar.py`
- Test: `destilado/test_verificar.py`

**Interfaces:**
- Produces: CLI flag `--allow FILE`, where each line is one exact problem line to accept. With `--knowledge`, `--books` is required (exit 2 without it). A missing `--allow` file exits 2.

- [ ] **Step 1: Write the failing tests.** In the CLI block, after the `out.getvalue()` assert, add:

```python
    kdir = d / "k"
    kdir.mkdir()
    (kdir / "f.md").write_text('## F001 · Arc\nSay "this is a long original example sentence for the check".\n')
    bdir = d / "books"
    bdir.mkdir()
    (bdir / "Book.md").write_text("unrelated text")
    kb = base + ["Book - Author.md", "--knowledge", str(kdir)]
    with contextlib.redirect_stdout(io.StringIO()):
        assert v.main(kb) == 2  # --books missing
        assert v.main(kb + ["--books", str(bdir)]) == 1  # one quote flag
        allow = d / "allow.md"
        allow.write_text('quotes: f.md: "this is a long original example sentence for the check"\n')
        assert v.main(kb + ["--books", str(bdir), "--allow", str(allow)]) == 0
        assert v.main(kb + ["--books", str(bdir), "--allow", str(d / "nope.md")]) == 2
```

- [ ] **Step 2: Run and confirm failure.** Run `python3 -I test_verificar.py`. Expected: `AssertionError` on `v.main(kb) == 2`.

- [ ] **Step 3: Implement.** Add `"--allow"` to `FLAGS`. In `main`, after the required-flags check:

```python
    if "--knowledge" in opts and "--books" not in opts:
        print("error: --books is required with --knowledge (the copy check against full books)")
        return 2
    allowed = set()
    if "--allow" in opts:
        if not Path(opts["--allow"]).is_file():
            print(f"error: --allow file not found: {opts['--allow']}")
            return 2
        allowed = set(Path(opts["--allow"]).read_text().splitlines())
```

Before the `print(f"checked: ...")` line, add `problems = [p for p in problems if p not in allowed]`. Update the usage docstring with `[--allow FILE]` and the `--books` rule.

- [ ] **Step 4: Run tests.** Run `python3 -I test_verificar.py`. Expected: `ok`.

- [ ] **Step 5: Re-check the pilot with the new rules (no commit of outputs).** Run:

```bash
cd $ROOT/destilado && python3 -I verificar.py --cards fichas-gemini --clusters piloto/clusters.md --droplog piloto/drop-log.md --knowledge ../story-engine/knowledge --books ../md "Stories That Stick - Kindra Hall.md"
```

Expected: exit 1. You should see `ids:` lines saying the pilot's 2-digit IDs (`F01`, …) are not defined, because the pilot clusters use `## F01 ·`, which the 3-digit rule no longer accepts. This is the expected sign that the width check works. The pilot files are replaced in the scale run. Paste the first 5 lines into the task report.

- [ ] **Step 6: Commit.**

```bash
git add verificar.py test_verificar.py && git commit -m "feat: verifier allowlist, books required with knowledge"
```

---

### Task 4: fuentes.py, card text behind each cluster

**Files:**
- Create: `destilado/fuentes.py`
- Test: `destilado/test_fuentes.py`

**Interfaces:**
- Consumes: `indice.section`, `indice.heading`, `indice.BULLET` (Task 1).
- Produces: `python3 -I fuentes.py --cards DIR --clusters FILE --out DIR`. It writes `DIR/<kind>-<family>.md` (kind slug: `framework`, `story-type`, `technique`). Each file holds, per cluster, the cluster heading, then `### <member> — <stem>` and the member's card text. It prints `missing: <member> — <stem>` for each member not found, and exits 1 if any are missing. Functions: `clusters(text) -> list[tuple[str, str, str, list[tuple[str, str]]]]` (heading, kind, family, members), `excerpt(card_text, name) -> str | None`.

- [ ] **Step 1: Write the failing test** `test_fuentes.py`:

```python
import contextlib, io, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fuentes

CARD = """## Frameworks

### Alpha Arc (Ch. 1)
- Step one.
- Step two.

### Beta Loop (Ch. 2)
- Other.

## Story types
- **Value Story** (Ch. 4):
  - *Purpose*: sell.
- **Founder Story**: origin.

## Techniques
- **Zoom In**: one scene.
  - detail line
- **Open Late**: mid-action.
"""

assert fuentes.excerpt(CARD, "Alpha Arc") == "### Alpha Arc (Ch. 1)\n- Step one.\n- Step two."
assert fuentes.excerpt(CARD, "Value Story") == "- **Value Story** (Ch. 4):\n  - *Purpose*: sell."
assert fuentes.excerpt(CARD, "Zoom In") == "- **Zoom In**: one scene.\n  - detail line"
assert fuentes.excerpt(CARD, "Nope") is None

CL = """# Clusters

## F001 · Arc
- Kind: framework
- Family: structure
- Members: Alpha Arc — Book - Author
- Core: x

## T001 · Zoom
- Kind: technique
- Family: finding
- Members: Zoom In — Book - Author; Ghost — Book - Author
- Core: y
"""
assert fuentes.clusters(CL) == [
    ("## F001 · Arc", "framework", "structure", [("Alpha Arc", "Book - Author")]),
    ("## T001 · Zoom", "technique", "finding", [("Zoom In", "Book - Author"), ("Ghost", "Book - Author")]),
]

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "cards").mkdir()
    (d / "cards" / "Book - Author.md").write_text(CARD)
    (d / "cl.md").write_text(CL)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = fuentes.main(["--cards", str(d / "cards"), "--clusters", str(d / "cl.md"), "--out", str(d / "out")])
    assert code == 1 and out.getvalue() == "missing: Ghost — Book - Author\n", out.getvalue()
    fw = (d / "out" / "framework-structure.md").read_text()
    assert "## F001 · Arc" in fw and "### Alpha Arc — Book - Author" in fw and "- Step two." in fw, fw
    assert "- **Zoom In**: one scene." in (d / "out" / "technique-finding.md").read_text()

print("ok")
```

- [ ] **Step 2: Run and confirm failure.** Run `python3 -I test_fuentes.py`. Expected: `ModuleNotFoundError: No module named 'fuentes'`.

- [ ] **Step 3: Implement** `fuentes.py`:

```python
#!/usr/bin/env python3
"""Collect the card text behind each cluster, one bundle per kind and family.
Usage: python3 -I fuentes.py --cards DIR --clusters FILE --out DIR
Writes DIR/<kind>-<family>.md. Prints 'missing: <member> — <stem>' per member
not found in its card. Exit 0 = all found, 1 = some missing."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from indice import BULLET, heading, section


def clusters(text):
    out = []
    for block in re.split(r"^(?=## [FST]\d+ ·)", text, flags=re.M)[1:]:
        field = lambda k: (re.search(rf"^- {k}: (.+)$", block, re.M) or [None, ""])[1].strip()
        members = [tuple(m.rsplit(" — ", 1)) for m in field("Members").split("; ") if " — " in m]
        out.append((block.splitlines()[0].strip(), field("Kind"), field("Family"), members))
    return out


def excerpt(card_text, name):
    for block in re.split(r"^(?=### )", section(card_text, "Frameworks"), flags=re.M):
        if block.startswith("### ") and heading(block.splitlines()[0][4:]) == name:
            return block.strip()
    for sec in ("Story types", "Techniques"):
        lines = section(card_text, sec).splitlines()
        for i, line in enumerate(lines):
            m = BULLET.match(line)
            if m and m.group(2).strip().rstrip(":").strip() == name:
                depth, end = len(m.group(1)), i + 1
                while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > depth):
                    end += 1
                return "\n".join(lines[i:end]).rstrip()
    return None


def main(argv):
    opts = dict(zip(argv[::2], argv[1::2]))
    cards, out = Path(opts["--cards"]), Path(opts["--out"])
    out.mkdir(parents=True, exist_ok=True)
    bundles, missing = {}, []
    for head, kind, family, members in clusters(Path(opts["--clusters"]).read_text()):
        parts = [head]
        for name, stem in members:
            card = cards / f"{stem}.md"
            text = excerpt(card.read_text(), name) if card.is_file() else None
            if text is None:
                missing.append(f"missing: {name} — {stem}")
            else:
                parts.append(f"### {name} — {stem}\n\n{text}")
        bundles.setdefault(f"{kind.replace(' ', '-')}-{family}", []).append("\n\n".join(parts))
    for key, blocks in bundles.items():
        (out / f"{key}.md").write_text("\n\n".join(blocks) + "\n")
    print("\n".join(missing), end="\n" if missing else "")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests.** Run `python3 -I test_fuentes.py && python3 -I test_indice.py && python3 -I test_verificar.py`. Expected: `ok` three times.

- [ ] **Step 5: Dry run on the pilot clusters.** Run:

```bash
cd $ROOT/destilado && python3 -I fuentes.py --cards fichas-gemini --clusters piloto/clusters.md --out "$TMPDIR/fuentes-piloto"; echo "exit $?"; ls "$TMPDIR/fuentes-piloto" | wc -l; wc -w "$TMPDIR"/fuentes-piloto/*.md | tail -1
```

Expected: about 20 bundle files. The run may print `missing:` lines. For each one, decide whether the cause is a bug in `excerpt` (fix it and add a test case) or a member name the pilot cluster agent copied inexactly (expected; the reviewer counted 3 parent bullets). Report the missing count and the causes in the task report. Fewer than 10 missing, all from inexact names, passes.

- [ ] **Step 6: Commit.**

```bash
git add fuentes.py test_fuentes.py && git commit -m "feat: fuentes.py bundles the card text behind each cluster"
```

---

### Task 5: Clustering prompts, map and merge

**Files:**
- Create: `destilado/prompts/lote.md`, `destilado/prompts/fusion.md`
- Delete: `destilado/prompts/clusters.md`

**Interfaces:**
- Consumes: `RUN/lotes/<N>/secciones.md` (from `indice.py --out RUN/lotes/<N> <11 cards>`).
- Produces: per lot, `RUN/lotes/<N>/F.md`, `S.md`, `T.md` and `drop-log.md` with provisional IDs `<N>-F01`. Per kind, `RUN/clusters-<K>.md` (final 3-digit IDs) and `RUN/drop-<K>.md`. The controller concatenates these into `RUN/clusters.md` and `RUN/drop-log.md`.

- [ ] **Step 1: Write** `prompts/lote.md`:

````markdown
# Cluster one lot of book cards

You merge what one lot of storytelling book cards teaches into candidate clusters. A merge agent later combines all lots, so stay inside your lot and never assign final IDs.

## Inputs (the controller fills in RUN and N)
- SECTIONS: RUN/lotes/N/secciones.md (Frameworks, Story types and Techniques of each card in the lot). Read it completely before writing.

## Rules
- Merge items that share the same mechanism, even under different names. Keep items apart when their steps or purpose would make a writer act differently.
- Kinds: framework (multi-step model), story type, technique (single tactic). A framework heading that is really a story type or a technique goes in that kind.
- Family is one of: structure, finding, selection, data, delivery, persuasion, brand, review.
- Provisional IDs: N-F01, N-S01, N-T01 (two digits after the kind letter, prefixed with the lot number).
- Members: copy each item's name exactly. For a framework, use the `###` heading without its trailing chapter reference in parentheses. For a story type or technique, use the bold text of its bullet, without a trailing colon. Then write " — " (space, em dash, space), then the book stem (the `# ` heading above it in SECTIONS). Separate members with "; ".
- Every framework heading and every story-type or technique bullet in SECTIONS must appear in exactly one Members line, or in the drop log with a reason. A bullet that only labels a group of deeper bullets is not an item: list its children instead.
- Write Core in your own words. Never copy a sentence from SECTIONS.

## Outputs
Three files, RUN/lotes/N/F.md, RUN/lotes/N/S.md and RUN/lotes/N/T.md, each with entries in this format:

```markdown
## N-F01 · <Canonical name>
- Kind: framework
- Family: structure
- Members: <name> — <stem>; <name> — <stem>
- Core: 2–3 sentences: the shared mechanism (1 sentence for techniques).
- Differences worth keeping: bullets naming which author adds what, or "None".
```

RUN/lotes/N/drop-log.md: one line per dropped item, `- <name> — <stem>: <reason>`. Reasons: too book-specific, anecdote not method, restates a cluster without adding steps.

Reply with the counts of F, S and T entries and the number of dropped items.
````

- [ ] **Step 2: Write** `prompts/fusion.md`:

````markdown
# Merge the lots for one kind

You merge the candidate clusters of every lot for one kind (K = F, S or T) into the final clusters of story-engine.

## Inputs (the controller fills in RUN and K)
- RUN/lotes/*/K.md: the candidate clusters of every lot for this kind. Read all of them before writing.

## Rules
- Merge candidates from different lots that share the same mechanism. Keep them apart when their steps or purpose would make a writer act differently.
- Carry every member over exactly as written. Never rename, reword or drop a member. A merged cluster's Members line is the union of its candidates' members.
- You may move a candidate into the drop log only if it restates another cluster without adding steps. Then write each of its members as a separate drop-log line.
- Final IDs have three digits: F001, S001 or T001. Number in reading order, grouped by family (structure, finding, selection, data, delivery, persuasion, brand, review).
- Rewrite Core in your own words for the merged cluster. Merge the "Differences worth keeping" bullets.
- Family: when candidates disagree, pick the family where a writer would look for the item.

## Outputs
- RUN/clusters-K.md: entries in the candidate format (`## F001 · Name`, then the Kind, Family, Members, Core and Differences lines).
- RUN/drop-K.md: drop-log lines (`- <name> — <stem>: <reason>`), or an empty file.

Reply with the number of input candidates, the number of output clusters and the number of dropped members.
````

- [ ] **Step 3: Delete the old prompt and check for pilot leftovers.** Run:

```bash
cd $ROOT/destilado && git rm -q prompts/clusters.md && grep -nE "piloto|11 books|business pilot|F01\b|/Users/" prompts/lote.md prompts/fusion.md
```

Expected: no output, so grep exits 1.

- [ ] **Step 4: Commit.**

```bash
git add prompts/lote.md prompts/fusion.md && git commit -m "feat: map-reduce clustering prompts for the 55-card run"
```

---

### Task 6: Writer and fidelity prompts

**Files:**
- Modify (rewrite): `destilado/prompts/knowledge.md`, `destilado/prompts/fidelidad.md`

**Interfaces:**
- Consumes: `RUN/clusters.md`, `RUN/fuentes/<kind>-<family>.md` (Task 4), `RUN/dominios/<domain>.md` and `RUN/preguntas.md` (Task 1).
- Produces: the knowledge layout under `story-engine/knowledge/`, which is `frameworks/<family>.md`, `story-types/<family>.md`, `techniques/<family>.md`, `questions/<group>.md`, `domains/<domain>.md` and `rubric.md`. It also produces the fidelity report `RUN/fidelidad.md`.

- [ ] **Step 1: Rewrite** `prompts/knowledge.md` with this full text:

````markdown
# Write one story-engine knowledge file

You write TARGET, one knowledge file of story-engine, a storytelling plugin. Skills load this file before helping a user, and a QA agent checks drafts against it, so it must be precise, actionable and citable by ID.

## Inputs (the controller fills in RUN and TARGET)
- CLUSTERS: RUN/clusters.md. It is the only source of F, S and T IDs. Never invent an ID.
- SOURCES: the bundle named for your TARGET below. It holds the card text behind every cluster you write. Write only from SOURCES, never from the cluster summary alone.

## Rules
- English. Own words only: never copy a sentence from SOURCES. No quotes.
- Every step, claim and rule must trace to SOURCES. If no member card supports a step, drop the step. Do not add plausible steps of your own.
- Examples are original: a new short scenario with different people, setting and product. Never retell a book's example with new nouns.
- Attribute by surname in parentheses: (Hall; Simmons).
- Cite F, S and T by ID exactly as in CLUSTERS (three digits: F001).
- When an entry relates to an F, S or T in another file, cite the ID; do not repeat its content.
- Write every cluster assigned to your TARGET. Never drop one. Hard limit: 3,700 words (about 5,000 tokens). If you are over, shorten entries. If you are still over, stop and tell the controller how many words you need; the controller splits the file.
- Be concrete: every step and technique must say what to do, not what to value.

## Targets

**frameworks/<family>.md**: SOURCES = RUN/fuentes/framework-<family>.md. One entry per F cluster whose Family is <family>, in ID order. Start with `# Frameworks — <family>`.
```markdown
## F001 · Name
**Also known as:** Member name (Surname); Member name (Surname)
**Use when:** …
**Avoid when:** …
**Steps:**
1. …
**Common mistakes:** …
**Example:** 3–5 sentences, original.
**Sources:** Surname; Surname
```

**story-types/<family>.md**: SOURCES = RUN/fuentes/story-type-<family>.md. One entry per S cluster of that family. Start with `# Story types — <family>`.
```markdown
## S001 · Name
**Purpose:** … **Audience:** … **Teller:** …
**Choose when:** …
**Shape:** which F to use and how the beats map.
**Sources:** …
```

**techniques/<family>.md**: SOURCES = RUN/fuentes/technique-<family>.md. Every T cluster of that family. Start with `# Techniques — <family>`. One line each: `- **T001 · Name** — how to do it. When to use it. (Surname; Surname)`.

**questions/<group>.md**: SOURCES = RUN/preguntas.md. One writer writes all question files in one run. Merge and deduplicate every mining, testing and diagnostic question. Choose 6–12 groups by purpose (for example personal-memory, founder, customer, objections, leadership-lesson, data, diagnose-draft, character, scene). Write one file per group, starting with `# Questions — <group>`. Format: `- **Q001** question — what it surfaces (Surname)`. Number continuously across all groups.

**rubric.md**: SOURCES = every RUN/dominios/*.md. 8–10 criteria a reviewer scores a story draft with, built from the Principles and Mistakes sections. Must include: character, emotion, specific moment, concrete detail, tension or change, ending and takeaway, fit to the brief's objective (what the audience should think, feel, know or do), and audience fit. Keep the `## Using the rubric` section (20-point total, rewrite below 12 or on a 0 in R01, R05 or R08, at most 5 fixes) and label it as a story-engine convention, not a book claim.
```markdown
## R01 · Criterion
**Check:** what to look at in the draft.
**0:** … **1:** … **2:** …
**Typical failure:** …
**Fix:** what to change, citing F/T IDs.
```

**domains/<domain>.md**: SOURCES = RUN/dominios/<domain>.md (Principles and Mistakes of the cards tagged with that domain) plus CLUSTERS. Domain is one of: business, sales, leadership, marketing, brand, personal, oral, craft, data, science. Do not re-explain frameworks: cite IDs.
```markdown
# <Domain>
## When to use story in <domain>
## Goal map
| Goal | Story type | Framework | Key techniques |
## Principles
- Claim. Evidence: study | author experience | anecdote. (Surname)
## Mistakes
- Mistake → fix (IDs). (Surname)
## Formats
### <the 3–6 formats this domain uses, each with the S, F and T to use>
```

Write the file to /Users/sdavila/Desktop/Storytelling/story-engine/knowledge/TARGET (create subfolders if needed). Reply with the path, the word count, and the IDs you wrote.
````

- [ ] **Step 2: Rewrite** `prompts/fidelidad.md` with this full text:

````markdown
# Fidelity check of story-engine knowledge files

You did not write these files. Check that they say only what the source cards support.

## Inputs (the controller fills in RUN and FILES)
- FILES: the knowledge files assigned to you (paths under story-engine/knowledge/).
- RUN/clusters.md, and the bundles in RUN/fuentes/, RUN/dominios/ and RUN/preguntas.md, which hold the card text behind each entry.

## Steps
1. From each file in FILES, sample 2 entries (3 when the file has more than 30 entries). Spread the samples across the file, not only the first entries.
2. For each entry, find its card text in the bundles and decide:
   - supported: every step or claim appears in at least one source card.
   - partly: some step or claim has no source.
   - unsupported: the entry as a whole has no source.
3. Flag any example that retells a book's example instead of an original one, even with new nouns.

## Output
Append to RUN/fidelidad.md:

| ID / entry | File | Verdict | Unsupported part | Card evidence (stem, section) |

End with one total line for your FILES: supported / partly / unsupported / retold examples. Reply with that line.

The bar: at least 90% supported overall. Any file with a partly, unsupported or retold entry goes back to its writer, who re-checks the whole file against SOURCES, not only the sampled entries.
````

- [ ] **Step 3: Check for pilot leftovers.** Run:

```bash
cd $ROOT/destilado && grep -nE "piloto|11 pilot|business pilot|\bF01\b|cut low-value" prompts/knowledge.md prompts/fidelidad.md
```

Expected: no output.

- [ ] **Step 4: Commit.**

```bash
git add prompts/knowledge.md prompts/fidelidad.md && git commit -m "feat: writer and fidelity prompts for the 55-card layout"
```

---

### Task 7: Spec, handoff and ledger

**Files:**
- Modify: `story-engine/docs/superpowers/specs/2026-11-13-story-engine-design.md` (lines 31–33 layout, line 52 example, line 68 selection rules, lines 84–90 Steps B–C and budget, line 94 rollout)
- Modify: `story-engine/docs/superpowers/HANDOFF.md`, `story-engine/.superpowers/sdd/2026-11-13-knowledge-pipeline-pilot/progress.md`

- [ ] **Step 1: Update the spec layout** (lines 31–33) to:

```
  knowledge/
    rubric.md
    frameworks/<family>.md  story-types/<family>.md  techniques/<family>.md
    questions/<group>.md
    domains/  business sales leadership marketing brand personal oral craft data science (.md)
```

- [ ] **Step 2: Update the rest of the spec.**
  - Line 52: change the example to "a sales pitch reads `domains/sales.md` and the `frameworks/` family files it cites".
  - Line 68: change "per the selection rules" to "per the domain guide's Goal map".
  - Line 84, Step B: "map-reduce: one agent per lot of 11 cards writes candidate clusters (`prompts/lote.md`), then one merge agent per kind assigns final IDs F001/S001/T001 (`prompts/fusion.md`); `fuentes.py` then bundles the card text behind each cluster".
  - Line 85, Step C: "writers work from those bundles; `verificar.py` requires every cluster ID to have exactly one home".
  - Line 90: "Split every shared file by family (questions by group); a writer that cannot fit its clusters stops and the controller splits the file further."
  - Line 94: mark the pilot as done (2026-11-17).

- [ ] **Step 3: Update the HANDOFF.** Mark step 1 ("Antes de escalar") as done, and point to this plan and its commits. Step 2 becomes: "Escalar: correr `indice.py` por lote (5 × 11 fichas, orden alfabético) y en total, `lote.md` ×5, `fusion.md` ×3, `fuentes.py`, writers (Sonnet, máximo 4 en paralelo), `verificar.py` con `--books ../md` y `--allow escala/allow.md`, y fidelidad por archivo". Remove the domain-name collision note, because domain guides now live in `domains/`.

- [ ] **Step 4: Append to the ledger:** `Pre-scale fixes (plan 2026-11-17-pre-scale-fixes.md): done, destilado commits <first>..<last>.`

- [ ] **Step 5: Commit** (story-engine; the ledger is untracked):

```bash
cd $ROOT/story-engine && git add docs/superpowers && git commit -m "docs: spec and handoff for the 55-card layout"
```

---

## Out of scope (next plan: the scale run)

- Running the pipeline on the 55 cards.
- `knowledge/index.md` (ID → file) and freezing IDs. Do these after the scale run.
- Publication cleanup (`docs/superpowers/` scrub, examples F21 and F10). Nothing is published in this plan.
