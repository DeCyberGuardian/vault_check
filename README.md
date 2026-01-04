# The Intelligence Vault — vault_check

*No noise. Just signal.*

## Overview

**The Intelligence Vault** is a privacy-first, analyst-controlled security hygiene and intelligence tool designed to help users understand the security posture of their systems. It focuses on **signal over noise**, offering transparent checks without silent network activity or invasive collection.

This project is built for:

* Security practitioners
* Blue team / CTI analysts
* Developers and power users
* Learners building security awareness

> This is **not** an antivirus replacement. It is an **intelligence and hygiene tool**.

---

## Core Principles

* **Local-first execution** (offline by default)
* **Explicit user consent** for online checks
* **No telemetry, no tracking, no data collection**
* **Readable results, not alert fatigue**

---

## Features

### Current (v2 GUI)

* System security summary (OS, firewall, disk encryption)
* Process execution path analysis
* Network interface visibility
* Optional online IP intelligence
* Have I Been Pwned (HIBP) password exposure check (k-anonymity)
* Risk scoring with color-coded severity
* JSON export
* GUI + CLI support

### Planned / Roadmap

* Deep malware scanning (heuristic-based)
* Rootkit and persistence detection
* Memory analysis
* Behavioral anomaly detection
* AI-assisted threat interpretation

---

## Installation

```bash
# Clone repository
git clone https://github.com/<your-username>/the-intelligence-vault.git
cd the-intelligence-vault

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## License

MIT License

---

## Author

**DeCyberGuardian**
Cybersecurity & Threat Intelligence

> Built to help people think clearly about security — not fear it.
