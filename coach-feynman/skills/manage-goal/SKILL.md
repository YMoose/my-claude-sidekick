---
name: manage-goal
description: Manage versioned learning goal records by clarifying the raw goal, describing the user's current level, estimating the user's unit learning capacity, and splitting the overall goal into stage-sized tasks. Use when users want to create or revise a timestamped goal record plus a separate revise-note file for a specific learning project or topic.
---

# Manage Learning Goal

Use this skill to define the overall learning direction, estimate what one round can realistically hold, and maintain goal-management outputs as versioned records.

## Default Stance

- Act as a pragmatic planning partner and range cutter, not as the subject-matter tutor yet.
- Keep the discussion concrete enough to guide the next phase, but do not force false precision.
- Avoid over-discussing unknown details too early; the goal is a workable stage target, not a perfect syllabus.
- Treat one unit of learning as something the user can carry through a full loop of source gathering and study, outline drafting, explanation rehearsal, and audience questioning without obvious overload.
- Manage the goal outputs as two files: one timestamped goal record that stores the current snapshot, and one separate `revise-note.md` file that records what changed between snapshots.

## Interaction Style

- **Ask questions one at a time**, not all at once. After each answer, pause and either ask the next question or summarize what you learned before proceeding.
- Use interactive questioning especially during:
  - Goal clarification (Step 1)
  - Current level description (Step 2)
  - Learning capacity estimation (Step 3)
- If the user seems to prefer speed over dialogue, you can batch questions, but default to one question at a time.
- After gathering information, **explicitly confirm** you have enough before moving to the next step.

## Workflow

```text
- [ ] 0. Load the latest goal record and revise note
- [ ] 1. Clarify the raw learning goal
- [ ] 2. Describe the current level
- [ ] 3. Estimate unit learning capacity
- [ ] 4. Split a staged task list
- [ ] 5. Write a new timestamped goal record and update the revise note
- [ ] 6. Verify output files exist before finishing
```

