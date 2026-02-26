---
name: optimize-skill
description: Optimize Claude Code skills by analyzing structure, content quality, and adherence to best practices. Use when users ask to (1) optimize or improve a skill, (2) review skill quality, (3) restructure a bloated skill, or (4) create high-quality skills from existing content.
---

# Optimize Skill

Analyze and optimize Claude Code skills (SKILL.md files) by applying best practices and restructuring when needed.

## Workflow

1. **Identify target skill** - Use `--path` argument or ask user which skill to optimize
2. **Analyze SKILL.md** - Assess current state against [criteria](references/criteria.md)
3. **Report findings** - Show analysis with specific issues and recommendations
4. **Get confirmation** - Ask user before making any changes
5. **Execute changes** - Only after user approval

## Analysis Checklist

When analyzing a skill, check for:

### Structure
- [ ] Has proper frontmatter (name, description)
- [ ] Description is clear and includes trigger conditions
- [ ] Logical flow from overview to details
- [ ] Sections are well-organized

### Content Quality
- [ ] Instructions are specific and actionable
- [ ] Avoids redundancy and repetition
- [ ] Uses examples where helpful
- [ ] Links to references instead of embedding long content

### Best Practices
- [ ] Skill has a single, clear purpose
- [ ] Workflow steps are sequential and complete
- [ ] Error handling is documented
- [ ] Tips section provides practical guidance

### Maintainability
- [ ] Complex details moved to references/
- [ ] Scripts are in scripts/ directory
- [ ] Examples are in examples/ directory

## Common Optimizations

### 1. Split Large Skills
If SKILL.md exceeds 150 lines, consider:
- Moving detailed criteria to `references/criteria.md`
- Moving examples to `examples/` directory
- Moving step-by-step guides to `references/guide.md`

### 2. Improve Triggers
Enhance description with trigger phrases:
```yaml
description: Short description. Use when users ask to (1) action one, (2) action two, or (3) action three. Triggered by phrases like "keyword", "another keyword".
```

### 3. Clarify Workflow
Make steps more specific:
```markdown
## Workflow

1. **Step name** - Specific action with tool reference
2. **Next step** - Clear condition or action
```

### 4. Add Error Handling
Document common failure cases:
```markdown
## Error Handling

- If file not found: specific recovery action
- If parse fails: specific recovery action
```

## Output Format

After analysis, provide a structured report:

```markdown
## Skill Analysis: {skill-name}

### Summary
{brief assessment}

### Issues Found
1. **{category}**: {specific issue}
   - Recommendation: {how to fix}

### Strengths
- {what the skill does well}

### Recommended Changes
{list of specific edits or restructuring}
```

## References

- [Skill Criteria](references/criteria.md) - Detailed evaluation criteria
