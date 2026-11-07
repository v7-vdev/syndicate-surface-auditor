#!/usr/bin/env python3
"""
SYNDICATE :: Autonomous Surface Auditor
Principal Full-Stack Security Engineer & UX/UI Master Edition
Powered by Streamlit, Python Sockets, and Google GenAI
"""

import os
import sys
import json
import time
import subprocess
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import streamlit as st

# ==============================================================================
# STREAMLIT CONFIG & THEME INJECTION
# ==============================================================================
st.set_page_config(
    page_title="SYNDICATE :: Surface Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    /* Dark Cyberpunk / Corporate SOC Theme */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    code, pre, .terminal-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container background subtle gradient */
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }

    /* Card styling */
    .soc-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    /* Status Badges */
    .badge-online {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(46, 160, 67, 0.2);
        color: #3fb950;
        border: 1px solid #2ea043;
    }

    .badge-target {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        border: 1px solid #388bfd;
    }

    /* Terminal Console Window */
    .terminal-container {
        background-color: #05070a;
        border: 1px solid #1f242c;
        border-radius: 8px;
        padding: 16px;
        max-height: 400px;
        overflow-y: auto;
        color: #39ff14;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #000000 !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        color: #000000 !important;
    }

    /* Premium Billing-Ready Download Button */
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2ea043 0%, #238636 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.8px !important;
        border: 1px solid #3fb950 !important;
        border-radius: 6px !important;
        padding: 14px 24px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 18px rgba(46, 160, 67, 0.35);
    }

    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #3fb950 0%, #2ea043 100%) !important;
        box-shadow: 0 6px 24px rgba(63, 185, 80, 0.6);
        color: #ffffff !important;
        transform: translateY(-1px);
    }

    /* Accent-Colored Email Dispatch Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #7928ca 0%, #ff0080 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.8px !important;
        border: 1px solid #ff0080 !important;
        border-radius: 6px !important;
        padding: 14px 24px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 18px rgba(255, 0, 128, 0.35) !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ff0080 0%, #7928ca 100%) !important;
        box-shadow: 0 6px 25px rgba(255, 0, 128, 0.6) !important;
        transform: translateY(-1px);
        color: #ffffff !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
ORCHESTRATOR_SCRIPT = os.path.join(WORKSPACE_DIR, "syndicate_orchestrator.py")


def load_dotenv():
    """Loads key-value pairs from .env into os.environ if not already present."""
    env_path = os.path.join(WORKSPACE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        os.environ[k] = v

load_dotenv()


def dispatch_security_email(recipient_email: str, target_name: str, pdf_path: str) -> tuple[bool, str]:
    """
    Securely routes the executive security advisory to the recipient via Gmail SMTP SSL on port 465.
    """
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        return False, "Missing credentials: 'SENDER_EMAIL' or 'SENDER_PASSWORD' environment variables are not configured."

    if not os.path.exists(pdf_path):
        return False, f"Deliverable artifact '{os.path.basename(pdf_path)}' was not found on disk."

    msg = MIMEMultipart()
    msg["From"] = f"Syndicate Threat Intelligence <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = f"CRITICAL ADVISORY: Perimeter Attack Surface Disclosures for {target_name} [TLP:AMBER]"

    discovery_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    email_body = f"""Dear Executive Security Leadership,

During an automated perimeter security evaluation conducted by the Syndicate Security Audit Engine, active listener daemons and perimeter exposures were identified on your external infrastructure:

  • Target Entity: {target_name}
  • Timestamp of Discovery: {discovery_time}
  • Classification: TLP:AMBER (Confidential / Remediation Advised)

Attached to this communication is our full executive deliverable:
'EXECUTIVE_SECURITY_ADVISORY.pdf'

The attached advisory includes:
  1. Service identification, version disclosures, and network boundaries.
  2. Top known CVE threat vectors (including unauthenticated remote exploitation risks).
  3. Step-by-step firewall boundary and configuration remediation commands for Linux and Windows infrastructure.

This formal notification is delivered to facilitate immediate perimeter mitigation before unauthorized exploitation occurs.

Respectfully,

Lead Security Operations Architect
SYNDICATE SECURITY HOLDINGS
Incident Response & Attack Surface Intelligence Division
https://syndicate-security.internal
"""
    msg.attach(MIMEText(email_body, "plain"))

    try:
        with open(pdf_path, "rb") as f_attach:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f_attach.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}"
        )
        msg.attach(part)

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=15) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [recipient_email], msg.as_string())

        return True, f"Threat advisory deliverable successfully dispatched to {recipient_email} via smtp.gmail.com:465"
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail SMTP Authentication Failed. Ensure you are using a 16-character Google App Password (not your personal Google account password)."
    except Exception as e:
        return False, f"SMTP Transmission Failure: {str(e)}"


# ==============================================================================
# SIDEBAR CONFIGURATION
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM TELEMETRY")
    
    # Engine status checks
    gemini_key_present = bool(os.getenv("GEMINI_API_KEY"))
    email_creds_present = bool(os.getenv("SENDER_EMAIL") and os.getenv("SENDER_PASSWORD"))

    col1, col2 = st.columns([3, 2])
    with col1:
        st.write("Socket Scanner:")
        st.write("GenAI Engine:")
        st.write("SMTP Dispatch:")
    with col2:
        st.markdown('<span class="badge-online">ONLINE</span>', unsafe_allow_html=True)
        if gemini_key_present:
            st.markdown('<span class="badge-online">LINKED</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#f85149; font-weight:600;">KEY MISSING</span>', unsafe_allow_html=True)

        if email_creds_present:
            st.markdown('<span class="badge-online">READY</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#f0883e; font-weight:600;">NOT SET</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 SCAN TUNING")

    timeout_val = st.slider("Socket Connect Timeout (seconds)", min_value=0.3, max_value=3.0, value=1.0, step=0.1)
    evasion_mode = st.toggle("Evasion Timing Jitter", value=True, help="Randomizes packet inter-arrival times (0.15s - 0.40s) to bypass threshold IDS.")
    
    st.markdown("---")
    st.markdown("### 🛡️ ENGINE SPECIFICATIONS")
    st.caption("""
    - **Recon Layer:** Pure-socket non-blocking TCP connect sweep.
    - **Evasion:** Probe permutation + Gaussian micro-jitter.
    - **Intelligence:** Google GenAI (gemini-3.1-flash-lite) Threat Correlation.
    """)

# ==============================================================================
# MAIN DASHBOARD INTERFACE
# ==============================================================================
st.markdown("""
<div style="padding-bottom: 12px;">
    <h1 style="margin: 0; font-size: 2.3rem; letter-spacing: -0.5px; font-weight: 800; background: linear-gradient(90deg, #58a6ff, #39ff14); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        SYNDICATE :: Autonomous Surface Auditor
    </h1>
    <p style="color: #8b949e; margin-top: 4px; font-size: 0.98rem;">
        Enterprise-grade automated reconnaissance, service fingerprinting, and generative threat modeling pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

# Configuration Panel
with st.container():
    st.markdown('<div class="soc-card">', unsafe_allow_html=True)
    
    col_target, col_ports = st.columns([3, 2])

    with col_target:
        target_input = st.text_input(
            "Target Hostname, IPv4, or CIDR Block",
            value="scanme.nmap.org",
            placeholder="e.g. 192.168.1.1, scanme.nmap.org, or 10.0.0.0/29",
            help="Accepts fully qualified domain names, IPv4 addresses, or local subnets."
        )

    with col_ports:
        selected_ports = st.multiselect(
            "Target Port Scope",
            options=[21, 22, 80, 443, 8080, 3389, 8443, 25, 53],
            default=[21, 22, 80, 443, 8080],
            help="Select the common services you wish to audit on the target interface."
        )

    execute_clicked = st.button("⚡ EXECUTE SCAN", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SCAN EXECUTION & REAL-TIME STREAMING
# ==============================================================================
if execute_clicked:
    if not target_input.strip():
        st.error("[-] Target host or IP address is required.")
        st.stop()

    if not selected_ports:
        st.error("[-] At least one target port must be selected.")
        st.stop()

    ports_str = ",".join(str(p) for p in selected_ports)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_target = target_input.replace("/", "_").replace(".", "_")
    output_report_file = os.path.join(WORKSPACE_DIR, f"FINAL_ADVISORY_{clean_target}_{timestamp}.md")
    output_json_file = os.path.join(WORKSPACE_DIR, f"telemetry_{clean_target}_{timestamp}.json")

    # Command construction
    cmd = [
        sys.executable,
        ORCHESTRATOR_SCRIPT,
        "-t", target_input.strip(),
        "-p", ports_str,
        "--timeout", str(timeout_val),
        "-o", output_report_file
    ]
    if not evasion_mode:
        cmd.append("--no-jitter")

    st.markdown("### 📡 LIVE ORCHESTRATION CONSOLE")
    console_placeholder = st.empty()
    console_lines = []

    start_time = time.time()

    with st.status("Executing Syndicate Pipeline...", expanded=True) as status_box:
        st.write("Initializing child orchestrator subprocess...")
        
        sub_env = os.environ.copy()
        sub_env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            cwd=WORKSPACE_DIR,
            env=sub_env
        )

        for line in iter(process.stdout.readline, ''):
            clean_line = line.rstrip()
            if clean_line:
                console_lines.append(clean_line)
                # Keep last 15 lines visible in live display
                tail = "\n".join(console_lines[-18:])
                console_placeholder.code(tail, language="bash")

        process.stdout.close()
        return_code = process.wait()

        elapsed = round(time.time() - start_time, 2)

        if return_code == 0:
            status_box.update(label=f"Pipeline Completed Successfully in {elapsed}s", state="complete", expanded=False)
        else:
            status_box.update(label=f"Pipeline Exited with Code {return_code}", state="error", expanded=False)

    # ==============================================================================
    # REPORT PRESENTATION & DATA RENDER
    # ==============================================================================
    st.markdown("---")
    
    # Check if a markdown report was produced
    if os.path.exists(output_report_file):
        st.success(f"Audit completed in {elapsed} seconds. Surface threat advisory generated!")

        with open(output_report_file, "r", encoding="utf-8") as f:
            advisory_md = f.read()

        tab_advisory, tab_telemetry, tab_terminal = st.tabs([
            "📋 EXECUTIVE THREAT ADVISORY", 
            "📊 TELEMETRY JSON", 
            "💻 FULL CONSOLE LOG"
        ])

        with tab_advisory:
            st.markdown(advisory_md)
            st.download_button(
                label="📥 Download Threat Advisory (.md)",
                data=advisory_md,
                file_name=os.path.basename(output_report_file),
                mime="text/markdown",
                use_container_width=True
            )

        with tab_telemetry:
            # Locate the generated JSON
            matched_json = None
            if os.path.exists(output_json_file):
                matched_json = output_json_file
            else:
                # Look for matching pattern in directory
                for fname in os.listdir(WORKSPACE_DIR):
                    if fname.startswith(f"telemetry_{clean_target}") and fname.endswith(".json"):
                        matched_json = os.path.join(WORKSPACE_DIR, fname)
                        break

            if matched_json and os.path.exists(matched_json):
                with open(matched_json, "r", encoding="utf-8") as f:
                    telemetry_data = json.load(f)
                st.json(telemetry_data)
                st.download_button(
                    label="📥 Download Telemetry (.json)",
                    data=json.dumps(telemetry_data, indent=4),
                    file_name=os.path.basename(matched_json),
                    mime="application/json"
                )
            else:
                st.info("No separate telemetry JSON artifact was generated (Clean target surface).")

        with tab_terminal:
            st.code("\n".join(console_lines), language="bash")

        # ==============================================================================
        # PREMIUM BILLING-READY SECURITY ADVISORY (PDF) ACTION BLOCK
        # ==============================================================================
        executive_pdf_path = os.path.join(WORKSPACE_DIR, "EXECUTIVE_SECURITY_ADVISORY.pdf")
        pdf_ready = False

        try:
            from compile_advisory_pdf import compile_pdf_direct
            compile_pdf_direct(output_report_file, executive_pdf_path)
            pdf_ready = True
        except Exception as e:
            st.warning(f"[-] Document Automation Engine notice: {e}")

        if pdf_ready and os.path.exists(executive_pdf_path):
            with open(executive_pdf_path, "rb") as f_pdf:
                pdf_binary = f_pdf.read()

            st.markdown("---")
            st.markdown("""
            <div style="background: linear-gradient(90deg, #161b22 0%, #0d1117 100%); border: 1px solid #30363d; border-left: 4px solid #2ea043; border-radius: 8px; padding: 20px 24px; margin-top: 25px; margin-bottom: 16px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1.18rem; letter-spacing: -0.3px;">
                            🛡️ EXECUTIVE DELIVERABLE READY FOR CLIENT EXPORT
                        </h4>
                        <p style="margin: 5px 0 0 0; color: #8b949e; font-size: 0.88rem;">
                            Compiled by ReportLab Document Automation. Formatted with corporate header band, TLP:AMBER classification, structured service grids, and step-by-step firewall hardening rules.
                        </p>
                    </div>
                    <div>
                        <span style="background: rgba(46, 160, 67, 0.15); color: #3fb950; border: 1px solid #2ea043; padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;">
                            BILLING READY
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="📥 DOWNLOAD BILLING-READY SECURITY ADVISORY (PDF)",
                data=pdf_binary,
                file_name="EXECUTIVE_SECURITY_ADVISORY.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            # ==============================================================================
            # ENTERPRISE EMAIL DISPATCHING MODULE (SMTP SSL 465)
            # ==============================================================================
            st.markdown("---")
            target_decision_email = st.text_input(
                "Target Decision Maker's Corporate Email",
                placeholder="e.g. ciso@target-corporation.com or security-lead@target.com",
                key="target_decision_maker_corporate_email",
                help="Specify the executive recipient address for direct security deliverable routing."
            )

            dispatch_action_clicked = st.button(
                "✉️ DISPATCH THREAT ADVISORY TO TARGET",
                type="primary",
                use_container_width=True,
                key="dispatch_threat_advisory_btn"
            )

            if dispatch_action_clicked:
                clean_target_email = target_decision_email.strip()

                # Step 1: Input Validation
                if not clean_target_email or "@" not in clean_target_email or "." not in clean_target_email:
                    st.error("[-] Input Fault: Please provide a valid corporate recipient email address.")
                else:
                    # Step 2: Strict Transactional Logic Block
                    with st.spinner("Connecting to smtp.gmail.com:465 via SSL/TLS and transmitting deliverable..."):
                        try:
                            # Verify environment configurations
                            load_dotenv()
                            sender_user = os.getenv("SENDER_EMAIL")
                            sender_secret = os.getenv("SENDER_PASSWORD")

                            if not sender_user or not sender_secret:
                                raise ValueError("Missing authentication credentials: 'SENDER_EMAIL' or 'SENDER_PASSWORD' are not set in environment or .env file.")

                            # Read and encode local PDF artifact
                            local_pdf_path = os.path.join(WORKSPACE_DIR, "EXECUTIVE_SECURITY_ADVISORY.pdf")
                            if not os.path.exists(local_pdf_path):
                                raise FileNotFoundError(f"Local artifact '{os.path.basename(local_pdf_path)}' not found in workspace.")

                            with open(local_pdf_path, "rb") as pdf_file_obj:
                                pdf_data_bytes = pdf_file_obj.read()

                            # Match recipient domain dynamically for cold outreach personalization
                            recipient_domain = clean_target_email.split("@")[-1].lower()
                            org_identifier = recipient_domain.split(".")[0].upper()
                            dispatch_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

                            # Assemble MIME Container
                            mail_container = MIMEMultipart()
                            mail_container["From"] = f"Syndicate Threat Operations <{sender_user}>"
                            mail_container["To"] = clean_target_email
                            mail_container["Subject"] = f"SECURITY ADVISORY // Critical Perimeter Exposure Disclosures ({recipient_domain}) [TLP:AMBER]"
                            
                            # Silently append BCC tracker back to sender for delivery confirmation
                            mail_container["Bcc"] = sender_user

                            cold_outreach_body = f"""Dear Security Leadership & Technical Decision Makers at {org_identifier} ({recipient_domain}),

During an active perimeter reconnaissance assessment conducted by the Syndicate Autonomous Security Engine, unauthorized listener daemons and exposed perimeter transmission vectors were identified across network infrastructure associated with {recipient_domain}.

ASSESSMENT TELEMETRY & DELIVERABLE SPECIFICATIONS:
---------------------------------------------------------------------------------
• Target Entity / Domain     : {recipient_domain}
• Timestamp of Discovery     : {dispatch_timestamp}
• Sensitivity Classification : TLP:AMBER (Confidential / Immediate Remediation Advised)
• Attached Deliverable       : EXECUTIVE_SECURITY_ADVISORY.pdf
---------------------------------------------------------------------------------

KEY DELIVERABLE HIGHLIGHTS:
1. Exact perimeter daemon version disclosures and transport-layer boundary classifications.
2. Top known CVE threat vectors (including unauthenticated remote exploitation and cleartext credential exposures).
3. Concrete, copy-pasteable firewall rules and configuration hardening playbooks for immediate boundary mitigation (Linux UFW/iptables and Windows PowerShell).

This formal notification and technical dossier have been routed directly to your technical leadership to facilitate immediate mitigation before unauthorized external exploitation occurs.

Respectfully,

Lead Security Operations Architect
SYNDICATE SECURITY HOLDINGS
Perimeter Intelligence & Threat Operations Division
https://syndicate-security.internal
"""
                            mail_container.attach(MIMEText(cold_outreach_body, "plain"))

                            # Base64 attachment packaging
                            pdf_mime_payload = MIMEBase("application", "octet-stream")
                            pdf_mime_payload.set_payload(pdf_data_bytes)
                            encoders.encode_base64(pdf_mime_payload)
                            pdf_mime_payload.add_header(
                                "Content-Disposition",
                                "attachment",
                                filename="EXECUTIVE_SECURITY_ADVISORY.pdf"
                            )
                            mail_container.attach(pdf_mime_payload)

                            # Route via Google SMTP Relays on Port 465 SSL
                            secure_ssl_ctx = ssl.create_default_context()
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=secure_ssl_ctx, timeout=20) as smtp_relays:
                                smtp_relays.login(sender_user, sender_secret)
                                # Transmit to primary recipient and silent BCC tracker
                                smtp_relays.sendmail(sender_user, [clean_target_email, sender_user], mail_container.as_string())

                            # Step 5: Zero-error confirmation feedback
                            st.success("🚀 DISPATCH SUCCESSFUL: Server accepted transaction. Deliverable has left the chamber.")
                            print(f"\n[+] DISPATCH CONFIRMED: Deliverable successfully transmitted to {clean_target_email} (BCC: {sender_user}) via smtp.gmail.com:465")

                        except FileNotFoundError as fnf_err:
                            st.error(f"[-] File-Missing Fault: {fnf_err}")
                            print(f"[-] File-Missing Fault: {fnf_err}", file=sys.stderr)
                        except smtplib.SMTPAuthenticationError:
                            st.error("[-] Authentication Fault: Gmail SMTP authentication rejected. Verify that SENDER_EMAIL and the 16-character App Password in .env are active.")
                            print("[-] SMTP Authentication Fault: Invalid credentials.", file=sys.stderr)
                        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, ssl.SSLError) as conn_err:
                            st.error(f"[-] Connection Fault: Secure SSL tunnel connection failed to smtp.gmail.com:465 - {conn_err}")
                            print(f"[-] Connection Fault: {conn_err}", file=sys.stderr)
                        except Exception as general_err:
                            st.error(f"[-] Transactional Fault: {general_err}")
                            print(f"[-] Transactional Fault: {general_err}", file=sys.stderr)

    else:
        # Check if the scan completed cleanly with no open ports
        st.info("ℹ️ **Target Surface Clean**: No open ports were detected on the specified host. AI advisory generation was bypassed to conserve resources.")
        with st.expander("View Full Console Execution"):
            st.code("\n".join(console_lines), language="bash")

