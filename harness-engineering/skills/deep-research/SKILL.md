---
name: deep-research
description: Multi-source research skill that gathers information through multiple retrieval methods, evaluates source quality, cross-validates claims, and synthesizes findings into a structured report with citations. Use when the user needs information that requires looking beyond your training data — including comparisons ("A vs B"), technology evaluations, trend analysis, competitive analysis, literature reviews, "what's the latest on X", "what do people think about Y", "help me understand Z", or any question where gathering evidence from multiple independent sources would produce a better answer.
---

# Deep Research Skill

This skill performs multi-source research: gathering information, evaluating source quality, and synthesizing findings into a structured report. The key principle: **every claim in the report should trace back to evidence found during research — no guessing.**

## Research Pipeline

Follow these phases in order. Each phase builds on the previous one.

### Phase 1: Plan the Search Strategy

Research operates in a multi-dimensional search space. Each dimension constrains where and how to look. Currently defined dimensions:

- **Query relevance** — what angle to search (from highly relevant to loosely related)
- **Freshness** — how new the information needs to be (from newest to oldest)
- **Source credibility** — who to trust (from high to low credibility)

Think of the search space as a volume around the ideal query. When initial results are insufficient, expand the search radius in this order: Expand Relevance first，Relax Freshness next, only when high‑credibility sources yield nothing, Downgrade Source last. Varying the words costs little signal loss. Varying time dilutes recency. Varying source dilutes trust. So protect trust the longest.

Based on this strategy, formulate a search plan for the current question: which dimensions are most relevant, where to start, and how far to expand. This plan is the output of Phase 1 — adjust it as you discover what's available.

#### Source Quality Tiers

Not all sources are equal. Use this hierarchy when deciding where to search:

Tier 0 — Local ground truth (highest priority when relevant):
  - User's own codebase (source code, config, dependencies)
  - Local documentation and README

Tier 1 — Primary sources (highest credibility):
  - Official documentation, RFCs, and standards
  - Peer-reviewed papers (arXiv, PubMed, Semantic Scholar)
  - Source code repositories (GitHub, Gitlab, etc.)
  - Official announcements / changelogs
  - Government & institutional data (.gov, WHO, IMF, census)
  - Wikipedia (good for overviews, always verify specifics)

Tier 2 — Expert analysis:
  - Hacker News discussions
  - YouTube deep-dive videos / Conference talks / Podcasts
  - Technical blogs by core maintainers / industry practitioners
  - High-voted answers on Stack Overflow / Zhihu
  - Industry reports (Gartner, McKinsey, Pew Research)
  - Mainstream news outlets (Reuters, Bloomberg, NYT, etc.)

Tier 3 — Community signal:
  - Reddit discussions
  - X/Twitter threads
  - GitHub Issues/PRs
  - Forum discussions (specialized communities)

Tier 4 — Supplementary:
  - News aggregators
  - Prediction markets (Polymarket — useful for forecasting topics)
  - Crowdsourced platforms (Quora, Zhihu general answers)

For Tier 1 sources, prefer Browser to verify content directly; Web Search is for discovery only. For Tier 2–4, Web Search is usually sufficient.

#### Query Relevance

Don't search the original question as-is. Decompose it into 2-4 sub-queries from different angles to maximize coverage:

- **Direct**: The question as stated. "React vs Vue 2026 comparison"
- **Specific angle**: One dimension of the question. "React performance benchmarks", "Vue ecosystem maturity"
- **Contrarian**: What critics say. "React problems scaling", "Vue limitations enterprise"
- **Adjacent**: Related context that informs the question. "Frontend framework trends 2026", "React vs Vue developer survey"

If results from one angle are thin, reformulate with synonyms or try a different angle. If 2+ reformulations yield nothing, that angle is exhausted — move on. Conversely, if results are overwhelming, narrow the scope by adding constraints (specific version, platform, or time range).

#### Freshness

Information freshness is independent of source credibility. Freshness is essential when the topic moves fast (security, releases, current events); it's less critical for established concepts and practices.

- `breaking` — Only last 30 days. For security incidents, new releases, breaking changes, current events.
- `balanced` — Prefer recent, accept older foundational content. Default for most research.
- `evergreen` — Time matters less. For concepts, algorithms, established practices.

### Phase 2: Execute Search

Execute the plan from Phase 1. Before searching, quickly verify which tools are available in the current environment — this is a one-time check so you don't need to verify everytime. Skip unavailable tools for the entire session.

