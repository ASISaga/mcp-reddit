import os
from typing import Optional
import asyncpraw
import asyncpraw.models
from fastmcp import FastMCP
import logging

mcp = FastMCP("Reddit MCP")

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_REFRESH_TOKEN = os.getenv("REDDIT_REFRESH_TOKEN")

logging.getLogger().setLevel(logging.WARNING)


def _create_reddit_client() -> asyncpraw.Reddit:
    """Create an asyncpraw Reddit client using configured credentials."""
    kwargs: dict = dict(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="MCP Reddit Server/1.0",
    )
    if REDDIT_REFRESH_TOKEN:
        kwargs["refresh_token"] = REDDIT_REFRESH_TOKEN
    return asyncpraw.Reddit(**kwargs)


def _get_post_type(submission: asyncpraw.models.Submission) -> str:
    """Determine the type of a submission."""
    if submission.is_self:
        return "text"
    if hasattr(submission, "gallery_data") and submission.gallery_data:
        return "gallery"
    return "link"


def _get_content(submission: asyncpraw.models.Submission) -> str:
    """Extract the main content of a submission."""
    if submission.is_self:
        return submission.selftext or ""
    return submission.url


def _format_submission(submission: asyncpraw.models.Submission) -> str:
    """Format a submission for human-readable display."""
    return (
        f"Title: {submission.title}\n"
        f"Score: {submission.score}\n"
        f"Comments: {submission.num_comments}\n"
        f"Author: {str(submission.author) if submission.author else '[deleted]'}\n"
        f"Type: {_get_post_type(submission)}\n"
        f"Content: {_get_content(submission)}\n"
        f"Link: https://reddit.com{submission.permalink}\n"
        f"---"
    )


def _format_comment_tree(comment: asyncpraw.models.Comment, depth: int = 0, max_depth: int = 3) -> str:
    """Recursively format a comment tree with proper indentation."""
    if depth >= max_depth:
        return ""
    indent = "-- " * depth
    content = (
        f"{indent}* Author: {str(comment.author) if comment.author else '[deleted]'}\n"
        f"{indent}  Score: {comment.score}\n"
        f"{indent}  {comment.body}\n"
    )
    for reply in comment.replies:
        if isinstance(reply, asyncpraw.models.Comment):
            content += "\n" + _format_comment_tree(reply, depth + 1, max_depth)
    return content


async def _fetch_listing(listing_generator, limit: int) -> str:
    """Collect and format posts from a listing generator."""
    posts = []
    async for submission in listing_generator:
        posts.append(_format_submission(submission))
        if len(posts) >= limit:
            break
    return "\n\n".join(posts) if posts else "No posts found."


