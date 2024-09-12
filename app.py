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
        ("Enter text directly", "Upload a text file", "Upload a PDF file", "Enter Wikipedia page URL")
    )


    # If "Enter text directly"
    if input_method == "Enter text directly":
        st.session_state.text_input = st.text_area("Enter text directly here")

    # If "Upload a text file"
    elif input_method == "Upload a text file":
        uploaded_text_file = st.file_uploader("Choose a text file", type="txt")
        if uploaded_text_file is not None:
            st.session_state.text_input = file_text(uploaded_text_file)

    # If "Upload a PDF file"
    elif input_method == "Upload a PDF file":
        uploaded_pdf_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf_file is not None:
            st.session_state.text_input = extract_text_from_pdf(uploaded_pdf_file)

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
            summary = text_summarize(st.session_state.text_input)
            st.write("Summarized Text:")
            st.write(summary)
        else:
            st.error("No text provided for summarization.")

if __name__ == "__main__":
    main()
