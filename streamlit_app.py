import requests
import streamlit as st
from app.feedback.store import save_feedback
st.title("MedIntel")

question = st.text_input(
    "Ask a medical question"
)

if st.button("Ask"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={
            "question": question
        }
    )

    data = response.json()

    st.write(data["answer"])

    st.subheader("📚 Sources")

    for source in data["sources"]:

        with st.expander(
            f"{source['book']} (Page {source['page']})"
        ):
            st.write(source["text"][:1000])
            
    col1, col2 = st.columns(2)

    with col1:

        if st.button("👍 Helpful"):

            save_feedback(
                question,
                data["answer"],
                5
            )

            st.success(
                "Feedback saved"
            )

    with col2:

        if st.button("👎 Not Helpful"):

            save_feedback(
                question,
                data["answer"],
                1
            )

            st.warning(
                "Feedback saved"
            )