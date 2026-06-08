import streamlit as st
import requests

S_URL = "http://127.0.0.1:8000"



research_tab, web_tab, pdf_tab, summary_tab = st.tabs(
    [
        "🔍 Research Assistant",
        "🌐 Web Search",
        "📄 PDF Reader",
        "📝 Summarizer"
    ]
)

# ---------------- RESEARCH ASSISTANT ---------------- #

with research_tab:

    st.header("AI Research Assistant")

    topic = st.text_input(
        "Enter Research Topic",
        placeholder="Quantum Computing"
    )

    if st.button("Research"):

        response = requests.post(
            f"{S_URL}/research",
            json={
                "topic": topic
            }
        )

        data = response.json()

        st.markdown(data["response"])

# ---------------- WEB SEARCH ---------------- #

with web_tab:

    topic_search = st.text_input(
        "Topic",
        key="search"
    )

    if st.button("Search Web"):

        response = requests.get(
            f"{S_URL}/web_search",
            params={
                "topic": topic_search
            }
        )

        st.markdown(response.json()["response"])

# ---------------- PDF READER ---------------- #

with pdf_tab:

    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if pdf:

        if st.button("Read PDF"):

            files = {
                "file": pdf
            }

            response = requests.post(
                f"{S_URL}/pdf_reader",
                files=files
            )

            data = response.json()

            st.text_area(
                "Extracted Text",
                data["text"],
                height=300
            )

# ---------------- SUMMARIZER ---------------- #

with summary_tab:

    text = st.text_area(
        "Paste Content"
    )

    if st.button("Summarize"):

        response = requests.post(
            f"{S_URL}/summarize",
            json={
                "text": text
            }
        )

        data = response.json()

        st.markdown(data["response"])