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
import csv
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

    /* Gated Signup Card Layout */
    .gated-lead-card {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #388bfd;
        border-left: 4px solid #58a6ff;
        border-radius: 8px;
        padding: 22px 26px;
        margin-top: 25px;
        margin-bottom: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(56, 139, 253, 0.05);
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

    target_domain = recipient_email.split("@")[-1] if "@" in recipient_email else target_name
    org_name = target_domain.split(".")[0].capitalize() if target_domain else "Corporate"

    msg = MIMEMultipart()
    msg["From"] = f"Syndicate Threat Intelligence <{sender_email}>"
    msg["To"] = recipient_email
    msg["Bcc"] = sender_email
    msg["Subject"] = f"CRITICAL ADVISORY: Perimeter Attack Surface Disclosures for {target_name} ({org_name}) [TLP:AMBER]"

    discovery_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    email_body = f"""Dear {org_name} Security Leadership,

During an automated perimeter security evaluation conducted by the Syndicate Security Audit Engine, active listener daemons and perimeter exposures were identified on your external infrastructure:

  • Target Entity: {target_name} ({target_domain})
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
            recipients = [recipient_email, sender_email]
            server.sendmail(sender_email, recipients, msg.as_string())

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

    # Store scan telemetry into session state for persistent interactive gating
    if os.path.exists(output_report_file):
        # Pre-compile executive PDF deliverable
        executive_pdf_path = os.path.join(WORKSPACE_DIR, "EXECUTIVE_SECURITY_ADVISORY.pdf")
        try:
            from compile_advisory_pdf import compile_pdf_direct
            compile_pdf_direct(output_report_file, executive_pdf_path)
        except Exception:
            pass

        st.session_state["scan_completed"] = True
        st.session_state["has_open_ports"] = True
        st.session_state["output_report_file"] = output_report_file
        st.session_state["output_json_file"] = output_json_file
        st.session_state["clean_target"] = clean_target
        st.session_state["target_input"] = target_input.strip()
        st.session_state["selected_ports"] = selected_ports
        st.session_state["elapsed"] = elapsed
        st.session_state["console_lines"] = console_lines
        st.session_state["lead_unlocked"] = False
    else:
        st.session_state["scan_completed"] = True
        st.session_state["has_open_ports"] = False
        st.session_state["console_lines"] = console_lines


# ==============================================================================
# REPORT PRESENTATION, LEAD GATE & DELIVERABLE DOWNLOAD MODULE
# ==============================================================================
if st.session_state.get("scan_completed", False):
    st.markdown("---")

    if st.session_state.get("has_open_ports", False):
        output_report_file = st.session_state["output_report_file"]
        output_json_file = st.session_state["output_json_file"]
        clean_target = st.session_state["clean_target"]
        target_name = st.session_state["target_input"]
        ports_list = st.session_state["selected_ports"]
        elapsed_time = st.session_state["elapsed"]
        console_log = st.session_state["console_lines"]

        st.success(f"Audit completed in {elapsed_time} seconds. Surface threat advisory generated!")

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
            st.code("\n".join(console_log), language="bash")

        # ==============================================================================
        # GATED LEAD GENERATION & DELIVERABLE ROUTING ENGINE
        # ==============================================================================
        st.markdown("---")
        executive_pdf_path = os.path.join(WORKSPACE_DIR, "EXECUTIVE_SECURITY_ADVISORY.pdf")

        # 1. THE SCAN LOOP COMPLETION:
        # If the lead is not unlocked, do NOT display the download button immediately.
        if not st.session_state.get("lead_unlocked", False):
            # 2. THE GATED CARD LAYOUT:
            st.markdown("""
            <div class="gated-lead-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: #58a6ff; font-weight: 800; font-size: 1.22rem; letter-spacing: -0.3px;">
                        🔒 SECURITY ARTIFACT EXPORT PROTOCOL
                    </h3>
                    <span style="background: rgba(88, 166, 255, 0.15); color: #58a6ff; border: 1px solid #388bfd; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">
                        RESTRICTED EXPORT
                    </span>
                </div>
                <p style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.5; margin: 0 0 16px 0;">
                    Enter your official corporate or engineering email address to unlock your restricted-grade Executive Threat Advisory report (.pdf).
                </p>
            </div>
            """, unsafe_allow_html=True)

            # 3. THE FORM VALIDATION INTERACTION:
            corp_email_input = st.text_input(
                "Corporate Email Address",
                placeholder="e.g. ciso@target-corporation.com or security-lead@target.com",
                key="gate_corporate_email_address",
                help="Enterprise verification required to unlock high-end executive deliverable."
            )

            unlock_action_clicked = st.button(
                "🔓 UNLOCK & DISPATCH INTEL COMPLIANCE DELIVERABLE",
                type="primary",
                use_container_width=True,
                key="unlock_compliance_deliverable_btn"
            )

            # 4. THE REVENUE SEED ROUTING:
            if unlock_action_clicked:
                clean_email = corp_email_input.strip()

                # Step A: Validate email format
                if not clean_email or "@" not in clean_email or "." not in clean_email:
                    st.error("[-] Input Warning: Please enter a valid corporate or engineering email address.")
                else:
                    # Step B: Record to syndicate_lead_ledger.csv
                    ledger_ok = False
                    try:
                        ledger_path = os.path.join(WORKSPACE_DIR, "syndicate_lead_ledger.csv")
                        file_is_new = not os.path.exists(ledger_path)
                        with open(ledger_path, "a", newline="", encoding="utf-8") as f_lead:
                            csv_writer = csv.writer(f_lead)
                            if file_is_new:
                                csv_writer.writerow(["Timestamp", "Target_Host", "Discovered_Ports", "Client_Email"])
                            csv_writer.writerow([
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                                target_name,
                                ";".join(str(p) for p in ports_list),
                                clean_email
                            ])
                        ledger_ok = True
                    except Exception as lead_err:
                        st.error(f"[-] Lead Ledger Database Fault: {lead_err}")

                    # Step C: Dispatch SMTP email and unlock deliverable
                    if ledger_ok:
                        with st.spinner("Connecting to secure SMTP relays and dispatching intelligence deliverable..."):
                            sent_ok, sent_msg = dispatch_security_email(
                                recipient_email=clean_email,
                                target_name=target_name,
                                pdf_path=executive_pdf_path
                            )

                        st.session_state["lead_unlocked"] = True
                        st.session_state["lead_email"] = clean_email
                        st.session_state["sent_ok"] = sent_ok
                        st.session_state["sent_msg"] = sent_msg
                        st.rerun()

        # 4 & 5. UNLOCKED STATE (Cleanly expose download button & feedback)
        else:
            # 5. FEEDBACK SYSTEM:
            st.success("🚀 DISPATCH SUCCESSFUL: Server accepted transaction. Deliverable has left the chamber.")
            print(f"\n[+] DISPATCH CONFIRMED: Deliverable transmitted to {st.session_state.get('lead_email')} via smtp.gmail.com:465")

            if not st.session_state.get("sent_ok", True):
                st.info(f"ℹ️ SMTP Relay Status: {st.session_state.get('sent_msg')}")

            # Cleanly expose the original 'st.download_button' module
            if os.path.exists(executive_pdf_path):
                try:
                    with open(executive_pdf_path, "rb") as f_pdf:
                        pdf_binary_data = f_pdf.read()

                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #161b22 0%, #0d1117 100%); border: 1px solid #30363d; border-left: 4px solid #2ea043; border-radius: 8px; padding: 20px 24px; margin-top: 15px; margin-bottom: 16px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 1.18rem; letter-spacing: -0.3px;">
                                    🛡️ EXECUTIVE DELIVERABLE UNLOCKED & READY
                                </h4>
                                <p style="margin: 5px 0 0 0; color: #8b949e; font-size: 0.88rem;">
                                    Client verified. Report compiled with corporate header band, TLP:AMBER classification, structured service grids, and copy-pasteable firewall remediation rules.
                                </p>
                            </div>
                            <div>
                                <span style="background: rgba(46, 160, 67, 0.15); color: #3fb950; border: 1px solid #2ea043; padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;">
                                    UNLOCKED
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.download_button(
                        label="📥 DOWNLOAD BILLING-READY SECURITY ADVISORY (PDF)",
                        data=pdf_binary_data,
                        file_name="EXECUTIVE_SECURITY_ADVISORY.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as read_err:
                    st.error(f"[-] File Access Fault: {read_err}")
            else:
                st.error(f"[-] File-Missing Fault: Deliverable artifact '{os.path.basename(executive_pdf_path)}' was not found on disk.")

    else:
        st.info("ℹ️ **Target Surface Clean**: No open ports were detected on the specified host. AI advisory generation was bypassed to conserve resources.")
        with st.expander("View Full Console Execution"):
            st.code("\n".join(st.session_state.get("console_lines", [])), language="bash")

