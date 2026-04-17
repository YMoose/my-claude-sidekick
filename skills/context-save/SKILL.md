---
name: context-save
description: Save, export, or anchor-filter a Claude session context on disk. Use this skill whenever the user asks to save context, export or archive the current chat, back up the session before `/clear`, or keep only the part of a saved session starting from a specific conversation block. Default to the bundled scripts instead of manually copying from `~/.claude/projects/`.
compatibility: Requires `python3` and read access to `~/.claude/projects/`.
---

# Context Save

Use the bundled scripts instead of manual file copying or ad hoc JSONL edits.

## Inputs

- The user request may include:
  - which conversation block to keep, described in natural language
  - where to export the saved context
- For export-only requests, focus on the destination path.
- For partial-context requests, first interpret the user's description of the block they want to keep, then locate the matching anchor from the exported session.
- If the user does not provide an export path, the export script defaults to the current Claude working directory.
- In normal skill execution, the skill runtime substitutes `$CLAUDE_SESSION_ID` into the command before running the script.

## Workflow

### 1. Export the current session

From this skill directory, run:

```bash
python3 scripts/save_context.py --session-id $CLAUDE_SESSION_ID -o <export-path>
```

In skill runtime, `$CLAUDE_SESSION_ID` in the command above is replaced before `save_context.py` runs. The script itself expects an explicit `--session-id`.

When no export path is provided, the exported session is saved directly under the current Claude working directory as `./<session-id>/`.

This creates `<destination>/<session-id>/` with:

- the main `session-id.jsonl`
- the copied `session-id/` companion directory when present

### 2. If the user wants only part of the session, locate the anchor and filter the export

#### 2.1 List anchor candidates

Run:

```bash
python3 scripts/filter_context.py <exported-session-dir> --list-anchors
```

The script prints JSON candidates. Only use anchors that represent the start of a whole conversation block:

- normal user messages
- command messages
- compaction-summary user messages

Do not anchor on:

- `tool_result` user messages
- IDE-injected messages such as `<ide_opened_file>` and `<ide_selection>`
- arbitrary middle-of-block assistant/tool activity

If the user's description is ambiguous, show 2-3 candidate anchors and ask them to confirm one UUID.

#### 2.2 Filter by the chosen anchor

After the user confirms an anchor UUID, the script should usually operate on the current exported session by creating a new filtered replacement first:

```bash
python3 scripts/filter_context.py <exported-session-dir> --anchor-uuid <uuid> -o <output-dir>
```

`-o` is an output root directory, not the final session directory. The filtered result is written to `<output-dir>/<session-id>/`. If you omit `-o`, the script defaults to the current working directory and writes the filtered result to `./<session-id>/`.

The filter script:

- keeps the selected anchor and its descendant transcript messages
- never splits a conversation block in the middle
- preserves the exported session structure needed for the filtered result
- first writes the filtered result into a new temporary copy
- after success, removes the previous exported session directory and keeps the new filtered one in its place

So this is not a true in-place edit of the files. It is a replacement flow on the exported copy when the final target directory matches the current exported session directory, which is still safe because the exported copy is already separate from the live Claude session under `~/.claude/projects/`.

If you pass `-o` and point it somewhere else, the script writes a separate filtered copy instead.

### 3. Summarize the result

On success, report:

- the exact export or filtered directory
- whether the main transcript was copied or filtered
- whether the companion session directory was copied

Do not claim the context was cleared.

### 4. Offer `/clear`

After a successful export, suggest `/clear` as an optional next step:

- explain that the session is now saved on disk and `/clear` can start a fresh context for a new task
- explain that they can also keep going in the current session if they want to continue from the existing context
- tell the user to run `/clear` themselves if they want a fresh window

Do not auto-clear and do not present `/clear` as required.

## Failure Handling

- If the script cannot find the transcript, inspect [references/session-structure.md](references/session-structure.md) to help the user locate the right session.
- If the destination cannot be created or written, suggest a writable path such as `/tmp/...` or a directory under the user's home folder.
- If the filter script rejects the anchor, rerun `--list-anchors` and choose a candidate UUID instead of manually editing the JSONL.

## Read Next Only When Needed

- [references/session-structure.md](references/session-structure.md) for Claude session storage layout, anchor rules, and baseline snapshot behavior
