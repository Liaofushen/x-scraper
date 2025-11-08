#!/usr/bin/env python3
"""
Basic SDK Usage Examples

This file demonstrates the simplest ways to use X-Scraper as an SDK.
"""

# Example 1: Simplest possible usage - just get latest tweets
print("=" * 60)
print("Example 1: Get Latest Tweets (Simplest API)")
print("=" * 60)

from xscraper.sdk import get_latest_tweets

try:
    # Get the 5 most recent tweets from a user
    tweets = get_latest_tweets('stable', count=5)

    print(f"✓ Got {len(tweets)} tweets\n")

    for i, tweet in enumerate(tweets, 1):
        print(f"Tweet {i}:")
        print(f"  Text: {tweet['text'][:100]}...")
        print(f"  Time: {tweet['created_at']}")
        print(f"  Likes: {tweet['metrics'].get('favorite_count', 0)}")
        print()

except Exception as e:
    print(f"Error: {e}")


# Example 2: Using the function API
print("\n" + "=" * 60)
print("Example 2: Function API with More Control")
print("=" * 60)

from xscraper.sdk import scrape_tweets_guest

try:
    # Scrape up to 10 tweets and save to file
    tweets = scrape_tweets_guest(
        username='stable',
        max_tweets=10,
        output_file='data/sdk_example_output.json'
    )

    print(f"✓ Scraped {len(tweets)} tweets")
    print(f"✓ Saved to data/sdk_example_output.json\n")

    # Print summary
    if tweets:
        latest = tweets[0]
        print("Latest tweet:")
        print(f"  {latest['text'][:150]}...")
        print(f"  Posted: {latest['created_at']}")

except Exception as e:
    print(f"Error: {e}")


# Example 3: Using the context manager for more control
print("\n" + "=" * 60)
print("Example 3: Context Manager API (Advanced)")
print("=" * 60)

from xscraper.sdk import XScraperClient

try:
    # Use context manager for automatic cleanup
    with XScraperClient(guest_mode=True) as client:
        result = client.get_user_tweets('stable', max_tweets=5)

        print(f"✓ User: {result['user_data'].get('display_name', 'Unknown')}")
        print(f"✓ Tweets scraped: {result['tweet_count']}")
        print(f"✓ Unique tweets: {result['unique_tweet_count']}")
        print(f"✓ Duration: {result.get('scraping_duration', 0):.2f}s")

except Exception as e:
    print(f"Error: {e}")


# Example 4: Extract specific data
print("\n" + "=" * 60)
print("Example 4: Extracting Specific Data")
print("=" * 60)

try:
    tweets = get_latest_tweets('stable', count=10)

    # Calculate total engagement
    total_likes = sum(t['metrics'].get('favorite_count', 0) for t in tweets)
    total_retweets = sum(t['metrics'].get('retweet_count', 0) for t in tweets)

    print(f"Analysis of {len(tweets)} tweets:")
    print(f"  Total likes: {total_likes:,}")
    print(f"  Total retweets: {total_retweets:,}")
    print(f"  Avg likes per tweet: {total_likes / len(tweets):.1f}")
    print(f"  Avg retweets per tweet: {total_retweets / len(tweets):.1f}")

except Exception as e:
    print(f"Error: {e}")


print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
