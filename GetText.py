from PyPDF2 import PdfReader
import urllib.request
import bs4 as bs
import re
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import pdfplumber
from io import BytesIO
from bidi.algorithm import get_display
import tempfile


pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/tessdata'

def is_scanned(uploaded_file):

    is_scanned = True
    reader = PdfReader(uploaded_file)
    for page_num in range(len(reader.pages)):
        text = reader.pages[page_num].extract_text()
        if text and text.strip():  
            is_scanned = False
            break
    return is_scanned

def extract_text_from_pdf(uploaded_file):
    # Create a temporary file to save the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name
    
    try:
        # Check if the PDF is scanned
        if is_scanned(temp_pdf_path):
            # Convert PDF to images
            pages = convert_from_path(temp_pdf_path, 500)

            text = ""
            for page in pages:
                img_byte_arr = BytesIO()
                page.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)

                page_text = pytesseract.image_to_string(Image.open(img_byte_arr), lang = 'ara')
                page_text = page_text.replace("-\n", "")
                text += page_text
            
            return text
        else:
            text = ""
            try:
                with pdfplumber.open(temp_pdf_path) as pdf_document:
                    for page in pdf_document.pages:
                        text += page.extract_text() or ""

                text = get_display(text)
            except Exception as e:
                print(f"Error extracting text from PDF: {e}")
            
            return text
    finally:
        # Cleanup: Remove the temporary file
        os.remove(temp_pdf_path)
    

# Read wikipedia page url and return its Text   
def wiki_text(url):
    scrap_data = urllib.request.urlopen(url)
    article = scrap_data.read()
    parsed_article = bs.BeautifulSoup(article,'lxml')
    
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    
    for p in paragraphs:
        article_text += p.text
    
    #Removing all unwanted characters
    article_text = re.sub(r'\[[0-9]*\]', '', article_text)

    return article_text
