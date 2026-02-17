<p align="center">
  <img src="./assets/logo.png" alt="Security Update Automation Logo" width="260"/>
</p>

<h1 align="center">🔐 Security Update Automation</h1>

<p align="center">
  Automated Security Advisory Generation Tool for SOC Teams
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" />
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-red.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success.svg" />
</p>

---

## 📌 Overview

Security Update Automation is a modular Python-based tool designed to fetch, process, classify, and generate structured security advisories from online security feeds.
Built specifically for Security Operations Center (SOC) workflows, this tool automates repetitive monitoring, prioritization, and notification tasks and integrates directly with Microsoft Teams.

---

## 🚀 Features

- 🔎 Automated security news collection  
- 🧹 News cleaning and normalization  
- 🏷 Severity classification and prioritization  
- 🛡 CVE extraction  
- 📝 Structured advisory generation  
- 📣 Microsoft Teams webhook notification  
- 🧱 Modular layered architecture  
- ⚙ CLI-based execution support  

---

## 🏗 Architecture Overview

Collector → Processor → Advisory Generator → Notifier


### Execution Flow

1. Load feed sources from `data/feeds.txt`  
2. Fetch security updates  
3. Clean and normalize content  
4. Classify severity & extract CVEs  
5. Generate structured advisory  
6. Send notification to Microsoft Teams (optional)  

---

## 📂 Project Structure

```text
security-update-automation/
│
├── assets/
│   └── logo.png
│
├── src/
│   ├── main.py
│   ├── collector/
│   │   ├── __init__.py
│   │   └── fetch_news.py
│   │
│   ├── processor/
│   │   ├── __init__.py
│   │   ├── clean_news.py
│   │   ├── news_classifier.py
│   │   └── advisory_generator.py
│   │
│   ├── notifier/
│   │   ├── __init__.py
│   │   └── teams_client.py
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py
│
├── data/
│   └── feeds.txt
│
├── tests/
│   └── test_teams.py
│
├── VERSION
├── CHANGELOG.md
├── SECURITY.md
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠 Setup Guide

Follow these steps to configure and run the project.

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/security-update-automation.git
cd security-update-automation
```

---

### 2️⃣ Create Virtual Environment

#### Windows / WSL

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```


### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```


### 4️⃣ Configure Microsoft Teams Webhook

```bash
cp .env.example .env
```

Edit `.env`:

```text
TEAMS_WEBHOOK_URL=https://your-teams-webhook-url
```


### 5️⃣ Configure Security Feed Sources

Edit the feeds file:

```text
data/feeds.txt
```

Add one feed URL per line, for example:

```text
https://example.com/rss.xml
https://another-source.com/feed
```


### 6️⃣ Run Application

#### Basic Execution

```bash
python -m src.main
```

#### Send Microsoft Teams Notification

```bash
python -m src.main --notify
```

#### Limit Number of Processed Items

```bash
python -m src.main --limit 5 --notify
```
---

## 📊 Sample Advisory Output

```text
🚨 SECURITY NEWS UPDATE

Title: High Severity Security Advisory on vulnerability
Description: A vulnerability in XYZ solutions is found & patched in v20.310.
Source: https://abc.com/rss.xml
Priority: High
OEM / Product: XYZ
CVE IDs: CVE-2026-0001
Published: 2026-02-01 00:00 UTC
Reference Links: https://abc.com/rss.xml
```

---

## 🔒 Security Considerations

- Store secrets only in `.env`
- Do not commit webhook URLs
- Validate external feed content
- Review generated advisories before distribution
- Follow responsible disclosure practices

---

## 📦 Release Information

Current Version: **v1.0.0**

See `CHANGELOG.md` for detailed release history.

---

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository  
2. Create a feature branch  
3. Commit changes with clear messages  
4. Submit a pull request  

Please ensure:

- No secrets are committed  
- Code follows modular structure  
- Documentation is updated if required  

---

## 📝 License

This project is licensed under the MIT License.  
See the `LICENSE` file for full details.

---

## 👨‍💻 Author

**Chinmoy Pathak**  
Security Analyst | Security Automation Enthusiast  

Built to demonstrate practical SOC automation engineering and structured security monitoring workflows.