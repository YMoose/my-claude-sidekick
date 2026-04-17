# Execution Plan Review Schemas

This document defines lightweight JSON structures for evaluating and iterating on execution plans. These files live in the review workspace you create for a specific plan, not inside the skill itself.

## evals.json

Use `evals/evals.json` to capture the planning scenarios or review prompts you want to test a plan against.

```json
{
  "plan_title": "Add resumable harness execution",
  "evals": [
    {
      "id": 1,
      "prompt": "Create an execution plan for adding resumable execution to the harness plugin.",
      "expected_outcome": "A novice can identify the relevant files, implement the feature, and validate it without extra context.",
      "context_files": [
        "README.md",
        ".claude/plugins/harness-engineer/plugin.json"
      ],
      "expectations": [
        "The plan names the files that will be edited.",
        "The plan includes exact validation steps.",
        "The plan explains recovery if resume data is missing or stale."
      ]
    }
  ]
}
```

Fields:

- `plan_title`: Human-readable title for the plan under review.
- `evals[].id`: Unique integer identifier.
- `evals[].prompt`: The task brief or review request.
- `evals[].expected_outcome`: Plain-language description of success.
- `evals[].context_files`: Optional list of repo-relative files the plan depends on.
- `evals[].expectations`: Verifiable statements the grader should check.

## grading.json

`grading.json` is the output of `agents/grader.md`.

```json
{
  "plan_path": "/abs/path/to/plan.md",
  "summary": {
    "overall_score": 4.2,
    "verdict": "revise",
    "top_risks": [
      "Validation names no concrete command",
      "Recovery guidance is missing for partial migrations"
    ]
  },
  "criteria": [
    {
      "name": "self_contained",
      "score": 4,
      "passed": true,
      "evidence": "The plan names the files and commands needed for implementation.",
      "risk": "The repository orientation is good, but one acronym is undefined."
    }
  ],
  "expectations": [
    {
      "text": "The plan includes exact validation steps.",
      "passed": false,
      "evidence": "The validation section says 'run tests' but does not name a command."
    }
  ],
  "missing_sections": [],
  "improvement_actions": [
    {
      "priority": "high",
      "section": "Validation and Acceptance",
      "action": "Add the exact test command and expected output.",
      "reason": "A novice executor cannot verify success from the current text."
    }
  ]
}
```

Fields:

- `summary.overall_score`: Overall execution-readiness score on the same 1-5 scale used for rubric criteria.
- `summary.verdict`: Use `ship`, `revise`, or `rewrite`.
- `criteria[]`: Structured rubric results with evidence and risk notes.
- `expectations[]`: Explicit expectation checks from `evals.json`.
- `missing_sections`: Required sections absent from the plan.
- `improvement_actions[]`: Prioritized next edits.

## comparison.json

`comparison.json` is the output of `agents/comparator.md`.

```json
{
  "winner": "A",
  "reasoning": "Plan A is more self-contained and gives precise validation commands.",
  "rubric": {
    "A": {
      "purpose_and_outcome": 4,
      "self_contained": 5,
      "repo_orientation": 4,
      "work_plan_specificity": 4,
      "validation_and_acceptance": 5,
      "idempotence_and_recovery": 4,
      "living_document_hygiene": 5,
      "language_and_jargon": 4,
      "overall_score": 4.5
    },
    "B": {
      "purpose_and_outcome": 4,
      "self_contained": 3,
      "repo_orientation": 4,
      "work_plan_specificity": 3,
      "validation_and_acceptance": 2,
      "idempotence_and_recovery": 2,
      "living_document_hygiene": 3,
      "language_and_jargon": 3,
      "overall_score": 2.9
    }
  },
  "quality_summary": {
    "A": {
      "strengths": [
        "Names exact files to edit",
        "Includes expected command outputs"
      ],
      "weaknesses": [
        "Could explain one dependency in plainer language"
      ]
    },
    "B": {
      "strengths": [
        "Has a clear purpose section"
      ],
      "weaknesses": [
        "Leaves key design decisions unresolved",
        "Validation is too vague for a novice executor"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "target": "B",
      "priority": "high",
      "section": "Validation and Acceptance",
      "suggestion": "Add the exact validation command and expected output.",
      "expected_impact": "Makes the plan verifiable for a novice executor."
    }
  ],
  "revision_goal": {
    "target": "B",
    "current_state": "Plan B has a good purpose section but remains risky in validation and recovery.",
    "goal_for_next_revision": "Make the weaker plan self-contained enough that the executor does not need to guess."
  }
}
```

## history.json

Use `history.json` to track the current best revision during iterative improvement.

```json
{
  "started_at": "2026-04-05T09:30:00Z",
  "plan_title": "Add resumable harness execution",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "overall_score": 3.8,
      "result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "overall_score": 4.4,
      "result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "overall_score": 4.8,
      "result": "won",
      "is_current_best": true
    }
  ]
}
```

Fields:

- `current_best`: Identifier of the best-known revision.
- `iterations[].result`: Use `baseline`, `won`, `lost`, or `tie`.
- `iterations[].overall_score`: Score from the latest grader or comparator pass, using the shared 1-5 overall score scale.
