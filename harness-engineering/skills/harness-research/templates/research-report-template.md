---
Status: Draft / In Review / Final
Last Updated: 2026-04-12
---

# SURVEY.md
This research report captures the context-gathering and research findings that shape the execution plan. Keep it concise, traceable, and easy to carry forward into `PLANS.md`. Update it whenever new research, assumptions, user answers, or feasibility findings materially change the planning picture.

## Contents
- Terms & Concepts
- User Intent
- Research Subjects
- Dependencies
- Validation Strategy
- Risks and Pitfalls

## Terms & Concepts
Clear definitions for domain-specific jargon, acronyms, or internal project names used in this document. This keeps everyone aligned when reading downstream artifacts.

Examples:
- `Auth Gateway`: The internal NGINX proxy handling all `/api/v1/*` traffic (from user).
- `Legacy Export`: The Python 2.7 script at `scripts/daily_dump.py`.
- `North Star Metric`: The single metric that best captures the core value delivered to users (e.g., 'Messages Sent Per Day').

## User Intent
Summarize what the user said about the task. Capture the core request, not implementation details.

- Current State Snapshot
- What the user wants: A one-sentence restatement of the request.
- Expected outcome: What does "done" look like from the user's perspective?
- Why it matters: The user's underlying motivation or pain point.
- Main constraints: Any explicit boundaries the user mentioned (time, budget, tools, compatibility).

Example:
- Current State Snapshot: the auth service is on EC2
- What the user wants: Migrate the auth service from EC2 to ECS Fargate.
- Expected outcome: Same API behavior, zero downtime during cutover.
- Why it matters: Current EC2 maintenance is consuming 20% of on-call time.
- Main constraints: Must keep the existing PostgreSQL RDS instance untouched.

## Research Subjects
This section documents findings from external research and local code exploration. Findings feed into later sections for structured analysis. Topics naturally form a tree, but here we flatten it into a linear sequence for readability—use.

Common research directions (non-exhaustive):
- Prior Art: How others have solved similar problems or its sub-problems.
- Limits & Boundaries: What are the hard constraints (technical, legal, performance, resource) and the key interfaces (contracts, data, users) that define the edges of this work?
- Uncertainty Hotspots: Where is the knowledge incomplete, where are assumptions being made, and what might break if those are wrong?
- Failures & Lessons: What broke in similar attempts, and what does that warn us about?
- Anything that might help the task

> Source Quality Rule: If a key finding relies on a single, non-authoritative source, mark it with `[WARNING: UNCERTAIN]`.

### Subject: aaa
Why and how this subject help the task

- Source: A link/local file path/others source link
    Findings: …
    Related to(Optional): Describe connections to other subjects (e.g., "Refines constraint X from Subject Y", "Depends on findings from Subject Z").

- [WARNING: UNCERTAIN] Source: xxx
    Findings: …

## Dependencies
List what this task needs to proceed—whether external resources, prior outputs, or ongoing conditions. This helps the planner sequence actions and the executor prepare.

Typical categories:
- Resources: Tools, materials, equipment, or funds.
- Information: Data, documents, credentials, or answers.
- Access: Permissions, approvals, or physical/logical entry.
- Conditions: States that must hold true (e.g., availability of a person, completed prior step).
- Others

Mark each dependency with one of:
- `[BLOCKING]` — Missing and cannot proceed meaningfully without it.
- `[NICE-TO-HAVE]` — Missing but work can proceed or substitute exists.
- `[READY]` — Already available (regardless of importance).

Examples:
- [BLOCKING]Design brief from client
    - Why needed: Defines scope, audience, and deliverables. Without it, any draft work is speculative.
    - Current status: Awaiting client response (follow-up scheduled for Monday).

- [READY]Existing brand assets
    - Why needed: Logos, color palettes, and fonts for consistent visual design.
    - Current status: Available in shared drive `/Marketing/Brand`.

### Prerequisite Prototyping (Optional)
Use this section when feasibility depends on proof-of-concept work, toy implementations, dependency investigation, or other prototype-style validation.

- Prototype goal: …
    What it is meant to validate: …
    How to run it: …
    Promotion or discard criteria: …
    Connection to current plan: …

## Validation Strategy
**IMPORTANT** This section researches and defines how to verify that the expected outcome has been achieved.A clear validation strategy serves as a **feedback loop** to significantly improves the overall quality of task completion. Without it, "done" remains a guess. Research validation strategy for the task as a whole, as well as to internal milestones, branch decisions, or intermediate deliverables.

Validation can be **quantitative** (metrics, thresholds, counts) or **qualitative** (behaviors, observations, approvals). For each key outcome, describe the method and the specific success condition.

Examples:
- Validation for: Rollback Safety
    Timing: During staging cutover
    Why chosen: Zero-downtime constraint requires a verified fallback.
    Method: Trigger simulated failure during staging cutover.
    Success condition: Traffic reverts to legacy system within < 60s with no 5xx errors.

- Validation for: Migration completeness
    Timing: Post-Migration execution
    Why chosen: User expects all legacy data to be available in the new system.
    Method: Run row count comparison script on top 50 tables.
    Success condition: Row counts match exactly between source and destination.

- Validation for: Performance acceptability
    Timing: Integration testing phase
    Why chosen: The task must not degrade user experience.
    Method: Compare p95 latency before and after change using 24-hour traffic replay.
    Success condition: p95 latency increase < 5%.

## Risks and Pitfalls
**IMPORTANT** Foreseeable risks and what the executor should watch out for. Each risk should link to a specific dependency, assumption, or decision point identified earlier—this makes it actionable rather than abstract.

Examples:
- Risk: Client delays providing the design brief.
    Linked to: Dependency `[BLOCKING]` Design brief from client.
    Why it matters: Work cannot start; team goes idle.
    Mitigation / Watch-out: Set clear deadline with client; if delayed, pivot to internal research tasks.

- Risk: Migrated data contains silent corruption.
    Linked to: Validation "Migration completeness" row count check.
    Why it matters: Row counts may match but values could be garbled.
    Mitigation / Watch-out: Add checksum sampling on critical columns, not just row counts.

- Risk: Performance degradation under peak load.
    Linked to: Assumption that new service handles same concurrency as old.
    Why it matters: p95 latency might spike only under real traffic.
    Mitigation / Watch-out: Use traffic replay with realistic concurrency before cutover.

## Solved Blocks
Records blocking items that were resolved during research, this section keeps the decision trail visible for downstream work.

- Issue : [Brief description of the block]
    Why blocked: Why planning could not proceed without resolving this.
    Method to solve: how the issue be solved (e.g. `[HIGH]Inferences` or `User Answer`)
    Why reasonable: *(If `[INFERRED]`)* The evidence or logic supporting the assumption.
    User's words: *(If `[USER ANSWER]`)* The exact response or a paraphrase.
    Revisit Trigger: What specific condition or new information would invalidate this assumption?
    Planning impact: How the resolution shaped the downstream plan.