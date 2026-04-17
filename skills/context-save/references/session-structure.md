# Claude Code Session File Structure

Read this file when the export script cannot find the session automatically, or when you need to explain where Claude stores transcripts, companion files, and anchor-based filtered exports.

## JSONL Transcript File

Location: `~/.claude/projects/<sanitized-cwd>/<session-id>.jsonl`

The sanitized CWD path replaces `/` with `-` and prepends `-`. For example:
- CWD `/home/ye/yzh/engineering` → `-home-ye-yzh-engineering`
- Full path: `~/.claude/projects/-home-ye-yzh-engineering/<uuid>.jsonl`

Each line in the JSONL file is a separate JSON object. Key entry types:

### Permission Mode Entry
```json
{"type":"permission-mode","permissionMode":"default","sessionId":"<uuid>"}
```

### File History Snapshot
```json
{"type":"file-history-snapshot","messageId":"<uuid>","snapshot":{...}}
```

### User Message
```json
{
  "parentUuid": null,
  "type": "user",
  "message": {"role": "user", "content": "..."},
  "uuid": "<uuid>",
  "timestamp": "..."
}
```

### Assistant Message
```json
{
  "parentUuid": "<parent-uuid>",
  "type": "assistant",
  "message": {
    "role": "assistant",
    "content": [{"type": "text", "text": "..."}, {"type": "tool_use", ...}],
    "model": "...",
    "id": "msg_..."
  },
  "uuid": "<uuid>",
  "timestamp": "..."
}
```

### Message Chain

Messages form a tree via `uuid` + `parentUuid`. The conversation chain is walked leaf→root via `buildConversationChain()`. Branching is supported (multiple children of the same parent).

For anchor filtering, treat only these entries as transcript messages:

- `user`
- `assistant`
- `attachment`
- `system`

`progress`, `queue-operation`, and `file-history-snapshot` entries are not part of the `parentUuid` chain.

## Anchor Filtering Rules

When preparing a filtered copy from a saved session:

- The anchor must be a main-transcript user message `uuid`.
- Valid anchor candidates are:
  - normal user messages
  - command-message user messages
  - compaction-summary user messages
- Invalid anchors include:
  - `tool_result` user messages
  - IDE-injected messages such as `<ide_opened_file>` and `<ide_selection>`
  - arbitrary mid-block assistant or tool activity

Filtering keeps:

- the anchor itself
- all descendant transcript messages whose `parentUuid` chain stays under that anchor
- the very first transcript message as a preserved root if the anchor is not already the first transcript message

If the first transcript message is preserved as a root, rewrite `anchor.parentUuid` to that root message's `uuid`.

## File History Snapshot Rules

`file-history-snapshot` entries do not have their own `uuid` and do not participate in the transcript chain.

For a filtered copy:

- Scan backward from the anchor in original JSONL line order.
- The nearest earlier `file-history-snapshot` becomes the baseline snapshot.
- Rewrite both:
  - the outer `messageId`
  - the inner `snapshot.messageId`
  to the anchor `uuid`.
- Normalize that baseline snapshot to `isSnapshotUpdate: false`.
- Delete older pre-anchor snapshots.
- Keep post-anchor snapshots only when their outer `messageId` still points to a kept transcript message.

This makes the filtered export start with a usable file-history baseline without keeping the full old snapshot history.

### Source Directory Information Inside JSONL

Besides the sanitized project directory in the file path, the transcript content itself may also contain the original source directory information.

Common places to look:

- Top-level `cwd` fields on many `user`, `assistant`, and tool-result entries
- Absolute paths embedded in `message.content`
- Tool inputs such as `file_path`, `path`, or shell command arguments
- Tool results that echo file paths back into the transcript

In practice, this means a session file may still reveal the original workspace path even after you only look at or copy the outer `~/.claude/projects/<sanitized-cwd>/...` location.

## Session Directory

Location: `~/.claude/projects/<sanitized-cwd>/<session-id>/`

May contain:

### `subagents/` Directory
Sub-agent transcript files from the Agent tool / teammate spawning:
- `agent-<id>.jsonl` — sub-agent conversation transcript (same JSONL format)
- `agent-<id>.meta.json` — sub-agent metadata (parent session, agent name, etc.)

For a filtered export, keep only the subagent files whose `agentId` is still referenced by the kept main transcript.

`subagents/*.jsonl` may contain even more explicit path information than the parent transcript because subagent prompts often include:

- the parent task's working directory via `cwd`
- skill file paths
- workspace or output paths
- tool inputs and tool results that reference absolute file locations

### `tool-results/` Directory
Cached tool execution output:
- `call_<id>.txt`, `<hash>.txt`, or similar persisted output files

When filtering a saved export, keep only tool-result files whose filenames still appear inside the kept main transcript or inside the kept subagent JSONL files.

## Metadata Files

In the same project directory:
- `title` — session title (appended, takes last entry)
- `tags` — session tags (appended)
- `<session-id>.jsonl` — the main transcript

## Portability Note

If you plan to move, replay, or sanitize a saved session, changing only the outer sanitized directory name is usually not enough. You may also need to rewrite embedded paths inside:

- `<session-id>.jsonl`
- `subagents/*.jsonl`
- any copied tool results that preserve path-like content