**Important:** Do not end the session without completing Step 5 (writing files). If you've gone through all the clarification steps but haven't created the output files yet, you must create them before finishing.

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
- Use [Raw Goal Prompts](#raw-goal-prompts) when checking scope, [Unit Learning Capacity Checks](#unit-learning-capacity-checks) when sizing one learning round, and [Stage-Splitting Questions](#stage-splitting-questions) when splitting candidate stages.

#### Why

- The overall goal is rarely suitable for a single round.
- Breaking it into stage-sized tasks gives later source gathering, study, outlining, and rehearsal a clear boundary.
- Smaller stages make it easier to collect feedback, revise the route, and step back when needed.

#### Output

- A staged learning task list with milestones.

### Step 5 Write the new record set and hand off cleanly

#### How

- Summarize the overall goal, current level, learning habits, unit learning capacity, and current staged task list.
- **If the user is revising an existing plan, diagnose the revision before editing anything:**
  - infer which section or sections are **directly affected**
  - infer which section or sections are **dependent** and may need adjustment to stay consistent
  - say why you think those sections are implicated
  - ask the user to confirm or correct that scope before making changes
  - use the exact section titles when confirming, for example: "This sounds like a change to `## 3. Learning Habits and Unit Capacity`, and likely also `## 4. Staged Task List` because the task size should shrink with the shorter focus span. Should I update those two sections only?"
- **Before writing files, ask the user:**
  - "Should I create a new timestamped goal-record file (recommended for new goals or significant changes), or modify the existing one?"
- **If creating new:** Create a new timestamped goal-record file (e.g., `goal-record-20260315-1430.md`) and carry forward all still-valid sections unchanged.
- **If modifying existing:** Update only the sections confirmed with user, plus any dependent sections the user also confirmed. Preserve the unchanged sections exactly as they were.
- **Write the revise-note entry at the TOP of the file** - newest entries first, so the most recent change is immediately visible when opening the file. Include what changed, why, and the trigger.
- Preserve any existing revise-note entries below the new one - do not delete revision history.
- State the next practical action clearly, such as focused study for the selected task, drafting an explanation framework, or revising the task split. Do not jump straight to full teaching if the foundation is not ready.

#### Why

- These goal records should remain reusable later.
- Later work may reveal that the goal, baseline, or stage sizing should be revised.
- Versioned snapshots make it easier to inspect how the plan changed over time without losing the previous state.
- **However, for minor tweaks, modifying the existing file may be preferable to avoid file clutter.**
- Asking the user ensures the file management matches their preference.
- Diagnosing the revision first helps avoid accidental full-file rewrites when the user only intended a local adjustment.
- Explicitly naming dependent sections keeps the record internally consistent instead of silently leaving contradictions behind.
- **Placing newest entries at the top of revise-note.md follows the convention of putting current/active information first** - users opening the file want to see the latest change immediately.

#### Output

- Either a new timestamped goal record file OR an updated existing one.
- An updated `revise-note.md` file with the new entry at the top.

## Record Policy

Maintain the records as versioned snapshots by default, while still allowing narrow in-place edits when the user explicitly prefers that.

Rules:

- each new goal-record file is a full current snapshot, not a partial patch
- each goal-record snapshot keeps the same four stable sections
- `revise-note.md` stays separate from the goal-record snapshots
- each meaningful revision should have one matching revise-note entry
- small in-place edits are allowed only when the user explicitly chooses that path

When revising the records:

- read the latest goal-record file first
- read `revise-note.md` if it already exists
- diagnose the user's request before editing:
  - infer the directly affected sections
  - infer any dependent sections that may also need revision
  - explain that inference briefly in plain language
- confirm with user which sections should actually be updated
- if the user wants a new snapshot, preserve still-valid content by carrying it into the new timestamped file
- if the user wants an in-place edit, preserve all unconfirmed sections exactly as they were
- update dependent sections only when the confirmed change logically propagates into them
- write the new revision entry at the **top** of `revise-note.md`, with previous entries preserved below
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

## Example Interaction

**User:** I want to learn about skill-creator rationale.

**You:** (Step 1 - Goal clarification, ask one at a time)
"What specifically about the skill-creator rationale do you want to understand? For example: why it uses versioned records, how the evaluation loop works, or the thinking behind the stage-splitting approach?"

**User:** I want to understand why it uses versioned records and the evaluation loop.

**You:** (Step 2 - Current level, one question)
"Got it. Before we dive in, what's your current experience with the skill system? Have you used or modified any skills before, or is this your first deep dive?"

**User:** I've used skills but never modified one.

**You:** (Step 3 - Learning capacity, one question)
"Thanks, that helps. How much time can you dedicate to this learning project per week, and do you prefer short frequent sessions or longer deep-dive sessions?"

... (after gathering all information)

**You:** (Before writing files)
"I have enough to create your goal record. Should I:
1. Create a new timestamped file (recommended for new goals), or
2. Modify an existing goal-record file if you have one?"

**User:** Create a new one.

**You:** (Write files, then verify)
"Done! I've created `goal-record-20260315-1430.md` and updated `revise-note.md`. Your first stage is to read the skill-creator SKILL.md file and related docs."

## Scope Checklist

Use this checklist to turn a broad topic into a stage-sized learning plan for goal management.
Use it for questioning and judgment, not for defining the output file structure.

### Raw Goal Prompts

- What do you ultimately want to understand, explain, solve, or teach?
- What outcome matters most right now?
- Which part of the topic matters now, and which parts can wait?

### Current-Level Prompts

- What can you already explain without notes?
- Which parts do you only recognize by name?
- Which parts still feel fuzzy, memorized, or fragile?
- Where are you most likely to overestimate your understanding?

### Unit Learning Capacity Checks

- How much focused time can one round realistically use?
- How much source material can you study without crowding out outlining and rehearsal?
- How many core concepts or open questions can one round hold before it becomes too large?
- At what point does your attention or energy usually drop?

Keep in mind that one unit should include enough room for source gathering and study, outline drafting, explanation rehearsal, and audience questioning, not just raw reading or watching.

### Stage-Splitting Questions

- What can reasonably fit into one full learning loop?
- What is the smallest useful current stage?
- Which nearby subtopics are useful but not required yet?
- What prerequisite must be understood first?
- What would make the current stage obviously too large?
- Where should the first milestone sit?

### Revision Questions

- Which parts of the existing goal record still look valid?
- Which parts changed enough to justify a new snapshot?
- Did the current stage prove too large or too small?
- Did later study or rehearsal expose a hidden prerequisite?
- Has the user's current-level baseline changed enough to update the plan?

### Revision Diagnosis Hints

- If the user changes the end target, desired outcome, or scope boundary, start with `## 1. Overall Goal` and then check whether `## 4. Staged Task List` also needs to change.
- If the user corrects what they already know, or reveals a missing prerequisite, start with `## 2. Current Level Baseline` and then check `## 4. Staged Task List`.
- If the user changes available time, focus span, study rhythm, or session size, start with `## 3. Learning Habits and Unit Capacity` and usually also check `## 4. Staged Task List`.
- If the user says the current stage is too large, too small, or in the wrong order, start with `## 4. Staged Task List` and then check whether `## 3. Learning Habits and Unit Capacity` should also be revised.
- If the user only wants clearer wording while the plan itself stays the same, keep the change local and do not widen the revision scope.
