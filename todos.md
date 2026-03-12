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
        state: done
        create_time: 2026-02-25
        remark: "claude offical done"
    - "optimize-skill skill":
        state: done
        create_time: 2026-02-25
        remark: "claude offical done"
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
    - "learning context Engineering & Prompt Engineering":
        state: pending
        create_time: 2026-02-26
        reference: 
            links:
                - "https://platform.claude.com/docs/en/build-with-claude/context-windows"
                - "https://mp.weixin.qq.com/s/C5w6sD4VGJjZ_xrW7vvjRA"
    - "package-snapshot skill":
        state: pending
        create_time: 2026-03-01
        description: "A skill to package all .claude config (skills and agents)"
    - "learn skill-creator plugin":
        state: pending
        create_time: 2026-03-11
        description: "Learn how to use the skill-creator plugin for skill development"
    - "费曼学习法 agent or skill":
        state: pending
        create_time: 2026-03-12
        description: "Create a Feynman learning method agent/skill for teaching and learning concepts"
relations:
    - ["copy some agents from x", "optimize orchestration-lead agent"]
    - ["optimize orchestration-lead agent", "add a plan skill"]
    - ["optimize-skill skill", "agent-evolutionist agent"]
    - ["optimize orchestration-lead agent", "agent-evolutionist agent"]
    - ["optimize-skill skill", "skill explore-github"]
    - ["技术方案调研专家agent", "optimize orchestration-lead agent"]
    - ["skill explore-github", "技术方案调研专家agent"]
    - ["技术方案调研专家agent", "技术文章审稿专家agent"]
    - ["optimize-skill skill", "learning context Engineering & Prompt Engineering"]
    - ["develop-skill skill", "package-snapshot skill"]
    - ["learn skill-creator plugin", "skill explore-github"]
    - ["learn skill-creator plugin", "package-snapshot skill"]
    - ["费曼学习法 agent or skill", "技术方案调研专家 agent"]
```

```mermaid
flowchart TD
    20260225_0["copy some agents from x"]
    20260225_1["optimize orchestration-lead agent"]
    20260225_2["agent-evolutionist agent"]
    20260225_3["skill explore-github"]
    20260225_4["技术方案调研专家 agent"]
    20260225_5["技术文章审稿专家 agent"]
    20260226_6["learning context Engineering & Prompt Engineering"]
    20260301_7["package-snapshot skill"]
    20260311_8["learn skill-creator plugin"]
    20260312_9["费曼学习法 agent or skill"]

    20260225_0 --> 20260225_1
    20260225_1 --> 20260225_2
    20260225_4 --> 20260225_1
    20260225_3 --> 20260225_4
    20260225_4 --> 20260225_5
    20260312_9 --> 20260225_4
    20260311_8 --> 20260225_3
    20260311_8 --> 20260301_7
```