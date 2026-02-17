"""
Application Configuration Settings
----------------------------------
Centralized configuration for Security Update Automation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# 📁 Base Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
FEEDS_FILE_PATH = DATA_DIR / "feeds.txt"

# ==========================================================
# 🔐 Environment Variables
# ==========================================================

TEAMS_WEBHOOK_URL: str = os.getenv("TEAMS_WEBHOOK_URL", "")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
MAX_NEWS_ITEMS: int = int(os.getenv("MAX_NEWS_ITEMS", 10))

# ==========================================================
# 🧠 Application Metadata
# ==========================================================

APP_NAME: str = "Security Update Automation"
APP_VERSION: str = "1.0.0"

# ==========================================================
# 🔎 Classification Keywords
# ==========================================================

HIGH_SEVERITY_KEYWORDS = [
    "critical",
    "zero-day",
    "remote code execution",
    "rce",
    "privilege escalation",
    "actively exploited"
]

MEDIUM_SEVERITY_KEYWORDS = [
    "vulnerability",
    "authentication bypass",
    "security flaw",
    "patch released"
]

LOW_SEVERITY_KEYWORDS = [
    "update",
    "maintenance",
    "bug fix",
    "improvement"
]
