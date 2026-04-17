# Platform-Specific Tools

This document covers dedicated CLI tools, MCP servers, and direct API calls for fast and reliable structured data retrieval from specific platforms. These methods are often faster and more precise than traditional web browsing.

> For source credibility tiers and platform-specific trust guidance, see [Information Search Space](search-space.md).

> Note: Not all tools listed are required — use what is available in your environment.

## Content

- [MCP](#MCP)
  - [idea-reality-mcp for preliminary research](#idea-reality-mcp-for-preliminary-research)
- [Dedicated CLI tools](#dedicated-cli-tools)
  - [`gh` for GitHub](#gh-for-github)
  - [`yt-dlp` for YouTube](#yt-dlp-for-youtube)
- [User script](#user-script)
- [API access via `curl`](#api-access-via-curl)
  - [API for Brave Search](#api-for-brave-search)
  - [API for Google](#api-for-serpapi-google-results)
  - [API for Hacker News](#api-for-hacker-news-algolia)
  - [API for Reddit](#api-for-reddit-json)
  - [API for Semantic Scholar](#api-for-semantic-scholar)
  - [API for arXiv](#api-for-arxiv)
  - [API for Crossref](#api-for-crossref)
  - [API for OpenAlex](#api-for-openalex)

## MCP
MCP servers enable AI applications to interact with external tools via a standardized protocol. They require the server to be installed, connected, and running. Checking availability first: verify the server is accessible from your environment. If the command or server is not found, skip MCP tools for this session.

Common errors during use:
- Empty results – Query may be incorrect or no data exists. Reformulate; if multiple attempts fail, that approach is exhausted.
- Wrong parameters – The server may expect specific input schemas. Try running the server's CLI with --help (if available) or refer to its documentation.

Supplementary:
- https://mcpservers.org/
- https://github.com/punkpeye/awesome-mcp-servers

### idea-reality-mcp for preliminary research

[idea-reality-mcp](https://github.com/mnemox-ai/idea-reality-mcp) is an MCP server that scans GitHub, npm, PyPI, Hacker News, Product Hunt, and Stack Overflow to check if your startup idea already exists. It returns a 0–100 reality score with evidence, trend detection, and pivot suggestions — so your AI agent can decide whether to build, pivot, or kill the idea before writing any code. Use this when you're about to start a new project and want to know if similar tools already exist, how competitive the space is, and whether the market is growing or declining.

## Dedicated CLI tools
CLI tools offer direct, high-performance access to platform-specific data and are ideal for deep exploration of a known service (e.g., GitHub repositories, YouTube metadata). They often require local installation. So checking availability first, run the base command. If you see command not found, skip the tool for this session.

Common errors during use:
- Empty results – Query may be malformed or no matching data exists. Reformulate; if 2+ attempts yield nothing, that angle is exhausted.
- Parse errors (e.g., when using jq) – Output format may have changed. Inspect the raw response or use an alternative parser.
- Wrong parameters – The command expects specific flags and syntax. try to get help of the command to see accepted options, or refer to the usage examples below.

### `gh` for GitHub

The `gh` CLI helps users discover relevant GitHub repositories based on their ideas, needs, or problems.

#### Prerequisites

1. The `gh` CLI must be authenticated. verify it by running `gh auth login`.

#### Usage

##### Search repositories

```bash
# Search by keyword, sorted by stars
gh search repos "query" --sort stars --limit 10

# Search with multiple keywords
gh search repos "<keyword1> <keyword2>" -L 20

# Search by topic
gh search repos --topic "<topic>" -L 20

# Search with filters (e.g., language, stars)
gh search repos "<keyword>" --language <language> --stars ">=1000" -L 20

# Get search results with details
gh search repos "<keyword>" -L 20 --json name,description,stargazersCount,forksCount,language,url,updatedAt

# Check recent activity
gh api repos/owner/repo/commits --paginate -q '.[0:5] | .[] | {date: .commit.author.date, message: .commit.message}'
```

Search for related terms to get comprehensive coverage. Use a layered approach:

1. **Start with user's descriptive terms** - e.g., for "run LLMs locally": `local llm`, `llm inference`
2. **Add technical synonyms** - e.g., `inference engine`, `model serving`, `quantization`
3. **Include well-known project names in the domain** - If you know major projects (e.g., `vllm`, `ollama`, `llama.cpp` for local LLMs), search these directly to ensure they're not missed

For instance:
- "double-entry bookkeeping" → search: `bookkeeping`, `accounting`, `double-entry`, `personal-finance`
- "run LLMs locally" → search: `local llm`, `llm inference`, `llm serving`, `vllm`, `ollama`, `llama.cpp`

##### Search issues and PRs

```bash
# Search issues across GitHub
gh search issues "bug report query" --limit 10

# Search issues in a specific repo
gh search issues "memory leak" --repo owner/repo --limit 10

# Search with state filter
gh search prs "feature" --repo owner/repo --state open --limit 10

# View a specific issue with comments
gh issue view 123 --repo owner/repo --comments
```

##### Releases, tags, discussions

```bash
# List recent releases
gh release list --repo owner/repo --limit 5

# Search discussions
gh api repos/owner/repo/discussions --paginate -q '.[] | {title: .title, url: .html_url, answers: .answer_count}'
```

##### Compare repos (for comparison research)

```bash
for repo in "owner1/repo1" "owner2/repo2"; do
  echo "=== $repo ==="
  gh repo view "$repo" --json stargazerCount,forkCount,updatedAt,description
done
```

#### Quality signals
- **Stars**: Popularity indicator (but not quality — some bad projects are popular)
- **Recent commits**: Is it actively maintained? Check `updatedAt`
- **Issue response time**: Are maintainers responsive?
- **Open vs closed issues ratio**: Lots of open issues with no response = red flag


### `yt-dlp` for YouTube

Get video metadata and transcripts without downloading the video.

#### Prerequisites

Verify `yt-dlp --version` returns a valid version. `jq` recommended for parsing JSON output.
- **`jq` parse error** — Unexpected response format. Try without `jq`, pipe raw output and parse manually.

#### Usage

##### Get video metadata

```bash
yt-dlp --dump-json "VIDEO_URL" | jq '{title, upload_date, view_count, like_count, description, channel, duration_string}'
```

##### Get subtitles/transcript

```bash
# Auto-generated subtitles (available for most videos)
yt-dlp --write-auto-sub --sub-lang en --skip-download --output "%(title)s" "VIDEO_URL"

# Manual subtitles (if creator uploaded them)
yt-dlp --write-sub --sub-lang en --skip-download --output "%(title)s" "VIDEO_URL"
```

##### Search YouTube from CLI

```bash
yt-dlp "ytsearch5:RAG retrieval augmented generation tutorial" --dump-json | jq '{title, view_count, upload_date, webpage_url}'
```

> If search terms contain special characters (`&`, `?`, `#`), wrap the entire `"ytsearchN:query"` in single quotes or URL-encode the query part.

#### Quality signals
- View count (high = popular, but not necessarily high quality)
- Like/view ratio (above 5% is good for technical content)
- Channel authority (known educators, conference channels)
- Upload date (check if recent enough for your time sensitivity)

### `ddgr` for DuckDuckGo
todo*(Not yet implemented — skip for now.)*: https://github.com/jarun/ddgr

### `wikiextractor` for Wikipedia
todo*(Not yet implemented — skip for now.)*: https://github.com/attardi/wikiextractor

### `hf` for Huggingface
todo*(Not yet implemented — skip for now.)*: https://huggingface.co/docs/huggingface_hub/guides/cli

## User script
todo*(Not yet implemented — skip for now.)*

## API access via `curl`

Direct HTTP calls to public and authenticated APIs return structured data (usually JSON) and are faster and more reliable than scraping.

**Global prerequisites** — run once before using any API:

```bash
curl --version && jq --version
```

If either is missing, skip all API access for this session. For individual APIs, only the specific key check is listed below.

Common HTTP errors:
- `401/403` – Authentication failed or access denied. Check the API key. if missing, skip the API.
- `429` – Rate limited. Wait briefly, then retry or skip the API.
- `5xx` – Server error. Retry once after a short wait; if it persists, skip the API.
- Timeout – Request taking too long. Kill it, simplify the query, or skip the API.

Common response errors:
- Empty results – Query returned no data. Reformulate; if 2+ attempts fail, the angle is exhausted.
- Parse errors – Unexpected response format. Try without `jq` and inspect raw output.
- Wrong parameters – Query string or API parameters may be incorrectly formatted. Consult the API's documentation (or the service's developer docs), and remember that spaces in queries must be URL-encoded.

Supplementary:
- https://github.com/public-apis/public-apis
- https://github.com/public-api-lists/public-api-lists

### API for Brave Search

#### Prerequisites

`BRAVE_SEARCH_API_KEY`. Check with `echo $BRAVE_SEARCH_API_KEY`. If missing, skip this API.

#### Usage

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY" \
  | jq '.web.results[] | {title, url, description}'
```


### API for SerpAPI (Google results)

#### Prerequisites

`SERPAPI_KEY`. Check with `echo $SERPAPI_KEY`. If missing, skip this API.

#### Usage

```bash
curl -s "https://serpapi.com/search.json?q=QUERY&api_key=$SERPAPI_KEY" \
  | jq '.organic_results[] | {title, link, snippet}'
```


### API for Hacker News (Algolia)

#### Prerequisites

No key required.

#### Usage

```bash
# Search stories
curl -s "https://hn.algolia.com/api/v1/search?query=QUERY&tags=story&hitsPerPage=10" \
  | jq '.hits[] | {title, points, num_comments, created_at, url}'

# Search comments
curl -s "https://hn.algolia.com/api/v1/search?query=QUERY&tags=comment&hitsPerPage=10" \
  | jq '.hits[] | {comment_text: .comment_text[:200], points, story_title}'  # [:200] limits output length; remove to get full text

# Get a specific story's comments
curl -s "https://hn.algolia.com/api/v1/items/ITEM_ID" \
  | jq '{title, points, children: [.children[] | {author, text: .text[:200], points}]}'
```

#### Quality signals
- Points (>100 = significant community interest)
- Comment count (lots of comments = active discussion)
- Check the top comment — often has valuable nuance or corrections


### API for Reddit (JSON)

#### Prerequisites

No key required. Use `-A "Mozilla/5.0"` header to avoid 403 blocks.

#### Usage

```bash
curl -s -A "Mozilla/5.0" "https://www.reddit.com/r/programming/search.json?q=QUERY&sort=top&t=year&limit=10" \
  | jq '.data.children[] | .data | {title, score, num_comments, url, permalink}'
```

### API for Semantic Scholar

#### Prerequisites

No key required.

#### Usage

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=QUERY&limit=5&fields=title,year,citationCount,abstract" \
  | jq '.data[] | {title, year, citationCount, abstract: .abstract[:200]}'
```

#### Quality signals
- Citation count (high = influential, but can be gamed)
- Year (recent for fast-moving fields)
- Publication venue (check if paper was later published in a conference/journal)


### API for arXiv

#### Prerequisites

No key required. Returns Atom XML (parse with Python).

#### Usage

```bash
curl -s "http://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5&sortBy=submittedDate&sortOrder=descending" \
  | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
for entry in tree.findall('.//{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
    published = entry.find('{http://www.w3.org/2005/Atom}published').text[:10]
    link = entry.find('{http://www.w3.org/2005/Atom}id').text
    print(f'{published} | {title} | {link}')
"
```

#### Quality signals
- Sort by `submittedDate` for most recent research
- Not yet peer-reviewed — treat as expert opinion, not established fact


### API for Crossref

#### Prerequisites

No key required.

#### Usage

```bash
curl -s "https://api.crossref.org/works?query=QUERY&rows=10" \
  | jq '.message.items[] | {title: .title[0], DOI, published: .published["date-parts"][0]}'
```


### API for OpenAlex

#### Prerequisites

No key required.

#### Usage

```bash
curl -s "https://api.openalex.org/works?search=QUERY" \
  | jq '.results[] | {title, publication_year, cited_by_count, doi}'
```
