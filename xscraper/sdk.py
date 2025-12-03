"""
X-Scraper SDK - Simple API for scraping X/Twitter user tweets

This module provides a simple SDK interface for scraping tweets without needing
to understand the internal complexity of the scraper.

Basic Usage:
    >>> from xscraper.sdk import scrape_tweets_guest
    >>> tweets = scrape_tweets_guest('stable', max_tweets=10)
    >>> print(f"Got {len(tweets)} tweets")

Advanced Usage with Context Manager:
    >>> with XScraperClient(guest_mode=True) as client:
    >>>     tweets = client.get_user_tweets('stable', max_tweets=10)
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .scraper import XScraper
from .playwright_scraper import PlaywrightScraper


class XScraperClient:
    """
    X-Scraper client with context manager support.

    Automatically handles initialization and cleanup of browser resources.

    Example:
        >>> with XScraperClient(guest_mode=True) as client:
        >>>     result = client.get_user_tweets('stable', max_tweets=20)
        >>>     print(f"Scraped {result['tweet_count']} tweets")
    """

    def __init__(self, config_path: str = "config.ini", guest_mode: bool = False):
        """
        Initialize the X-Scraper client.

        Args:
            config_path: Path to configuration file (default: config.ini)
            guest_mode: If True, scrapes without login (default: False)
        """
        self.config_path = config_path
        self.guest_mode = guest_mode
        self.scraper: Optional[XScraper] = None
        self._loop = None

    def __enter__(self):
        """Enter context manager"""
        self.scraper = XScraper(self.config_path, guest_mode=self.guest_mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup resources"""
        if self.scraper and self.scraper.playwright_scraper:
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.scraper.playwright_scraper.cleanup())
            except Exception as e:
                logging.warning(f"Error during cleanup: {e}")

    def get_user_tweets(
        self,
        username: str,
        max_tweets: int = 50,
        analyze: bool = False,
        analysis_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get tweets from a user's timeline.

        Args:
            username: Twitter username (without @)
            max_tweets: Maximum number of tweets to scrape
            analyze: Whether to perform AI analysis
            analysis_types: Types of analysis ('sentiment', 'topics', 'summary')

        Returns:
            Dictionary containing:
                - tweets: List of tweet dictionaries
                - tweet_count: Number of tweets scraped
                - user_data: User profile information
                - analysis: AI analysis results (if enabled)

        Example:
            >>> result = client.get_user_tweets('stable', max_tweets=10)
            >>> for tweet in result['tweets']:
            >>>     print(tweet['text'])
        """
        if not self.scraper:
            raise RuntimeError("Client not initialized. Use 'with XScraperClient() as client:'")

        if self.guest_mode:
            # Guest mode scraping
            coro = self.scraper.scrape_user_tweets_guest(
                username=username,
                max_tweets=max_tweets,
                analyze=analyze,
                analysis_types=analysis_types
            )
        else:
            # Authenticated scraping
            coro = self.scraper.scrape_user_tweets(
                username=username,
                count=max_tweets,
                analyze=analyze,
                analysis_types=analysis_types,
                unlimited_history=False,
                browser_mode=True
            )

        # Run async function
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)


def scrape_tweets_guest(
    username: str,
    max_tweets: int = 50,
    config_path: str = "config.ini",
    output_file: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Simple function to scrape tweets in guest mode (no login required).

    This is the easiest way to get started - just call this function with a username!

    Args:
        username: Twitter username to scrape (without @)
        max_tweets: Maximum number of tweets to get (default: 50)
        config_path: Path to config file (default: config.ini)
        output_file: Optional path to save results as JSON

    Returns:
        List of tweet dictionaries, each containing:
            - id: Tweet ID
            - text: Tweet text content
            - created_at: Tweet timestamp
            - metrics: Engagement metrics (likes, retweets, replies)
            - user: User information

    Example:
        >>> from xscraper.sdk import scrape_tweets_guest
        >>> tweets = scrape_tweets_guest('stable', max_tweets=10)
        >>> print(f"Got {len(tweets)} tweets")
        >>> for tweet in tweets:
        >>>     print(f"{tweet['created_at']}: {tweet['text'][:100]}")

    Raises:
        RuntimeError: If scraping fails
    """
    with XScraperClient(config_path=config_path, guest_mode=True) as client:
        result = client.get_user_tweets(username, max_tweets=max_tweets)

        # Save to file if requested
        if output_file:
            import json
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        if 'error' in result:
            raise RuntimeError(f"Scraping failed: {result['error']}")

        return result.get('tweets', [])


def scrape_tweets(
    username: str,
    max_tweets: int = 1000,
    config_path: str = "config.ini",
    output_file: Optional[str] = None,
    analyze: bool = False
) -> List[Dict[str, Any]]:
    """
    Scrape tweets in authenticated mode (requires Twitter login in config).

    This mode can scrape more tweets and access protected accounts.

    Args:
        username: Twitter username to scrape (without @)
        max_tweets: Maximum number of tweets to get (default: 1000)
        config_path: Path to config file with Twitter credentials
        output_file: Optional path to save results as JSON
        analyze: Whether to perform AI analysis (requires OpenAI key)

    Returns:
        List of tweet dictionaries

    Example:
        >>> from xscraper.sdk import scrape_tweets
        >>> tweets = scrape_tweets('stable', max_tweets=500)
        >>> print(f"Got {len(tweets)} tweets")

    Raises:
        RuntimeError: If scraping fails or credentials are missing
    """
    with XScraperClient(config_path=config_path, guest_mode=False) as client:
        result = client.get_user_tweets(
            username,
            max_tweets=max_tweets,
            analyze=analyze
        )

        # Save to file if requested
        if output_file:
            import json
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        if 'error' in result:
            raise RuntimeError(f"Scraping failed: {result['error']}")

        return result.get('tweets', [])


def get_latest_tweets(username: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Quick function to get the latest tweets from a user (guest mode).

    This is the simplest possible API - just username and count!

    Args:
        username: Twitter username (without @)
        count: Number of latest tweets to get (default: 10, max: 50)

    Returns:
        List of tweet dictionaries with text, time, and metrics

    Example:
        >>> from xscraper.sdk import get_latest_tweets
        >>> tweets = get_latest_tweets('stable', count=5)
        >>> for tweet in tweets:
        >>>     print(tweet['text'])
    """
    count = min(count, 50)  # Limit guest mode to 50 tweets
    return scrape_tweets_guest(username, max_tweets=count)


# Convenience aliases
get_user_tweets = scrape_tweets_guest
fetch_tweets = scrape_tweets_guest


__all__ = [
    'XScraperClient',
    'scrape_tweets_guest',
    'scrape_tweets',
    'get_latest_tweets',
    'get_user_tweets',
    'fetch_tweets',
]
