import requests
import logging
from config.settings import TEAMS_WEBHOOK_URL

logger = logging.getLogger(__name__)


def send_to_teams(message: str):
    if not TEAMS_WEBHOOK_URL:
        logger.warning("Teams webhook URL is not configured.")
        return False

    headers = {"Content-Type": "application/json"}
    payload = {"text": message}

    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        logger.info("Notification sent to Microsoft Teams successfully.")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Teams notification: {e}")
        return False