---
name: story-draft
description: Use even for short or quick pieces ("es algo rápido", "post corto"). Writes the story, or prepares it to be told out loud, from a structure, applying techniques from the story-engine knowledge base, then runs QA (knowledge audit and blind rubric review). Use when a structure is ready or the user asks to write, tell or finalize a story or a story-based piece (LinkedIn post, social post, script, speech, pitch), e.g. "write this story", "draft the pitch", "write a LinkedIn post about the day...", "make it a story and write it", "escríbeme un post sobre", "escribe un guion", "help me tell this out loud", "finalize this draft", "escribe la historia", "redacta el post", "cuéntala en voz alta", "escreva a história", "me ajuda a contar em voz alta".
---

# story-draft

Write the piece from a beat map and a knowledge trace. Answer in the user's language and write the piece in the language the audience will hear or read; keep the trace labels in English. All paths are relative to this skill's base directory.

## 0. Inputs

- Brief: from earlier skills, or build it from the request (Audience, Objective, Domain, Goal map row, Format, Length, Material), asking at most one question.
- Structure: a beat map with a `Knowledge trace` from story-structure. If there is none, invoke story-structure first (it runs gate 1), then continue here.
- A supplied draft to finalize: treat it as the first draft. If it has no `Knowledge trace`, rebuild the structure through story-structure from the draft's content before delivering; never deliver without a trace.

## 1. Hard gate: read before output

Never name a technique or framework you have not opened in this conversation. In the output and the trace, name only IDs you opened; call unopened IDs "the row's other options" instead of naming them. Never read `../../knowledge/index.md` whole: Grep `| <ID> |` in it, open the file in the third column, read only that ID's section (`## <ID> · Name`, or the `- **<ID> · Name**` line for techniques).

Read:
1. The framework and story type in the structure's trace (re-open them if they are not in this conversation).
2. The technique IDs in the brief's Goal map row (`../../knowledge/domains/<domain>.md`, `## Goal map`). Pick 2–4 that fit the beats.
3. If the piece is told live (talk, toast, pitch, meeting, video): also the `## Goal map` of `../../knowledge/domains/oral.md`; open the technique IDs of the row that fits and use the ones that live in `techniques/delivery-` files (`../../knowledge/techniques/delivery-a.md`, `../../knowledge/techniques/delivery-b.md`).

## 2. Write

- Follow the beats in order. Every framework step stays visible in the text.
- Use only the user's facts. Mark a missing fact as `[ask: ...]` rather than inventing it.
- Apply each chosen technique at a specific place and remember where.
- Oral version: write it to be said (short sentences, spoken rhythm), then add delivery notes per beat (pause, gesture, where to look, timing) from the delivery techniques you opened.
- No generic advice that no opened entry supports.
- Never stop without a draft. If the material is thin or generic, write the best draft the facts allow, mark every missing fact as `[ask: ...]`, run the gates, and list the questions for the user after the piece. Only story-review gives a score without a draft.

## 3. Knowledge trace

End with this block, exactly these labels:

```
Knowledge trace
- Read: <every knowledge file you opened>
- Framework: <name> (<file> <ID>) -> <paragraphs or beats where it is applied>
- Techniques: <name> (<ID>) -> <where it is applied>; one entry per technique
- Deviation: <why the framework differs from the Goal map row, or "none">
```

## 4. Gate 2: knowledge-auditor and story-reviewer

Skip only if the user said "no QA" (or "sin QA", "sem QA"), or the brief has `- QA: off`. The trace is still written.

Call both agents in parallel with the Agent tool:
- `subagent_type: story-engine:knowledge-auditor` with the brief, the piece, the trace and the absolute path of the plugin's `knowledge/` directory (this skill's base directory plus `../../knowledge`, resolved).
- `subagent_type: story-engine:story-reviewer` with the brief, the piece and the same `knowledge/` path. Never give the reviewer the trace, the beat map or any process notes.

Gate 2 passes when the auditor verdict is PASS (all 4 checks), the reviewer score is at least 14/20, and no rubric criterion scores 0.

If it fails: fix only what was flagged (the failing auditor checks; the reviewer's top problems and any criterion at 0), update the trace, and call both agents again, each with a fresh Agent call (not SendMessage; never run them in the background). At most 2 fix rounds. Still failing after 2 rounds: deliver anyway with a section `## QA pending` listing each failing check or criterion with its location. Never hide a failure.

## 5. Deliver

Deliver in your reply. Do not write or overwrite files unless the user asked for a file.

Give, in this order: the piece; the delivery notes (oral only); the knowledge trace; the final `Auditor verdict` block and `Reviewer score` line (when QA ran); `## QA pending` if any.
