#!/usr/bin/env python3
"""
Lightweight, Stealth-Conscious TCP Port Scanner & Vulnerability Profiler (v3.5)
Author: Cybersecurity Specialist
Standard Library Only: socket, ssl, re, json, random, time, sys, argparse, ipaddress
"""

import socket
import ssl
import re
import json
import random
import time
import sys
import argparse
import ipaddress
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Target ports with service classification and banner probe strategies
DEFAULT_PORTS = {
    21:   {"service": "FTP",      "proto": "read_first"},
    22:   {"service": "SSH",      "proto": "read_first"},
    80:   {"service": "HTTP",     "proto": "http"},
    443:  {"service": "HTTPS",    "proto": "https"},
    8080: {"service": "HTTP-Alt", "proto": "http"}
}

# Known vulnerability signatures for heuristic risk assessment
VULN_SIGNATURES = [
    {
        "ports": [21],
        "pattern": r"vsftpd 2\.3\.4",
        "cve": "CVE-2011-2523",
        "severity": "CRITICAL",
        "desc": "vsftpd 2.3.4 Backdoor - Command execution vulnerability."
    },
    {
        "ports": [21],
        "pattern": r".*",
        "cve": "CWE-319",
        "severity": "MEDIUM",
        "desc": "Cleartext Authentication: Plaintext transmission of credentials."
    },
    {
        "ports": [22],
        "pattern": r"OpenSSH_(8\.[5-9]|9\.[0-7])",
        "cve": "CVE-2024-6387",
        "severity": "HIGH",
        "desc": "regreSSHion: Potential unauthenticated Remote Code Execution in OpenSSH."
    },
    {
        "ports": [80, 8080],
        "pattern": r"Apache/2\.4\.(49|50)",
        "cve": "CVE-2021-41773 / CVE-2021-42013",
        "severity": "CRITICAL",
        "desc": "Path traversal and remote code execution in Apache HTTP Server."
    },
    {
        "ports": [80, 8080],
        "pattern": r".*",
        "cve": "CWE-319",
        "severity": "LOW",
        "desc": "Unencrypted HTTP: Lack of TLS transport protection."
    },
    {
        "ports": [8080],
        "pattern": r"(Apache-Coyote|Tomcat|Jetty|Werkzeug)",
        "cve": "EXPOSED-MGMT",
        "severity": "MEDIUM",
        "desc": "Dev/App server exposed; check for default administrative credentials."
    }
]


def grab_banner(target_ip: str, port: int, proto: str, timeout: float = 1.2) -> str:
    """Interrogates open ports to extract service identification banners."""
    try:
        if proto == "read_first":
            with socket.create_connection((target_ip, port), timeout=timeout) as s:
                banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
                return banner.splitlines()[0] if banner else "No identification string"

        elif proto in ("http", "https"):
            sock = socket.create_connection((target_ip, port), timeout=timeout)
            
            if proto == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock)

            with sock:
                probe = f"HEAD / HTTP/1.0\r\nHost: {target_ip}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
                sock.sendall(probe.encode("utf-8"))
                response = sock.recv(2048).decode("utf-8", errors="ignore")
                
                headers = []
                for line in response.splitlines():
                    if line.lower().startswith(("server:", "x-powered-by:")):
                        headers.append(line.strip())
                return " | ".join(headers) if headers else "HTTP Active (Headers suppressed)"

    except (socket.timeout, socket.error, ssl.SSLError):
        return "Service active (Probe filtered or timed out)"
    
    return "Unknown response"


def correlate_vulnerabilities(port: int, banner: str) -> List[Dict[str, str]]:
    """Correlates captured service banners with known security flaws."""
    matched = []
    for sig in VULN_SIGNATURES:
        if port in sig["ports"]:
            if re.search(sig["pattern"], banner, re.IGNORECASE):
                matched.append({
                    "cve": sig["cve"],
                    "severity": sig["severity"],
                    "desc": sig["desc"]
                })
    return matched


