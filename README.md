# story-engine

A Claude Code plugin that helps you find, structure, write, tell and review stories for business, sales, brand, marketing, leadership, personal, oral and data contexts.

It is built on a knowledge base distilled from 55 storytelling books (see [SOURCES.md](SOURCES.md)): 381 frameworks, 191 story types, 656 techniques, 635 questions and a 10-criterion rubric. The skills open the entries they use, say where they applied them, and two QA agents check the result, so you get the books' methods instead of generic advice.

The plugin works in any language you write in. Its content is in English.

## Install

From GitHub:

```
/plugin marketplace add sebdavila/story-engine
/plugin install story-engine@story-engine
```

From a local clone:

```
/plugin marketplace add /path/to/story-engine
/plugin install story-engine@story-engine
```

## Skills

| Skill | Use it when | Example |
|---|---|---|
| story-coach | You need a story but the request is vague. It builds a short brief (audience, objective, format, material) and routes. | "I need a story for Monday's meeting, can you help?" |
| story-mining | You don't have a story yet. It asks targeted questions and lists candidate stories. | "I'm pitching a CFO next week and have no customer story." |
| story-structure | You have material without shape. It picks a story type and framework for your objective and maps the beats. | "Structure the origin story of our coffee brand." |
| story-draft | The structure is ready, or you want the text or a version to tell out loud. It writes it and applies techniques. | "Help me tell this story out loud at our team offsite." |
| story-review | You have a draft or talk to evaluate. It scores it on the rubric and gives the top fixes. | "Score this data talk before my monthly review." |

You can start with any skill. Each one hands off to the next when it is done.

## Knowledge trace and QA

story-structure and story-draft end every output with a knowledge trace: the files read, the framework and techniques used, and where each one is applied.

Two QA agents check the work. They never see how it was made:

- **knowledge-auditor** opens every cited entry and checks that each ID exists, that every framework step is in the output, that each technique sits where the trace says, and that the framework fits your objective.
- **story-reviewer** scores the story on the rubric (R01–R10, out of 20) as your audience would receive it.

The gates:

- **Gate 1** runs after story-structure, with the auditor.
- **Gate 2** runs after story-draft, with both agents. It passes at 14/20 or more, with all four audit checks passing and no rubric criterion at 0.
- **Fix rounds.** If a gate fails, the skill fixes only what was flagged, for up to 2 rounds. Anything still failing is delivered under a "QA pending" section, never hidden.

For a short piece, say **"no QA"** to skip the gates. The trace is still written.

## Knowledge layout

```
knowledge/
  domains/       one guide per domain: when to use story, goal map, principles, mistakes, formats
  frameworks/    F001–F381, grouped by family
  story-types/   S001–S191
  techniques/    T001–T656
  questions/     Q IDs, in 11 groups (founder, customer, personal memory, diagnose a draft...)
  index.md       every F, S and T ID with its name and file
  rubric.md      R01–R10
```

Every entry is written in original words and credits its authors by surname. No text from the books is reproduced.

## License

MIT. See [LICENSE](LICENSE).
