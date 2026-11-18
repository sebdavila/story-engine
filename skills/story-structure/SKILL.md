---
name: story-structure
description: Gives a story its shape. Picks the story type and framework from the story-engine knowledge base by objective and format, maps the beats, writes a knowledge trace and runs a QA check. Use when there is material without shape or a structure to check, e.g. "structure this story", "make it a story", "turn my notes into a story", "make my pitch a story", "how should I order this", "turn these notes into a story arc", "check my outline", "estructura esta historia", "cómo ordeno esto", "arma el arco", "estruture esta história", "como organizo essa história".
---

# story-structure

Turn material into a beat map grounded in one framework from `knowledge/`. Answer in the user's language; keep the trace labels in English. All paths are relative to this skill's base directory.

## 0. Brief

Use the brief from story-coach or story-mining if it is in the conversation. If not, build it from the request (Audience, Objective, Domain, Goal map row, Format, Length, Material), asking at most one question. Domain is one of the 10 files in `../../knowledge/domains/`. If the user supplied a structure to check, run step 5 (the auditor) on it exactly as given, before changing anything; then fix only what the auditor flags, following steps 2–4 for the fixed parts.

## 1. Hard gate: read before output

Never name a framework, story type or technique you have not opened in this conversation. In the output and the trace, name only IDs you opened; call unopened IDs "the row's other options" instead of naming them. Never read `../../knowledge/index.md` whole (about 12,000 words): Grep it.

To open an entry: Grep `| <ID> |` in `../../knowledge/index.md`, open the file in the third column, read only the `## <ID> · Name` section (down to the next `## `).

## 2. Route A: from the Goal map to one framework

1. Open `../../knowledge/domains/<domain>.md` and read its `## Goal map` table and its `## Formats` section. Find the brief's Goal map row.
2. Open the row's story type IDs and framework IDs.
3. Pick one framework from the row whose steps fit the material, format and length. Pick the story type it serves.
4. If a framework outside the row fits much better, you may use it only after opening it, and the trace's `Deviation:` line must say why.

A row fits only if its Goal names the same job as the objective. Pick rows only from the brief's one domain; never borrow a row or a Formats entry from another domain guide to justify a framework.

No row fits (brief says `none: <keywords>`, or nothing matches): Grep the keywords in the Name column of `../../knowledge/index.md` (lines starting `| F` and `| S`), keep at most 2 candidates, open both, pick one, and say in the trace's `Deviation:` line that no Goal map row fit and which keywords you searched.

## 3. Beat map

One beat per framework step, in the framework's order. Each beat: the step name, what happens in this story (using the user's concrete facts, never invented ones; mark gaps as `[ask: ...]`), and the target length or time. Fit the domain's Formats guidance for the brief's format.

## 4. Knowledge trace

End the output with this block, exactly these labels:

```
Knowledge trace
- Read: <every knowledge file you opened>
- Framework: <name> (<file> <ID>) -> <beats where it is applied>
- Techniques: <name> (<ID>) -> <where>, or "none at structure stage"
- Deviation: <why the framework differs from the Goal map row, or "none">
```

## 5. Gate 1: knowledge-auditor

Skip this step only if the user said "no QA" (or "sin QA", "sem QA"), or the brief has `- QA: off`. The trace is still written.

Call the Agent tool with `subagent_type: story-engine:knowledge-auditor`. In the prompt give: the brief, the beat map, the trace, and the absolute path of the plugin's `knowledge/` directory (this skill's base directory plus `../../knowledge`, resolved). The auditor replies starting with `Auditor verdict: PASS|FAIL` and four numbered checks.

- PASS: deliver.
- FAIL: fix only what the auditor flagged (re-open entries as needed), update the trace, call the auditor again with a fresh Agent call (not SendMessage; never run it in the background). At most 2 fix rounds.
- Still failing after 2 rounds: deliver anyway, with a section `## QA pending` listing each failing check and its location. Never hide a failure.

Show the user the final auditor verdict block under the trace.

Deliver in your reply: the beat map, the trace and the verdict go in your answer. Do not write or overwrite files unless the user asked for a file.

## 6. Hand off

Offer story-draft to write the text or prepare the oral version. If the user already asked for a draft, invoke story-draft with the brief, beat map and trace.
