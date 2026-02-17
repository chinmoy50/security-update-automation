import logging
import argparse
import sys

from collector.fetch_news import fetch_news
from processor.clean_news import clean_news
from processor.news_classifier import classify_news
from processor.advisory_generator import generate_advisory
from notifier.teams_client import send_to_teams
from config.settings import (
    APP_NAME,
    APP_VERSION,
    TEAMS_WEBHOOK_URL,
    LOG_LEVEL
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Security Update Automation Tool"
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--notify", action="store_true")
    return parser.parse_args()


def validate_configuration(args):
    if args.notify and not TEAMS_WEBHOOK_URL:
        logger.error(
            "Teams webhook not configured. Please set TEAMS_WEBHOOK_URL in .env"
        )
        sys.exit(1)


def main():
    args = parse_arguments()

    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    validate_configuration(args)

    try:
        news = fetch_news(limit=args.limit)
        cleaned = clean_news(news)
        classified = classify_news(cleaned)
        advisory = generate_advisory(classified)

        if args.notify:
            send_to_teams(advisory)

        logger.info("Execution completed successfully.")

    except Exception as e:
        logger.exception(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()