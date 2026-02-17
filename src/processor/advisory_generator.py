#!/usr/bin/env python3

import os
import csv
import requests
import re
from datetime import datetime, timezone
from dotenv import load_dotenv

# ======================
# ENV & PATHS
# ======================

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
if not TEAMS_WEBHOOK_URL:
    raise RuntimeError("TEAMS_WEBHOOK_URL not set in .env file")

DATA_DIR = "data"
LOG_DIR = "logs"

CLEAN_NEWS_FILE = f"{DATA_DIR}/articles_clean.csv"
STATE_FILE = f"{DATA_DIR}/notified_urls.txt"
CRON_LOG = f"{LOG_DIR}/cron.log"

SUMMARY_MAX_CHARS = 300

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ======================
# LOGGING
# ======================

def log_cron():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(CRON_LOG, "a") as f:
        f.write(f"{ts} - Advisory script executed\n")


# ======================
# STATE HANDLING
# ======================

def load_notified():
    if not os.path.exists(STATE_FILE):
        return set()

    urls = set()
    with open(STATE_FILE, "r") as f:
        for line in f:
            if "|" in line:
                urls.add(line.split("|", 1)[1].strip())
    return urls


def save_notified(url):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(STATE_FILE, "a") as f:
        f.write(f"{ts} | {url}\n")


# ======================
# ENRICHMENT
# ======================

def truncate(text):
    return text if len(text) <= SUMMARY_MAX_CHARS else text[:SUMMARY_MAX_CHARS] + "..."


def extract_cves(text):
    cves = re.findall(r"CVE-\d{4}-\d{4,7}", text)
    return ", ".join(sorted(set(cves))) if cves else "N/A"


def detect_oem(title, summary):
    t = f"{title} {summary}".lower()

    mapping = {
        "Microsoft": ["microsoft", "windows", "office", "azure"],
        "Google": ["google", "chrome", "android"],
        "Apple": ["apple", "ios", "macos"],
        "Ubuntu": ["ubuntu"],
        "Red Hat": ["red hat", "rhel"],
        "VMware": ["vmware", "esxi", "vcenter"],
        "Cisco": ["cisco"],
        "Fortinet": ["fortinet", "fortigate"],
        "Palo Alto Networks": ["palo alto", "pan-os"],
        "Check Point": ["checkpoint"],
        "Juniper": ["juniper"]
    }

    for vendor, keys in mapping.items():
        if any(k in t for k in keys):
            return vendor

    return "Multiple / Not Vendor Specific"


def calculate_priority(title, summary):
    t = f"{title} {summary}".lower()

    if any(x in t for x in ["zero-day", "actively exploited", "in the wild"]):
        return "High"
    if any(x in t for x in ["critical", "rce", "remote code execution"]):
        return "High"
    if "patch" in t or "update" in t:
        return "Medium"

    return "Medium"


# ======================
# TEAMS SENDER
# ======================

def send_to_teams(card):
    r = requests.post(TEAMS_WEBHOOK_URL, json=card, timeout=20)
    return r.status_code == 200


# ======================
# MAIN
# ======================

def main():
    log_cron()
    print("[*] Running generate_security_advisory.py")

    if not os.path.exists(CLEAN_NEWS_FILE):
        print("[!] Clean CSV missing — aborting")
        return

    if os.path.getsize(CLEAN_NEWS_FILE) == 0:
        print("[!] Clean CSV empty — skipping alerts")
        return

    notified = load_notified()
    sent = 0

    with open(CLEAN_NEWS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            url = row.get("url", "").strip()
            title = row.get("title", "").strip()
            summary = row.get("summary", "").strip()
            source = row.get("source", "Unknown")
            published = row.get("published", "")

            if not url or url in notified:
                continue

            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                published_str = dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            except:
                published_str = published

            priority = calculate_priority(title, summary)
            oem = detect_oem(title, summary)
            cves = extract_cves(f"{title} {summary}")

            teams_card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": "Security News Update",
                "themeColor": "0076D7",
                "title": "SECURITY NEWS UPDATE",
                "sections": [{
                    "activityTitle": title,
                    "facts": [
                        {"name": "Source", "value": source},
                        {"name": "Priority", "value": priority},
                        {"name": "OEM / Product", "value": oem},
                        {"name": "CVE IDs", "value": cves},
                        {"name": "Published", "value": published_str}
                    ],
                    "text": truncate(summary)
                }],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "View Reference",
                    "targets": [{"os": "default", "uri": url}]
                }]
            }

            print(f"[+] Sending: {title}")

            if send_to_teams(teams_card):
                save_notified(url)
                sent += 1

    print(f"[✓] Sent {sent} new alerts")


if __name__ == "__main__":
    main()