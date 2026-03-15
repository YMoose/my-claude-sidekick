---
name: draft-outline
description: Optimize a user's explanation framework or teaching plan by repairing structure, enriching weak spots, and simplifying for live teaching. Use when users already have a rough outline, framework, or teaching draft and want help improving it for actual explanation or teaching.
---

# Draft Teaching Plan

Use this skill after the user has already studied the topic they want to explain and drafted something of their own, even if that draft is rough. The user leads. This skill acts as an optimizer: inspect, repair, enrich, simplify, and sharpen what the user has already written.

## Default Stance

- Treat the user's draft as the primary object.
- Optimize before you rewrite.
- Work in small revision rounds: one issue cluster at a time by default.
- Preserve the user's voice and ownership unless the user explicitly asks for a full rewrite.
- Keep three layers distinct:
  - explanation framework
  - teaching plan draft
  - lean teaching plan
- Prefer one clear main line over broad coverage.
- Use examples and analogies only when they reduce confusion.
- If the user has not drafted anything yet, first help them produce the smallest viable framework instead of writing the whole plan for them.

## Workflow

```text
- [ ] Confirm the topic, audience, and current draft
- [ ] Diagnose the explanation framework
- [ ] Repair and enrich the teaching plan draft
- [ ] Simplify it for live teaching
- [ ] Hand off to audience rehearsal
```

### 1. Confirm the topic, audience, and current draft

#### How

- Start from the specific topic or subtopic the user wants to explain, the user's studied notes, and the user's own rough draft.
- Ask who the explanation is for if that changes vocabulary, pacing, or examples.
- If the user has no audience yet, keep the plan beginner-friendly.
- If the user has no draft yet, ask for a rough framework first or help them sketch the smallest viable one.

#### Why

- This skill optimizes something concrete; it works best when there is already a draft, however rough.
- Different audiences need different ordering, examples, and detail levels.

#### Output

- A confirmed teaching target, audience assumption, and current draft state.

### 2. Diagnose the explanation framework

#### How

- Inspect the user's framework with the structural heuristics later in this file.
- Identify the main line, section order, missing definitions, and broken logical bridges.
- Point out where the draft is thin, overloaded, misordered, or too dependent on hidden assumptions.
- If the draft is mostly notes rather than a framework, help the user reshape it into a minimal explanation framework first.

#### Why

- Notes are for the learner; an explanation framework is for the listener.
- If the framework is unstable, adding examples and analogies only makes the draft heavier and messier.

#### Output

- A repaired explanation framework or a concrete diagnosis of what must change.

### 3. Repair and enrich the teaching plan draft

#### How

- Work from the user's draft section by section.
- Add only the examples, analogies, definitions, and transitions that help the listener follow the framework.
- Make hidden assumptions explicit.
- Decide which learned details are useful now and which can be deferred.
- When possible, suggest targeted revisions instead of replacing whole sections.
- Focus each pass on the highest-leverage issue first instead of trying to fix everything at once.

#### Why

- A framework alone is too thin to teach from.
- This step closes the gap between "I understand it" and "someone else can follow it."
- User ownership stays stronger when the skill improves the draft instead of silently replacing it.

#### Output

- An improved teaching plan draft, or a list of targeted revisions when full rewriting is unnecessary.

### 4. Simplify into a lean teaching plan

#### How

- Cut repeated points, decorative jargon, low-value side trails, and early complexity.
- Check whether each section serves the main line.
- Shorten any part that could be said more clearly in fewer words.
- Keep the mechanism visible while trimming everything that does not earn its place.
- Explain what was cut or deferred when that helps the user learn how to simplify their own writing.

#### Why

- Simplification serves the audience, but it also forces the user to sort out the real priorities in their own understanding.
- A lean plan is easier to teach, easier to question, and easier to revise after rehearsal.

#### Output

- A lean teaching plan ready for audience rehearsal.

## Preferred Response Structure

This skill is an optimizer, not a default ghostwriter.
Prefer the lightest response that still helps the user move forward.

Default response order:

1. Draft diagnosis
2. Suggested revisions
3. Revised section or revised framework only where needed
4. Simplification notes when relevant

Response guidance:

- Start with what is structurally wrong before proposing rewrites.
- Prefer targeted revisions over full rewrites.
- Revise only the sections that actually need intervention when possible.
- Give feedback in small rounds, usually one issue cluster at a time.
- Do not dump every problem and every fix at once even if the user explicitly asks for a full review list.
- If the user asks for light-touch help, return diagnosis plus suggested revisions only.
- Even if the user asks for heavier or more autonomous help, you may provide stronger revisions, but still present the biggest changes step by step instead of unloading everything in one response.
- Keep the user's voice and ownership visible in the revised result.

## Structural Heuristics

There is no fixed template here. Adapt the shape to the topic, audience, and goal.
Treat the following as options and checks, not as mandatory slots.

### Common Shapes

- Concept: explain what something is or how it works.
- Process: explain how something unfolds step by step.
- Comparison: explain how nearby options differ and when to choose each one.

### Concept Checks

Useful checks:

1. Is there a plain-language thesis?
2. Is it clear why this matters?
3. Are prerequisites or definitions introduced early enough?
4. Is the core mechanism visible?
5. Is there an anchor example?
6. Are boundaries or failure cases named?
7. Is there a short recap?

### Process Checks

Useful checks:

1. Is the goal of the process clear?
2. Are inputs or starting conditions stated?
3. Are the main steps in a usable order?
4. Are decision points visible?
5. Is there an example run-through?
6. Is there a failure mode?
7. Is there a short recap?

### Comparison Checks

Useful checks:

1. Is the decision being made explicit?
2. Is the shared ground clear?
3. Are the key differences visible?
4. Is it clear when to choose each option?
5. Is there a short case example?
6. Is common confusion addressed?
7. Is there a short recap?

### Diagnosis Prompts

- Where is the main line hard to follow?
- Which term must be defined earlier?
- Where is the hidden logical bridge?
- Which section is overloaded or misplaced?
- Which detail belongs later or can be deferred?
- Is the current shape even the right one for this topic?

### Expansion Prompts

- Which example best prevents confusion?
- Which analogy adds intuition without distortion?
- Which transition is needed between these two sections?
- Which learned detail is necessary for this audience?
- Which detail is true but not useful right now?

### Simplification Checks

- Cut sections that do not serve the main line.
- Move one concrete example upward if the explanation turns abstract too early.
- Replace repeated explanation with one clearer sentence.
- Simplify only after the mechanism is visible.
- Keep the shape flexible; keep the listener path clear.

## Guardrails

- Do not restart research when the problem is structure.
- Do not mistake a list of points for a listener-friendly explanation.
- Do not add analogies that distort the mechanism.
- Do not keep every learned detail just because the user worked hard to learn it.
- Do not simplify away the core mechanism.
- Do not replace the user's draft wholesale unless the user asks for that level of intervention.
- If the framework is still unstable, repair the framework before polishing the plan.