def scan_single_target(target_ip: str, target_label: str, ports_to_scan: Dict[int, Dict[str, str]], timeout: float, jitter: bool) -> List[Dict[str, Any]]:
    """Performs a randomized, stealthy port scan on a single resolved target IP."""
    scan_order = list(ports_to_scan.keys())
    random.shuffle(scan_order)

    print(f"\n[*] Probing {target_label} [{target_ip}] (Shuffled ports: {scan_order})")
    print("-" * 75)

    findings: List[Dict[str, Any]] = []

    for port in scan_order:
        meta = ports_to_scan[port]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            status = sock.connect_ex((target_ip, port))

            # IF/ELSE: Strictly isolate and report open/vulnerable ports
            if status == 0:
                sock.close()
                banner = grab_banner(target_ip, port, meta["proto"], timeout=timeout)
                threats = correlate_vulnerabilities(port, banner)

                findings.append({
                    "port": port,
                    "service": meta["service"],
                    "banner": banner,
                    "vulnerabilities": threats
                })

                print(f"[+] OPEN PORT: {port:<5}/tcp | Service: {meta['service']:<10}")
                print(f"    Banner : {banner}")
                if threats:
                    for t in threats:
                        print(f"    VULN   : [{t['severity']}] {t['cve']} -> {t['desc']}")
                else:
                    print("    STATUS : Open (No immediate CVE signature matched)")
                print()
            else:
                # Port is closed or filtered - drop silently
                sock.close()

        except (socket.timeout, socket.error):
            sock.close()

        # Stealth timing: micro-jitter to evade rate-limiting heuristics
        if jitter:
            time.sleep(random.uniform(0.15, 0.40))

    return findings


def resolve_targets(raw_target: str) -> List[str]:
    """Resolves a hostname, single IP, or CIDR block into a list of IPv4 addresses."""
    # Check if CIDR notation
    if "/" in raw_target:
        try:
            net = ipaddress.ip_network(raw_target, strict=False)
            hosts = [str(ip) for ip in net.hosts()]
            return hosts if hosts else [str(net.network_address)]
        except ValueError:
            pass

    # Single host / domain name
    try:
        resolved = socket.gethostbyname(raw_target)
        return [resolved]
    except socket.gaierror:
        print(f"[-] DNS Resolution failed for '{raw_target}'.")
        return []


def main():
    parser = argparse.ArgumentParser(description="Stealth TCP Port Scanner & Vulnerability Profiler")
    parser.add_argument("-t", "--target", help="Target hostname, IP, or CIDR (e.g. 192.168.1.1, scanme.org, 10.0.0.0/29)")
    parser.add_argument("-p", "--ports", help="Comma-separated custom ports (e.g. 21,22,80,443,8080)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Per-port socket timeout in seconds (default: 1.0)")
    parser.add_argument("--no-jitter", action="store_true", help="Disable inter-packet micro-jitter (faster scan)")
    parser.add_argument("-o", "--output", help="Optional custom JSON output filename")

    args = parser.parse_args()

    print("=" * 75)
    print("      STEALTH PORT SCANNER & VULNERABILITY AUDITOR (v3.5)           ")
    print("=" * 75)

    # 1. Acquire target
    target_input = args.target
    if not target_input:
        target_input = input("Enter target IP address, hostname, or CIDR: ").strip()

    if not target_input:
        print("[-] Target input cannot be empty. Exiting.")
        sys.exit(1)

    targets = resolve_targets(target_input)
    if not targets:
        print("[-] No valid targets to scan. Exiting.")
        sys.exit(1)

    # 2. Configure target ports
    ports_to_scan = dict(DEFAULT_PORTS)
    if args.ports:
        ports_to_scan = {}
        for p_str in args.ports.split(","):
            p_clean = p_str.strip()
            if p_clean.isdigit():
                p = int(p_clean)
                ports_to_scan[p] = DEFAULT_PORTS.get(p, {"service": f"Custom-{p}", "proto": "read_first"})

    print(f"[*] Total target IP(s) queued : {len(targets)}")
    print(f"[*] Ports per target           : {list(ports_to_scan.keys())}")
    print(f"[*] Socket Timeout             : {args.timeout}s")
    print(f"[*] Micro-Jitter Evasion       : {'Disabled' if args.no_jitter else 'Active (0.15s - 0.40s)'}")

    all_results: Dict[str, Any] = {}

    for ip in targets:
        findings = scan_single_target(
            target_ip=ip,
            target_label=target_input,
            ports_to_scan=ports_to_scan,
            timeout=args.timeout,
            jitter=not args.no_jitter
        )
        if findings:
            all_results[ip] = findings

    print("-" * 75)
    print(f"[*] Scan cycle complete. Hosts with exposed vectors: {len(all_results)}/{len(targets)}")

    # 3. Export JSON report
    if all_results:
        filename = args.output if args.output else f"scan_{targets[0].replace('.', '_')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "target_input": target_input,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "results": all_results
            }, f, indent=4)
        print(f"[+] Full audit report generated: {filename}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Execution terminated by user.")
        sys.exit(0)