Then for each step in the plan, pick the most fitting available tool, search, and evaluate. Results may inform plan adjustments (e.g. expanding scope where evidence is thin, or trying different angles based on what you find).

For each result, collect:

- Information source
- Title and key claims
- Date (check if within freshness window)
- Engagement signals (upvotes, stars, views, citations — whatever is available)

#### Search Tools

Once you identify where to look in the space, pick the most fitting tool.

There are several tools, ordered by priority. Some have a dedicated reference file — read the relevant one when you need it:

1. **File Search** — Your built-in tools for searching the user's local dir.
2. **Platform-Specific Tools** — Command-line and MCP access to specific platforms. `gh`, `curl`, `yt-dlp`. See `references/platform-tools.md`. 
3. **Browser** — Leverage browser capabilities for JS-rendered sites and login-protected pages. `Chrome CDP`. See `references/browser.md`.
4. **Web Search** — Built-in search for broad discovery and general queries. It is the last option due to its higher costs.

If a higher-priority tool fails, returns insufficient results, or is unavailable in the current environment, fall back to the next one.

Always work with what you have. Don't refuse to research just because the ideal tool isn't available — adapt and do the best you can with the tools at hand.

#### Adapting to search scenarios

- **High-volume / noisy topics**: Skip Tier 3-4 sources entirely. Prioritize meta-analyses and roundups that already synthesized the noise. Distinguish hype (lots of shallow repetition) from genuine depth (multiple substantive discussions).
- **Sparse data**: Expand query angles more aggressively — try adjacent and contrarian angles. Relax freshness requirements — older foundational content may still apply. Distinguish "genuinely little information exists" from "wrong search terms" — if the latter, reformulate rather than give up.

#### Cross-validation

As you collect results, assess each piece of evidence — especially pay extra attention to unfamiliar domains outside your knowledge boundary. Check if claims are supported by multiple independent sources. Watch for: only a single low-credibility source, sources contradicting each other, outdated evidence, or no corroboration found after searching. When multiple independent sources agree, confidence increases. When validation fails, mark the claim with `[WARNING: UNCERTAIN]`. New evidence and insights from cross-validation may inform plan adjustments — update the search plan if the evidence leads in a different direction. The user is better off knowing what's uncertain than receiving false confidence.

#### Stop criteria

Move to synthesis when any of these are met:
- **Sufficient coverage**: 5+ relevant results across at least 3 different source types
- **Diminishing returns**: Results are repeating the same content across rounds
- **Answer confidence**: The core question has been answered with 2+ independent sources cross-validating, and no major contradictions remain unresolved
- **Search limit**: 100 search actions total — if you've hit this limit, write the report with what you have

**You are also the judge of when you've learned enough.** You can ask yourself: "Am I confident enough to answer the user's question?" If yes, stop and write the report. Over-researching wastes the user's time.

### Phase 3: Synthesize Results

Organize findings into a structured list. Return results directly in the conversation. Each entry represents one search step:

```yaml
- keyword: "{search keyword / purpose}"
  tags: ["[WARNING: UNCERTAIN]"]  # only if applicable
  findings: "What you found, key claims and insights."
  date:  # only if confidently determined
  sources:  # required — URL, filepath, or any traceable link
  tool: # the type of tool finally used
  related:
    - "Supplementary links for deeper exploration"

# End with:
stop_reason:  # why you stopped — e.g., sufficient coverage, confident in answer, diminishing returns, no information at all, etc.
summary: "2-5 sentences answering the core question based on all findings. (If a specific aspect yielded no credible information, state that explicitly rather than omitting or guessing.)"
further:  # based on user intent and findings, suggest aspects worth exploring deeper
  - "Related topics or angles not fully covered"
```

Keep findings concise — the user can follow the source links for details. Only write to a file if the user explicitly asks.

#### Quality Checklist

Before finalizing, verify:
- [ ] Every claim has at least one source
- [ ] Uncertain claims are tagged with `[WARNING: UNCERTAIN]`
- [ ] Conflicting evidence presents both sides
- [ ] Source bias is noted when relevant (e.g., vendor-funded benchmarks, opinion pieces)
- [ ] Sources span at least 2 different platforms

## References

- `references/search-space.md` — Source quality weights and trust calibration per platform
- `references/platform-tools.md` — Platform-specific tools: CLI and API access for structured data retrieval
- `references/browser.md` — Browser capabilities for JS-rendered sites and login-protected pages