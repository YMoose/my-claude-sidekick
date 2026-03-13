---
name: optimize-claude-md
description: Optimize CLAUDE.md files by extracting knowledge into separate files and maintaining a clean index. Use when users ask to (1) optimize or reorganize CLAUDE.md, (2) update the knowledge index, (3) clean up a bloated CLAUDE.md, or (4) set up knowledge file structure for a project.
---

# Optimize CLAUDE.md

Analyze CLAUDE.md first then optimize it by extracting knowledge into separate files when needed.

## Workflow

1. **Determine project root** - Use `--path` argument or current working directory
2. **Analyze CLAUDE.md** - Assess if optimization is needed (see [criteria](references/criteria.md))
3. **Report findings** - Show analysis and recommendation to user
4. **Get confirmation** - Ask user before making any changes
5. **Execute changes** - Only after user approval

## Error Handling

- If `./knowledge/` dir or `docs` dir doesn't exist, create it (after confirmation)
- If no `.md` files found, create empty index
- If CLAUDE.md can't be parsed, preserve raw content and append index section

## Tips for Better Adherence in CLAUDE.md

- Add emphasis (e.g., "IMPORTANT" or "YOU MUST") to critical instructions
- If Claude ignores a rule despite having it, the file is probably too long
- If Claude asks questions answered in CLAUDE.md, the phrasing might be ambiguous
- tell user to treat CLAUDE.md like code: review when things go wrong, prune regularly