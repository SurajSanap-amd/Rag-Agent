import streamlit as st
from src.tools import (
    tool_search_documents,
    tool_calculate_expression,
    tool_manage_todos,
)

st.set_page_config(page_title="Tools Demo", page_icon="🛠️")

st.title("🛠️ Tools Only Demo")

tab1, tab2, tab3 = st.tabs(["RAG Search", "Calculator", "Todo Manager"])

with tab1:
    st.subheader("RAG Document Search")
    q = st.text_input("Question about your documents:", key="rag_q")
    if st.button("Search Documents"):
        if not q.strip():
            st.warning("Please enter a query.")
        else:
            res = tool_search_documents(q)
            st.text_area("Result", res, height=300)

with tab2:
    st.subheader("Calculator Tool")
    expr = st.text_input("Enter expression (e.g., 5 * (2 + 3))", key="calc_expr")
    if st.button("Calculate"):
        if not expr.strip():
            st.warning("Please enter an expression.")
        else:
            res = tool_calculate_expression(expr)
            st.write(res)

with tab3:
    st.subheader("Todo Manager")
    action = st.selectbox("Action", ["add", "list", "remove"])
    item = st.text_input("Todo item (needed for add/remove)", key="todo_item")

    if st.button("Run Todo Action"):
        res = tool_manage_todos(action=action, item=item or None)
        st.write(res)


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
