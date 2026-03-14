# Revise Note Template

Use this template for the separate revision-history file.

## File Name

```text
revise-note.md
```

Keep one `revise-note.md` file and append a new entry whenever a new timestamped goal-record snapshot is created.

## Purpose

This file records what changed for each goal-record snapshot and why that snapshot was necessary.

## Recommended Structure

```markdown
# Revise Note

## goal-record-YYYYMMDD-HHMM.md
- Changed sections: ...
- What changed: ...
- Why: ...
- Trigger: ...
```

## Entry Rules

Each entry should capture:

- which goal-record snapshot this note belongs to
- which sections changed
- what changed in practical terms
- why the change was necessary
- what triggered the change

## Typical Triggers

- the user understands more than before
- the user was less prepared than the baseline suggested
- the current stage proved too large or too small
- later source study exposed hidden prerequisites
- rehearsal exposed missing concepts, weak examples, or unrealistic pacing
- the user's available time or energy changed

## Good Notes

Prefer concise notes such as:

```markdown
## goal-record-20260314-1530.md

- Changed sections: Current Level Baseline, Staged Task List
- What changed: narrowed the current stage from topic X to prerequisite Y
- Why: later study showed Y was required before X
- Trigger: hidden prerequisite discovered during source gathering
```
