import streamlit as st
import tempfile
import os
from summarizer import text_summarize
from GetText import extract_text_from_pdf, file_text, wiki_text, extractOCR

def main():
    st.title('Text Summarizer')

    # Initialize session state variables if they don't exist
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""

    if 'language' not in st.session_state:
        st.session_state.language = "ar"

    # User chooses the input method
    input_method = st.radio(
        "**Choose the input method**", 
        ("Upload a text file", "Upload a PDF file", "Upload scanned PDF file", "Enter Wikipedia page URL")
    )

    # Language selection
    language = st.selectbox(
        "Choose the language of the text",
        ["Arabic", "English"],
        index=0
    )
    st.session_state.language = language 

    # If "Upload a text file"
    if input_method == "Upload a text file":
        uploaded_text_file = st.file_uploader("Choose a text file", type="txt")
        if uploaded_text_file is not None:
            st.session_state.text_input = file_text(uploaded_text_file)

    # If "Upload a PDF file"
    elif input_method == "Upload a PDF file":
        uploaded_pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf_file is not None:
            st.session_state.text_input = extract_text_from_pdf(uploaded_pdf_file)

    # If "Upload scanned PDF file"
    elif input_method == "Upload scanned PDF file":
        uploaded_pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_pdf_file.read())
                temp_pdf_path = temp_file.name
            
            st.session_state.text_input = extractOCR(temp_pdf_path, st.session_state.language)
            os.remove(temp_pdf_path)  # Delete the temporary file after processing

    # If "Enter Wikipedia page URL"
    elif input_method == "Enter Wikipedia page URL":
        wiki_url = st.text_input("Enter Wikipedia page URL")
        if st.button("Fetch Wikipedia content", key="fetch_wiki_button"):
            fetched_text = wiki_text(wiki_url)
            if fetched_text:
                st.session_state.text_input = fetched_text
                st.success("Successfully fetched content from Wikipedia!")
            else:
                st.error("Failed to fetch content from the URL.")

    # Button to summarize
    if st.button('Summarize', key="summarize_button"):
        if st.session_state.text_input:
            summary = text_summarize(st.session_state.text_input, st.session_state.language)
            st.write("Summarized Text:")
            st.write(summary)
        else:
            st.error("No text provided for summarization.")

if __name__ == "__main__":
    main()
