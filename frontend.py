# import streamlit as st

# from ai_agent import get_response_from_ai_agent 
# st.set_page_config(page_title="Agentic Chatbot", page_icon=":robot_face:", layout="centered")
# st.title("AI Chatbot Agents")
# st.write("Create and Intreact with the AI Agents")
# system_prompt = st.text_area("Define Your AI  agents",height=70,placeholder="Type your system prompt here")
# model_Name_GROQ=["llma-3.3-70b-versatile"]
# model_Name_OPENAI=["gpt-4o-mini"]

# provider = st.selectbox("Select Model Provider", ("GROQ", "OpenAI"))
# if provider == "GROQ":
#     model_name = st.selectbox("Select Model", model_Name_GROQ)
# elif provider == "OpenAI":
#     model_name = st.selectbox("Select Model", model_Name_OPENAI)


# allow_web_search = st.checkbox("Allow Web Search (Tavily)")
# user_query = st.text_input(" Enter Your Query",height=150, placeholder="ASK Any Things")

# if st.button("Ask Agent"):
#     if user_query.strip() == "":
        
#         response = get_response_from_ai_agent(llm_id=model_name, query=user_query, allow_search=allow_web_search, system_prompt=system_prompt, provider=provider)
#         st.subheader("Agent Response")
#         st.markdown("**final response:**{response}")
        
        # Save conversation history
import streamlit as st
import requests

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
:root {
    --bg:       #0d0f14;
    --surface:  #151820;
    --border:   #1f2430;
    --accent:   #00e5ff;
    --accent2:  #7c4dff;
    --text:     #e8ecf0;
    --muted:    #6b7589;
    --user-bg:  #1a1f2e;
    --bot-bg:   #111420;
    --success:  #00e5a0;
    --danger:   #ff4d6d;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Space Mono', monospace !important;
    color: var(--accent) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* ── Sidebar widgets ── */
.stSelectbox > label, .stTextArea > label,
.stCheckbox > label, .stTextInput > label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

.stSelectbox [data-baseweb="select"] > div,
.stTextArea textarea,
.stTextInput input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stSelectbox [data-baseweb="select"] > div:focus-within,
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.12) !important;
}

/* ── Chat area wrapper ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: var(--bg);
}

.chat-header {
    padding: 18px 28px 14px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--surface);
}

.chat-header-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.04em;
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 8px var(--success);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.model-badge {
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent);
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.2);
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.06em;
}

/* ── Messages ── */
.messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.msg-row {
    display: flex;
    gap: 12px;
    max-width: 820px;
}

.msg-row.user { margin-left: auto; flex-direction: row-reverse; }
.msg-row.bot  { margin-right: auto; }

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

.avatar.user-av { background: linear-gradient(135deg, var(--accent2), #b04dff); }
.avatar.bot-av  { background: linear-gradient(135deg, #00b4cc, var(--accent)); }

.bubble {
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 0.9rem;
    line-height: 1.65;
    max-width: 680px;
}

.bubble.user-bubble {
    background: var(--user-bg);
    border: 1px solid rgba(124,77,255,0.25);
    border-top-right-radius: 3px;
    color: var(--text);
}

.bubble.bot-bubble {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-top-left-radius: 3px;
    color: var(--text);
}

.bubble code {
    background: rgba(0,229,255,0.08);
    padding: 1px 5px;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82em;
    color: var(--accent);
}

/* ── Typing indicator ── */
.typing { display: flex; gap: 4px; padding: 4px 0; align-items: center; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--muted); animation: blink 1.2s infinite; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80%,100%{opacity:0.2} 40%{opacity:1} }

/* ── Input row ── */
.input-row {
    padding: 16px 28px 20px;
    border-top: 1px solid var(--border);
    background: var(--surface);
}

/* ── Send button ── */
.stButton button {
    background: linear-gradient(135deg, var(--accent2), #5c35c9) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    padding: 10px 22px !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
    text-transform: uppercase !important;
}
.stButton button:hover { opacity: 0.85 !important; }

/* ── Clear button ── */
.stButton.clear button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
}

/* ── Error / success alerts ── */
.stAlert {
    background: rgba(255,77,109,0.08) !important;
    border: 1px solid rgba(255,77,109,0.3) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── Checkbox ── */
.stCheckbox span { color: var(--text) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ──────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000/chat"

MODELS = {
    "Groq": [
        "llama-3.3-70b-versatile",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
    ],
    "OpenAI": [
        "gpt-4o-mini",
    ],
}

# ─── Session State ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"|"assistant", "content": str}

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Agent Config")
    st.divider()

    system_prompt = st.text_area(
        "System Prompt",
        height=130,
        placeholder="You are a helpful AI assistant...",
        value="You are a helpful AI assistant.",
    )

    st.markdown("### Model")
    provider = st.selectbox("Provider", list(MODELS.keys()))
    model_name = st.selectbox("Model", MODELS[provider])

    allow_web_search = st.checkbox("🌐 Enable Web Search (Tavily)", value=False)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        st.markdown(
            f"<div style='font-family:Space Mono,monospace;font-size:0.65rem;"
            f"color:#6b7589;padding-top:10px;'>v1.0 · FastAPI</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<div style='font-family:Space Mono,monospace;font-size:0.62rem;"
        "color:#3a4055;text-align:center;'>Backend: 127.0.0.1:8000</div>",
        unsafe_allow_html=True,
    )

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="chat-header">
    <div class="status-dot"></div>
    <span class="chat-header-title">🤖 AI Agent</span>
    <span class="model-badge">{provider} · {model_name}</span>
</div>
""", unsafe_allow_html=True)

# ─── Chat Messages ────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#3a4055;">
            <div style="font-size:2.5rem;margin-bottom:12px;">🤖</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.8rem;
                        letter-spacing:0.1em;color:#6b7589;">
                AGENT READY · ASK ANYTHING
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                st.markdown(f"""
                <div class="msg-row user">
                    <div class="avatar user-av">👤</div>
                    <div class="bubble user-bubble">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-row bot">
                    <div class="avatar bot-av">🤖</div>
                    <div class="bubble bot-bubble">{content}</div>
                </div>
                """, unsafe_allow_html=True)

# ─── Input Area ───────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col_input, col_btn = st.columns([6, 1])

with col_input:
    user_query = st.text_input(
        label="user_input",
        label_visibility="collapsed",
        placeholder="Type your message and press Send…",
        key="user_input",
    )

with col_btn:
    send = st.button("Send ➤", use_container_width=True)

# ─── Handle Send ──────────────────────────────────────────────────────────────
def call_backend(query: str) -> str:
    """Send request to FastAPI backend and return response text."""
    # Build messages history as list of strings (last is current query)
    history = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    history.append(query)

    payload = {
        "model_name": model_name,
        "model_provider": provider,
        "system_prompt": system_prompt,
        "messages": history,
        "allow_search": allow_web_search,
    }

    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            return f"⚠️ Backend Error: {data['error']}"

        return data.get("response", "No response received.")

    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure FastAPI server is running on port 8000."
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. The model might be taking too long."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


if send and user_query.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_query.strip()})

    # Show typing indicator while calling backend
    with st.spinner("Agent is thinking…"):
        bot_reply = call_backend(user_query.strip())

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Rerun to refresh chat
    st.rerun()

elif send and not user_query.strip():
    st.warning("Please enter a message before sending.")
      
      
      
      
        
