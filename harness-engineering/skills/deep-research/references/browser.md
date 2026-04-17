# Browser (User's Existing Browser via CDP)

Connect to the user's already-running browser via Chrome DevTools Protocol. This reuses the user's real login sessions, cookies, and extensions — no need to re-authenticate.

## Prerequisites

1. Before using browser tools, ensure the debug Chrome is running. Check and launch if needed:

```bash
# Check if debug Chrome is already running
curl -s http://127.0.0.1:9222/json/version > /dev/null 2>&1 && echo "running" || echo "not running"

# If not running, launch it (headed mode — needed for initial login):
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome-debug" &

# Or headless mode (after login is done, no visible window):
google-chrome --headless=new --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome-debug" &
```

Note: Chrome does not allow remote debugging on the default profile. Use a separate `--user-data-dir`.

**Headless vs headed:** Use headed mode when you need the user to log in to a new site (they must see and interact with the login page). Once cookies are saved, headless mode works fine — no visible window needed. Some sites may detect and block headless browsers; if that happens, switch back to headed mode.

2. The `chrome-devtools-mcp` must be configured with `--browserUrl` pointing to the debug Chrome's CDP port. Add to `.mcp.json` or Claude Code settings:
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"]
       }
     }
   }
   ```
   **Important:** Do NOT use `--autoConnect` — it launches a separate Chrome instance with its own empty profile, which will not have the user's login sessions. Use `--browserUrl` to connect to the debug Chrome launched in step 1.

3. To verify, check if the MCP server can list pages. If it fails, the browser is not connected.

## Key Advantage

**Your real browser has all your login sessions.** Navigate directly to Reddit, YouTube, X/Twitter, etc. — you'll see the content as if you opened it yourself.

## When to Use

- Sites behind login walls (Reddit, X/Twitter, YouTube with account-specific content)
- Reading login-protected content that cannot be accessed otherwise
- When you need the user's real browsing context
- Documentation sites with client-side rendering (SPA docs)
- Any page where search snippets aren't enough and you need the full content
- Sites requiring interaction (clicking, scrolling, form filling)

## When NOT to Use

- Static content with a known URL → use `webReader` MCP instead (faster, returns structured markdown)
- GitHub repos/issues → use `gh` CLI instead (faster, more reliable)
- Simple web search → use `WebSearch` tool instead

## Limitations

- Requires separate Chrome launch with `--remote-debugging-port`
- Cannot use the default Chrome profile (Chrome restriction)
- Login sessions are NOT shared with the user's daily Chrome — the user must log in to sites once in the debug-profile Chrome. After that, cookies persist across sessions.
- MCP config must use `--browserUrl` (not `--autoConnect`) to connect to the correct Chrome instance

## Workflow

```
1. browser_navigate(url)       → Load the page in your browser
2. browser_snapshot()          → Get accessibility tree / page structure
3. browser_click / browser_type → Interact if needed
4. browser_evaluate(js)        → Extract specific data from the page
5. browser_close()             → Close the tab when done
```

## Tips

- **Reddit**: Always use `old.reddit.com` — lighter page, cleaner structure, no JS-heavy UI
- **YouTube**: Navigate to the video page, use snapshot to find "Show transcript" button, click it, then evaluate JS to extract transcript
- **Login-protected sites**: Just navigate directly — you're already logged in
- **Tabs**: Use `browser_tabs(action="new")` to open multiple pages. Close tabs when done.
- **Data extraction**: Prefer `browser_snapshot` for structured data. Use `browser_take_screenshot` only when you need visual layout.
- **Data size**: `browser_evaluate` returns serialized JSON. For large extractions (e.g., full page text), prefer `browser_snapshot` or paginate your extraction.

## Examples

### Reading a Zhihu page (login-protected)

```
1. browser_navigate("https://www.zhihu.com/question/123456")
   → You're already logged in — no auth needed
2. browser_snapshot() → get the question and answers
3. browser_evaluate("() => Array.from(document.querySelectorAll('.AnswerItem')).map(a => ({author: a.querySelector('.AuthorInfo-name')?.textContent?.trim(), content: a.querySelector('.RichContent-inner')?.textContent?.trim()?.substring(0, 200)}))")
```

## Error Handling

- **Navigation timeout** — Page too slow to load. Close the tab, fall back to WebSearch or `curl` for that content.
- **Blank page / crash** — Site may block automated access. Try a different URL or switch to WebSearch.
- **Snapshot returns empty** — Page may not have finished rendering. Wait a moment and retry, or use `browser_evaluate` to check `document.readyState`.
- **Login wall despite using CDP** — User may not be logged in to that site. Skip the site, note it in the report.
- **Element not found** — Page structure may have changed. Try `browser_snapshot` to get the current structure, then locate the element by a different selector.
