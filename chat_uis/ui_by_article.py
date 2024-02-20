import streamlit as st

from chat_uis.chat_utils import st_chat_containers
from model_versions import model_from_article_split


def chat_ui_by_article() -> None:
    """Chatbot UI with chunking by article"""

    if "init_push" not in st.session_state:
        st.session_state["init_push"] = True
        st.session_state["messages_push"] = []
        st.session_state["cited_docs"] = []

    st.title("Retrieval Chat 📬")

    container1, container2, user_query = st_chat_containers("Chat", "Citations")

    with container1:
        for message in st.session_state["messages_push"]:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        if user_query:
            st.chat_message("user").markdown(user_query)

            with st.spinner("Thinking..."):
                answer_module = model_from_article_split(user_query)
                ai_answer = answer_module['answer']
                st.session_state["cited_docs"] = answer_module['source_documents']
                print(answer_module['source_documents'])
            st.chat_message("assistant").markdown(ai_answer)

            st.session_state["messages_push"] += [
                {"role": "human", "message": user_query},
                {"role": "ai", "message": ai_answer},
            ]

    with container2:
        for doc in st.session_state["cited_docs"]:
            with st.expander(f"{doc.metadata['source']}"):
                st.markdown(doc.page_content)
