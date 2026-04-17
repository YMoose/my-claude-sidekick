# Planning Focus by Task Type 

Load this file only when the task matches one of the scenarios below. Each scenario adds plan-writing guidance for a recurring class of work that needs more structure than the baseline execution-plan rules.

## Architecture-sensitive implementation tasks

Use this scenario when the task is a programming or system implementation change that materially affects system structure rather than a narrow local edit. Typical signals include introducing a new subsystem, splitting responsibilities across modules, changing cross-layer boundaries, defining or reshaping interfaces, changing data models or state flow, or coordinating behavior across multiple components.

In these cases, the plan should contain a compact technical design, not just a list of files to edit. The design should be concrete enough that a downstream executor does not have to re-derive the architecture while implementing.

Include the following details when they matter:

- The responsibilities of each affected module, component, service, or layer.
- The key interfaces, contracts, or function boundaries that connect those pieces.
- The main data flow, control flow, or state transitions that the implementation relies on.
- The important design decisions and tradeoffs, including why this structure is preferred over obvious alternatives.
- The compatibility constraints, migration boundaries, or invariants that must remain true during implementation.
- The validation strategy that proves the design works at both the boundary level and the user-visible behavior level.

Keep this guidance right-sized. Do not turn every implementation plan into a long architecture document. For small or isolated edits, naming the files, functions, and validation steps is enough. Escalate to explicit design guidance only when the executor would otherwise need to make non-trivial structural decisions on their own.

Failure mode to avoid: a plan that names files and tasks but leaves the module boundaries, ownership, contracts, or migration shape implicit. That kind of plan looks specific but still forces the executor to redesign the solution during implementation.

## Refactor tasks

Prefer additive code changes followed by subtractions that keep tests passing. Parallel implementations (e.g., keeping an adapter alongside an older path during migration) are fine when they reduce risk or enable tests to continue passing during a large migration. Describe how to validate both paths and how to retire one safely with tests. When working with multiple new libraries or feature areas, consider creating spikes that evaluate the feasibility of these features _independently_ of one another, proving that the external library performs as expected and implements the features we need in isolation.

## data analytics tasks

https://github.com/microsoft/TaskWeaver
https://github.com/ruc-datalab/DeepAnalyze

## research tasks

调研相关概念
逐步调研深入，发掘关联，验证

## todo

增加“非功能性约束”的主动探测提示
现状分析
用户描述的研究侧重于“能不能做”（可行性），容易忽略“做出来好不好用”（非功能性需求）。下游计划常因忽略性能、合规、成本约束而需要推倒重来。

改进建议
在研究步骤清单中显式加入一个非功能性需求（NFR）探测清单，作为研究者的思考脚手架：

Security & Compliance：此任务是否涉及PII数据？是否需要审计日志？

Cost & Resource：预期API调用量级？计算资源上限？

Latency & Throughput：是离线批处理还是在线API？SLO预期？

Maintainability：计划产出的组件预计生命周期？由谁维护？

如果用户未提供，研究报告中应包含推断出的默认NFR假设（例如：“假设为内部工具，单用户并发，无严格SLA要求”）。

针对不同的场景，添加非功能性需求调研方向的建议