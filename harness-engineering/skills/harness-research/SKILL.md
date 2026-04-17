---
name: harness-research
description: Conduct thorough research to inform planning. Use when a task requires external knowledge, feasibility validation, prior art discovery, or gathering evidence to ensure a concrete and executable plan. 
---

# Harness research
For big-picture orientation only, harness engineering breaks a general task into four parts: `researching`->`planning`->`executing`->`inspecting`. This skill is responsible for the `researching` part of the workflow.

## Workflow

This step is mainly about the `researching` part. Start by understanding the user's intent and then research and gather information to make sure the plan is concrete, feasible, and executable.

Do not keep the results of context gathering and research only in your working memory, Use [Research Report Template](templates/research-report-template.md) and distill what you learned and what you and user decided into the research report (`SURVEY.md`).

### Use the existing context first

Use the current conversation and any local context first to establish the baseline planning picture. Learn from what the user has already specified, determine what can already be inferred from the existing context, and identify which parts of the plan are still underspecified.

If the user already has a draft plan, audit that draft before rewriting it.

### Research beyond the existing context

Use this step to validate or refine your understanding, surface important considerations the user may not have mentioned or considered and learn from useful approaches in similar tasks or prior solutions.

Use the [Planning Focus by Task Type](references/planning-focus-by-task-type.md) as guide to broaden and diversify the scope and dimensions of the research.

Proactively search for relevant external knowledge when it will improve the quality of the plan. This may include web search, Google, Google Scholar, GitHub, official documentation, standards, papers, issue threads, and similar projects or implementations. Use external research to discover prior art, validate feasibility, compare approaches, identify hidden risks, and find practical implementation patterns that should shape the plan.

For well-defined and decomposable research scopes (e.g., covering both academic literature and open-source implementations), you may spawn [deep-researcher agents](./agents/deep-researcher.md) to explore different angles. It can save your context space and time. Each agent is given a clear **context and objective**—for example: *"Look into RAG evaluation metrics in recent academic papers"* or *"Find active GitHub projects implementing local LLM inference."* Collect and merge their results into your main research log during synthesis.

To avoid analysis paralysis, stop researching and start documenting when:

- **Information Saturation**: Two consecutive search or review cycles yield **no new entities** among the tracked categories: *architectural components, constraints, decision forks, or risk sources*.
- **Confidence Saturation**: A critical assertion is supported by **sufficient independent evidence** (e.g., 2+ authoritative sources for a fact claim; 1 strong evidence chain with no contradictions for an inference). Additional evidence would **not change the decision**.
- **Blocking Absence**: A necessary piece of information **cannot be obtained autonomously** (e.g., missing user input, inaccessible internal doc, permission-restricted system). Continued self-directed search is unproductive.

### Handle uncertainty, infeasibility, contradictions and dilemmas

If research shows that the task is infeasible, only feasible under materially different constraints, internally contradictory, or blocked by a hard trade-off that you cannot reasonably resolve after you have exhausted the existing context and your own research and careful reasoning, try to determine whether it can be handled safely with a reasoned inference based on the existing context first. 

Reasoned Inference is a logical conclusion drawn directly from available evidence. If it is sufficient to unblock planning, record it in the research report under the "Solved Blocks" section by the type `Inferences` with a confidence tag ([HIGH], [MEDIUM], [LOW]). Example: "Inferred PostgreSQL 15 is used ([MEDIUM] confidence, based on docker-compose.yml but not yet confirmed in production CI logs).

If a reasoned inference is not possible, explain the issue clearly and ask the user the most focused question that would unblock planning. Record the question and the answer in the research report. After new information is obtained, return to the start of `Gather context` and work through the step again.

### Acceptance criteria in the `researching` part

**SURVEY.md**

NON-NEGOTIABLE REQUIREMENTS for `SURVEY.md`:

- No missing part that the downstream planner might need. The report must fully contain all mandatory sections defined by the [template](templates/research-report-template.md).
- No open question that would materially block drafting a concrete and executable plan. 
- No important finding or claim should appear in the text without an explicit source label or citation. Each one must be clearly attributed to user input, local context, research, or a reasonable inference based on available evidence.
- No mix up among Facts vs Interpretations vs Assumptions. Each must be explicitly labeled and separated in the text.
- No implementation directives or task decomposition in it. The report must remain strictly observational and analytical; it documents what is known, not what to do next.

## Reference files

- `templates/research-report-template.md`: Template for the research report (`SURVEY.md`), defining all mandatory sections.
- `references/schemas.md`: JSON formats for eval prompts, grading outputs, comparison outputs, and iteration history.
- `references/planning-focus-by-task-type.md`: Guide to broaden research scope and dimensions by task type.
- `agents/grader.md`: Instructions for grading one plan revision.