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
