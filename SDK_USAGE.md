# X-Scraper SDK Usage Guide

The X-Scraper SDK provides a simple, Pythonic API for scraping tweets from X/Twitter without needing to understand the internal complexity.

## Quick Start

### Installation

```bash
pip install uv
uv sync
playwright install chromium
```

### Simplest Usage (3 lines!)

```python
from xscraper.sdk import get_latest_tweets

tweets = get_latest_tweets('stable', count=10)
print(f"Got {len(tweets)} tweets!")
```

## API Reference

### Simple Functions

#### `get_latest_tweets(username, count=10)`

The simplest way to get tweets - just username and count!

```python
from xscraper.sdk import get_latest_tweets

# Get 5 most recent tweets
tweets = get_latest_tweets('stable', count=5)

for tweet in tweets:
    print(tweet['text'])
    print(f"Likes: {tweet['metrics']['favorite_count']}")
```

**Parameters:**
- `username` (str): Twitter username without @
- `count` (int): Number of tweets to get (max 50 for guest mode)

**Returns:** List of tweet dictionaries

---

#### `scrape_tweets_guest(username, max_tweets=50, config_path='config.ini', output_file=None)`

More control over guest mode scraping.

```python
from xscraper.sdk import scrape_tweets_guest

# Scrape and save to file
tweets = scrape_tweets_guest(
    username='stable',
    max_tweets=20,
    output_file='tweets.json'
)
```

**Parameters:**
- `username` (str): Twitter username
- `max_tweets` (int): Max tweets to scrape (default 50)
- `config_path` (str): Path to config file
- `output_file` (str, optional): Save results to this file

**Returns:** List of tweet dictionaries

---

#### `scrape_tweets(username, max_tweets=1000, config_path='config.ini', output_file=None, analyze=False)`

Authenticated scraping (requires Twitter login in config).

```python
from xscraper.sdk import scrape_tweets

# Requires Twitter credentials in config.ini
tweets = scrape_tweets(
    username='stable',
    max_tweets=500,
    analyze=True  # Enable AI analysis (requires OpenAI key)
)
```

**Parameters:**
- `username` (str): Twitter username
- `max_tweets` (int): Max tweets to scrape (default 1000)
- `config_path` (str): Path to config file with credentials
- `output_file` (str, optional): Save results to this file
- `analyze` (bool): Enable AI analysis

**Returns:** List of tweet dictionaries

---

### Context Manager API

For more control and automatic resource cleanup:

```python
from xscraper.sdk import XScraperClient

with XScraperClient(guest_mode=True) as client:
    result = client.get_user_tweets('stable', max_tweets=20)

    print(f"User: {result['user_data']['display_name']}")
    print(f"Tweets: {result['tweet_count']}")
    print(f"Duration: {result['scraping_duration']}s")
```

**XScraperClient Parameters:**
- `config_path` (str): Path to config file
- `guest_mode` (bool): Use guest mode (no login)

**Methods:**
- `get_user_tweets(username, max_tweets, analyze, analysis_types)`: Get tweets from user

## Tweet Data Structure

Each tweet is a dictionary with the following structure:

```python
{
    'id': '1987023923733799399',
    'text': 'Tweet content here...',
    'created_at': '2025-11-08T05:06:35.000Z',
    'user': {
        'id': '1875020395557883905',
        'username': 'stable',
        'display_name': 'Stable',
        'followers_count': 157572,
        'verified': False
    },
    'metrics': {
        'retweet_count': 55,
        'favorite_count': 264,
        'reply_count': 93,
        'quote_count': 12
    },
    'hashtags': ['#example'],
    'urls': ['https://example.com'],
    'media': [],
    'is_retweet': False,
    'is_reply': False
}
```

## Common Use Cases

### 1. Get Latest Tweets

```python
from xscraper.sdk import get_latest_tweets

tweets = get_latest_tweets('stable', count=10)

for tweet in tweets:
    print(f"{tweet['created_at']}: {tweet['text'][:100]}...")
```

### 2. Save to File

```python
from xscraper.sdk import scrape_tweets_guest

tweets = scrape_tweets_guest(
    'stable',
    max_tweets=50,
    output_file='data/stable_tweets.json'
)

print(f"Saved {len(tweets)} tweets")
```

### 3. Analyze Engagement

```python
from xscraper.sdk import get_latest_tweets

tweets = get_latest_tweets('stable', count=20)

total_likes = sum(t['metrics']['favorite_count'] for t in tweets)
total_retweets = sum(t['metrics']['retweet_count'] for t in tweets)

print(f"Total engagement:")
print(f"  Likes: {total_likes:,}")
print(f"  Retweets: {total_retweets:,}")
print(f"  Avg likes/tweet: {total_likes / len(tweets):.1f}")
```

### 4. Filter Tweets

```python
from xscraper.sdk import get_latest_tweets

tweets = get_latest_tweets('stable', count=30)

# Get only popular tweets
popular = [t for t in tweets if t['metrics']['favorite_count'] > 100]

print(f"Found {len(popular)} popular tweets")
```

### 5. Extract Hashtags

```python
from xscraper.sdk import get_latest_tweets
import re
from collections import Counter

tweets = get_latest_tweets('stable', count=50)

# Find all hashtags
all_hashtags = []
for tweet in tweets:
    hashtags = re.findall(r'#\w+', tweet['text'])
    all_hashtags.extend(hashtags)

# Most common hashtags
most_common = Counter(all_hashtags).most_common(10)
print("Top hashtags:")
for tag, count in most_common:
    print(f"  {tag}: {count}")
```

### 6. Compare Multiple Users

```python
from xscraper.sdk import scrape_tweets_guest

users = ['stable', 'ethereum', 'bitcoin']
results = {}

for user in users:
    tweets = scrape_tweets_guest(user, max_tweets=10)
    avg_likes = sum(t['metrics']['favorite_count'] for t in tweets) / len(tweets)
    results[user] = avg_likes

print("Average likes per tweet:")
for user, avg in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"  @{user}: {avg:.1f}")
```

### 7. With Error Handling

```python
from xscraper.sdk import scrape_tweets_guest

def safe_scrape(username, retries=3):
    for attempt in range(retries):
        try:
            return scrape_tweets_guest(username, max_tweets=10)
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed after {retries} attempts: {e}")
                return []
            print(f"Attempt {attempt + 1} failed, retrying...")

tweets = safe_scrape('stable')
```

## Configuration

For guest mode (no login), create minimal `config.ini`:

```ini
[SCRAPING]
output_directory = ./data
```

For authenticated mode, add Twitter credentials:

```ini
[TWITTER]
username = your_username
email = your_email@example.com
password = your_password

[SCRAPING]
output_directory = ./data
max_tweets_per_session = 1000
```

## Limits

### Guest Mode
- ✅ No login required
- ✅ Quick setup
- ⚠️ Limited to ~50 tweets (first page)
- ⚠️ Cannot access protected accounts

### Authenticated Mode
- ✅ Access to more tweets (~800-1000 per session)
- ✅ Can scrape protected accounts you follow
- ✅ Historical search support
- ⚠️ Requires Twitter credentials

## Examples

Check the `examples/` directory for more:

- `quickstart.py` - Simplest usage
- `sdk_basic_usage.py` - Common use cases
- `sdk_advanced_usage.py` - Advanced patterns

## Support

For issues or questions:
- Check examples in `examples/` directory
- Read full documentation in `README.md`
- Report bugs on GitHub

## License

This project is for educational and research purposes only. Please respect Twitter's Terms of Service.
