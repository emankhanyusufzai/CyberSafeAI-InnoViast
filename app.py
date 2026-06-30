# app.py
# CyberSafe AI - Main Streamlit Application (v4 Final)

import streamlit as st
from utils.chatbot import get_response
from utils.error_handler import validate_input
from utils.risk_checker import check_risk_level

st.set_page_config(
    page_title="CyberSafe AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --cyber-bg:      #050b14;
        --cyber-surface: #0a1628;
        --cyber-panel:   #0f1f35;
        --cyber-card:    #132035;
        --cyber-border:  #1a3a5c;
        --cyber-accent:  #00d4ff;
        --cyber-green:   #00ff88;
        --cyber-red:     #ff3355;
        --cyber-orange:  #ff8800;
        --cyber-text:    #c8d8e8;
        --cyber-muted:   #7a9ab8;
        --cyber-heading: #e8f4ff;
    }

    html, body, .stApp {
        background-color: var(--cyber-bg) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--cyber-text) !important;
    }

    #MainMenu, footer { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden !important; }
    [data-testid="stDecoration"] { visibility: hidden !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 2.5rem !important; }

    /* Kill the empty header bar gap at the very top */
    header[data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        background: transparent !important;
    }
    [data-testid="stAppViewContainer"] { padding-top: 0 !important; }

    /* Hide the little chain-link "copy anchor" icon next to headings */
    h1 a, h2 a, h3 a, h1 svg, h2 svg, h3 svg {
        display: none !important;
    }

    /* ── 1️⃣ Sidebar — slim width, won't fight Streamlit's collapse/expand ── */
    [data-testid="stSidebar"] {
        background-color: var(--cyber-surface) !important;
        border-right: 1px solid var(--cyber-border) !important;
        min-width: 210px !important;
        max-width: 210px !important;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 210px !important;
        max-width: 210px !important;
        width: 210px !important;
    }

    .sidebar-logo {
        display: flex; align-items: center; gap: 8px;
        padding: 12px 0 4px;
    }
    .sidebar-logo .shield { font-size: 22px; filter: drop-shadow(0 0 8px #00d4ff88); }
    .sidebar-logo .brand-name { font-size: 16px; font-weight: 700; color: var(--cyber-heading); }
    .sidebar-logo .brand-name span { color: var(--cyber-accent); }
    .sidebar-tagline { font-size: 10px; color: var(--cyber-muted); margin: 0 0 8px; font-style: italic; }

    .status-bar {
        display: inline-flex; align-items: center; gap: 5px;
        font-size: 10.5px; color: var(--cyber-green); font-weight: 600;
        padding: 5px 10px;
        background: rgba(0,255,136,0.07); border: 1px solid rgba(0,255,136,0.2);
        border-radius: 20px; margin-bottom: 4px;
    }
    .status-bar .s-dot {
        width: 6px; height: 6px; background: var(--cyber-green); border-radius: 50%;
        box-shadow: 0 0 6px var(--cyber-green); animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%,100% { opacity:1; transform:scale(1); }
        50% { opacity:0.5; transform:scale(0.8); }
    }

    .section-label {
        font-size: 9px; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: var(--cyber-accent);
        margin: 12px 0 6px; display: flex; align-items: center; gap: 6px;
    }
    .section-label::after { content:''; flex:1; height:1px; background:var(--cyber-border); }

    .stButton > button {
        background: linear-gradient(135deg, var(--cyber-panel), var(--cyber-card)) !important;
        color: var(--cyber-text) !important;
        border: 1px solid var(--cyber-border) !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        font-size: 11.5px !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
        transition: all 0.22s ease !important;
        font-weight: 400 !important;
        margin-bottom: 8px !important;
    }
    .stButton > button:hover {
        border-color: var(--cyber-accent) !important;
        color: var(--cyber-accent) !important;
        background: rgba(0,212,255,0.07) !important;
        box-shadow: 0 0 14px rgba(0,212,255,0.18) !important;
        transform: translateX(3px) !important;
    }

    .clear-btn > button {
        background: rgba(255,51,85,0.07) !important;
        border-color: rgba(255,51,85,0.3) !important;
        color: #ff5577 !important;
        font-size: 11.5px !important;
    }
    .clear-btn > button:hover {
        background: rgba(255,51,85,0.14) !important;
        border-color: var(--cyber-red) !important;
        color: var(--cyber-red) !important;
        box-shadow: 0 0 14px rgba(255,51,85,0.22) !important;
        transform: none !important;
    }

    hr { border:none !important; border-top:1px solid var(--cyber-border) !important; margin:10px 0 !important; }

    .about-box {
        background: var(--cyber-panel); border: 1px solid var(--cyber-border);
        border-radius: 10px; padding: 12px 14px; margin-top: 4px;
        font-size: 11px; color: var(--cyber-muted); line-height: 1.6;
    }
    .about-box b { color: var(--cyber-text); font-weight: 600; }

    /* ── Secure Mode Badge ── */
    .secure-badge {
        position: fixed; top: 16px; right: 20px; z-index: 9999;
        display: flex; align-items: center; gap: 7px;
        background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.28);
        border-radius: 20px; padding: 5px 14px;
        font-size: 11px; font-weight: 600; color: var(--cyber-green); letter-spacing: 0.4px;
    }
    .secure-badge .sb-dot {
        width: 6px; height: 6px; background: var(--cyber-green); border-radius: 50%;
        box-shadow: 0 0 6px var(--cyber-green); animation: pulse-dot 2s infinite;
    }

    /* ── Main Header ── */
    .main-header { text-align: center; padding: 6px 0 14px; }
    .main-header .title-badge {
        display: inline-flex; align-items: center; gap: 10px;
        background: rgba(0,212,255,0.06); border: 1px solid rgba(0,212,255,0.25);
        border-radius: 40px; padding: 5px 18px 5px 12px; margin-bottom: 10px;
        font-size: 11px; color: var(--cyber-accent); letter-spacing: 1px;
        font-weight: 600; text-transform: uppercase;
    }
    .main-header .title-badge .dot {
        width: 7px; height: 7px; background: var(--cyber-green); border-radius: 50%;
        box-shadow: 0 0 6px var(--cyber-green); animation: pulse-dot 2s infinite;
    }
    .main-header h1 {
        font-size: 3.2em !important; font-weight: 800 !important;
        color: var(--cyber-heading) !important; letter-spacing: -1px !important;
        margin: 0 0 6px !important; line-height: 1.05 !important;
    }
    .main-header h1 span {
        color: var(--cyber-accent);
        text-shadow: 0 0 30px rgba(0,212,255,0.55), 0 0 60px rgba(0,212,255,0.2);
    }
    .main-header .subtitle { font-size: 14px; color: var(--cyber-muted); margin: 0 0 12px; }

    /* ── Status Panel ── */
    .status-panel {
        display: flex; align-items: center; justify-content: center; gap: 20px;
        background: rgba(0,255,136,0.04); border: 1px solid rgba(0,255,136,0.15);
        border-radius: 12px; padding: 10px 24px; margin-bottom: 16px;
    }
    .status-item {
        display: flex; align-items: center; gap: 6px;
        font-size: 12px; color: var(--cyber-green); font-weight: 600;
    }
    .status-item .si-dot {
        width: 6px; height: 6px; background: var(--cyber-green); border-radius: 50%;
        box-shadow: 0 0 6px var(--cyber-green); animation: pulse-dot 2s infinite;
    }
    .status-sep { color: var(--cyber-border); font-size: 14px; }

    /* ── 4️⃣ Welcome Screen — hides when chat starts ── */
    .welcome-screen { text-align: center; padding: 20px 20px 0; }
    .welcome-screen .icon-ring {
        width: 90px; height: 90px;
        background: radial-gradient(circle at center, rgba(0,212,255,0.10) 0%, rgba(0,212,255,0.01) 70%);
        border: 1.5px solid rgba(0,212,255,0.28); border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 42px; margin-bottom: 14px;
        animation: shield-glow 4s ease-in-out infinite;
    }
    @keyframes shield-glow {
        0%,100% { box-shadow: 0 0 20px rgba(0,212,255,0.12), 0 0 50px rgba(0,212,255,0.05); }
        50% { box-shadow: 0 0 28px rgba(0,212,255,0.22), 0 0 70px rgba(0,212,255,0.09); }
    }
    .welcome-screen h3 { font-size: 20px; color: var(--cyber-heading); font-weight: 700; margin: 0 0 5px; }
    .welcome-screen h3 a, .welcome-screen h3 a svg { display: none !important; }
    .welcome-screen .welcome-sub { font-size: 13px; color: var(--cyber-muted); margin: 0 0 18px; font-style: italic; }

    .capabilities-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 10px; max-width: 560px; margin: 0 auto 16px; text-align: left;
    }
    .cap-card {
        background: var(--cyber-panel); border: 1px solid var(--cyber-border);
        border-radius: 10px; padding: 11px 13px;
        display: flex; align-items: center; gap: 9px;
        font-size: 12.5px; color: var(--cyber-text); font-weight: 500;
        transition: border-color 0.2s; cursor: default;
    }
    .cap-card:hover { border-color: var(--cyber-accent); }
    .cap-card .cap-icon { font-size: 18px; flex-shrink: 0; }
    .welcome-cta { font-size: 13px; color: var(--cyber-accent); font-weight: 500; padding: 4px 0 0; margin-bottom: 0; }

    /* ── 3️⃣ Chat Bubbles — WhatsApp style ── */
    .chat-wrap {
        background: var(--cyber-surface); border: 1px solid var(--cyber-border);
        border-radius: 16px; padding: 20px 24px; margin-bottom: 16px;
    }

    /* User bubble — right aligned, blue */
    .user-message-wrap { display: flex; justify-content: flex-end; margin: 10px 0; }
    .user-message {
        background: linear-gradient(135deg, #0d3a7a, #0a52c4);
        color: #d0e8ff; padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 72%; font-size: 14px; line-height: 1.65;
        border: 1px solid rgba(0,102,255,0.4);
        box-shadow: 0 3px 16px rgba(10,82,196,0.3);
    }
    .user-message .msg-label {
        font-size: 10px; font-weight: 700; letter-spacing: 1px;
        text-transform: uppercase; color: rgba(208,232,255,0.55); margin-bottom: 5px;
        display: flex; align-items: center; gap: 5px; justify-content: flex-end;
    }

    /* AI bubble — left aligned, dark */
    .bot-message-wrap { display: flex; justify-content: flex-start; margin: 10px 0; }
    .bot-message {
        background: var(--cyber-card); color: var(--cyber-text);
        padding: 13px 17px; border-radius: 4px 18px 18px 18px;
        max-width: 84%; font-size: 14px; line-height: 1.75;
        border: 1px solid var(--cyber-border);
        border-left: 3px solid var(--cyber-accent);
        box-shadow: 0 3px 16px rgba(0,0,0,0.3);
    }
    .bot-message .msg-label {
        font-size: 10px; font-weight: 700; letter-spacing: 1px;
        text-transform: uppercase; color: var(--cyber-accent); margin-bottom: 7px;
        display: flex; align-items: center; gap: 6px;
    }
    .bot-message .msg-label::before {
        content:''; width:6px; height:6px; background:var(--cyber-accent);
        border-radius:50%; box-shadow:0 0 7px var(--cyber-accent); display:inline-block;
    }
    .bot-message p { margin: 5px 0; }
    .bot-message ul, .bot-message ol { margin: 6px 0 6px 18px; padding: 0; }
    .bot-message li { margin-bottom: 4px; line-height: 1.6; }
    .bot-message code {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.15);
        padding: 1px 5px; border-radius: 4px; font-size: 12.5px; color: var(--cyber-accent);
    }
    .bot-message strong { color: var(--cyber-heading); font-weight: 600; }

    /* Typing indicator */
    .typing-indicator {
        display: flex; align-items: center; gap: 12px; padding: 13px 17px;
        background: var(--cyber-card); border: 1px solid var(--cyber-border);
        border-left: 3px solid var(--cyber-accent);
        border-radius: 4px 18px 18px 18px; max-width: 200px; margin: 10px 0;
    }
    .typing-indicator .ti-label { font-size: 12.5px; color: var(--cyber-accent); font-weight: 500; }
    .typing-dots { display:flex; gap:5px; align-items:center; }
    .typing-dots span {
        width:7px; height:7px; background:var(--cyber-accent); border-radius:50%;
        animation:bounce-dot 1.4s infinite; box-shadow:0 0 5px var(--cyber-accent);
    }
    .typing-dots span:nth-child(2) { animation-delay:0.2s; }
    .typing-dots span:nth-child(3) { animation-delay:0.4s; }
    @keyframes bounce-dot {
        0%,80%,100%{transform:scale(0.7);opacity:0.5} 40%{transform:scale(1.1);opacity:1}
    }

    /* Risk badges */
    .risk-badge-wrap { display:flex; align-items:center; gap:10px; padding:8px 14px; border-radius:8px; margin:8px 0; font-size:13px; }
    .risk-badge-wrap.high { background:rgba(255,51,85,0.1); border:1px solid rgba(255,51,85,0.3); }
    .risk-badge-wrap.medium { background:rgba(255,136,0,0.1); border:1px solid rgba(255,136,0,0.3); }
    .risk-pill { padding:3px 12px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
    .risk-pill.high { background:var(--cyber-red); color:#fff; }
    .risk-pill.medium { background:var(--cyber-orange); color:#fff; }
    .risk-msg { color:var(--cyber-muted); }

    /* ── Input row — exact spec: 60px height, 82/18 split, 15px gap, centered ── */
    .input-row { margin: 0 auto !important; max-width: 1100px !important; }
    .input-row div[data-testid="stHorizontalBlock"] {
        gap: 15px !important;
        align-items: center !important;
    }
    .input-row div[data-testid="column"]:nth-of-type(1) {
        flex: 0 0 82% !important;
        max-width: 82% !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
    }
    .input-row div[data-testid="column"]:nth-of-type(2) {
        flex: 0 0 18% !important;
        max-width: 18% !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
    }
    .input-row div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        width: 100% !important;
    }
    .input-row div[data-testid="stElementContainer"] {
        margin: 0 !important;
        width: 100% !important;
    }

    /* ── Input box — fixed 60px on every wrapper layer ── */
    .stTextInput { margin: 0 !important; }
    .stTextInput > div {
        height: 60px !important;
    }
    .stTextInput > div > div {
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
    }
    .stTextInput > div > div > input {
        background: var(--cyber-panel) !important; color: var(--cyber-text) !important;
        border: 1px solid var(--cyber-border) !important; border-radius: 12px !important;
        padding: 0 20px !important; font-size: 15px !important;
        height: 60px !important; line-height: 60px !important; box-sizing: border-box !important;
        font-family: 'Inter', sans-serif !important; transition: border-color 0.25s, box-shadow 0.25s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--cyber-accent) !important;
        box-shadow: 0 0 0 3px rgba(0,212,255,0.18), 0 0 16px rgba(0,212,255,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #6a9abf !important; opacity: 1 !important; font-size: 15px !important;
    }
    .stTextInput label { display: none !important; }

    /* ── Send Button — exact same 60px height as input ── */
    .send-btn { margin: 0 !important; width: 100% !important; }
    .send-btn div[data-testid="stButton"] { margin: 0 !important; width: 100% !important; }
    .send-btn button {
        background: linear-gradient(90deg, #00C6FF, #0072FF) !important;
        color: #fff !important; border: none !important; border-radius: 12px !important;
        font-weight: 700 !important; font-size: 15px !important;
        height: 60px !important; min-height: 60px !important; max-height: 60px !important; width: 100% !important;
        box-sizing: border-box !important; letter-spacing: 0.3px !important;
        margin: 0 !important; padding: 0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        box-shadow: 0 4px 18px rgba(0,114,255,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .send-btn button p {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        line-height: 1 !important;
        color: #fff !important;
    }
    .send-btn button:hover {
        background: linear-gradient(90deg, #00d4ff, #0072FF) !important;
        box-shadow: 0 0 22px rgba(0,212,255,0.8), 0 4px 26px rgba(0,114,255,0.45) !important;
        transform: translateY(-2px) !important;
        color: #fff !important;
    }

    .privacy-notice {
        display: flex; align-items: center; justify-content: center; gap: 6px;
        font-size: 11px; color: var(--cyber-muted); margin-top: 7px;
    }

    /* Footer */
    .cyber-footer {
        text-align:center; padding:14px 0 18px; font-size:11.5px; color:var(--cyber-muted);
        letter-spacing:0.5px; display:flex; align-items:center; justify-content:center; gap:8px;
    }
    .cyber-footer .dot { color:var(--cyber-border); }
</style>
""", unsafe_allow_html=True)

# ── Secure Mode Badge ──────────────────────────────────────────
st.markdown("""
<div class="secure-badge">
    <div class="sb-dot"></div> 🔒 Secure Mode Active
</div>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = ""

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="shield">🛡️</span>
        <span class="brand-name">Cyber<span>Safe</span> AI</span>
    </div>
    <p class="sidebar-tagline">Personal Cybersecurity Awareness Assistant</p>
    <div class="status-bar"><div class="s-dot"></div> AI Online · Systems Ready</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">Quick Questions</div>', unsafe_allow_html=True)

    suggestions = [
        ("🎣", "What is phishing?"),
        ("🔐", "How to create a strong password?"),
        ("🦠", "What is ransomware?"),
        ("📶", "Is public WiFi safe?"),
        ("🔒", "What is 2FA?"),
        ("📧", "How to secure my Gmail?"),
        ("🌐", "How to identify fake websites?"),
        ("🛡️", "What is a VPN?"),
    ]

    for icon, text in suggestions:
        if st.button(f"{icon}  {text}", key=text, use_container_width=True):
            st.session_state.suggested_question = f"{icon} {text}"

    st.markdown("---")
    st.markdown('<div class="section-label">Session</div>', unsafe_allow_html=True)
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggested_question = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-box">
        CyberSafe AI helps you stay safe online — answering cybersecurity questions in simple, clear language.<br><br>
        <b>Track:</b> AI Solutions Engineering<br>
        <b>Model:</b> Google Gemini
    </div>
    """, unsafe_allow_html=True)

# ── Main Header ───────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="title-badge"><div class="dot"></div> AI-Powered Security Assistant</div>
    <h1>Cyber<span>Safe</span> AI</h1>
    <p class="subtitle">Ask anything about cybersecurity, digital privacy, and online safety</p>
</div>
""", unsafe_allow_html=True)

# ── Status Panel ──────────────────────────────────────────────
st.markdown("""
<div class="status-panel">
    <div class="status-item"><div class="si-dot"></div> 🟢 AI Online</div>
    <span class="status-sep">|</span>
    <div class="status-item"><div class="si-dot"></div> 🟢 Gemini Connected</div>
    <span class="status-sep">|</span>
    <div class="status-item"><div class="si-dot"></div> 🟢 Secure</div>
</div>
""", unsafe_allow_html=True)

# ── 4️⃣ Welcome hides when chat starts ────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-screen">
        <div class="icon-ring">🛡️</div>
        <h3>Welcome to CyberSafe AI</h3>
        <p class="welcome-sub">Your intelligent cybersecurity companion — always online, always secure.</p>
        <div class="capabilities-grid">
            <div class="cap-card"><span class="cap-icon">🔐</span> Password Security</div>
            <div class="cap-card"><span class="cap-icon">🎣</span> Phishing Detection</div>
            <div class="cap-card"><span class="cap-icon">🦠</span> Malware & Ransomware</div>
            <div class="cap-card"><span class="cap-icon">🌐</span> Safe Browsing</div>
            <div class="cap-card"><span class="cap-icon">📧</span> Email Protection</div>
            <div class="cap-card"><span class="cap-icon">🛡️</span> VPN & Privacy</div>
        </div>
        <p class="welcome-cta">👇 Ask your cybersecurity question below or pick one from the sidebar</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # ── 3️⃣ Chat Bubbles — WhatsApp style ──
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message-wrap">
                <div class="user-message">
                    <div class="msg-label">You &nbsp;👤</div>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message-wrap">
                <div class="bot-message">
                    <div class="msg-label">CyberSafe AI</div>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Input Area — same line, equal height, bottom aligned ──────
st.markdown('<div class="input-row">', unsafe_allow_html=True)
col1, col2 = st.columns([4.6, 1], vertical_alignment="center")

with col1:
    user_input = st.text_input(
        "Ask a question",
        value=st.session_state.suggested_question,
        placeholder="🔍 Ask your cybersecurity question...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    st.markdown('<div class="send-btn">', unsafe_allow_html=True)
    send_clicked = st.button("✈ Send", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="privacy-notice">
    🔒 Your conversations are not stored permanently.
</div>
""", unsafe_allow_html=True)

# ── Handle Input ──────────────────────────────────────────────
if send_clicked and user_input:
    st.session_state.suggested_question = ""
    is_valid, error_msg = validate_input(user_input)

    if not is_valid:
        st.error(error_msg)
    else:
        risk = check_risk_level(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        if risk:
            level = risk["level"].lower()
            st.markdown(f"""
            <div class="risk-badge-wrap {level}">
                <span class="risk-pill {level}">{risk["level"]}</span>
                <span class="risk-msg">{risk["message"]}</span>
            </div>
            """, unsafe_allow_html=True)

        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-indicator">
            <span class="ti-label">🛡️ CyberSafe AI</span>
            <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
        """, unsafe_allow_html=True)

        response = get_response(user_input, st.session_state.messages[:-1])
        typing_placeholder.empty()

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="cyber-footer">
    🛡️ CyberSafe AI
    <span class="dot">·</span>
    Built with Streamlit &amp; Google Gemini
</div>
""", unsafe_allow_html=True)
