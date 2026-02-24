---
name: literature-mine
description: Build citation graphs from academic literature for research exploration and literature review. Use when asked to find related papers, explore a research field.
---

Build citation graphs from academic literature to understand research landscapes and paper relationships.

## Workflow

1. **Define the research area** - Confirm the field with the user, or ask them to provide 1-2 seed papers
2. **Find seed papers** - If not provided, identify 1-2 classic/highly-cited papers in the field and confirm with user
3. **Backward citation search** - Find highly-cited papers referenced by the seed papers
4. **Forward citation search** - Find highly-cited papers that cite the seed papers
5. **Collect metadata** - Gather basic info for all papers (title, authors, year, venue, citations, short summary)
6. **Build JSON** - Create a structured JSON file with paper data and citation relationships
7. **Generate visualization** - Run `json_to_citation_graph.py` to create an interactive HTML graph

## JSON Schema

```json
{
  "data": [
    {
      "id": 1,
      "title": "Paper title",
      "authors": "Author A, Author B",
      "year": 2020,
      "venue": "Journal Name",
      "citations": 1500,
      "url": "https://...",
      "doi": "10.xxx/xxx",
      "cited": [2, 3]
    }
  ]
}
```

The `cited` array contains IDs of papers that this paper references.

## Output

- a JSON file named `${CLAUDE_SESSION_ID}-literature-mine_N.json` where N prevents collisions
- a HTML file named `${CLAUDE_SESSION_ID}-literature-mine_N.html` where N prevents collisions:

```bash
python scripts/json_to_citation_graph.py papers.json -o output.html
```

## Resources

- **Search strategies**: See [references/google_scholar_search.md](references/google_scholar_search.md) for search operators, filtering, and citation chain techniques
- **Example output**: See [examples/sample.json](examples/sample.json) for the expected JSON format
