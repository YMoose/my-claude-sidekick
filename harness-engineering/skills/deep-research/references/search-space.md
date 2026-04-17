# Information Search Space

Source credibility tiers, trust calibration, and platform-specific guidance organized by research domain.

> For the tools to access these platforms (CLI, MCP, curl APIs), see [Platform-Specific Tools](platform-tools.md).

## Contents

- [Source Credibility](#source-credibility)
- [Source by Domain](#source-by-domain)
  - [General](#general)
  - [Software Engineering](#software-engineering)
  - [Academic Research](#academic-research)
  - [Current Events & News](#current-events--news)

## Source Credibility

Not all sources are equally reliable. Use the tier hierarchy when deciding where to search and how much to trust results:

Tier 0 — Local ground truth: The user's own codebase, local docs, and config files. No source is more relevant than the actual code and configuration the user is working with. Always check here first when the question involves the user's project.

Tier 1 — Primary sources: Official documentation, peer-reviewed papers, source code repositories, standards and RFCs. These have direct authority — created by the people who built or formally studied the subject. Can be trusted as standalone evidence for factual claims.

Tier 2 — Expert analysis: Technical blogs by practitioners, conference talks, high-voted Stack Overflow answers, industry reports, mainstream journalism. Written by knowledgeable people but filtered through personal experience and interpretation — generally reliable but verify specifics against Tier 1 when possible.

Tier 3 — Community signal: Reddit threads, HN discussions, X/Twitter posts, GitHub issues. Crowdsourced opinions with varying expertise levels. Useful for opinions, trends, and real-time sentiment, but individual contributions are unvetted — require cross-validation before citing as evidence.

Tier 4 — Supplementary: News aggregators, prediction markets, Q&A platforms. Aggregated or crowdsourced with minimal filtering. Use for background context or when higher tiers yield nothing. Never cite as sole evidence for a claim.

Tiers are defaults, not absolutes. Adjust based on context:

1. **Relevance overrides credibility.** A Tier 3 source that directly answers the question is more useful than a Tier 1 source on the wrong topic.
2. **Author matters more than platform.** A blog post by a framework's creator (Tier 2) may be more authoritative than an official doc that hasn't been updated. Factor in author credibility when identifiable.
3. **Freshness can override credibility.** For `breaking` topics, a Tier 3 source from today beats a Tier 1 source from two years ago. However, this is a *source selection* rule within a given search, not a reordering of the Ripple Rule's *expansion sequence*. You still try high-credibility fresh sources first; this override applies when they don't exist.
4. **Engagement signals add confidence within a platform** See specific sources for details.

## Source by Domain

> `tool_hint` indicates the highest-priority tool for that source. If it is unavailable or returns empty result, fall back to the next best tool in the toolkit.

```yaml
# tool_hint 可选值:
#   cli:gh       → GitHub CLI (gh)
#   cli:yt-dlp   → YouTube metadata/transcript tool (yt-dlp)
#   api          → REST API via curl (see platform-tools.md for endpoints)
#   browser      → Needs browser rendering or login state (Chrome CDP)
#   web_search   → Built-in search for broad discovery and general querie
```

### General

Broad information gathering — opinions, trends, current events, overviews, and topics that don't fit a specialized domain.

```yaml
- Google:
    overview: Default search engine for broad discovery. Use site - operator to target specific platforms.
    strength: Broadest web coverage, good for initial discovery
    limitation: Results influenced by personalization and SEO; snippets are shallow — follow through to primary sources
    url: https://www.google.com/
    tool_hint: web_search
- Bing:
    overview: Alternative search engine. Sometimes surfaces different results than Google. Powers ChatGPT/Copilot search.
    strength: Different ranking algorithm — may find results Google misses
    limitation: Smaller index than Google; same SEO and personalization issues
    url: https://www.bing.com/
    tool_hint: web_search
- Brave Search:
    overview: Privacy-focused search engine with independent index. Good alternative when Google/Bing results are insufficient.
    strength: Independent index — not reliant on Google or Bing; privacy-respecting
    limitation: Smaller index than Google; API requires subscription key
    url: https://search.brave.com/
    tool_hint: api
- Hacker News:
    overview: High-point threads (500+) indicate community interest, not correctness. Always read the top comment — often contains corrections or nuance. Strong Silicon Valley bias.
    strength: Tech community discussions and discovering expert opinions
    limitation: Non-tech topics — SV bias dominates
    url: https://news.ycombinator.com/
    tool_hint: api
    signal: Higher point totals generally indicate more substantive discussion and community vetting. Scores above ~500 are strong signals; lower scores are still usable but require more scrutiny.
- Reddit:
    overview: Quality varies enormously by subreddit (r/programming >> r/coding). Sort by "top" or "best" to find quality comments. Check for moderator-verified answers or "OP confirmed" markers.
    strength: Diverse opinions and community-sourced answers
    limitation: Not definitive for technical answers without cross-validation
    url: https://www.reddit.com/
    tool_hint: api
    signal: Higher upvotes generally indicate better-accepted answers. Posts above ~1000 upvotes carry strong signal; lower scores are still usable but check for moderator-verified or OP-confirmed markers.
- X/Twitter:
    overview: Verify claims through other sources before citing. Watch for satire accounts and impersonation.
    strength: Real-time information, breaking news, and expert hot takes
    limitation: No depth or nuance — 280 chars limits reasoning
    url: https://x.com/
    tool_hint: web_search
- YouTube:
    overview: Transcripts are the most valuable data — extract them when possible. Conference talks (PyCon, JSConf, etc.) are generally high quality. Sponsored content should be discounted.
    strength: Tutorials, conference talks, and visual explanations
    limitation: Not reliable for precise factual claims — verify details from primary sources
    url: https://www.youtube.com/
    tool_hint: cli:yt-dlp
    signal: Higher view counts generally correlate with substantive content. Videos above ~100K views are more likely to be quality; lower views do not rule out value — check channel authority and topic relevance.
- Wikipedia:
    overview: Always verify specifics through original sources.
    strength: Quick overviews and finding primary sources via references
    limitation: Not a primary citation source
    url: https://en.wikipedia.org/
    tool_hint: web_search
- News Outlets:
    overview: Prefer wire services (Reuters, AP) and established outlets. Check if the article is reporting facts or editorializing.
    strength: Current events and reported facts
    limitation: Not ideal for technical depth
    tool_hint: web_search
- Prediction Markets:
    overview: Useful as a supplementary signal for "what the crowd thinks will happen."
    strength: Forecasting and probability estimation
    limitation: Not authoritative for factual claims
    url: https://polymarket.com/
    tool_hint: web_search
- Weibo:
    overview: Chinese social media platform — similar to X/Twitter. Good for real-time Chinese public opinion and trending topics.
    strength: Real-time Chinese social sentiment and trending discussions
    limitation: Heavy censorship; noise from marketing accounts; 140-char limit on original posts
    url: https://weibo.com/
    tool_hint: web_search
- Zhihu:
    overview: Chinese Q&A platform — similar to Quora. Long-form answers with varying quality. Some high-quality expert contributions.
    strength: In-depth Chinese-language answers on diverse topics
    limitation: Quality varies widely; SEO-farmed content increasing; requires cross-validation
    url: https://www.zhihu.com/
    tool_hint: browser
- Bilibili:
    overview: Chinese video platform with substantial tech tutorial content. Transcripts/subtitles often available.
    strength: Chinese-language tech tutorials, course content, and tech talks
    limitation: Entertainment-heavy; sponsored content common; harder to extract transcripts than YouTube
    url: https://www.bilibili.com/
    tool_hint: web_search
```

### Software Engineering

Technical research involving code, frameworks, libraries, APIs, and development tools

```yaml
- Official Docs:
    overview: Trust by default, but check the date — docs can lag behind actual behavior. Prefer docs for the specific version being used, not "latest" which may differ.
    strength: Authoritative API references, configuration guides, and version-specific behavior
    limitation: Opinions or real-world gotchas — docs describe intended behavior, not actual edge cases
    tool_hint: web_search
- GitHub:
    overview: Star count reflects popularity, not quality—10K+ stars indicate wide adoption but not necessarily correctness. Instead, consider the last commit date, issue response time, and contributor count. A well-written README often signals a higher-quality project.
    strength: Finding source code, libraries, and active projects
    limitation: Not ideal for high-level explanations or comparisons
    url: https://github.com/
    tool_hint: cli:gh
    signal: Prioritize maintenance quality over star count. A well-maintained repo with recent commits and responsive issues is a stronger signal than an abandoned repo with high stars.
- Stack Overflow:
    overview: Accepted answers are usually reliable, but check if they're outdated — look at the date and version tags. High-vote newer answers may supersede the accepted one.
    strength: Specific technical questions and error resolution
    limitation: Not ideal for open-ended or opinion-based questions
    url: https://stackoverflow.com/
    tool_hint: web_search
    signal: Accepted answers with high votes are generally reliable, but check dates and version tags — a newer high-vote answer may supersede the accepted one.
    overview: Chinese tech community focused on frontend, backend, and mobile development. Articles are generally practical and code-heavy.
    strength: Chinese-language technical articles and tutorials
    limitation: Quality varies; some articles are republished/rephrased content
    url: https://juejin.cn/
    tool_hint: web_search
- CSDN:
    overview: One of the largest Chinese tech blog platforms. Coverage is broad but quality is uneven.
    strength: Massive archive of Chinese tech content; good for niche error messages
    limitation: Heavy paywalls, SEO farming, and low-quality reposts — cross-validate claims
    url: https://www.csdn.net/
    tool_hint: web_search
- V2EX:
    overview: Chinese tech community forum. Good for developer opinions and discussions.
    strength: Community discussions on tech tools, career, and developer life
    limitation: Small community; not authoritative for factual claims
    url: https://www.v2ex.com/
    tool_hint: web_search
```

### Academic Research

Scientific and scholarly research — papers, citations, literature reviews, and evidence-based claims.

```yaml
- Papers:
    overview: Published in venue > preprint > working paper. Citation count is a rough influence proxy (but can be gamed). Check if the paper has been retracted or heavily criticized.
    strength: Evidence-based claims and established findings
    limitation: Not ideal for fast-moving topics where peer review lags behind practice
    tool_hint: web_search
    signal: Higher citation counts generally indicate greater influence, but verify the paper has not been retracted or heavily criticized. Citation counts can be gamed in some venues.
- Google Scholar:
    overview: Comprehensive search across academic publishers, repositories, and universities. Good for finding specific papers by title or author.
    strength: Broadest coverage of academic literature
    limitation: No API — requires browser access; limited filtering and sorting options
    url: https://scholar.google.com/
    tool_hint: browser
- arXiv:
    overview: Not yet peer-reviewed — treat as expert opinion, not established fact.
    strength: Cutting-edge research in fast-moving fields
    limitation: Not peer-reviewed — findings may not hold up
    url: https://arxiv.org/
    tool_hint: api
- Semantic Scholar:
    overview: Use it as a discovery tool then find originals.
    strength: Finding citation networks, related work, and tracing how a paper has been received
    limitation: Not ideal for reading full papers
    url: https://www.semanticscholar.org/
    tool_hint: api
- CNKI:
    overview: Largest Chinese academic database — journals, dissertations, conference papers. Essential for Chinese-language academic research.
    strength: Comprehensive coverage of Chinese academic publications
    limitation: Paywalled; interface is clunky; requires institutional access for full text
    url: https://www.cnki.net/
    tool_hint: browser
- Wanfang:
    overview: Chinese academic database — alternative to CNKI with some unique content.
    strength: Supplementary to CNKI for Chinese academic literature
    limitation: Smaller coverage than CNKI; also paywalled
    url: https://www.wanfangdata.com.cn/
    tool_hint: browser
- Crossref:
    overview: DOI registry and metadata lookup for academic publications. Good for verifying publication details and finding DOIs.
    strength: Authoritative metadata for published works across all publishers
    limitation: Metadata only — no full text or abstracts for many entries
    url: https://www.crossref.org/
    tool_hint: api
- OpenAlex:
    overview: Open scholarly catalog covering works, authors, institutions, and concepts. Good for bibliometric analysis and discovery.
    strength: Fully open data — no rate limits, no auth required; broad coverage of scholarly works
    limitation: Newer database — may have gaps in older or niche publications
    url: https://openalex.org/
    tool_hint: api
```

### Current Events & News

Breaking news, ongoing events, policy changes, and time-sensitive information.

```yaml
- Reuters:
    overview: Wire service — prioritizes factual reporting over editorializing. Often the original source behind other outlets' stories.
    strength: Fast, factual, low-bias reporting
    limitation: Limited depth — brief articles without analysis
    url: https://www.reuters.com/
    tool_hint: web_search
- AP News:
    overview: Wire service similar to Reuters. Widely syndicated across US outlets.
    strength: Factual baseline for news events
    limitation: US-centric perspective
    url: https://apnews.com/
    tool_hint: web_search
- BBC:
    overview: Public broadcaster with global coverage. Generally balanced but has institutional perspective.
    strength: International coverage and analysis
    limitation: State-funded bias concerns; slower on breaking tech news
    url: https://www.bbc.com/news
    tool_hint: web_search
- Bloomberg:
    overview: Financial and business news. Strong on markets, economics, and corporate reporting.
    strength: Business, finance, and economic analysis
    limitation: Paywalled; business-focused lens may miss social angles
    url: https://www.bloomberg.com/
    tool_hint: web_search
- Google News:
    overview: Aggregates headlines from multiple outlets. Useful for seeing how different sources cover the same story.
    strength: Quick overview of coverage breadth across outlets
    limitation: Aggregator only — must follow through to individual articles
    url: https://news.google.com/
    tool_hint: web_search
- Xinhua:
    overview: China's official state news agency. Authoritative for Chinese government policy and official positions.
    strength: Authoritative source for Chinese government statements and policy
    limitation: State-controlled — reflects official narrative only
    url: https://www.xinhuanet.com/
    tool_hint: web_search
- The Paper:
    overview: Chinese digital news outlet known for in-depth investigative reporting and analysis.
    strength: In-depth Chinese news analysis and investigative reporting
    limitation: Subject to Chinese media regulations; limited coverage of sensitive topics
    url: https://www.thepaper.cn/
    tool_hint: web_search
- Caixin:
    overview: Chinese financial and business news outlet. Known for relatively independent reporting on economic policy.
    strength: Business, finance, and economic policy analysis in China
    limitation: Paywalled; business-focused lens
    url: https://www.caixin.com/
    tool_hint: web_search
```
