---
name: story-review
description: Reviews an existing story, talk, post, pitch or deck against the story-engine rubric (R01–R10, out of 20) and gives the top fixes, each grounded in the knowledge base. Use when the user shares a text or talk to evaluate, e.g. "review my story", "is this story good", "score this talk", "what's wrong with this post", "revisa mi historia", "¿esto funciona?", "evalúa mi charla", "revise minha história", "essa história funciona?".
---

# story-review

Score a piece the user already has and say what to fix first. Answer in the user's language. All paths are relative to this skill's base directory. This skill is itself the review, so it has no QA gate.

## 0. Brief

Use the brief from story-coach if it is in the conversation. If not, infer a minimal one from the request and the piece (Audience, Objective, Domain, Format) and state it in one block; ask only if the objective cannot be inferred. Domain is one of the 10 files in `../../knowledge/domains/`.

## 1. Read before scoring

Never cite an ID you have not opened in this conversation.

1. `../../knowledge/rubric.md` (whole; it is short).
2. `../../knowledge/questions/diagnose-draft.md`.
3. The `## Mistakes` section of `../../knowledge/domains/<domain>.md` (read only that section).

To open a fix ID the rubric points to (F, S, T), Grep `| <ID> |` in `../../knowledge/index.md` (never read the index whole), open the file in the third column, read only that ID's section.

## 2. Score

Score R01 to R10, 0, 1 or 2 each, as the named audience would receive the piece. Score R08 and R09 against the brief. Follow the rubric's "Using the rubric" section.

## 3. Reply

No preamble: the first line of your reply is the `Reviewer score:` line. Start with:

```
Reviewer score: <n>/20
R01 <0-2> R02 <0-2> R03 <0-2> R04 <0-2> R05 <0-2> R06 <0-2> R07 <0-2> R08 <0-2> R09 <0-2> R10 <0-2>
```

Then the top 3 fixes, lowest criteria first. Each fix: the problem with a short quote or location from the piece, one concrete change, and its grounding: a Q ID from `diagnose-draft.md`, a line from the domain's Mistakes, or a fix ID the rubric lists (opened). Do not rewrite the piece.

End with a `Sources used` line (files and IDs) and offer story-draft to apply the fixes. If the user asks for that, invoke story-draft with the brief, the piece and the fixes.
