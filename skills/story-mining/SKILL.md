---
name: story-mining
description: Finds the story when the user has none yet. Asks mining questions from the story-engine question bank, lists candidate stories and picks one that fits the objective. Use when the user says "I don't have a story", "I have no example", "what story could I tell", or brings only raw facts, e.g. "no tengo una historia", "no se me ocurre qué contar", "qué historia puedo contar", "não tenho uma história", "que história eu posso contar".
---

# story-mining

Find candidate stories in the user's own material. Do not structure or write the story here; hand the chosen candidate to story-structure.

Answer in the user's language. All paths are relative to this skill's base directory.

## 0. Brief

Use the brief from story-coach if it is in the conversation. If not, build a minimal one from the request: Audience, Objective, Domain (one of the 10 files in `../../knowledge/domains/`), Goal map row (read only the `## Goal map` table of that domain file). Ask at most one question if the objective is unclear.

## 1. Read before asking

Hard gate: read these before your first mining question. Never name an ID you have not opened.

1. The story type IDs in the brief's Goal map row. For each, Grep `\| <ID> \|` (pipes escaped) in `../../knowledge/index.md` (never read the index whole), open the file in the third column, and read only that `## <ID> · Name` section. It tells you what kind of incident to look for.
2. One or two question groups from `../../knowledge/questions/`, chosen by the brief:

| Brief points to | Group |
|---|---|
| founder, company origin, pitch, investors, recruiting | `../../knowledge/questions/founder-and-origin.md` |
| customer, case study, sales, win-back | `../../knowledge/questions/customer-and-buyer.md` |
| the teller's own life, family, toast, memoir | `../../knowledge/questions/personal-memory.md` |
| leader, team, values, change, culture | `../../knowledge/questions/leadership-and-organization.md` |
| brand, content, social, campaign | `../../knowledge/questions/brand-and-content.md` |
| data, research, business case | `../../knowledge/questions/data-and-argument.md` |
| fiction, characters, stakes | `../../knowledge/questions/character-and-conflict.md` |
| objective or audience still fuzzy | `../../knowledge/questions/objective-and-audience.md` |

Questions are lines `- **Q123** ...`. Pick the ones that aim at a lived scene, not an opinion.

If the Goal map row is `none: <keywords>`, Grep the English keywords in the Name column of `../../knowledge/index.md` (lines starting `| S`), keep at most 2 candidate story types, open them, and say so to the user.

## 2. Mine

- Ask at most 5 questions per round, in plain words adapted to the user's case. One question per line. Do not show Q IDs to the user.
- If the user's request already holds the raw material, skip asking and mine it directly.
- Listen for moments: a specific time and place, a person who wanted something, a choice, a change.

## 3. Candidates

List 3 to 5 candidates. For each: one line with the incident, one line on why it serves the objective, and the story type it fits (name and ID, only IDs you opened). Then pick one with a one-line reason tied to the brief, and ask the user to confirm or choose another.

Close with a short `Sources used` line: the files and Q IDs you drew on.

## 4. Hand off

When the user confirms (or in a non-interactive run, with your pick), invoke story-structure with the brief plus the chosen candidate and every concrete detail the user gave. Mining has no QA gate.
