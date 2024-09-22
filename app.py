import streamlit as st
from summarizer import text_summarize
from GetText import extract_text_from_pdf, file_text, wiki_text

def main():
    st.title('Text Summarizer')

    # Initialize session state variables if they don't exist
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""

    # User chooses the input method
    input_method = st.radio(
        "**Choose the input method**", 
        ("Enter text directly", "Upload a PDF file")
    )


    # If "Enter text directly"
    if input_method == "Enter text directly":
        st.session_state.text_input = st.text_area("Enter text directly here")

    # If "Upload a PDF file"
    elif input_method == "Upload a PDF file":
        uploaded_pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf_file is not None:
            st.session_state.text_input = extract_text_from_pdf(uploaded_pdf_file)


    # Button to summarize
    if st.button('Summarize', key="summarize_button"):
        if st.session_state.text_input:
            summary = text_summarize(st.session_state.text_input)
            st.write("Summarized Text:")
            st.write(summary)
        else:
            st.error("No text provided for summarization.")

if __name__ == "__main__":
    main()
