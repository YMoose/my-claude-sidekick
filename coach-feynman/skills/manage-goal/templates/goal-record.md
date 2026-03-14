# Goal Record Template

Use this template for the timestamped goal-record snapshot file.

## Naming Rule

The actual output file should use this naming pattern:

```text
goal-record-YYYYMMDD-HHMM.md
```

Guidelines:

- use the local date and time when the snapshot is created
- create a new file for each meaningful revision
- keep older snapshot files as history
- do not place revision notes inside this file

## Purpose

This file stores the current planning snapshot for the learning cycle in one place.

## Recommended Structure

```markdown
# Goal Record

## 1. Overall Goal
...

## 2. Current Level Baseline
...

## 3. Learning Habits and Unit Capacity
...

## 4. Staged Task List
...
```

Keep the section titles stable so later snapshots are easy to compare.

## Section Requirements

### 1. Overall Goal

Record at least:

- the overall learning goal
- the intended result or use case
- important scope boundaries
- what is intentionally not covered yet

### 2. Current Level Baseline

Record at least:

- what the user can already explain
- what the user only vaguely recognizes
- what the user does not understand yet
- fragile or misleading areas

### 3. Learning Habits and Unit Capacity

Record at least:

- available time or time budget
- preferred learning style or study rhythm
- attention and energy constraints
- unit learning capacity
- overload warning signs

When recording unit learning capacity, use one or more lenses such as:

- time budget
- source-material volume
- number of core concepts
- number of open questions
- likely attention drop-off point

### 4. Staged Task List

Record at least:

- the current stage
- the ordered stage task list
- milestones
- prerequisites or dependencies between stages
- notes on why the current stage size was chosen

## Snapshot Policy

When revising the record:

1. Read the latest goal-record snapshot first.
2. Preserve still-valid content.
3. Create a new timestamped file instead of overwriting the old one.
4. Keep the four section titles stable.
5. Write revision history in `revise-note.md`, not here.

## Consistency Rules

Check these relationships explicitly:

- the staged task list must point toward the overall goal
- the current-level baseline must justify why the current stage starts where it does
- the unit capacity estimate must justify why the current stage is this size

If two sections disagree, repair the disagreement instead of leaving it implicit.
