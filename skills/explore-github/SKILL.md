---
name: explore-github
description: How to explore GitHub repositories using the gh CLI to find projects related to a user's idea or need. Use this skill whenever the user mentions searching, digging, exploring, or finding projects on GitHub. Also use it when a user describes an idea, concept, or problem and wants to discover existing GitHub projects, tools, or repositories. Examples: "search GitHub for X", "dig into GitHub repos", "find projects for bookkeeping" → discover tools like beancount, ledger, and related projects.
---

# Explore GitHub Repositories

This skill helps users discover relevant GitHub repositories based on their ideas, needs, or problems. It uses the `gh` CLI to search and explore repositories, then produces a curated markdown summary report.

## When to Use

Use this skill when:
- A user mentions **searching**, **digging**, **exploring**, or **finding** projects on GitHub
- A user asks to "search GitHub", "dig into GitHub", "explore GitHub repos for X"
- A user describes an idea or concept and wants to find related GitHub projects
- A user asks "what tools exist for X" or "show me GitHub repos for X"
- A user mentions wanting to "find projects", "discover repos", or "see what's on GitHub"

Even if the user doesn't explicitly mention GitHub, if they're describing a need that could be met by existing open-source tools, use this skill to help them discover what's available.

## Prerequisites

The `gh` CLI must be installed and authenticated. If not available, inform the user they need to install it from https://cli.github.com/manual/ and run `gh auth login`.

## Workflow

### 1. Parse the User's Request

Extract key concepts, keywords, and domain from the user's idea. For example:
- "I want to start double-entry bookkeeping" → keywords: `bookkeeping`, `accounting`, `double-entry`, `personal-finance`
- "I need a task runner for my projects" → keywords: `task runner`, `build tool`, `automation`

### 2. Search GitHub Using gh

Use multiple search strategies to find relevant repositories:

```bash
# Search by topic
gh repo search <keyword> --topic

# Search by keyword in name/description
gh repo search <keyword>

# Search with multiple keywords
gh repo search "<keyword1> <keyword2>" --limit 20
```

Search for related terms to get comprehensive coverage. Use a layered approach:

1. **Start with user's descriptive terms** - e.g., for "run LLMs locally": `local llm`, `llm inference`
2. **Add technical synonyms** - e.g., `inference engine`, `model serving`, `quantization`
3. **Include well-known project names in the domain** - If you know major projects (e.g., `vllm`, `ollama`, `llama.cpp` for local LLMs), search these directly to ensure they're not missed

For instance:
- "double-entry bookkeeping" → search: `bookkeeping`, `accounting`, `double-entry`, `personal-finance`
- "run LLMs locally" → search: `local llm`, `llm inference`, `llm serving`, `vllm`, `ollama`, `llama.cpp`

### 3. Gather Repository Details

For each promising repository found, collect:

```bash
# Get repo info (stars, description, language)
gh repo view <owner/repo> --json name,description,stars,forks,openIssues,primaryLanguage,url,updatedAt

# Get README content
gh repo view <owner/repo> --json readme

# Get file structure (optional, for deeper analysis)
gh repo view <owner/repo> --json files
```

### 4. Select Top Repositories

Rank repositories by:
1. **Relevance** - How well the repo matches the user's stated need
2. **Popularity** - Star count as a proxy for community adoption
3. **Activity** - Recent updates indicate maintained projects
4. **Quality signals** - Good README, clear documentation, open issues handling

Select 5-10 top repositories for the report.

### 5. Generate Markdown Report

Produce a structured report with the following format:

```markdown
# GitHub Exploration: [User's Idea/Need]

## Summary
Brief overview of the landscape and key findings.

## Top Recommendations

### 1. [repo-name](url)
**Description:** Project description from README or repo
**Stars:** ⭐ 1.2k | **Forks:** 234 | **Language:** Python
**Last Updated:** 2 weeks ago
**Why it's relevant:** Explanation of why this matches the user's need

### 2. [repo-name](url)
...

## Alternative Options
Brief mentions of other notable projects that didn't make the top list.

## Getting Started
Suggested next steps: which repo to explore first, what to look for.
```

## Output Guidelines

- **Be concise but informative** - Each repo should have enough detail to understand its value
- **Include direct links** - Make it easy for the user to visit the repos
- **Explain relevance** - Don't assume the user knows why a repo is relevant; explain the connection
- **Note trade-offs** - If repos have different strengths (e.g., one is simpler, another more powerful), mention them
- **Show variety** - Include a mix of established/stable and newer/innovative projects when available

## Edge Cases

- **No results found** - Try broader search terms or synonyms. If still nothing, inform the user the space may not have much open-source activity.
- **Too many results** - Narrow down with additional keywords or sort by stars/recently updated.
- **Private repos needed** - If the user needs private repos and gh is authenticated with appropriate access, include them. Otherwise, note that private repos require authentication.
- **gh CLI not available** - Inform the user they need to install and authenticate gh CLI first.

## Example

**User:** "I want to start double-entry bookkeeping for my personal finances"

**Skill searches:** `bookkeeping`, `accounting`, `double-entry`, `personal-finance`

**Report includes:**
1. **beancount/beancount** - Python-based, popular for programmers
2. **ledger/ledger** - C++ implementation, mature project
3. **simonmichael/hledger** - Haskell-based, actively maintained
4. **michaelgradowski/beancount-docker** - Easy setup for beancount
...

## Scripts

If you find yourself repeatedly generating the same type of analysis (e.g., formatting repo data, comparing multiple repos), consider creating a helper script in `scripts/` to streamline future runs.
