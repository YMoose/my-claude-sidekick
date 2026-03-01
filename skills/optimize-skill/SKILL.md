---
name: optimize-skill
description: Optimize Claude Code skills by analyzing structure, content quality, and adherence to best practices. Use when users ask to (1) optimize or improve a skill, (2) review skill quality, (3) restructure a bloated skill, or (4) create high-quality skills from existing content.
---

# Optimize Skill

Analyze and optimize Claude Code skills by applying best practices and restructuring when needed.

## Workflow
Copy this checklist to track your progress:

```
- [ ] Step 1: Identify target skill
- [ ] Step 2: Validate the full set against the guideline
- [ ] Step 3: Refine each part of skills (SKILL.md/supporting documents/scripts)
- [ ] Step 4: Present a structured report
```

### Step 1: Identify target skill

Use `--path` argument or ask user which skill to optimize

### Step 2: Validate the full set against the guideline

1. **Remove redundancy, Concise is key** - llm is already very smart and knows most of gereral knowledge. Challenge directly on uncertain info by ask llm "Can I assume Claude knows this?", delete it if llm knows. 
2. **Use consistent terminology** - Choose one term and use it throughout all the documents.
3. **Avoid time-sensitive information** - Keep a working version, include old/compatible versions as appendices.
4. **Avoid Windows-style paths** - Use forward slashes `/` in all file paths for cross-platform compatibility.
5. **Avoid offering too many options** - When describing tools or methods, recommend a default approach instead of listing multiple alternatives.
6. **Only proceed when all requirements are met**

### Step 3: Refine each part of skills

A skill is a folder containing:
- SKILL.md (required): Instructions in Markdown with YAML frontmatter
- linked documents (optional): Supporting documentation loaded as needed
- tools (optional): Executable code (Python, Bash, etc.) and MCP

**Workflow for each part**:

1. If it's SKILL.md -> Use [validate_frontmatter](scripts/validate_frontmatter.py) to validate its frontmatter.
2. Refine the current part following its own best-practices:
   - 
   - Checklist
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met

### Step 4: Present a structured report

Output a summary of completed changes and the rationale behind each decision. No further user confirmation needed at this stage.

## Output Format

After optimization, output a summary report:

```markdown
## Skill Optimization Summary: {skill-name}

### Changes Made
1. **{file/section}**: {what was changed}
   - Rationale: {why this change was made}

### Summary
{brief overview of the optimization}
```