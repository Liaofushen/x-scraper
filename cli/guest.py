import asyncio
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .utils import save_result_with_analysis, parse_analysis_types
from xscraper.playwright_scraper import PlaywrightScraper
from xscraper.config_manager import ConfigManager
from xscraper.ai_analyzer import AIAnalyzer


console = Console()


@click.command()
@click.argument('username')
@click.option('--max-tweets', '-n', default=50, help='Maximum number of tweets to scrape (default: 50)')
@click.option('--output', '-o', help='Output file path (optional)')
@click.option('--analyze/--no-analyze', default=False, help='Perform AI analysis (requires OpenAI API key)')
@click.option('--analysis-types', '-a', default='sentiment,topics,summary', help='Analysis types (comma-separated)')
@click.pass_context
def guest(ctx: click.Context, username: str, max_tweets: int, output: Optional[str],
          analyze: bool, analysis_types: str) -> None:
    """
    Scrape user tweets in guest mode (no login required).

    This mode scrapes tweets that are publicly visible without authentication.
    It's limited to the first page of tweets but doesn't require Twitter credentials.

    Example: python main.py guest stable --max-tweets 20
    """

    async def run_guest_scrape() -> None:
        config_manager = ConfigManager(ctx.obj['config'], guest_mode=True)

        # Initialize Playwright scraper in guest mode
        scraper = None
        try:
            console.print(f"[bold green]Starting guest scrape for @{username}[/bold green]")
            console.print(f"Mode: Guest (no login required)")
            console.print(f"Max tweets: {max_tweets}")

            # Create scraper in guest mode with minimal configuration
            proxy_settings = config_manager.get_proxy_settings()
            scraper = PlaywrightScraper(
                guest_mode=True,
                proxy_config=proxy_settings if proxy_settings.get('enable_proxy_rotation') else None
            )

            await scraper.initialize()

            # Perform guest scraping
            with console.status(f"[bold yellow]Scraping tweets from @{username}..."):
                result = await scraper.scrape_user_tweets_guest(username, max_tweets)

            if result.get('error'):
                console.print(f"[red]Error: {result['error']}[/red]")
                return

            tweet_count = result.get('tweet_count', 0)
            console.print(f"[green]✓[/green] Successfully scraped {tweet_count} tweets")

            # AI analysis if requested
            if analyze and tweet_count > 0:
                ai_settings = config_manager.get_ai_settings()
                if not ai_settings.get('openai_api_key'):
                    console.print("[yellow]Warning: AI analysis requested but no OpenAI API key found in config[/yellow]")
                else:
                    try:
                        console.print("[blue]Performing AI analysis...[/blue]")
                        analyzer = AIAnalyzer(
                            api_key=ai_settings['openai_api_key'],
                            model=ai_settings.get('model', 'gpt-4o-mini'),
                            max_tokens=ai_settings.get('max_tokens', 1000),
                            temperature=ai_settings.get('temperature', 0.7)
                        )

                        analysis_list = parse_analysis_types(analysis_types)
                        analysis_result = await analyzer.analyze_tweets(result['tweets'], analysis_list)
                        result['analysis'] = analysis_result
                        console.print("[green]✓[/green] AI analysis completed")
                    except Exception as e:
                        console.print(f"[yellow]Warning: AI analysis failed: {e}[/yellow]")

            # Save results
            if output:
                save_path = Path(output)
            else:
                # Default output path
                output_dir = Path(config_manager.get_scraping_settings().get('output_directory', './data'))
                output_dir.mkdir(exist_ok=True)
                filename = f"{username}_guest_{max_tweets}tweets.json"
                save_path = output_dir / filename

            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                console.print(f"[green]Results saved to: {save_path}[/green]")
            except Exception as e:
                console.print(f"[red]Error saving results: {e}[/red]")

            # Print summary
            if result.get('user_data'):
                user_data = result['user_data']
                if user_data.get('display_name'):
                    console.print(f"User: {user_data['display_name']} (@{username})")
                if user_data.get('bio'):
                    console.print(f"Bio: {user_data['bio'][:100]}...")

        except Exception as e:
            console.print(f"[red]Scraping failed: {e}[/red]")

        finally:
            if scraper:
                await scraper.cleanup()

    # Run the async scraping function
    asyncio.run(run_guest_scrape())