@mcp.tool()
async def fetch_reddit_hot_threads(subreddit: str, limit: int = 10) -> str:
    """
    Fetch hot threads from a subreddit.

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)

    Returns:
        Human readable string containing list of post information
    """
    try:
        async with _create_reddit_client() as reddit:
            sr = await reddit.subreddit(subreddit)
            return await _fetch_listing(sr.hot(limit=limit), limit)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def fetch_reddit_new_threads(subreddit: str, limit: int = 10) -> str:
    """
    Fetch new threads from a subreddit.

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)

    Returns:
        Human readable string containing list of post information
    """
    try:
        async with _create_reddit_client() as reddit:
            sr = await reddit.subreddit(subreddit)
            return await _fetch_listing(sr.new(limit=limit), limit)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def fetch_reddit_top_threads(subreddit: str, limit: int = 10, time_filter: str = "week") -> str:
    """
    Fetch top threads from a subreddit.

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)
        time_filter: One of "hour", "day", "week", "month", "year", "all" (default: "week")

    Returns:
        Human readable string containing list of post information
    """
    try:
        async with _create_reddit_client() as reddit:
            sr = await reddit.subreddit(subreddit)
            return await _fetch_listing(sr.top(time_filter=time_filter, limit=limit), limit)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def fetch_reddit_rising_threads(subreddit: str, limit: int = 10) -> str:
    """
    Fetch rising threads from a subreddit.

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)

    Returns:
        Human readable string containing list of post information
    """
    try:
        async with _create_reddit_client() as reddit:
            sr = await reddit.subreddit(subreddit)
            return await _fetch_listing(sr.rising(limit=limit), limit)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def fetch_reddit_post_content(post_id: str, comment_limit: int = 20, comment_depth: int = 3) -> str:
    """
    Fetch detailed content of a specific post.

    Args:
        post_id: Reddit post ID
        comment_limit: Number of top level comments to fetch (default: 20)
        comment_depth: Maximum depth of comment tree to traverse (default: 3)

    Returns:
        Human readable string containing post content and comments tree
    """
    try:
        async with _create_reddit_client() as reddit:
            submission = await reddit.submission(post_id)
            await submission.load()
            content = (
                f"Title: {submission.title}\n"
                f"Score: {submission.score}\n"
                f"Author: {str(submission.author) if submission.author else '[deleted]'}\n"
                f"Type: {_get_post_type(submission)}\n"
                f"Content: {_get_content(submission)}\n"
            )
            await submission.comments.replace_more(limit=0)
            top_comments = [
                c for c in submission.comments
                if isinstance(c, asyncpraw.models.Comment)
            ][:comment_limit]
            if top_comments:
                content += "\nComments:\n"
                for comment in top_comments:
                    content += "\n" + _format_comment_tree(comment, max_depth=comment_depth)
            else:
                content += "\nNo comments found."
            return content
    except Exception as e:
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def get_subreddit_info(subreddit: str) -> str:
    """
    Get information about a subreddit.

    Args:
        subreddit: Name of the subreddit

    Returns:
        Human readable string containing subreddit information
    """
    try:
        async with _create_reddit_client() as reddit:
            sr = await reddit.subreddit(subreddit)
            await sr.load()
            return (
                f"Name: r/{sr.display_name}\n"
                f"Title: {sr.title}\n"
                f"Description: {sr.public_description}\n"
                f"Subscribers: {sr.subscribers:,}\n"
                f"Active Users: {sr.accounts_active}\n"
                f"NSFW: {sr.over18}\n"
                f"URL: https://reddit.com{sr.url}\n"
            )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def get_user_profile(username: str) -> str:
    """
    Get profile information for a Reddit user.

    Args:
        username: Reddit username

    Returns:
        Human readable string containing user profile information
    """
    try:
        async with _create_reddit_client() as reddit:
            redditor = await reddit.redditor(username)
            await redditor.load()
            return (
                f"Username: u/{redditor.name}\n"
                f"Post Karma: {redditor.link_karma:,}\n"
                f"Comment Karma: {redditor.comment_karma:,}\n"
                f"Reddit Premium: {redditor.is_gold}\n"
            )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def search_reddit(
    query: str,
    subreddit: Optional[str] = None,
    limit: int = 10,
    sort: str = "relevance",
    time_filter: str = "all",
) -> str:
    """
    Search Reddit posts.

    Args:
        query: Search query string
        subreddit: Limit search to a specific subreddit; searches all of Reddit when omitted
        limit: Number of results to return (default: 10)
        sort: One of "relevance", "hot", "top", "new", "comments" (default: "relevance")
        time_filter: One of "all", "day", "hour", "month", "week", "year" (default: "all")

    Returns:
        Human readable string containing search results
    """
    try:
        async with _create_reddit_client() as reddit:
            target_subreddit = subreddit if subreddit else "all"
            sr = await reddit.subreddit(target_subreddit)
            results = sr.search(query, sort=sort, time_filter=time_filter, limit=limit)
            posts = []
            async for submission in results:
                posts.append(_format_submission(submission))
            return "\n\n".join(posts) if posts else "No results found."
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
