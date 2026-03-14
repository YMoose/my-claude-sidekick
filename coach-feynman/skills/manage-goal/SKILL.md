---
name: manage-goal
description: Manage versioned learning goal records by clarifying the raw goal, describing the user's current level, estimating the user's unit learning capacity, and splitting the overall goal into stage-sized tasks. Use when users want to create or revise a timestamped goal record plus a separate revise-note file for the current learning cycle.
---

# Manage Learning Goal

Use this skill to define the overall learning direction, estimate what one round can realistically hold, and maintain goal-management outputs as versioned records.

## Default Stance

- Act as a pragmatic planning partner and range cutter, not as the subject-matter tutor yet.
- Keep the discussion concrete enough to guide the next phase, but do not force false precision.
- Avoid over-discussing unknown details too early; the goal is a workable stage target, not a perfect syllabus.
- Treat one unit of learning as something the user can carry through a full loop of source gathering and study, outline drafting, explanation rehearsal, and audience questioning without obvious overload.
- Manage the goal outputs as two files: one timestamped goal record that stores the current snapshot, and one separate `revise-note.md` file that records what changed between snapshots.

## Workflow

```text
- [ ] 0. Load the latest goal record and revise note
- [ ] 1. Clarify the raw learning goal
- [ ] 2. Describe the current level
- [ ] 3. Estimate unit learning capacity
- [ ] 4. Split a staged task list
- [ ] 5. Write a new timestamped goal record and update the revise note
```

### Step 1 Clarify the raw learning goal

#### How

- Ask what the user wants to eventually understand, explain, solve, or teach.
- Ask what result they want from learning this topic.
- Turn the raw intention into a clearer goal definition without forcing excessive detail.

#### Why

- A raw learning goal is often vague, oversized, or framed too broadly to guide the next phases.
- Clarifying the goal creates a usable direction for later diagnosis, source collection, and stage splitting.
- Do not push this too far; the user's understanding is still shallow and the goal may shift as learning progresses.

#### Output

- A clearer definition of the overall learning goal.

### Step 2 Describe the current level

#### How

- Discuss the user's current foundation from multiple angles.
- Help them separate:
  - what they can already explain
  - what they only vaguely recognize
  - what they do not understand yet
- Keep the pass lightweight; capture a useful baseline rather than a full audit.

#### Why

- Without a baseline, the agent cannot estimate the gap between the user and the target.
- Later source collection, source study, and stage planning become unfocused if the current level is unknown.
- Over-analyzing at this point wastes time; finer detail can be filled in during later learning.

#### Output

- A practical description of the user's current knowledge level.

### Step 3 Estimate learning habits and unit learning capacity

#### How

- Ask about the user's learning habits, available time, attention patterns, and preferred ways of learning.
- Estimate the user's unit learning capacity together with them.
- Treat unit learning capacity as the amount of content the user can plausibly carry through one loop of source gathering and study, outline drafting, explanation rehearsal, and audience questioning.
- Describe this capacity with one or more dimensions such as:
  - learning time
  - source-material volume
  - number of open questions
  - number of core concepts
- Reserve room for the effort needed in later outline-building, explanation, and questioning.

#### Why

- Stage tasks cannot be split by topic size alone; they also depend on the user's real pace, energy, and attention cost.
- The point is to keep one round in a zone that still moves forward without obvious overload.
- If the unit is too large, the user is more likely to accumulate frustration, feel increasingly unable to learn the topic, and lose the desire to continue.
- Unit learning capacity is not fixed; it can be learned, adjusted, and improved over time.

#### Output

- A description of the user's learning habits.
- A working estimate of unit learning capacity.

### Step 4 Split a staged learning task list

#### How

- Combine the clearer goal definition, the current-level baseline, and the unit learning capacity estimate.
- Use the current level as the starting point and the clearer goal as the direction.
- Split the path into stage-sized learning tasks with milestones.
- Use [references/scope-checklist.md](references/scope-checklist.md) when the user needs help checking scope or splitting stages.

#### Why

- The overall goal is rarely suitable for a single round.
- Breaking it into stage-sized tasks gives later source gathering, study, outlining, and rehearsal a clear boundary.
- Smaller stages make it easier to collect feedback, revise the route, and step back when needed.

#### Output

- A staged learning task list with milestones.

### Step 5 Write the new record set and hand off cleanly

#### How

- Summarize the overall goal, current level, learning habits, unit learning capacity, and current staged task list.
- Create a new timestamped goal-record file instead of overwriting the previous snapshot.
- Append a concise entry to `revise-note.md` describing what changed and why.
- State the next phase as source collection and study for the current stage, not full explanation yet.

#### Why

- These goal records should remain reusable later.
- Later work may reveal that the goal, baseline, or stage sizing should be revised.
- Versioned snapshots make it easier to inspect how the plan changed over time without losing the previous state.

#### Output

- A new timestamped goal record file.
- An updated `revise-note.md` file.

## Record Policy

Maintain the records as versioned snapshots rather than as one overwritten file.

Rules:

- each new goal-record file is a full current snapshot, not a partial patch
- each goal-record snapshot keeps the same four stable sections
- `revise-note.md` stays separate from the goal-record snapshots
- each new snapshot should have one matching revise-note entry

When revising the records:

- read the latest goal-record file first
- read `revise-note.md` if it already exists
- preserve still-valid content by carrying it into the new snapshot
- create a new timestamped goal-record file instead of overwriting the old one
- append one concise revision entry to `revise-note.md`
- avoid collapsing revision notes back into the goal-record file

## Output Format

Produce two files:

- `goal-record-YYYYMMDD-HHMM.md`
- `revise-note.md`

Use the bundled templates for the exact file structure:

- [templates/goal-record.md](templates/goal-record.md)
- [templates/revise-note.md](templates/revise-note.md)

## Guardrails

- Do not accept a scope so broad that later teach-back will collapse.
- Do not force detailed discussion of a domain the user barely knows yet.
- Do not turn goal-setting into deep research.
- Do not fake precision; if the goal is still blurry, keep narrowing it.
- Do not size the current stage without accounting for later source study, outline drafting, and rehearsal effort.
- Do not overwrite an older goal-record snapshot when the change is meaningful enough to deserve a new version.
- Do not merge revision history back into the main goal-record file.
- Prefer one strong subgoal over an impressive but unusable plan.

## Resources

- Use [references/scope-checklist.md](references/scope-checklist.md) when checking scope, estimating unit learning capacity, or splitting candidate stages.
