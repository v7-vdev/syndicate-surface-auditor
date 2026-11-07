#!/usr/bin/env python3
"""
AI-Powered Port Vulnerability & Hardening Advisor (Google GenAI Edition)
Author: Elite Cybersecurity Consultant & Principal Engineer
Engine: Official 'google-genai' SDK
Requirements: pip install google-genai
"""

import os
import sys
import argparse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SYSTEM_PROMPT = """You are an elite principal cybersecurity consultant and senior threat analyst.
Your objective is to ingest a list of open network ports provided by an auditor, perform rigorous technical threat modeling, and return an enterprise-grade Vulnerability & Remediation Advisory in clean GitHub-Flavored Markdown.

For EVERY port provided, you must produce:
### 1. Service Identification & Architectural Context
- Standard Service Name & Transport Layer (TCP/UDP)
- Common Production Daemons / Implementations (e.g., vsftpd, OpenSSH, Apache, Nginx)
- Expected Network Boundary (External Internet-facing vs. Internal segmentation)

### 2. Top 3 Known Critical Vulnerabilities & Threat Vectors
- Cite specific CVE identifiers where applicable (e.g., CVE-2024-6387, CVE-2021-41773).
- Threat vector mechanics: How adversaries exploit this exposure (e.g., buffer overflows, unauthenticated RCE, cleartext credential sniffing, brute-force enumeration).
- CVSS Severity rating (CRITICAL / HIGH / MEDIUM).

### 3. Concrete Hardening & Step-by-Step Remediation Commands
- Boundary Enforcement: Immediate firewall blocking commands (provide Linux `ufw`/`iptables` and Windows PowerShell `New-NetFirewallRule` syntax).
- Configuration Hardening: Exact configuration directives (e.g., disabling anonymous login, enforcing key-based SSH authentication, disabling root login, TLS/SSL cipher suites).
- Service Disablement: Commands to stop and disable unnecessary daemons (`systemctl disable --now <service>`).

Maintain a precise, authoritative, and offensive-defensive cybersecurity tone. Do not include conversational filler."""


def load_dotenv():
    """Lightweight .env loader using standard library only."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val


def get_gemini_client():
    """
    Validates the GEMINI_API_KEY environment variable and instantiates the client.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n" + "=" * 70, file=sys.stderr)
        print("[-] CONFIGURATION ERROR: 'GEMINI_API_KEY' environment variable not found.", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print("\n[!] Set your Google Gemini API key to proceed:\n", file=sys.stderr)
        print("    [PowerShell]:   $env:GEMINI_API_KEY=\"AIzaSy...\"", file=sys.stderr)
        print("    [Command Prompt]: set GEMINI_API_KEY=AIzaSy...", file=sys.stderr)
        print("    [Linux / macOS]: export GEMINI_API_KEY=\"AIzaSy...\"\n", file=sys.stderr)
        sys.exit(1)

    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError:
        print("[-] 'google-genai' package is not installed. Run: pip install google-genai", file=sys.stderr)
        sys.exit(1)


def generate_advisory(ports_input: str, model: str = "gemini-3.1-flash-lite") -> str:
    client = get_gemini_client()
    try:
        from google.genai import types
    except ImportError:
        print("[-] 'google-genai' package is not installed. Run: pip install google-genai", file=sys.stderr)
        sys.exit(1)
    user_query = f"The following network ports were identified as OPEN during an assessment:\nPorts: {ports_input}\nGenerate the technical advisory report."

    # List of candidate models in order of priority for automatic fallback
    candidate_models = [model, "gemini-3.5-flash-lite", "gemini-3.8-flash"]
    # De-duplicate while preserving order
    candidate_models = list(dict.fromkeys(candidate_models))

    last_error = None
    for candidate in candidate_models:
        print(f"[*] Querying Google GenAI model [{candidate}]...")
        try:
            response = client.models.generate_content(
                model=candidate,
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2
                )
            )
            return response.text
        except Exception as e:
            print(f"[!] Model {candidate} returned error: {e}. Attempting fallback...")
            last_error = e

    print(f"[-] All GenAI model attempts failed: {last_error}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Google GenAI Port Security Advisor")
    parser.add_argument("-p", "--ports", help="Open ports input string (e.g. 'Port 21 and Port 80')")
    parser.add_argument("-m", "--model", default="gemini-3.1-flash-lite", help="Model name (default: gemini-3.1-flash-lite)")
    parser.add_argument("-o", "--output", help="Output markdown filename")
    args = parser.parse_args()

    ports_input = args.ports
    if not ports_input:
        ports_input = input("Enter open ports (e.g., 'Port 21 and Port 80'): ").strip()

    if not ports_input:
        print("[-] Port specification required.", file=sys.stderr)
        sys.exit(1)

    report_md = generate_advisory(ports_input, model=args.model)
    print("\n" + "=" * 75)
    print(report_md)
    print("=" * 75)

    out_file = args.output or f"security_advisory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[+] Report saved to: {out_file}\n")


if __name__ == "__main__":
    main()
