#!/usr/bin/env python3
"""
SYNDICATE SECURITY HOLDINGS - GROWTH ARCHITECTURE DIVISION
Script: compile_launch_assets.py
Description: Autonomous compiler for the SYNDICATE Product Hunt launch campaign deck.
             Generates high-converting marketing copy, founder narratives, PLG mechanics,
             and lead-capture conversion architectures into 'PRODUCT_HUNT_LAUNCH_DECK.md'.
"""

import os
import sys
from datetime import datetime, timezone

# Enforce clean UTF-8 console output for Windows terminal environments
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(WORKSPACE_DIR, "PRODUCT_HUNT_LAUNCH_DECK.md")

# ==============================================================================
# SECTION 1: THE PRIMARY HOOKS & EXECUTIVE METRICS
# ==============================================================================
PRIMARY_HOOKS = {
    "product_name": "SYNDICATE :: Autonomous Surface Auditor",
    "tagline": "Run stealthy network socket scans and get elite, Gemini-3.1 powered threat advisories in one click.",
    "punchline": "Turn blind perimeter exposure into client-ready, boardroom-grade security advisories in under 30 seconds.",
    "pricing_model": "100% Free Public Audit Engine (Freemium Lead-Gen Architecture)",
    "target_audience": "Founders, CTOs, DevOps Engineers, Pentesting Agencies, Solo Developers",
    "primary_categories": ["Cybersecurity", "Developer Tools", "Artificial Intelligence", "SaaS"],
    "live_demo_url": "https://syndicate-surface-auditor-dgvuuxcbeccrckhe9va9sk.streamlit.app/",
    "github_repo_url": "https://github.com/v7-vdev/syndicate-surface-auditor"
}

# ==============================================================================
# SECTION 2: THE EXPLOITATION STORY (Product Hunt Description Block)
# ==============================================================================
EXPLOITATION_STORY = """# ⚔️ THE EXPLOITATION STORY: Why Firewalls Lie & Scanners Fail

92% of corporate cyber breaches don't start with complex zero-days. They start with an **unmonitored port 22 listener**, a forgotten **Apache staging host on port 80**, or an unpatched daemon leaking its entire banner version to automated Shodan crawlers.

Most startups and lean engineering teams cannot afford a $40,000/year enterprise SOC or a $15,000 external penetration test. Meanwhile, traditional command-line scanners (like raw `nmap`) require manual orchestration, lack contextual intelligence, and produce messy terminal outputs that non-security founders cannot turn into immediate remediation actions.

### 🛡️ Enter SYNDICATE: The Product-Led Growth (PLG) Security Pipeline

**SYNDICATE :: Autonomous Surface Auditor** transforms raw network reconnaissance into high-ticket, boardroom-ready security intelligence with zero installation required:

```
[Target Domain/IP] 
       │
       ▼
 [Stealth Socket Engine] ──(Randomized Probing + Micro-Jitter)──► [Live Telemetry Stream]
       │
       ▼
 [Gemini 3.1 Neural SOC] ──(CVE Correlation: regreSSHion, Apache)──► [Executive Markdown]
       │
       ▼
 [ReportLab Engine] ─────► [Corporate PDF Deliverable] ─────► [Automated SMTP Dispatch]
```

#### ⚡ Core Technological Breakthroughs:

1. **Jittered Stealth Socket Architecture (`stealth_scanner.py`)**:
   - Built on pure Python asynchronous non-blocking sockets.
   - Injects sub-second randomized micro-jitter between probes to bypass threshold-based IDS/IPS rate limits and stateful perimeter firewalls.
   - Performs aggressive banner grabbing without triggering defensive alarm states.

2. **Gemini 3.1 Flash-Lite Autonomous Threat Modeling (`port_advisor_gemini.py`)**:
   - Ingests raw socket banners and correlates listener signatures against active vulnerability indices.
   - Automatically cross-examines known threat vectors (such as **CVE-2024-6387 regreSSHion** on OpenSSH and **CVE-2021-41773 Path Traversal** on Apache).
   - Generates bulletproof, copy-pasteable firewall rules (`iptables`, `ufw`, `PowerShell NetSecurity`) and hardening configs (`sshd_config`, `apache2.conf`).

3. **ReportLab Document Automation Engine (`compile_advisory_pdf.py`)**:
   - Converts the threat assessment into a polished, billing-ready **Executive Security Advisory PDF**.
   - Features corporate dark-gray headers, official **TLP:AMBER** confidentiality classification, clean structured telemetry grids, and C-suite executive summaries.
"""

