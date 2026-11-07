#!/usr/bin/env python3
"""
Syndicate Orchestrator // Autonomous Attack Surface Assessment Pipeline
Author: Elite Cybersecurity Architect
Architecture:
  [Phase 1: Reconnaissance] -> Executes stealth_scanner.py (Subprocess)
  [Phase 2: Ingestion]      -> Parses forensic JSON telemetry
  [Phase 3: Threat AI]      -> Dispatches discovered vectors to port_advisor_gemini.py
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# Ensure standard output and error streams handle Unicode seamlessly across Windows codepages
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANNER_SCRIPT = os.path.join(WORKSPACE_DIR, "stealth_scanner.py")
ADVISOR_SCRIPT = os.path.join(WORKSPACE_DIR, "port_advisor_gemini.py")


def banner():
    print(r"""
===========================================================================
  ____  _   _ _   _ ____ ___ ____    _  _____ _____ 
 / ___|| | | | \ | |  _ \_ _/ ___|  / \|_   _| ____|
 \___ \| |_| |  \| | | | | | |     / _ \ | | |  _|  
  ___) |  _  | |\  | |_| | | |___ / ___ \| | | |___ 
 |____/|_| |_|_| \_|____/___\____/_/   \_\_| |_____|
      :: AUTONOMOUS ATTACK SURFACE ORCHESTRATOR ::
===========================================================================
    """)


def verify_prerequisites():
    """Validates presence of core orchestration modules and Python environment."""
    if not os.path.exists(SCANNER_SCRIPT):
        print(f"[-] FATAL: Scanner engine not found at: {SCANNER_SCRIPT}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(ADVISOR_SCRIPT):
        print(f"[-] FATAL: AI Advisor engine not found at: {ADVISOR_SCRIPT}", file=sys.stderr)
        sys.exit(1)


def execute_reconnaissance(target: str, ports: Optional[str], timeout: float, no_jitter: bool, json_output_path: str) -> bool:
    """
    Executes 'stealth_scanner.py' as an isolated child subprocess.
    """
    print("\n" + "=" * 75)
    print(f"[*] PHASE 1: DISPATCHING RECONNAISSANCE ENGINE")
    print(f"[*] Target Scope: {target}")
    print("=" * 75)

    cmd = [
        sys.executable,
        SCANNER_SCRIPT,
        "-t", target,
        "--timeout", str(timeout),
        "-o", json_output_path
    ]

    if ports:
        cmd.extend(["-p", ports])
    if no_jitter:
        cmd.append("--no-jitter")

    try:
        # Run scanner and stream stdout live to operator terminal
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[-] Reconnaissance subprocess terminated abnormally (Exit code: {e.returncode})", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"[-] Unable to invoke Python interpreter at: {sys.executable}", file=sys.stderr)
        return False


def extract_open_ports(json_path: str) -> List[int]:
    """
    Ingests and parses scanner JSON output, isolating uniquely identified open ports.
    """
    if not os.path.exists(json_path):
        print(f"[-] Telemetry artifact missing: {json_path}", file=sys.stderr)
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)

        results = data.get("results", {})
        open_ports = set()

        for host_ip, findings in results.items():
            for item in findings:
                port_num = item.get("port")
                if port_num is not None:
                    open_ports.add(int(port_num))

        return sorted(list(open_ports))
    except Exception as e:
        print(f"[-] Telemetry parsing failed: {e}", file=sys.stderr)
        return []


def execute_ai_threat_modeling(open_ports: List[int], final_report_path: str) -> bool:
    """
    Transforms extracted ports into a structured parameter string and triggers 'port_advisor_gemini.py'.
    """
    ports_arg = ", ".join([f"Port {p}" for p in open_ports])

    print("\n" + "=" * 75)
    print(f"[*] PHASE 2: THREAT MODELING & ADVISORY GENERATION")
    print(f"[*] Feeding Discovered Surface Vectors: {ports_arg}")
    print(f"[*] Output Report Artifact: {final_report_path}")
    print("=" * 75 + "\n")

    cmd = [
        sys.executable,
        ADVISOR_SCRIPT,
        "-p", ports_arg,
        "-o", final_report_path
    ]

    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[-] Threat Advisory subprocess failed (Exit code: {e.returncode})", file=sys.stderr)
        return False


def main():
    banner()
    verify_prerequisites()

    parser = argparse.ArgumentParser(
        description="Syndicate Orchestrator - Automated Reconnaissance to Threat Intelligence Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-t", "--target", help="Target hostname, IPv4 address, or CIDR block")
    parser.add_argument("-p", "--ports", help="Custom comma-separated port list (e.g. 21,22,80,443,8080)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Per-port socket timeout in seconds (default: 1.0)")
    parser.add_argument("--no-jitter", action="store_true", help="Disable evasion timing jitter for accelerated scans")
    parser.add_argument("-o", "--output", help="Custom output path for the final Markdown Threat Advisory")

    args = parser.parse_args()

    # 1. Acquire Target
    target = args.target
    if not target:
        target = input("Enter target IP, hostname, or CIDR: ").strip()

    if not target:
        print("[-] Error: A target must be specified to initialize the syndicate pipeline.", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_target = target.replace("/", "_").replace(".", "_")
    temp_json_path = os.path.join(WORKSPACE_DIR, f"telemetry_{clean_target}_{timestamp}.json")
    final_report_path = args.output or os.path.join(WORKSPACE_DIR, f"FINAL_ADVISORY_{clean_target}_{timestamp}.md")

    # 2. Phase 1: Reconnaissance
    scan_success = execute_reconnaissance(
        target=target,
        ports=args.ports,
        timeout=args.timeout,
        no_jitter=args.no_jitter,
        json_output_path=temp_json_path
    )

    if not scan_success:
        print("[-] Syndicate aborted during reconnaissance phase.", file=sys.stderr)
        sys.exit(1)

    # 3. Phase 2: Ingest & Extract Ports
    open_ports = extract_open_ports(temp_json_path)

    if not open_ports:
        print("\n" + "=" * 75)
        print("[*] ORCHESTRATION SUMMARY: CLEAN TARGET SURFACE")
        print(f"[*] No open ports were detected on target '{target}'.")
        print("[*] Bypassing AI Threat Modeling phase to conserve API quota.")
        print("=" * 75 + "\n")
        sys.exit(0)

    print(f"\n[+] Ingestion Complete: Isolated {len(open_ports)} exposed port(s): {open_ports}")

    # 4. Phase 3: AI Threat Modeling & Remediation Generation
    advisory_success = execute_ai_threat_modeling(
        open_ports=open_ports,
        final_report_path=final_report_path
    )

    # 5. Pipeline Finalization
    print("\n" + "=" * 75)
    print("                    SYNDICATE PIPELINE COMPLETE                    ")
    print("=" * 75)
    if advisory_success:
        print(f"[+] 1. Reconnaissance Telemetry Artifact : {temp_json_path}")
        print(f"[+] 2. Executive Threat Advisory Report   : {final_report_path}")
        print("\n[*] Execution finished successfully with zero manual intervention.")
    else:
        print("[-] Advisory generation encountered an error. Telemetry JSON preserved for inspection.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Syndicate pipeline halted by operator.")
        sys.exit(0)

