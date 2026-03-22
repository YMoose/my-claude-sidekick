---
name: rehearse-teaching
description: Rehearse teaching or teach-back by simulating a thoughtful target audience or beginner and asking unit-by-unit audience questions that expose unclear concepts, missing links between units, weak examples, overload, and unanswered questions. Use when the user wants to practice teaching, roleplay a listener, get mock student questions, test whether an explanation is understandable, run a rehearsal unit on one teaching unit, or complete a full rehearsal round across a teaching plan.
---

# Rehearse Teaching

Use this skill after the user already has something to teach: a section, a slide, a teaching draft, or a live explanation. The user leads. This skill acts as a pressure-tester: the main agent manages the rehearsal, the audience subagent listens and asks questions like the audience, and together they expose the next repair.

## Core Terms

- Teaching plan: the user's full explanation, lesson, or presentation flow.
- Teaching unit: one bounded piece of that teaching plan, such as one slide, one section, one concept, one example, or one core question.
- Rehearsal unit: the full interaction cycle on one teaching unit. The user teaches that teaching unit, the audience subagent questions it, the user answers, and the exchange continues until the audience subagent either understands that teaching unit well enough from the listener's point of view or the user cannot answer a blocking audience question, which the main agent then records in the unanswered-question list.
- Rehearsal round: the full pass across the whole teaching plan after all teaching units have completed their rehearsal units.

## Default Stance

- Treat the user's current teaching unit as the primary object inside the current rehearsal unit.
- Use a two-agent structure by default: the main agent manages the current rehearsal unit and tracks the overall rehearsal round; the audience subagent stays in role as the listener.
- Pressure-test before you rewrite.
- Let the audience subagent ask and follow up as needed inside each rehearsal unit. Do not force a fixed question count in advance.
- Keep the audience subagent in the listener's point of view, not the expert's point of view, even when the audience is set to a sharper level.
- Separate a teaching-plan problem from an understanding problem. That distinction controls the next repair.
- If the user cannot answer a question, record it explicitly in the unanswered-question list instead of papering over it.

## Workflow

```text
- [ ] Confirm the audience and define the teaching units
- [ ] Run rehearsal units with the audience subagent and record the exchange
- [ ] Classify the failures across the rehearsal round
- [ ] Hand off to the next repair or next rehearsal round
```
### 1. Confirm the audience and define the teaching units

#### How

- Start from the user's current teaching plan, draft, slides, or rough explanation.
- Work with the user to split that material into teaching units.
- Keep each teaching unit bounded enough for one rehearsal unit.
- Estimate the audience's prior knowledge from the teaching target, not from the user's own current level alone.
- Use the user's real target audience description if the user provides one.
- If no clear audience description exists, default to a sharp beginner.

#### Why

- A fixed audience keeps the feedback coherent.
- Splitting the teaching plan into teaching units keeps each rehearsal unit focused and makes it easier to locate where the real problem sits.
- A bounded teaching unit makes it easier to tell whether the real problem is inside the unit itself or in the logic the listener is supposed to follow across it.

#### Output

- A confirmed audience setup
- a teaching-unit split

### 2. Run rehearsal units with the audience subagent and record the exchange

#### How

- Spawn one dedicated audience subagent that reads the confirmed audience setup .
- Confirm which teaching unit is the current unit for the current rehearsal unit.
- Let the user either teach the teaching unit live or just provide the prepared material for it.
- Give audience subagent the current teaching unit and let the audience subagent question.
- Let the main agent relay every audience question to the user and every user answer back to the audience subagent.
- Let the exchange proceed question by question instead of fixing a question batch size in advance.
- Keep the rehearsal unit running until the audience subagent either understands the current teaching unit or hits a blocking unanswered question that the main agent records explicitly.
- Keep an explicit unanswered-question list.
- Pay special attention to the questions the user could not answer cleanly or at all.
- Capture where the user sounded unsure, hand-wavy, or tempted to skip ahead.
- Distinguish what landed cleanly, what needed follow-up, and what remained unresolved when the rehearsal unit stopped.

