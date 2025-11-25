import streamlit as st

from src.agent import run_agent
from src.vectorstore import has_documents
from utils.ui_components import chat_message

st.set_page_config(page_title="Chat with Agent", page_icon="🤖")

# ---------- Custom CSS for colorful design ----------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top, #1f2937 0, #020617 40%, #000000 100%);
        color: #e5e7eb;
    }
    .chat-card {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.9);
    }
    .status-chip-ok {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.15);
        color: #bbf7d0;
        font-size: 0.8rem;
        border: 1px solid rgba(34, 197, 94, 0.6);
    }
    .status-chip-warn {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(234, 179, 8, 0.1);
        color: #facc15;
        font-size: 0.8rem;
        border: 1px solid rgba(250, 204, 21, 0.5);
    }
    .tool-chip {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.15);
        color: #bfdbfe;
        font-size: 0.75rem;
        border: 1px solid rgba(59, 130, 246, 0.7);
        margin-top: 0.4rem;
    }
    .title-accent {
        background: linear-gradient(90deg, #38bdf8, #a855f7, #f97316);
        -webkit-background-clip: text;
        color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="title-accent">🤖 Chat with AI Agent (RAG + Tools)</h1>',
    unsafe_allow_html=True,
)

# ---------- Document status indicator ----------
docs_available = has_documents()

if docs_available:
    st.markdown(
        '<span class="status-chip-ok">📚 Documents loaded · RAG enabled</span>',
        unsafe_allow_html=True,
    )
    st.caption("The agent can now answer questions based on your uploaded PDFs / notes.")
else:
    st.markdown(
        '<span class="status-chip-warn">⚠️ No documents uploaded yet</span>',
        unsafe_allow_html=True,
    )
    st.caption("You can still use tools like calculator and todo, but RAG answers will be limited.")

st.write("")

# ---------- Chat container card ----------
with st.container():
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # list of (role, text, tool_name)

    # Show previous messages
    for role, text in st.session_state.chat_history:
        chat_message(role, text)

    st.write("---")

    # Input box
    user_input = st.text_input("Type your message here:", key="user_input")

    col1, col2 = st.columns([3, 1])
    with col1:
        send_btn = st.button("Send 💬", use_container_width=True)
    with col2:
        clear_btn = st.button("Clear Chat 🧹", use_container_width=True)

    # Clear chat
    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    # Handle send
    if send_btn and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append(("user", user_input))
        chat_message("user", user_input)

        # Hacker-style mini status while agent thinks
        with st.spinner("Agent booting tools, scanning knowledge base, thinking..."):
            result = run_agent(user_input)

        answer = result["answer"]
        tool_name = result["tool_name"]
        tool_output = result["tool_output"]

        # Append tool chip at the end of answer (if any tool used)
        if tool_name:
            answer = answer + f"\n\n<span class='tool-chip'>🛠 Tool used: `{tool_name}`</span>"

        st.session_state.chat_history.append(("assistant", answer))
        # Allow HTML in answer (for tool chip)
        st.markdown(
            f"<div style='margin-top:0.5rem'>{answer}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Footer ----------
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.65);
            text-align: center;
            padding: 10px 0;
            color: white;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .footer-text {
            background: linear-gradient(90deg, #00eaff, #6e00ff);
            -webkit-background-clip: text;
            color: transparent;
            font-weight: 600;
        }
    </style>

    <div class="footer">
        <span class="footer-text">🚀 Built by Suraj Sanap</span>
    </div>
    """,
    unsafe_allow_html=True,
)