# ==============================================================================
# SECTION 3: THE FOUNDER'S INAUGURAL ANNOUNCEMENT (First Comment Template)
# ==============================================================================
MAKER_COMMENT = """# 🚀 THE MAKER'S FIRST COMMENT: From Zero to Automated SOC

> **Author:** Ved (Principal Architect & Creator, BCA Student)  
> **Topic:** Welcome to the SYNDICATE Launch!

Hey Product Hunt community! 👋

I'm Ved, a passionate BCA student and security enthusiast, and today I'm thrilled to introduce you to **SYNDICATE :: Autonomous Surface Auditor**.

### 💡 The Genesis Story:
A few months ago, while testing infrastructure security, I noticed a recurring, dangerous trend: brilliant founders launch disruptive apps, but their backend cloud instances leave raw SSH (port 22) and development HTTP (port 80) wide open to the public internet. Within 12 minutes of spinning up a fresh VPS, automated bots and vulnerability bots are already hammering the perimeter.

When founders ask how to fix it, enterprise security vendors quote them tens of thousands of dollars. The open-source CLI tools exist, but parsing terminal flags and translating raw banner outputs into actionable board presentations takes hours that busy founders don't have.

I built **SYNDICATE** from absolute scratch to solve this:
- **No bloated installs:** A dark, sleek Streamlit dashboard that runs seamlessly in your browser.
- **Stealthy telemetry:** Pure Python socket scanner with randomized jitter that respects server thresholds.
- **AI-Powered Incident Response:** Powered by Google's cutting-edge **Gemini 3.1**, turning open ports into precise, verified hardening playbooks and CVE advisories.
- **Instant Executive Deliverables:** One-click automated PDF generation formatted with corporate headers and copy-pasteable firewall commands.

### 🎁 My Free Gift to the Community:
The entire live audit engine is hosted and ready for you right now. 

👉 **Audit your infrastructure live (Free):**  
[https://syndicate-surface-auditor-dgvuuxcbeccrckhe9va9sk.streamlit.app/](https://syndicate-surface-auditor-dgvuuxcbeccrckhe9va9sk.streamlit.app/)

👉 **Inspect our open-source codebase on GitHub:**  
[https://github.com/v7-vdev/syndicate-surface-auditor](https://github.com/v7-vdev/syndicate-surface-auditor)

**My challenge to every founder, CTO, and developer here today:**  
Paste your primary domain or public staging IP into the scanner. Watch the live console stream in real time. If SYNDICATE discovers an exposed listener, grab the generated mitigation playbook and patch it before dinner.

I'll be hanging out in the comments all day—I'd love to hear your feedback, feature requests, and edge-case network setups! Let's fortify your perimeter together. 🛡️
"""

# ==============================================================================
# SECTION 4: THE CONVERSION TRAP REVEAL (Monetization & Lead-Gen Blueprint)
# ==============================================================================
CONVERSION_TRAP_REVEAL = """# 💰 THE CONVERSION TRAP REVEAL: Monetizing Free Top-of-Funnel Traffic

How does a 100% free security tool generate recurring high-ticket monthly retainer revenue?

By deploying a psychological **Restricted-Artifact Value Gate**:

### 🎯 The 4-Step Funnel Architecture:

1. **The Frictionless Hook (Zero Barrier to Entry)**:
   - Users land on the sleek dark-themed dashboard.
   - They enter their Target Host and select ports. No signup or credit card required.
   - The scanner executes immediately, streaming live console output and proving undeniable utility.

2. **The High-Value Deliverable Reveal**:
   - The scan completes and displays the markdown assessment.
   - Simultaneously, the backend quietly executes `compile_advisory_pdf.py`, generating a pristine, boardroom-ready `EXECUTIVE_SECURITY_ADVISORY.pdf`.
   - The raw download button is **strictly gated** behind the **"🔒 SECURITY ARTIFACT EXPORT PROTOCOL"** card.

3. **The Executive Email Capture Gate**:
   - To unlock the formal PDF deliverable, decision makers must input their corporate email address.
   - The interaction verifies the email and instantly records the lead into `syndicate_lead_ledger.csv`:
     ```
     [Timestamp] | [Target Domain] | [Discovered Open Ports] | [Client Corporate Email]
     ```
   - This builds an exceptionally high-intent B2B database of companies with verified, active perimeter vulnerabilities.

4. **The Instant Value Shock (Automated SMTP Routing)**:
   - The moment the client clicks **"🔓 UNLOCK & DISPATCH INTEL COMPLIANCE DELIVERABLE"**:
     - The browser download button unlocks instantly.
     - A background SSL SMTP worker (`smtp.gmail.com:465`) dispatches the encrypted advisory directly to the executive's corporate inbox with dynamic domain personalization.
     - A silent `Bcc` tracking flag pings the internal sales team, triggering an automated warm outreach sequence for full-scale monthly penetration testing retainers.

**Result:** 100% organic, viral Product Hunt traffic is continuously converted into qualified enterprise cybersecurity leads.
"""

