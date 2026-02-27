```yaml
nodes:
    - "copy some agents from x":
        state: pending
        create_time: 2026-02-25
        reference:
            link: https://github.com/anthropics/claude-code
            agents:
                - "plugins/pr-review-toolkit/agents/pr-test-analyzer.md"
                - "plugins/pr-review-toolkit/agents/code-simplifier.md"
                - "plugins/plugin-dev/agents/skill-reviewer.md"
                - "plugins/plugin-dev/agents/agent-creator.md"
                - "plugins/feature-dev/agents/code-explorer.md"
                - "plugins/feature-dev/agents/code-architect.md"
                - "plugins/hookify/agents/conversation-analyzer.md (about evolution)"
    - "optimize orchestration-lead agent":
        state: pending
        create_time: 2026-02-25
    - "add a plan skill":
        state: pending
        create_time: 2026-02-25
    - "develop-skill skill":
        state: pending
        create_time: 2026-02-25
    - "agent-evolutionist agent":
        state: pending
        create_time: 2026-02-25
    - "skill explore-github":
        state: pending
        create_time: 2026-02-25
    - "技术方案调研专家agent":
        state: pending
        create_time: 2026-02-25
    - "技术文章审稿专家agent":
        state: pending
        create_time: 2026-02-25
    - "learning context Engineering (Prompt Engineering)":
        state: pending
        create_time: 2026-02-26
        reference: 
            links:
                - "https://platform.claude.com/docs/en/build-with-claude/context-windows"
relations:
    - ["copy some agents from x", "optimize orchestration-lead agent"]
    - ["optimize orchestration-lead agent", "add a plan skill"]
    - ["develop-skill skill", "agent-evolutionist agent"]
    - ["optimize orchestration-lead agent", "agent-evolutionist agent"]
    - ["develop-skill skill", "skill explore-github"]
    - ["技术方案调研专家agent", "optimize orchestration-lead agent"]
    - ["skill explore-github", "技术方案调研专家agent"]
    - ["技术方案调研专家agent", "技术文章审稿专家agent"]
    - ["develop-skill skill", "learning context Engineering (Prompt Engineering)"]
```

```mermaid
flowchart TD
    20260225_0["copy some agents from x"]
    20260225_1["optimize orchestration-lead agent"]
    20260225_2["add a plan skill"]
    20260225_3["develop-skill skill"]
    20260225_4["agent-evolutionist agent"]
    20260225_5["skill explore-github"]
    20260225_6["技术方案调研专家agent"]
    20260225_7["技术文章审稿专家agent"]
    20260226_8["learning context Engineering (Prompt Engineering)"]

    20260225_0 --> 20260225_1
    20260225_1 --> 20260225_2
    20260225_3 --> 20260225_4
    20260225_1 --> 20260225_4
    20260225_3 --> 20260225_5
    20260225_6 --> 20260225_1
    20260225_5 --> 20260225_6
    20260225_6 --> 20260225_7
    20260225_3 --> 20260226_8
```