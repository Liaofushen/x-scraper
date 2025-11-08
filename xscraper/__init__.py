from .config_manager import ConfigManager
from .twitter_session import TwitterSession
from .playwright_scraper import PlaywrightScraper
from .ai_analyzer import AIAnalyzer
from .scraper import XScraper
from .checkpoint_manager import CheckpointManager

# SDK imports for easy access
from .sdk import (
    XScraperClient,
    scrape_tweets_guest,
    scrape_tweets,
    get_latest_tweets,
    get_user_tweets,
    fetch_tweets
)
from .exceptions import (
    XScraperError,
    AuthenticationError,
    SessionExpiredError,
    InvalidCredentialsError,
    RateLimitError,
    BotDetectionError,
    NetworkError,
    ProxyError,
    PageLoadError,
    ScrapingError,
    TweetExtractionError,
    NoTweetsFoundError,
    ConfigurationError,
    InvalidConfigError,
    MissingConfigError,
    AIAnalysisError,
    CheckpointError
)
from .decorators import retry_on_network_error, handle_rate_limit, log_errors

__all__ = [
    # Core classes
    "ConfigManager",
    "TwitterSession",
    "PlaywrightScraper",
    "AIAnalyzer",
    "XScraper",
    "CheckpointManager",
    # SDK functions (recommended for most users)
    "XScraperClient",
    "scrape_tweets_guest",
    "scrape_tweets",
    "get_latest_tweets",
    "get_user_tweets",
    "fetch_tweets",
    # Exceptions
    "XScraperError",
    "AuthenticationError",
    "SessionExpiredError",
    "InvalidCredentialsError",
    "RateLimitError",
    "BotDetectionError",
    "NetworkError",
    "ProxyError",
    "PageLoadError",
    "ScrapingError",
    "TweetExtractionError",
    "NoTweetsFoundError",
    "ConfigurationError",
    "InvalidConfigError",
    "MissingConfigError",
    "AIAnalysisError",
    "CheckpointError",
    "retry_on_network_error",
    "handle_rate_limit",
    "log_errors"
]