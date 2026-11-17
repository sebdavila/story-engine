# story-engine — design

Date: 2026-11-13
Status: approved in conversation, pending written review

## Goal

An open-source Claude Code plugin that helps anyone find, structure, write, deliver and review stories for business, brand, personal and data contexts. The plugin is built from a distillation of 55 storytelling books, applied through process skills and checked by QA agents, so the agent actually uses that knowledge instead of falling back to generic advice.

## Scope

- Domains (v0.1): business and sales, brand, personal and oral, craft and data.
- Language: English. Skill descriptions also carry Spanish and Portuguese trigger phrases. The plugin answers in the user's language.
- Out of scope for v0.1: per-format skills (talk, post, video), SessionStart hook, non-Claude-Code manifests.

## Architecture

```
story-engine/
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  skills/
    story-coach/       entry point: builds the brief, routes
    story-mining/      find the story
    story-structure/   choose arc and framework
    story-draft/       write or prepare for live telling
    story-review/      audit against the rubric
  agents/
    knowledge-auditor.md
    story-reviewer.md
  knowledge/
    rubric.md
    frameworks/<family>.md  story-types/<family>.md  techniques/<family>.md
    questions/<group>.md
    domains/  business sales leadership marketing brand personal oral craft data science (.md)
  evals/
  README.md  SOURCES.md  LICENSE (MIT)
```

### Skills

| Skill | Triggers on | Does | Hands off to |
|---|---|---|---|
| story-coach | vague storytelling requests | builds the brief; asks only what is missing; routes | the skill that fits the brief |
| story-mining | "I don't have a story", raw material, no story yet | mining questions from `questions.md`; lists candidate stories; picks with the brief | story-structure |
| story-structure | material without shape | picks story type and framework by objective and format; maps beats | QA gate 1, then story-draft |
| story-draft | structure ready, or "write/tell this story" | writes the text or the oral version, applying techniques | QA gate 2 |
| story-review | an existing text or talk to evaluate | scores with `rubric.md`; top fixes | story-draft, if asked |

Each skill can also be triggered directly when the request is explicit.

**Brief** (kept in the conversation, not in files): audience; what they should think, feel, know or do; format; length; available material; domain.

**Knowledge loading:** each skill reads only the `knowledge/` files the brief calls for (for example, a sales pitch reads `domains/sales.md` and the `frameworks/` family files it cites). Skills reference these files by path relative to the skill's base directory (`../../knowledge/...`); verify during implementation that this resolves when the plugin is installed.

### Knowledge enforcement

1. **Hard gate in each skill:** read the relevant `knowledge/` files before producing output. Never name a framework or technique without having opened the file that defines it.
2. **Knowledge trace:** every output of story-structure and story-draft ends with:
   ```
   Knowledge trace
   - Read: <files>
   - Framework: <name> (<file> <ID>) -> where it is applied
   - Techniques: <name> (<ID>) -> where it is applied
   ```
3. **QA agents**, which never see the drafting process:

| Agent | Input | Checks | Returns |
|---|---|---|---|
| knowledge-auditor | brief, output, trace | opens the cited files; every framework step is present in the output; every cited technique sits where the trace says; the framework choice fits the brief per the domain guide's Goal map; flags generic advice not grounded in `knowledge/` | pass/fail per check, with location |
| story-reviewer | brief and story only | scores with `rubric.md` (character, emotion, moment, detail, tension, ending, brief objective) | score, top 3 problems, fix for each |

**Gates**
- Gate 1, after story-structure: knowledge-auditor.
- Gate 2, after story-draft: knowledge-auditor and story-reviewer in parallel.
- Fix loop: at most 2 rounds. Anything still failing is delivered to the user, flagged, never hidden.
- story-mining has no gate (exploratory).
- The user can say "no QA" to skip the gates for short pieces.

## Knowledge pipeline (local, never committed)

Lives in `../destilado/` next to the repo. Books and cards never enter the repo.

1. **Book cards:** Gemini (Antigravity CLI, `gemini-4-argon-high`) runs `prompt-ficha.md` on each book through `run-gemini.sh` (5 at a time). One card per book in `fichas-gemini/`: frameworks, techniques, story types, questions, principles, mistakes, exercises, distinct contribution, quotes, each with a chapter reference. Pilot validated on 2 books against Claude-made cards: same fidelity, richer detail.
2. **Step A — index** (Python script, no model): frontmatter and framework headings into `indice.md`.
3. **Step B — clusters** (map-reduce): one agent per lot of 11 cards writes candidate clusters from the Frameworks, Story types and Techniques sections (`prompts/lote.md`); then one merge agent per kind assigns final IDs F001/S001/T001 (`prompts/fusion.md`) into `clusters.md`, with canonical names, sources and differences worth keeping. `fuentes.py` then bundles the card text behind each cluster.
4. **Step C — knowledge files** (1 Claude agent per file): writers work from those bundles, never from cluster summaries alone; domain guides from the Principles and Mistakes of the cards tagged with that domain plus `clusters.md`. `verificar.py` requires every cluster ID to have exactly one home.
5. **Step D — verification** (agent): every entry traces to at least one card; every card framework is merged or listed in `drop-log.md` with a reason; copyright rules hold.

**Knowledge entry format:** ID, canonical name, also known as, sources, use when, avoid when, steps, common mistakes, short original example.

**Budget:** about 5K tokens per knowledge file. Split every shared file by family (questions by group); a writer that cannot fit its clusters stops and the controller splits the file further.

**Copyright:** own words only, attribution as "(Hall; Davis)", no copied examples, no quotes in the repo. `SOURCES.md` lists all 55 books.

**Rollout:** run steps A–D on the 11 business books first (`business.md` plus a first `frameworks.md`). Review, then extend to all 55. Pilot done 2026-11-17; pre-scale fixes in `plans/2026-11-17-pre-scale-fixes.md`.

## Testing

Evals with the `skill-creator` loop, about 15 cases in `evals/`:
- Routing (3): vague request; direct review request; ambiguous structure-vs-draft request.
- Per skill (8): two each for mining, structure, draft and review, across pitch, brand, personal and data.
- QA (4): missing trace blocks delivery; seeded misapplied framework is caught by the auditor; generic text is not approved by the reviewer; "no QA" skips the gates.

Each case checks: right skill triggered, trace present, cited files actually read, output meets the brief.

## Distribution

- Public GitHub repo `sebdavila/story-engine`, version 0.1.0, MIT.
- Install: `/plugin marketplace add sebdavila/story-engine`, then `/plugin install story-engine@story-engine`.
- Creating the public repo and pushing require explicit user confirmation.
