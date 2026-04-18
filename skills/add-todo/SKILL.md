---
name: add-todo
description: Add new todo items to task tracking files (todos.md) with dependency tracking. Use when the user wants to add a new task, track dependencies between tasks, or update their task tracking file. Triggered by phrases like "add a todo", "new task", "track this task", or when working with todos.md files. Also triggers when marking tasks as done - completed tasks are automatically removed from the mermaid graph.
---

# Add Todo

Add new tasks to task tracking file with YAML/JSON structure and optional mermaid flowchart.

## Workflow

1. **Read file**: Read current task tracking file to understand context
2. **Understand task**: Clarify new task's purpose and scope
3. **Identify dependencies**: Check if task depends on or blocks existing tasks (ask if unclear)
4. **Update data**: Add task to YAML/JSON section using Edit tool
5. **Update flowchart and relations(optional)**: If mermaid exists, run generate_mermaid.py and update both the mermaid diagram **and** the relations section in YAML.
   - The script outputs mermaid first, then `---FILTERED_RELATIONS---` followed by the filtered relations YAML.
   - Replace the YAML `relations:` section with the filtered output so relations and mermaid edges stay in sync.
6. **Confirm**: Verify update with user

## File Format

Task tracking files use this structure:

```yaml
nodes:
    - "task name":
        state:        # required: task status
        create_time:  # required: creation timestamp
        finish_time:  # optional
        ...           # other infos
relations:
    - ["prerequisite task", "dependent task"]
```

Optional mermaid diagram:

```mermaid
flowchart TD
    id[task name]
    id1 --> id2
```

## Script

### generate_mermaid.py

Generate mermaid from YAML/JSON string:

```bash
python scripts/generate_mermaid.py '<yaml_or_json_string>'
```

**Note**: The script outputs two sections separated by `---FILTERED_RELATIONS---`:
1. Mermaid flowchart (done nodes excluded)
2. Filtered relations YAML (only relations between active nodes)

Use both outputs to update the tracking file — replace the mermaid block **and** the relations section so they stay consistent.

Example with YAML:
```bash
python scripts/generate_mermaid.py 'nodes:
    - "task A":
        state: done
    - "task B":
        state: pending
relations:
    - ["task A", "task B"]'
```

Output (task A excluded):
```
flowchart TD
    id0["task B"]

---FILTERED_RELATIONS---

```
(No relations remain because task A is done.)

Example with JSON:
```bash
python scripts/generate_mermaid.py '{"nodes":[{"name":"task A"},{"name":"task B"}],"relations":[["task A","task B"]]}'
```

