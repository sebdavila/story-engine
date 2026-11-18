---
name: story-coach
description: Entry point for storytelling help, including short or quick pieces. Builds a short brief (audience, objective, domain, format, length, material) and routes to the right story-engine skill. Use when a storytelling request is vague or mixed, e.g. "help me tell a story", "I need a story for my presentation", "make this more of a story", "ayúdame con una historia", "necesito contar una historia", "cómo cuento esto", "me ajuda a contar uma história", "preciso de uma história para minha apresentação". For an explicit request (find a story, structure, write, review) the specific skill can trigger directly.
---

# story-coach

Build the brief, then hand off. Do not write the story here and do not name any framework, story type or technique: the next skill picks them after opening the files that define them.

Answer in the user's language. Keep the brief labels in English.

## 1. Build the brief

Fill this block from what the user already said. Ask only for what is missing: each message holds exactly one question (one question mark, one topic; do not bundle "and who is the audience?"), at most 3 questions in total. If the user does not know, state the default you will use and move on.

```
Brief
- Audience:
- Objective: <what they should think, feel, know or do>
- Domain: <one of: brand, business, craft, data, leadership, marketing, oral, personal, sales, science>
- Goal map row: <exact Goal cell text, or "none: <keywords searched>">
- Format:
- Length:
- Material: <what the user has: facts, notes, a memory, a draft, nothing yet>
```

Ask in this order of importance: objective, audience, material. Format and length have defaults (spoken, 2–3 minutes; or written, 300 words) unless the request implies otherwise.

## 2. Pick the domain

Do not read the domain guides whole. Grep `^## When to use` with about 8 lines of context across `../../knowledge/domains/` (relative to this skill's base directory). Pick the domain whose situations match the objective and audience. When two fit, prefer the one closer to the audience: a pitch to a buyer is `sales`, a talk to one's own team is `leadership`, a toast is `personal`, a spoken telling of any kind may add `oral` later in story-draft.

## 3. Pick the Goal map row

Open `../../knowledge/domains/<domain>.md` and read only its `## Goal map` table. Copy the Goal cell that best matches the objective into `Goal map row`. If no row fits, write `none: ` plus 2–4 keywords that describe the objective; the next skill searches the index with them.

## 4. Route

| Situation | Hand off to |
|---|---|
| No story yet, only a need ("I don't have a story", raw facts with no incident) | story-mining |
| Material exists (a memory, a case, notes) but has no shape | story-structure |
| A structure exists, or the user says write or tell it | story-draft (it runs story-structure first if there is no structure) |
| An existing text or talk to evaluate | story-review |

Show the brief to the user in a short block, say which skill comes next and why in one line, then invoke that skill with the Skill tool. If you asked a question in this turn, stop and wait for the answer before routing.

The user can say "no QA" (or "sin QA", "sem QA") to skip the QA gates for a short piece. Carry it in the brief as a last line `- QA: off`.
