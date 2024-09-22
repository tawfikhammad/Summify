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
    if is_scanned(uploaded_file):
        # Convert PDF to images
        pages = convert_from_path(uploaded_file, 500)

        text = ""
        for page in pages:
            # Convert each page to an image and extract text
            img_byte_arr = BytesIO()
            page.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)

            page_text = pytesseract.image_to_string(Image.open(img_byte_arr))
            page_text = page_text.replace("-\n", "")
            text += page_text
        
        return text
    else:
        # Handle the case where the PDF is not scanned
        text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf_document:
                for page in pdf_document.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        
        return text


def file_text(file):
    text = file.read().decode("utf-8")
    text = text.replace("\n", '')

    return text
    

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
