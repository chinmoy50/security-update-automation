import requests
import logging
from config.settings import FEEDS_FILE_PATH, MAX_NEWS_ITEMS

logger = logging.getLogger(__name__)


def load_feeds():
    try:
        with open(FEEDS_FILE_PATH, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error("Feeds file not found.")
        return []


def fetch_news(limit=None):
    feeds = load_feeds()
    news_items = []

    for url in feeds:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            news_items.append({
                "source": url,
                "content": response.text
            })

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch feed {url}: {e}")

    if limit:
        return news_items[:limit]

    return news_items[:MAX_NEWS_ITEMS]