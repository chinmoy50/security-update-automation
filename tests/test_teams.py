import requests
from config import TEAMS_WEBHOOK_URL

payload = {
    "text": "✅ Security News Automation test message from Ubuntu VM"
}

r = requests.post(TEAMS_WEBHOOK_URL, json=payload)
print("Status:", r.status_code)
