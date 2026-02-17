import re
from config.settings import (
    HIGH_SEVERITY_KEYWORDS,
    MEDIUM_SEVERITY_KEYWORDS,
    LOW_SEVERITY_KEYWORDS
)


def extract_cves(text: str):
    return re.findall(r"CVE-\d{4}-\d{4,7}", text)


def determine_severity(text: str):
    text_lower = text.lower()

    for keyword in HIGH_SEVERITY_KEYWORDS:
        if keyword in text_lower:
            return "High"

    for keyword in MEDIUM_SEVERITY_KEYWORDS:
        if keyword in text_lower:
            return "Medium"

    for keyword in LOW_SEVERITY_KEYWORDS:
        if keyword in text_lower:
            return "Low"

    return "Uncategorized"


def classify_news(news_items: list):
    classified = []

    for item in news_items:
        severity = determine_severity(item)
        cves = extract_cves(item)

        classified.append({
            "content": item,
            "severity": severity,
            "cves": cves
        })

    return classified