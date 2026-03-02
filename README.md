# MCP Reddit Server
[![smithery badge](https://smithery.ai/badge/@adhikasp/mcp-reddit)](https://smithery.ai/server/@adhikasp/mcp-reddit)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides tools for fetching and analyzing Reddit content using Reddit's **official OAuth2 API** via [asyncpraw](https://asyncpraw.readthedocs.io/).

<a href="https://glama.ai/mcp/servers/3cg9gdyors"><img width="380" height="200" src="https://glama.ai/mcp/servers/3cg9gdyors/badge" alt="mcp-reddit MCP server" /></a>

## Features

- Fetch hot, new, top, and rising threads from any subreddit
- Get detailed post content including full comment trees
- Search Reddit posts across all subreddits or within a specific one
- Retrieve subreddit metadata and user profile information
- Fully authenticated via Reddit's official OAuth2 API (no scraping)

## Installation

### Installing via Smithery

To install Reddit Content for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@adhikasp/mcp-reddit):

```bash
npx -y @smithery/cli install @adhikasp/mcp-reddit --client claude
```

### Manual Installation
```json
{
  "reddit": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"],
    "env": {
      "REDDIT_CLIENT_ID": "<your_client_id>",
      "REDDIT_CLIENT_SECRET": "<your_client_secret>",
      "REDDIT_REFRESH_TOKEN": "<your_refresh_token>"
    }
  }
}
```

## Authentication

This server uses Reddit's official OAuth2 API. You need to [create a Reddit app](https://www.reddit.com/prefs/apps) and set the following environment variables:

| Variable | Description |
|---|---|
| `REDDIT_CLIENT_ID` | OAuth2 client ID from your Reddit app |
| `REDDIT_CLIENT_SECRET` | OAuth2 client secret from your Reddit app |
| `REDDIT_REFRESH_TOKEN` | (Optional) Refresh token for authenticated access |

Read-only operations work with just `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`.

## Available Tools

| Tool | Description |
|---|---|
| `fetch_reddit_hot_threads` | Fetch hot posts from a subreddit |
| `fetch_reddit_new_threads` | Fetch newest posts from a subreddit |
| `fetch_reddit_top_threads` | Fetch top posts from a subreddit (with time filter) |
| `fetch_reddit_rising_threads` | Fetch rising posts from a subreddit |
| `fetch_reddit_post_content` | Fetch a post's full content and comment tree |
| `get_subreddit_info` | Retrieve metadata about a subreddit |
| `get_user_profile` | Retrieve a Reddit user's public profile |
| `search_reddit` | Search posts across Reddit or within a subreddit |

## Usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli):

```
$ llm what are latest hot thread in r/victoria3

I'll fetch the latest hot threads from the Victoria 3 subreddit for you.

Tool Calls:
  fetch_reddit_hot_threads
  Args:
    subreddit: victoria3


Based on the hot threads, here are the key highlights from the Victoria 3 subreddit:

1. Dev Diary #126 - Update 1.8 Overview
   - Major updates planned for the game, including:
     - Political Movement Rework (Ideological Forces)
     - Discrimination Rework
     - Food Availability, Famines, and Harvest Incidents
     - Additional features like Companies owning buildings and Bulk Nationalization

2. Dev Diary #138 - Pivot of Empire Update
   - Update 1.8 "Masala Chai" has been released
   - Focuses on India with new Journal Entries, Events, and Immersion Pack
   - 10 new achievements added
   - Save games from 1.7.7 are not compatible with 1.8

3. Interesting Community Discussions:
   - A player shared a detailed experience of retaking Constantinople as Greece, highlighting the complex population dynamics
   - Humorous posts about game mechanics, such as investment rights and political movements
   - Various memes and gameplay screenshots showcasing unique game situations

The most upvoted thread is the Dev Diary #126, which provides an in-depth look at the upcoming game mechanics improvements, particularly the reworks to political movements and discrimination systems.

Would you like me to elaborate on any of these points or provide more details about the Victoria 3 update?
```