# ==============================================================================
# SECTION 5: COMPILER EXECUTION LOGIC
# ==============================================================================
def compile_launch_deck():
    """Compiles all launch assets into a master Markdown document."""
    generation_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    deck_content = f"""# 🚀 SYNDICATE :: PRODUCT HUNT LAUNCH MARKETING CAMPAIGN DECK
**Generated:** {generation_timestamp}  
**Architecture:** Autonomous Attack Surface Intelligence & Lead-Generation Funnel  
**Repository:** [{PRIMARY_HOOKS['github_repo_url']}]({PRIMARY_HOOKS['github_repo_url']})  
**Live Production URL:** [{PRIMARY_HOOKS['live_demo_url']}]({PRIMARY_HOOKS['live_demo_url']})

---

## 📌 TABLE OF CONTENTS
1. [Executive Launch Metadata & Primary Hooks](#1-executive-launch-metadata--primary-hooks)
2. [The Exploitation Story (Product Description Block)](#2-the-exploitation-story-the-description-block)
3. [The Maker's Inaugural Announcement (First Comment Template)](#3-the-makers-inaugural-announcement-first-comment-template)
4. [The Conversion Trap Reveal (PLG Lead Generation Engine)](#4-the-conversion-trap-reveal-the-conversion-trap-reveal)
5. [Social Proof & Launch Day Tweet Storm](#5-social-proof--launch-day-tweet-storm)

---

## 1. EXECUTIVE LAUNCH METADATA & PRIMARY HOOKS

| Asset Parameter | Configured Value |
| :--- | :--- |
| **Product Name** | `{PRIMARY_HOOKS['product_name']}` |
| **Marketing Tagline** | *"{PRIMARY_HOOKS['tagline']}"* |
| **Elevator Pitch** | {PRIMARY_HOOKS['punchline']} |
| **Pricing Model** | {PRIMARY_HOOKS['pricing_model']} |
| **Target Persona** | {PRIMARY_HOOKS['target_audience']} |
| **Topic Categories** | {", ".join(PRIMARY_HOOKS['primary_categories'])} |
| **Live App Endpoint** | [{PRIMARY_HOOKS['live_demo_url']}]({PRIMARY_HOOKS['live_demo_url']}) |
| **Source Repository** | [{PRIMARY_HOOKS['github_repo_url']}]({PRIMARY_HOOKS['github_repo_url']}) |

---

{EXPLOITATION_STORY}

---

{MAKER_COMMENT}

---

{CONVERSION_TRAP_REVEAL}

---

## 5. SOCIAL PROOF & LAUNCH DAY TWEET STORM

### 🐦 Launch Tweet (Thread Starter):
```text
🚨 92% of cyber breaches start with a single exposed port.

Today, we're launching SYNDICATE on @ProductHunt:
An autonomous attack surface auditor that scans your perimeter with stealth micro-jitter, models CVEs using Gemini 3.1, and outputs billing-ready executive security PDFs in seconds.

100% Free. Test your armor now 👇
{PRIMARY_HOOKS['live_demo_url']}
```

### 🐦 The Tech Architecture Tweet:
```text
Why does traditional scanning fail?
Threshold firewalls detect synchronous port sweeps in milliseconds.

SYNDICATE uses:
🔹 Asynchronous non-blocking sockets with sub-second randomized jitter
🔹 Google Gemini 3.1 Flash-Lite threat modeling
🔹 ReportLab corporate PDF compiler

Zero fluff. Pure defense.
```

---
*Deck compiled by SYNDICATE Growth Engine v2.0.*
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(deck_content)

    print("=" * 78)
    print("  [+] VICTORY: PRODUCT HUNT LAUNCH DECK COMPILED SUCCESSFULLY!")
    print(f"  [+] Target Artifact Path: {OUTPUT_FILE}")
    print(f"  [+] Payload Size: {len(deck_content)} bytes")
    print(f"  [+] Status: Boardroom & Community Ready (100% Zero-Error Execution)")
    print("=" * 78)


if __name__ == "__main__":
    compile_launch_deck()
