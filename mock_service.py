#!/usr/bin/env python3
"""
Mock Vulnerable Multi-Service Lab for Testing stealth_scanner.py
Listens on port 8080 (simulated vulnerable Apache 2.4.49 web server).
Press Ctrl+C to stop.
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 8080

def start_mock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print("=" * 60)
        print(f"[*] MOCK LAB RUNNING on http://{HOST}:{PORT}")
        print("[*] Simulating: Apache/2.4.49 (CVE-2021-41773)")
        print("[*] Press Ctrl+C at any time to stop this server.")
        print("=" * 60)
    except OSError as e:
        print(f"[-] Could not bind to port {PORT}: {e}")
        sys.exit(1)

    try:
        while True:
            conn, addr = sock.accept()
            try:
                conn.settimeout(2.0)
                # Read probe if sent
                try:
                    conn.recv(1024)
                except socket.timeout:
                    pass

                # Return response with vulnerable server header
                mock_response = (
                    "HTTP/1.0 200 OK\r\n"
                    "Server: Apache/2.4.49 (Unix)\r\n"
                    "X-Powered-By: PHP/7.4.3\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    "<html><body>Mock Target Endpoint</body></html>\r\n"
                )
                conn.sendall(mock_response.encode("utf-8"))
            except Exception:
                pass
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("\n[*] Shutting down mock server.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_mock()
