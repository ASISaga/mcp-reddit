# Archive

This directory contains code that has been retired in favour of the official Reddit API.

## `reddit_fetcher_redditwarp.py`

Original implementation of the MCP Reddit server tools that used the
[`redditwarp`](https://github.com/Pyprohly/redditwarp) library. `redditwarp`
accesses Reddit without requiring OAuth credentials, which is not aligned with
Reddit's official API requirements.

**Replaced by:** `src/mcp_reddit/reddit_fetcher.py` — rewritten to use
[`asyncpraw`](https://asyncpraw.readthedocs.io/) (Async Python Reddit API
Wrapper), which is the community-maintained async client for Reddit's official
OAuth2 API.

### Why it was archived

- Reddit's [Developer Terms](https://www.redditinc.com/policies/data-api-terms)
  require API consumers to authenticate via OAuth2.
- `redditwarp` bypassed OAuth by hitting public JSON endpoints, which is
  considered scraping and is against Reddit's terms of service.
- The new implementation uses `asyncpraw`, which fully authenticates through
  Reddit's official OAuth2 API.
