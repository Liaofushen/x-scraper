#!/usr/bin/env python3
"""
Demo script for guest mode scraping functionality.
This demonstrates how to use the new guest mode feature.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from xscraper.scraper import XScraper


async def demo_guest_scraping():
    """Demonstrate guest mode scraping functionality"""
    print("🚀 X-Scraper Guest Mode Demo")
    print("=" * 40)

    # Initialize scraper in guest mode
    scraper = XScraper(config_path="config.ini", guest_mode=True)

    # Example username (using a public account)
    username = "stable"  # This is a public account that should be accessible
    max_tweets = 5  # Just a few tweets for testing

    try:
        print(f"📱 Starting guest scraping for @{username}")
        print(f"🎯 Target: {max_tweets} tweets")
        print()

        result = await scraper.scrape_user_tweets_guest(
            username=username,
            max_tweets=max_tweets,
            analyze=False  # Skip AI analysis for demo
        )

        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return

        # Display results
        tweets = result.get('tweets', [])
        user_data = result.get('user_data', {})

        print(f"✅ Success! Scraped {len(tweets)} tweets")
        print(f"👤 User: {user_data.get('display_name', username)} (@{username})")
        if user_data.get('bio'):
            print(f"📝 Bio: {user_data['bio'][:100]}...")
        print()

        # Show first few tweets
        for i, tweet in enumerate(tweets[:3], 1):
            print(f"🐦 Tweet {i}:")
            print(f"   Text: {tweet.get('text', '')[:100]}...")
            print(f"   Time: {tweet.get('created_at', 'Unknown')}")
            if tweet.get('metrics'):
                metrics = tweet['metrics']
                print(f"   Engagement: ❤️ {metrics.get('favorite_count', 0)} | 🔄 {metrics.get('retweet_count', 0)} | 💬 {metrics.get('reply_count', 0)}")
            print()

        # Save results
        output_dir = Path("./data")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{username}_guest_demo.json"

        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        print(f"💾 Results saved to: {output_file}")
        print()
        print("🎉 Guest mode demo completed successfully!")

    except Exception as e:
        print(f"❌ Demo failed: {e}")

    finally:
        # Cleanup
        if hasattr(scraper, 'playwright_scraper') and scraper.playwright_scraper:
            await scraper.playwright_scraper.cleanup()


if __name__ == "__main__":
    print("Starting guest mode demo...")
    print("Note: This will open a browser window briefly.")
    print()

    # Run the demo
    asyncio.run(demo_guest_scraping())