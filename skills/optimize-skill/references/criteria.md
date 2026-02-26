# Skill Optimization Criteria

## Core Principles

- **Key question**: "Would removing this make the skill less effective?" If not, cut it.
- Skills should be focused on a single, well-defined purpose
- Instructions should be specific enough that Claude knows exactly what to do
- Avoid duplicating information that Claude already knows or can infer
- Skills are loaded on demand - they don't need to cover every edge case

## Frontmatter Requirements

### Name
- Use kebab-case (e.g., `optimize-skill`, not `Optimize Skill`)
- Should be action-oriented and descriptive
- Keep it short (2-4 words)

### Description
- Start with a brief summary of what the skill does
- Include trigger conditions using "Use when users ask to..."
- Add "Triggered by phrases like..." for keyword matching
- Keep total description under 3 sentences

**Good example:**
```yaml
description: Optimize Claude Code skills by analyzing structure and content quality. Use when users ask to (1) optimize a skill, (2) review skill quality, or (3) restructure a skill. Triggered by phrases like "optimize skill", "improve skill", "review skill".
```

**Bad example:**
```yaml
description: This skill helps you make your skills better.
```

## Content Structure

### Required Sections

1. **Title** - H1 matching the skill name
2. **Brief intro** - 1-2 sentences explaining purpose
3. **Workflow** - Numbered steps with clear actions
4. **Additional sections** as needed

### Section Organization

Order sections by importance:
1. Workflow (most important)
2. Key concepts/format specs
3. Error handling
4. Tips and best practices
5. References to other files

## What to Include vs Exclude

### ✅ Include

- Specific tool usage patterns
- File format specifications
- Decision criteria and heuristics
- Common pitfalls and how to avoid them
- Examples of input/output formats
- Error handling for likely failures

### ❌ Exclude

- General programming knowledge
- Tool documentation that Claude already knows
- Verbose explanations of concepts
- Long lists of edge cases (link to reference instead)
- Tutorial-style content

## Workflow Guidelines

### Step Format

Use consistent format for workflow steps:

```markdown
1. **Action name** - Brief description with tool/condition
```

**Good:**
```markdown
1. **Read file** - Use Read tool to examine current content
2. **Analyze structure** - Check for required sections
```

**Bad:**
```markdown
1. First, you should read the file
2. Then analyze it
```

### Step Count

- Aim for 4-7 workflow steps
- If more steps needed, consider splitting the skill
- Each step should be a distinct, meaningful action

### Conditional Steps

Mark optional or conditional steps clearly:

```markdown
4. **Update flowchart** (optional) - If mermaid diagram exists, regenerate it
5. **Handle errors** - Only if previous step failed
```

## Reference Files

### When to Create References

Create reference files when:
- Content exceeds 50 lines and is not core workflow
- Detailed criteria or heuristics are needed
- Multiple examples would clutter main file
- Content is educational rather than instructional

### Reference Directory Structure

```
skill-name/
├── SKILL.md           # Main skill file
├── references/        # Detailed reference content
│   ├── criteria.md    # Evaluation criteria
│   ├── guide.md       # Detailed how-to guides
│   └── examples.md    # Extended examples
├── examples/          # Example files
│   └── sample.ext
└── scripts/           # Helper scripts
    └── helper.py
```

## Quality Indicators

### Signs of a Good Skill

- **Clear purpose** - One specific task, well-defined
- **Actionable** - Claude knows exactly what to do
- **Self-contained** - Minimal need to read other files
- **Appropriate length** - 50-150 lines for main file
- **Good triggers** - Clear when to use the skill

### Signs of a Skill Needing Optimization

- **Multiple purposes** - Trying to do too many things
- **Vague instructions** - "Handle the data appropriately"
- **Excessive length** - Over 200 lines in main file
- **Missing triggers** - No clear use cases in description
- **Redundant content** - Repeating Claude's built-in knowledge

## Anti-Patterns

### 1. Kitchen Sink Skill
One skill trying to do everything related to a domain.

**Fix:** Split into focused skills with clear boundaries.

### 2. Tutorial Skill
Long explanations of concepts rather than actionable instructions.

**Fix:** Move educational content to references, keep instructions in main file.

### 3. Over-Specified Skill
Every possible edge case documented.

**Fix:** Cover common cases, let Claude handle edge cases intelligently.

### 4. Under-Specified Skill
Vague instructions that leave too much to interpretation.

**Fix:** Add specific examples, clear criteria, and explicit tool usage.

### 5. Orphaned Content
References to files that don't exist or commands that won't work.

**Fix:** Verify all references and test all commands.

## Optimization Process

1. **Read and understand** the current skill
2. **Identify the core purpose** - what is this skill really for?
3. **Check against criteria** - mark issues found
4. **Propose specific changes** - not just "make it better"
5. **Get user approval** before making changes
6. **Apply changes** and verify

## Measurement

A skill is well-optimized when:
- Claude uses it correctly without clarification
- The skill produces consistent results
- The main file is under 150 lines
- All references and examples work
- The description accurately captures when to use it
