#!/usr/bin/env python3
"""
Advanced SDK Usage Examples

This file demonstrates more advanced use cases of the X-Scraper SDK.
"""

from datetime import datetime
from collections import Counter
import re


# Example 1: Analyze tweet content
print("=" * 60)
print("Example 1: Content Analysis")
print("=" * 60)

from xscraper.sdk import get_latest_tweets

try:
    tweets = get_latest_tweets('stable', count=20)

    # Find most common hashtags
    all_hashtags = []
    for tweet in tweets:
        hashtags = re.findall(r'#\w+', tweet['text'])
        all_hashtags.extend(hashtags)

    if all_hashtags:
        most_common = Counter(all_hashtags).most_common(5)
        print("Most common hashtags:")
        for tag, count in most_common:
            print(f"  {tag}: {count} times")
    else:
        print("No hashtags found")

    # Find mentions
    all_mentions = []
    for tweet in tweets:
        mentions = re.findall(r'@\w+', tweet['text'])
        all_mentions.extend(mentions)

    if all_mentions:
        most_common_mentions = Counter(all_mentions).most_common(5)
        print("\nMost mentioned users:")
        for mention, count in most_common_mentions:
            print(f"  {mention}: {count} times")

except Exception as e:
    print(f"Error: {e}")


# Example 2: Filter tweets by criteria
print("\n" + "=" * 60)
print("Example 2: Filtering Tweets")
print("=" * 60)

try:
    tweets = get_latest_tweets('stable', count=20)

    # Filter tweets with high engagement
    popular_tweets = [
        t for t in tweets
        if t['metrics'].get('favorite_count', 0) > 100
    ]

    print(f"Found {len(popular_tweets)} tweets with >100 likes:")
    for tweet in popular_tweets[:3]:
        print(f"\n  Likes: {tweet['metrics']['favorite_count']}")
        print(f"  Text: {tweet['text'][:100]}...")

except Exception as e:
    print(f"Error: {e}")


# Example 3: Compare multiple users
print("\n" + "=" * 60)
print("Example 3: Compare Multiple Users")
print("=" * 60)

from xscraper.sdk import scrape_tweets_guest

users_to_compare = ['stable', 'ethereum', 'bitcoin']

try:
    user_stats = {}

    for username in users_to_compare:
        try:
            tweets = scrape_tweets_guest(username, max_tweets=10)

            if tweets:
                avg_likes = sum(t['metrics'].get('favorite_count', 0) for t in tweets) / len(tweets)
                avg_retweets = sum(t['metrics'].get('retweet_count', 0) for t in tweets) / len(tweets)

                user_stats[username] = {
                    'tweets': len(tweets),
                    'avg_likes': avg_likes,
                    'avg_retweets': avg_retweets
                }
        except Exception as e:
            print(f"  Failed to get tweets for @{username}: {e}")
            continue

    print("\nUser Comparison:")
    print(f"{'User':<15} {'Tweets':<10} {'Avg Likes':<15} {'Avg RTs':<15}")
    print("-" * 60)
    for user, stats in user_stats.items():
        print(f"{user:<15} {stats['tweets']:<10} {stats['avg_likes']:<15.1f} {stats['avg_retweets']:<15.1f}")

except Exception as e:
    print(f"Error: {e}")


# Example 4: Custom data processing
print("\n" + "=" * 60)
print("Example 4: Custom Data Processing")
print("=" * 60)

try:
    tweets = get_latest_tweets('stable', count=15)

    # Process tweets into a custom format
    processed_data = []
    for tweet in tweets:
        processed_data.append({
            'content': tweet['text'][:100],
            'engagement_score': (
                tweet['metrics'].get('favorite_count', 0) * 1 +
                tweet['metrics'].get('retweet_count', 0) * 2 +
                tweet['metrics'].get('reply_count', 0) * 1.5
            ),
            'timestamp': tweet['created_at'],
            'has_media': '[Media tweet' in tweet['text']
        })

    # Sort by engagement score
    processed_data.sort(key=lambda x: x['engagement_score'], reverse=True)

    print("Top 3 tweets by engagement score:")
    for i, data in enumerate(processed_data[:3], 1):
        print(f"\n{i}. Score: {data['engagement_score']:.0f}")
        print(f"   Text: {data['content']}...")
        print(f"   Has media: {data['has_media']}")

except Exception as e:
    print(f"Error: {e}")


# Example 5: Error handling
print("\n" + "=" * 60)
print("Example 5: Robust Error Handling")
print("=" * 60)

def safe_scrape_user(username: str, max_retries: int = 3):
    """Scrape with retry logic"""
    from time import sleep

    for attempt in range(max_retries):
        try:
            tweets = scrape_tweets_guest(username, max_tweets=10)
            return tweets
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Attempt {attempt + 1} failed, retrying...")
                sleep(2)
            else:
                print(f"  All attempts failed: {e}")
                return []

# Test with valid and invalid users
for test_user in ['stable', 'nonexistent_user_12345']:
    print(f"\nTrying to scrape @{test_user}...")
    tweets = safe_scrape_user(test_user)
    if tweets:
        print(f"  ✓ Success! Got {len(tweets)} tweets")
    else:
        print(f"  ✗ Failed to get tweets")


print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
