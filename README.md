# Text Summarization App
---
This application allows users to summarize text from different sources using NLP techniques.

----

## Table of Contents
---
1. Overview


----

## Overview
---
This project is a Text Summarizer app built using **Streamlit**. The app allows users to input text in various formats, including:
* direct text input
* text files
* PDF files
* and Wikipedia URLs

then generate a summarized version of the provided text. Using NLP techniques to extract key sentences from the text and display a concise summary.

----

## How Code Works
---
### 1. `app.py`
This file contains the Streamlit app. It handles the user interface, manages input methods, and displays results. the file contain two parts:

The user's input choice:

1. **"Enter text directly"**:
   - The user manually input text and it is saved in the session state variable `st.session_state.text_input`.


2. **"Upload a text file"**:
   - The user upload a `.txt` file using `st.file_uploader()` and the code reads the contents of the file using the `file_text()` function Then the stored in `st.session_state.text_input`

3. **"Upload a PDF file"**:
   - The user upload a `.pdf` file using `st.file_uploader()` the text is extracted using the `extract_text_from_pdf()` function and the text is saved to the session state variable.

4. **"Enter Wikipedia page URL"**:
   - The user input a Wikipedia page URL. Once the user must click the "Fetch Wikipedia content" button to retrieve the content from the given Wikipedia page Using `wiki_text()` func. If the scraping is successful, the fetched Wikipedia content is saved in `st.session_state.text_input`
   

Summarizing the Text:

   - After any of the above input methods the user can click the "Summarize" button. The code checks if `st.session_state.text_input` contains any text. If text is available, it calls the `text_summarize()` function to generate a summary. Finally the summarized text is then displayed to the user.


### 2. `summarizer.py`
This file contains the `text_summarize` function, which is responsible for processing the text and generating the summary.

I summary the steps are:

- Tokenizes the text into sentences and words.
- Removes stopwords and computes word frequency.
- Scores each sentence based on the importance of words it contains.
- Extracts and returns the MOST IMPORTANT sentences as a summary.

### 3. `GetText.py`
This file provides utility functions for extracting text from different sources:
- **`extract_text_from_pdf`**: Extracts text from a PDF file.
- **`file_text`**: Reads and processes a text file.
- **`wiki_text`**: Scrapes and extracts text from a Wikipedia page.
- **`extractOCR`**: For extracting text from image-based PDF files using OCR. WILL BE ADDED  

----

## Interact with API:
---
I Build a treamlit app and connect it with Streamlit cloud to can be interacted with others.

### Access the App from this link:

LET'S interact with app:

Feel free to use any docu (.pdf or .txt), any wikipedia URL or put the text manually and the app will show the summary of text.

----

## Watch the Demo
---
[DEMO]()