#### Why

- The audience subagent is there to listen and question; the main agent is there to preserve structure and memory.
- The audience voice stays cleaner when it is separated from the coordinating voice.
- A dedicated listener makes the rehearsal feel more like a real interaction.
- Having the main agent relay both directions lets it record the full rehearsal process and use that process to suggest the next useful repair, while keeping the audience agent in listener role. It also helps the rehearsal unit stay orderly without collapsing the two voices into one.
- A question-by-question exchange makes it easier for the user to answer, repair, and continue the rehearsal unit.
- Letting confusion surface inside the unit reveals where the user's intended structure does not match the listener's actual experience.
- A teaching draft can look fine on the page while still failing from the listener's point of view.
- A rehearsal unit should recreate the moment where understanding succeeds or breaks, not just inspect the material in the abstract.

#### Output

- A rehearsal-unit record 
- An unanswered-question list.

### 3. Classify the failures across the rehearsal round

#### How

- After all teaching unit solved, review records across the rehearsal round 
- Group important issues by teaching unit and by failure type.
- Treat these as teaching-plan problems:
  - ordering
  - emphasis
  - transitions
  - example choice
  - terminology timing
  - too much or too little detail
- Treat these as understanding problems: the issue is not mainly how the material is arranged, but that some part of the underlying understanding is still missing or unstable.
  - missing prerequisite: the current teaching unit depends on an earlier idea, term, or step that has not been established clearly enough yet
  - unsupported claim: the user makes a statement, conclusion, or comparison but cannot support it with a reason, mechanism, example, or source
  - concept gap: the user seems to know the label or rough idea, but cannot explain clearly what it is, how it works, or how it connects to nearby ideas
  - confusion about mechanism, boundary, or distinction
- Say which class each important issue falls into and why.
- Highlight recurring problems that show up across multiple teaching units.

#### Why

- Looking across the whole rehearsal round makes it easier to see whether a problem is local to one teaching unit or structural across the teaching plan.
- Not every failure should send the user back to more study.
- The value of rehearsal is not just finding a flaw, but locating which layer the flaw belongs to.

#### Output

- A classified issue list for the rehearsal round, tied back to the affected teaching units.

### 4. Hand off to the next repair or next rehearsal round

#### How

- For teaching-plan problems, suggest the smallest useful revision to the affected teaching unit or to the overall teaching plan.
- For understanding problems, point the user back to the most relevant source material or study notes for the affected teaching unit, and give guidance on what to revisit, instead of directly supplying the missing explanation.
- Turn the rehearsal-round record into one clear report using [templates/output.md](templates/output.md) before discussing the next move.
- Discuss the next move with the user and let them choose whether to revise the affected teaching units, revisit source study, run another rehearsal round, or finish; if another rehearsal round is on the table and the base audience can already follow, ask whether they want that later round to use a sharper audience. Add the next move into the report.

#### Why

- A full rehearsal-round report helps the user see the most important remaining problems in the teaching plan before deciding what to improve next.
- Small, targeted repair suggestions are usually better for the user because they help the user understand and improve the material more actively than rewriting everything at once.

#### Output

- A full rehearsal-round report, structured with [templates/output.md](templates/output.md), that includes the rehearsal-round record and a clear next move.

## Guardrails

- Do not interrogate like an adversarial expert unless the user explicitly asks.
- Do not flood the user with every possible question at once.
- Do not rewrite the entire lesson in one dump when a local repair would do.
- Do not confuse the user's knowledge with the audience's knowledge.
- Do not force an answer when the user does not have one; record the gap.
- Do not stay vague; point to the exact unit, sentence, transition, example, or claim that triggered the question.

## Resources

- Use [templates/output.md](templates/output.md) when structuring the response to the user.











