import configparser
from typing import Dict, Any
from pathlib import Path

from .exceptions import InvalidConfigError, MissingConfigError


class ConfigManager:

    def __init__(self, config_path: str = "config.ini", guest_mode: bool = False):
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        self.guest_mode = guest_mode
        self.load_config()
    
    def load_config(self) -> None:
        if not self.config_path.exists():
            raise MissingConfigError(f"Configuration file not found: {self.config_path}")
        
        try:
            self.config.read(self.config_path)
            self._validate_config()
        except InvalidConfigError:
            raise
        except MissingConfigError:
            raise
        except Exception as e:
            raise InvalidConfigError(f"Failed to parse configuration file: {e}") from e
    
    def _get_boolean(self, section: str, option: str, fallback: bool) -> bool:
        """Safely get boolean value, handling empty strings"""
        value = self.config.get(section, option, fallback='')
        if not value or value.strip() == '':
            return fallback
        return self.config.getboolean(section, option, fallback=fallback)

    def _get_int(self, section: str, option: str, fallback: int) -> int:
        """Safely get int value, handling empty strings"""
        value = self.config.get(section, option, fallback='')
        if not value or value.strip() == '':
            return fallback
        return self.config.getint(section, option, fallback=fallback)

    def _get_float(self, section: str, option: str, fallback: float) -> float:
        """Safely get float value, handling empty strings"""
        value = self.config.get(section, option, fallback='')
        if not value or value.strip() == '':
            return fallback
        return self.config.getfloat(section, option, fallback=fallback)

    def get_twitter_credentials(self) -> Dict[str, str]:
        """Get Twitter account credentials from config."""
        if not self.config.has_section('TWITTER'):
            return {'username': '', 'email': '', 'password': ''}
        
        return {
            'username': self.config.get('TWITTER', 'username', fallback=''),
            'email': self.config.get('TWITTER', 'email', fallback=''),
            'password': self.config.get('TWITTER', 'password', fallback='')
        }
    
    def get_ai_settings(self) -> Dict[str, Any]:
        return {
            'openai_api_key': self.config.get('AI', 'openai_api_key', fallback='') or '',
            'model': self.config.get('AI', 'model', fallback='gpt-4') or 'gpt-4',
            'max_tokens': self._get_int('AI', 'max_tokens', 1000),
            'temperature': self._get_float('AI', 'temperature', 0.7)
        }
    
    def get_scraping_settings(self) -> Dict[str, Any]:
        return {
            'default_tweet_count': self._get_int('SCRAPING', 'default_tweet_count', 50),
            'max_tweet_count': self._get_int('SCRAPING', 'max_tweet_count', 1000),
            'save_to_file': self._get_boolean('SCRAPING', 'save_to_file', True),
            'output_format': self.config.get('SCRAPING', 'output_format', fallback='json') or 'json',
            'output_directory': self.config.get('SCRAPING', 'output_directory', fallback='./data') or './data',
            'scroll_delay_min': self._get_float('SCRAPING', 'scroll_delay_min', 3.0),
            'scroll_delay_max': self._get_float('SCRAPING', 'scroll_delay_max', 6.0),
            'max_scroll_attempts': self._get_int('SCRAPING', 'max_scroll_attempts', 5000),
            'max_attempts_without_new': self._get_int('SCRAPING', 'max_attempts_without_new', 50),
            'max_tweets_per_session': self._get_int('SCRAPING', 'max_tweets_per_session', 800),
            'overlap_detection_threshold': self._get_int('SCRAPING', 'overlap_detection_threshold', 5),
            'guest_mode': self._get_boolean('SCRAPING', 'guest_mode', False),
            'guest_max_tweets': self._get_int('SCRAPING', 'guest_max_tweets', 50)
        }
    
    def get_timeout_settings(self) -> Dict[str, Any]:
        return {
            'page_load_timeout': self._get_int('TIMEOUTS', 'page_load_timeout', 60000),
            'element_wait_timeout': self._get_int('TIMEOUTS', 'element_wait_timeout', 30000),
            'button_click_timeout': self._get_int('TIMEOUTS', 'button_click_timeout', 10000),
            'cookie_verification_timeout': self._get_int('TIMEOUTS', 'cookie_verification_timeout', 15000),
            'login_complete_timeout': self._get_int('TIMEOUTS', 'login_complete_timeout', 20000),
            'short_wait_timeout': self._get_int('TIMEOUTS', 'short_wait_timeout', 5000),
            'post_login_page_delay': self._get_float('TIMEOUTS', 'post_login_page_delay', 5.0),
            'post_input_delay': self._get_float('TIMEOUTS', 'post_input_delay', 2.0),
            'post_navigation_delay': self._get_float('TIMEOUTS', 'post_navigation_delay', 3.0),
            'post_click_delay': self._get_float('TIMEOUTS', 'post_click_delay', 3.0),
            'verification_check_delay': self._get_float('TIMEOUTS', 'verification_check_delay', 2.0),
            'login_wait_delay': self._get_float('TIMEOUTS', 'login_wait_delay', 8.0),
            'page_refresh_short_delay': self._get_float('TIMEOUTS', 'page_refresh_short_delay', 2.0),
            'page_refresh_long_delay': self._get_float('TIMEOUTS', 'page_refresh_long_delay', 3.0)
        }

    def get_search_settings(self) -> Dict[str, Any]:
        return {
            'enable_historical_search': self._get_boolean('SEARCH', 'enable_historical_search', True),
            'chunk_type': self.config.get('SEARCH', 'chunk_type', fallback='monthly') or 'monthly',
            'max_tweets_per_date_range': self._get_int('SEARCH', 'max_tweets_per_date_range', 500),
            'search_delay_between_ranges': self._get_float('SEARCH', 'search_delay_between_ranges', 5.0)
        }
    
    def get_logging_settings(self) -> Dict[str, Any]:
        level = self.config.get('LOGGING', 'level', fallback='INFO')
        if not level or level.strip() == '':
            level = 'INFO'
        return {
            'level': level,
            'log_to_file': self._get_boolean('LOGGING', 'log_to_file', True),
            'log_file': self.config.get('LOGGING', 'log_file', fallback='./logs/scraper.log') or './logs/scraper.log',
            'max_log_size': self._get_int('LOGGING', 'max_log_size', 10485760),
            'backup_count': self._get_int('LOGGING', 'backup_count', 5)
        }
    
    def get_filter_settings(self) -> Dict[str, Any]:
        return {
            'min_followers': self._get_int('FILTERS', 'min_followers', 0),
            'verified_only': self._get_boolean('FILTERS', 'verified_only', False),
            'exclude_retweets': self._get_boolean('FILTERS', 'exclude_retweets', False),
            'exclude_replies': self._get_boolean('FILTERS', 'exclude_replies', False),
            'language': self.config.get('FILTERS', 'language', fallback='en') or 'en'
        }
    
    def get_proxy_settings(self) -> Dict[str, Any]:
        proxy_settings = {
            'enable_proxy_rotation': self._get_boolean('PROXY', 'enable_proxy_rotation', False),
            'validate_proxies_on_startup': self._get_boolean('PROXY', 'validate_proxies_on_startup', True),
            'rotation_url': self.config.get('PROXY', 'proxy_rotation_url', fallback='') or '',
            'proxies': []
        }
        
        proxy_list_str = self.config.get('PROXY', 'proxy_list', fallback='')
        if proxy_list_str.strip():
            proxy_list = [proxy.strip() for proxy in proxy_list_str.split(',') if proxy.strip()]
            proxy_settings['proxies'] = proxy_list
        
        return proxy_settings
    
    def get_setting(self, section: str, key: str, fallback: Any = None) -> Any:
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def update_setting(self, section: str, key: str, value: str) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, key, str(value))
    
    def save_config(self) -> None:
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)
    
    def _validate_config(self) -> None:
        errors = []

        # Skip Twitter credential validation in guest mode
        if not self.guest_mode:
            if not self.config.has_section('TWITTER'):
                errors.append("Missing required section: [TWITTER]")

            if self.config.has_section('TWITTER'):
                required_twitter = ['username', 'email', 'password']
                for field in required_twitter:
                    value = self.config.get('TWITTER', field, fallback='')
                    if not value or value.strip() == '':
                        errors.append(f"Missing required field: [TWITTER] {field}")
        
        if not self.config.has_section('SCRAPING'):
            errors.append("Missing required section: [SCRAPING]")
        
        if self.config.has_section('SCRAPING'):
            try:
                max_tweets = self.config.getint('SCRAPING', 'max_tweets_per_session')
                if max_tweets < 1:
                    errors.append(f"[SCRAPING] max_tweets_per_session must be >= 1, got {max_tweets}")
            except ValueError as e:
                errors.append(f"[SCRAPING] max_tweets_per_session must be a valid integer: {e}")
            
            try:
                scroll_min = self.config.getfloat('SCRAPING', 'scroll_delay_min', fallback=1.0)
                scroll_max = self.config.getfloat('SCRAPING', 'scroll_delay_max', fallback=3.0)
                
                if scroll_min < 0:
                    errors.append(f"[SCRAPING] scroll_delay_min must be >= 0, got {scroll_min}")
                if scroll_max < scroll_min:
                    errors.append(f"[SCRAPING] scroll_delay_max ({scroll_max}) must be >= scroll_delay_min ({scroll_min})")
            except ValueError as e:
                errors.append(f"[SCRAPING] Invalid scroll delay values: {e}")
            
            try:
                max_scrolls = self.config.getint('SCRAPING', 'max_scroll_attempts', fallback=100)
                if max_scrolls < 1:
                    errors.append(f"[SCRAPING] max_scroll_attempts must be >= 1, got {max_scrolls}")
            except ValueError as e:
                errors.append(f"[SCRAPING] max_scroll_attempts must be a valid integer: {e}")
            
            output_dir = self.config.get('SCRAPING', 'output_directory', fallback='')
            if not output_dir:
                errors.append(f"Missing required field: [SCRAPING] output_directory")
        
        if self.config.has_section('AI'):
            provider = self.config.get('AI', 'provider', fallback='').lower()
            if provider and provider not in ['openai', 'anthropic', 'none']:
                errors.append(f"[AI] Invalid provider '{provider}'. Must be: openai, anthropic, or none")

            if provider in ['openai', 'anthropic']:
                api_key = self.config.get('AI', 'api_key', fallback='')
                if not api_key or api_key.strip() == '':
                    errors.append(f"[AI] api_key is required when provider is '{provider}'")

            # Only validate max_tokens if it's set
            max_tokens_str = self.config.get('AI', 'max_tokens', fallback='')
            if max_tokens_str and max_tokens_str.strip():
                try:
                    max_tokens = int(max_tokens_str)
                    if max_tokens < 1:
                        errors.append(f"[AI] max_tokens must be >= 1, got {max_tokens}")
                except ValueError as e:
                    errors.append(f"[AI] max_tokens must be a valid integer: {e}")
        
        if self.config.has_section('TIMEOUTS'):
            for field in self.config.options('TIMEOUTS'):
                value_str = self.config.get('TIMEOUTS', field, fallback='')
                # Skip validation if field is empty (will use fallback in get methods)
                if value_str and value_str.strip():
                    try:
                        value = float(value_str)
                        if value < 0:
                            errors.append(f"[TIMEOUTS] {field} must be >= 0, got {value}")
                    except ValueError as e:
                        errors.append(f"[TIMEOUTS] {field} must be a valid number: {e}")
        
        if self.config.has_section('SEARCH'):
            # Only validate if values are set
            max_per_range_str = self.config.get('SEARCH', 'max_tweets_per_date_range', fallback='')
            if max_per_range_str and max_per_range_str.strip():
                try:
                    max_per_range = int(max_per_range_str)
                    if max_per_range < 1:
                        errors.append(f"[SEARCH] max_tweets_per_date_range must be >= 1, got {max_per_range}")
                except ValueError as e:
                    errors.append(f"[SEARCH] max_tweets_per_date_range must be a valid integer: {e}")

            delay_str = self.config.get('SEARCH', 'search_delay_between_ranges', fallback='')
            if delay_str and delay_str.strip():
                try:
                    delay = int(delay_str)
                    if delay < 0:
                        errors.append(f"[SEARCH] search_delay_between_ranges must be >= 0, got {delay}")
                except ValueError as e:
                    errors.append(f"[SEARCH] search_delay_between_ranges must be a valid integer: {e}")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {err}" for err in errors)
            raise InvalidConfigError(error_msg)