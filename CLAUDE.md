# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

X-Scraper is a Python-based Twitter/X scraping tool with the following architecture:

- **Entry Point**: `main.py` - CLI interface using Click framework
- **Core Module**: `src/` - Main scraping logic and utilities
- **CLI Commands**: `cli/` - Command implementations for different scraping modes
- **Configuration**: `config.ini` - Runtime configuration (template: `config.ini.template`)

### Key Components

- `src/scraper.py`: Main `XScraper` class that orchestrates scraping operations
- `src/playwright_scraper.py`: Browser automation using Playwright for web scraping
- `src/twitter_session.py`: Twitter session management and authentication
- `src/ai_analyzer.py`: OpenAI integration for tweet analysis
- `src/checkpoint_manager.py`: Resume functionality for interrupted scrapes
- `src/progress_manager.py`: Progress tracking and display
- `src/proxy_manager.py`: Proxy rotation and management
- `src/config_manager.py`: Configuration file parsing and validation

### CLI Architecture

The CLI is organized by scraping mode:
- `cli/user.py`: User timeline scraping
- `cli/search.py`: Keyword search scraping
- `cli/historical.py`: Historical date-range search
- `cli/interactive.py`: Interactive menu interface
- `cli/session.py`: Session management commands

## Common Development Commands

### Setup and Installation
```bash
# Install dependencies using uv
uv sync

# Install Playwright browsers
playwright install chromium

# Copy configuration template
cp config.ini.template config.ini
```

### Testing and Development
```bash
# Run the scraper in interactive mode
python main.py interactive

# Test user timeline scraping (requires login)
python main.py user <username> --max-tweets 10

# Test guest mode scraping (no login required)
python main.py guest <username> --max-tweets 20

# Test with AI analysis
python main.py user <username> --max-tweets 10 --analysis sentiment,topics,summary
python main.py guest <username> --max-tweets 20 --analyze
```

### Configuration

Before running, edit `config.ini` with required settings:
- `[TWITTER]`: username, email, password (required for authenticated modes)
- `[SCRAPING]`: output_directory, max_tweets_per_session (required)
- `[AI]`: openai_api_key, model (optional for AI analysis)
- `[PROXY]`: proxy settings (optional)

**Note**: Guest mode only requires `[SCRAPING]` section configuration.

## Key Technical Details

### Scraping Strategy
The tool supports three scraping approaches:
1. **Timeline Scraping**: Recent tweets with login (typically 800-1000 tweets max)
2. **Historical Search**: Date-range based search with login for older content
3. **Guest Mode Scraping**: Public tweets without login (limited to ~50 tweets from first page)

### Browser Automation
- Uses Playwright with Chromium for robust web scraping
- Handles Twitter's infinite scroll and dynamic loading
- Includes session persistence via cookies (`playwright_cookies.json`)
- Implements retry logic and rate limiting

### Data Pipeline
1. Browser automation extracts raw tweet data
2. Data is structured and deduplicated
3. Optional AI analysis using OpenAI GPT models
4. Output saved as JSON with rich metadata

### Error Handling
- Comprehensive retry mechanisms with exponential backoff
- Checkpoint system for resuming interrupted scrapes
- Proxy rotation for IP management
- Detailed logging and progress tracking