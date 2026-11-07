# SYNDICATE :: Autonomous Attack Surface Auditor

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67.0-FF4B4B.svg)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/Google_GenAI-Gemini_3.1-4285F4.svg)](https://ai.google.dev/)

An enterprise-grade autonomous attack surface reconnaissance, threat correlation, and automated client deliverable pipeline. Combines raw socket network telemetry with generative threat intelligence to produce client-ready security advisories and automated outreach packages.

---

## Architecture Overview

```
                      +-----------------------------+
                      |   Target Hostname / CIDR    |
                      +--------------+--------------+
                                     |
                       [Phase 1: Reconnaissance]
                                     v
                      +-----------------------------+
                      |     stealth_scanner.py      |
                      | (Non-blocking TCP Connect)  |
                      | (Permutation & Micro-Jitter)|
                      +--------------+--------------+
                                     |
                                     v (JSON Telemetry)
                      +-----------------------------+
                      |   syndicate_orchestrator    |
                      |   (Ingest & Quota Guard)    |
                      +--------------+--------------+
                                     |
                       [Phase 2: AI Threat Modeling]
                                     v
                      +-----------------------------+
                      |   port_advisor_gemini.py    |
                      | (Strict Red/Blue Team Model)|
                      +--------------+--------------+
                                     |
                        +------------+------------+
                        |                         |
                        v                         v
       +-------------------------------+  +-------------------------------+
       |    compile_advisory_pdf.py    |  |     app.py (Streamlit UI)     |
       |  (ReportLab Document Engine)  |  |   (Dark SOC Theme Dashboard)  |
       +---------------+---------------+  +---------------+---------------+
                       |                                  |
                       v                                  v
       +-------------------------------+  +-------------------------------+
       | EXECUTIVE_SECURITY_ADVISORY   |  |   Automated SMTP Dispatch     |
       | (.pdf Deliverable)            |  |   (Port 465 SSL + BCC Tracker)|
       +-------------------------------+  +-------------------------------+
```

---

## Core Capabilities

1. **Stealth TCP Connect Scanner (`stealth_scanner.py`)**:
   - Zero external dependency engine built purely on standard Python `socket` & `ssl`.
   - Probe sequence randomization to defeat sequential port scan heuristics (Snort, Suricata).
   - Dynamic micro-jitter delays (`0.15s` - `0.40s`) to mitigate threshold-based rate limits.
   - Non-invasive protocol inspection (`HEAD` probes and greeting string grabs).

2. **Automated Surface Orchestrator (`syndicate_orchestrator.py`)**:
   - Manages subprocess isolation and execution flow.
   - Intelligent Quota Guard: Bypasses AI threat calls if target surface is clean, conserving API tokens.

3. **GenAI Threat Modeler (`port_advisor_gemini.py`)**:
   - Powered by the official `google-genai` SDK (`gemini-3.1-flash-lite`).
   - Strict enterprise system prompt mapping discovered ports to CVE threat vectors (e.g. *regreSSHion*, *Path Traversal*).
   - Generates concrete remediation scripts for Linux (`ufw`/`iptables`) and Windows PowerShell (`New-NetFirewallRule`).

4. **ReportLab Document Automation (`compile_advisory_pdf.py`)**:
   - Generates client-ready `EXECUTIVE_SECURITY_ADVISORY.pdf`.
   - Features corporate header band (`#1e242b`), TLP:AMBER classification badges, service metric grid tables, and running pagination.

5. **Production Streamlit Dashboard (`app.py`)**:
   - Dark corporate Cyber Operations / SOC interface.
   - Real-time terminal output streaming via subprocess pipes.
   - Direct Base64 PDF deliverable downloads in browser.
   - **Integrated SMTP Relay**: Dispatches threat advisories to CISO/decision-maker inboxes via Gmail SSL (Port 465) with silent BCC delivery verification.

---

## Quick Start

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/v7-vdev/syndicate-surface-auditor.git
cd syndicate-surface-auditor
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and set your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Gemini API Key (Get from Google AI Studio: https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=AIzaSy...

# Gmail SMTP Dispatch (Requires Google Account App Password)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
```

### 3. Launch Dashboard

```bash
streamlit run app.py
```
Access the application at `http://localhost:8501`.

---

## CLI Usage

Every component can also be invoked independently from the command line:

```bash
# 1. Standalone Port Scan
python stealth_scanner.py -t scanme.nmap.org -p 22,80

# 2. Standalone AI Threat Advisory
python port_advisor_gemini.py -p "Port 22, Port 80" -o advisory.md

# 3. Full Autonomous Orchestration Cycle
python syndicate_orchestrator.py -t scanme.nmap.org -p 22,80 --no-jitter

# 4. Compile Markdown into Executive PDF
python compile_advisory_pdf.py
```

---

## Repository Structure

```text
├── app.py                      # Streamlit Dark SOC Dashboard & Web Application
├── syndicate_orchestrator.py   # Master automation pipeline orchestrator
├── stealth_scanner.py          # Pure Python socket port reconnaissance engine
├── port_advisor_gemini.py      # Google GenAI threat correlation & advisory engine
├── port_advisor.py             # OpenAI API threat correlation engine (Alternative)
├── compile_advisory_pdf.py     # ReportLab executive PDF document generator
├── mock_service.py             # Local simulated vulnerable target for offline testing
├── FINAL_ADVISORY.md           # Reference markdown threat assessment
├── requirements.txt            # Python dependencies
├── .env.example                # Template for required environment variables
├── .gitignore                  # Strict security gitignore (protects .env and secrets)
└── README.md                   # System documentation
```

---

## Security & Ethical Disclaimer

This tool is designed strictly for authorized penetration testing, vulnerability assessment, defensive network hardening, and educational research. Always obtain explicit written authorization before scanning third-party infrastructure.
