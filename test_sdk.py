#!/usr/bin/env python3
"""
Quick test script to demonstrate X-Scraper SDK usage
"""

print("=" * 70)
print("X-Scraper SDK Test".center(70))
print("=" * 70)

# Test 1: Simple API
print("\n1. Testing simple API: get_latest_tweets()")
print("-" * 70)

from xscraper.sdk import get_latest_tweets

try:
    tweets = get_latest_tweets('stable', count=5)
    print(f"✓ Successfully got {len(tweets)} tweets\n")

    for latest in tweets:
        print("Latest tweet:")
        print(f"  ID: {latest['id']}")
        print(f"  Time: {latest['created_at']}")
        print(f"  Text: {latest['text'][:120]}...")
        print(f"  Metrics: ❤️  {latest['metrics'].get('favorite_count', 0)} | "
              f"🔄 {latest['metrics'].get('retweet_count', 0)} | "
              f"💬 {latest['metrics'].get('reply_count', 0)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Functional API with save
# print("\n2. Testing functional API: scrape_tweets_guest()")
# print("-" * 70)

# from xscraper.sdk import scrape_tweets_guest

# try:
#     tweets = scrape_tweets_guest(
#         username='stable',
#         max_tweets=5,
#         output_file='data/test_sdk_output.json'
#     )
#     print(f"✓ Successfully scraped {len(tweets)} tweets")
#     print(f"✓ Saved to data/test_sdk_output.json")
# except Exception as e:
#     print(f"✗ Error: {e}")

# # Test 3: Context manager
# print("\n3. Testing context manager API: XScraperClient")
# print("-" * 70)

# from xscraper.sdk import XScraperClient

# try:
#     with XScraperClient(guest_mode=True) as client:
#         result = client.get_user_tweets('stable', max_tweets=3)

#         print(f"✓ User: {result['user_data'].get('display_name', 'Unknown')}")
#         print(f"✓ Tweets scraped: {result['tweet_count']}")
#         print(f"✓ Scraping duration: {result.get('scraping_duration', 0):.2f}s")
# except Exception as e:
#     print(f"✗ Error: {e}")

# print("\n" + "=" * 70)
# print("All tests completed!".center(70))
# print("=" * 70)
# print("\nSDK is ready to use!")
# print("Check SDK_USAGE.md for full documentation")
# print("=" * 70)
