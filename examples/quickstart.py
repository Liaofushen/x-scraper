#!/usr/bin/env python3
"""
X-Scraper SDK - Quick Start

The fastest way to get started with X-Scraper SDK!
"""

# ============================================================================
# OPTION 1: Single line to get tweets (easiest!)
# ============================================================================

from xscraper.sdk import get_latest_tweets

tweets = get_latest_tweets('stable', count=10)

print(f"Got {len(tweets)} tweets!")

for tweet in tweets[:3]:  # Show first 3
    print(f"\n{tweet['text'][:100]}...")
    print(f"❤️  {tweet['metrics'].get('favorite_count', 0)} likes")


# ============================================================================
# OPTION 2: Save to file
# ============================================================================

from xscraper.sdk import scrape_tweets_guest

tweets = scrape_tweets_guest(
    username='stable',
    max_tweets=20,
    output_file='my_tweets.json'  # Automatically saves here
)

print(f"\nSaved {len(tweets)} tweets to my_tweets.json")


# ============================================================================
# OPTION 3: Use as context manager (automatic cleanup)
# ============================================================================

from xscraper.sdk import XScraperClient

with XScraperClient(guest_mode=True) as client:
    result = client.get_user_tweets('stable', max_tweets=10)

    print(f"\nUser: {result['user_data'].get('display_name')}")
    print(f"Tweets: {result['tweet_count']}")


# ============================================================================
# That's it! Check the other example files for more advanced usage.
# ============================================================================
