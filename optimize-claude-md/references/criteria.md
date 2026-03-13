# CLAUDE.md Criteria

## Core Principles

- **Key question**: "Would removing this cause Claude to make mistakes?" If not, cut it.
- LLMs can follow ~150-200 instructions; Claude Code's system prompt already has ~50
- As instruction count increases, instruction-following quality decreases **uniformly**
- Bloated CLAUDE.md files cause Claude to ignore your actual instructions
- Rules get lost in the noise when the file is too long
- CLAUDE.md goes into every session. Only include what's relevant to ALL tasks.

## What to Include vs Exclude

### ✅ Include

- Bash commands Claude can't guess
- Code style rules that differ from defaults
- Testing instructions and preferred test runners
- Repository etiquette (branch naming, PR conventions)
- Architectural decisions specific to your project
- Developer environment quirks (required env vars)
- Common gotchas or non-obvious behaviors

### ❌ Exclude

- Anything Claude can figure out by reading code
- Standard language conventions
- Detailed API documentation (link instead)
- Information that changes frequently
- Long explanations or tutorials
- File-by-file descriptions
- Self-evident practices like "write clean code"

## When to Recommend Splitting

Extract content if CLAUDE.md has:

- **Too long** - Rules getting lost in noise
- **Task-specific instructions** - Content only relevant to certain tasks
- **Code style guidelines** - Should use linters, not CLAUDE.md
- **Code snippets** - Prefer `file:line` references
- **Detailed docs** - Link instead of embedding

## When CLAUDE.md is Already Good

No changes needed if:

- **Concise** - Only universally applicable content
- **Covers WHAT, WHY, HOW** - tech/stack, project purpose, how to work
- **Uses progressive disclosure** - links to separate docs for task-specific info

## Progressive Disclosure Patterns

CLAUDE.md serves as an overview that points Claude to detailed materials as needed.

### Pattern 1: High-level guide with references

Keep main content in CLAUDE.md, link to details:

```markdown
## Advanced topics
- **Testing**: See [TESTING.md](docs/TESTING.md)
- **Architecture**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **API reference**: See [API.md](docs/API.md)
```

### Pattern 2: Domain-specific organization

For projects with multiple domains, list domains with brief descriptions so Claude knows which to read:

```
docs/
├── frontend.md    # UI components, styling
├── backend.md     # API, database
├── testing.md     # Test conventions
└── deployment.md  # CI/CD, environments
```

### Pattern 3: Conditional details

Show basic content inline, link to advanced content:

```markdown
## Database queries

For simple queries, use the standard patterns.

**For complex aggregations**: See [COMPLEX_QUERIES.md](docs/COMPLEX_QUERIES.md)
**For migrations**: See [MIGRATIONS.md](docs/MIGRATIONS.md)
```

## Reference Structure Rules

### Avoid deeply nested references

Claude may partially read files when they're referenced from other referenced files.

**Keep references one level deep from CLAUDE.md.** Most reference files should link directly from CLAUDE.md.

### Structure longer reference files with table of contents

For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope even when previewing with partial reads.

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns

## Authentication and setup
...

## Core methods
...
```

## Anti-Patterns to Flag

- **Over-specified CLAUDE.md** → Ruthlessly prune; if Claude already does something correctly without the instruction, delete it
- **Code style guidelines** → Use linters/formatters instead
- **Hotfix appendages** → Remove behavior patches, fix root cause
- **Verbose examples** → Use references, not copies
- **Deeply nested references** → Flatten to one level from CLAUDE.md

## References

1. [Write An Effective CLAUDE.md](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)
2. [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
3. [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
