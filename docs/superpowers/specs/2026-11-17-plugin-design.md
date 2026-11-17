# story-engine plugin (Plan 2) — design

Date: 2026-11-17
Status: approved in conversation, pending written review
Parent spec: `2026-11-13-story-engine-design.md` (Architecture, Skills, Knowledge enforcement, Testing). This document adds what the parent left open and overrides it where they differ.

## Scope

Plan 2 builds the whole plugin locally: skills, QA agents, evals, manifests, README, SOURCES, LICENSE. It ends with the plugin installed from a local path and passing its evals. Nothing is published.

Plan 3 (separate spec and plan) does the publication: clean `docs/superpowers/`, review the F100 Common mistakes line that cites Parikh's deck, decide the git history for the public repo (a clean single initial commit is the likely choice, because older commits hold private paths), confirm the LICENSE holder name, create `sebdavila/story-engine` and push. Each step needs explicit user confirmation.

Unchanged from the parent: the 5 skills and their hand-offs, the 2 QA agents, the trace block, English content with Spanish and Portuguese trigger phrases, answers in the user's language.

## Knowledge layout the skills rely on

- `knowledge/domains/<domain>.md` (10): When to use, Goal map, Principles, Mistakes, Formats. Each Goal map row is one objective with its story type, framework and key technique IDs.
- `knowledge/frameworks/`, `story-types/`, `techniques/`: entries defined by `## F001 · Name` headings or `- **T001 · Name**` lines.
- `knowledge/questions/<group>.md` (11 groups; the parent's `questions.md` is now this folder).
- `knowledge/index.md`: one row per ID, `| ID | Name | File |`, about 12,000 words. Never loaded whole; always searched.
- `knowledge/rubric.md`: R01–R10, 0–2 each, 20 points total.

## Knowledge loading (route A)

The brief gains one field: **objective**, the Goal map row that fits. story-coach picks domain and objective.

To read an entry: grep its row in `index.md` (`grep "| F238 |" knowledge/index.md`), open that file, read only that ID's section.

| Skill | Reads |
|---|---|
| story-coach | "When to use" of the domain guides, to pick domain and objective. No frameworks. |
| story-mining | The Goal map row (story type); 1–2 `questions/` groups chosen by the brief (for example `founder-and-origin`, `customer-and-buyer`, `personal-memory`). |
| story-structure | The Goal map row; the story type and framework entries via `index.md`; the domain's Formats. |
| story-draft | The structure trace; the row's technique entries; `techniques/delivery-*` when the piece is told live. |
| story-review | `rubric.md`, `questions/diagnose-draft.md`, the domain's Mistakes. |

Rules for every skill:
- If no Goal map row fits, search the Name column of `index.md` by keyword, keep at most 2 candidates, and say so in the trace.
- Never name an ID that was not opened (the parent's hard gate).

Path: skills reference knowledge as `../../knowledge/...` relative to the skill directory. The first task confirms this resolves both with `claude --plugin-dir .` and with an install from a local marketplace. If it does not, use `${CLAUDE_PLUGIN_ROOT}/knowledge/...`.

## QA agents

**knowledge-auditor** — model `sonnet`; tools Read, Grep, Glob (read only). Input: brief, output, trace. Opens each cited ID through `index.md`. Four checks, each pass or fail with a location line:
1. Every cited ID exists.
2. Every step of the framework is present in the output.
3. Every technique sits where the trace says.
4. The framework matches the brief's Goal map row, or the trace justifies the deviation.

It also flags generic advice not grounded in `knowledge/`.

**story-reviewer** — model inherits the session's; tool Read, for `rubric.md` only. Input: brief and story only; never the trace or the process. Returns the R01–R10 score (out of 20), the top 3 problems and a fix for each.

**Gates** (parent rules hold: gate 1 after structure, gate 2 after draft, mining has none):
- Gate 2 passes when the auditor passes all 4 checks, the reviewer scores at least 14/20, and no rubric criterion scores 0. The 14/20 threshold is provisional; the evals calibrate it.
- Fix round: the skill fixes only what was flagged. After 2 rounds, anything still failing is delivered under a "QA pending" section that lists it.
- "no QA" skips the gates; the trace is still written.

## Evals

`evals/evals.json` in skill-creator format: 15 cases, each with a prompt and assertions. Prompts in English, except 3 in Spanish and 1 in Portuguese to test triggers.

Cases (from the parent): routing 3 (vague request; direct review request; ambiguous structure-vs-draft request); skills 8 (two each for mining, structure, draft, review, across pitch, brand, personal, data); QA 4 (missing trace blocks delivery; seeded misapplied framework caught by the auditor; generic text not approved by the reviewer; "no QA" skips the gates).

Grading is mixed:
- **Grader agent, mechanical:** the right skill triggered; trace present; every cited ID exists in `index.md` and its file was read (checked in the tool-call transcript); auditor verdict and reviewer score present; the expected outcome on QA cases.
- **User, quality:** reads the 8 skill cases in the skill-creator viewer and leaves one line per case.

Plan 2 is done when all 15 cases pass their mechanical assertions and the user approves at least 6 of the 8 on quality, within at most 3 iteration rounds. If round 3 does not get there, stop and report what fails.

No baseline run (no prior version; a no-skill comparison doubles the cost). Add one only if the user asks.

## Packaging

- `.claude-plugin/plugin.json`: name `story-engine`, version `0.1.0`, license MIT.
- `.claude-plugin/marketplace.json`: one plugin, source `./`.
- Each skill `description` carries English, Spanish and Portuguese trigger phrases. Each `SKILL.md` stays under about 500 lines; routing detail moves to the skill's `references/` if needed.
- Validate the manifests with `claude plugin validate` if that command exists, otherwise by checking them against the plugin docs.
- `README.md`: what it does, install, the 5 skills with one example each, the QA gates and "no QA".
- `SOURCES.md`: the 55 books with title, author and year, taken from the card frontmatter. Bibliographic data only, no card text.
- `LICENSE`: MIT, holder `sebdavila` (confirmed in Plan 3).
- Publish dry run: list the files the public repo would hold. `docs/superpowers/` and `.superpowers/` are excluded. Nothing is pushed.
