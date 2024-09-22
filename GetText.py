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

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def is_scanned(pdf_path):

    is_scanned = True
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)

        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            if text and text.strip():  
                is_scanned = False
                break
    return is_scanned

def extract_text_from_pdf(pdf_file):

    if is_scanned(pdf_file):
        pages = convert_from_path(file, 500)

        image_counter = 1
        for page in pages:
            filename = "page_" + str(image_counter) + ".jpg"
            page.save(filename, "JPEG")
            image_counter = image_counter + 1
    
        limit = image_counter-1
        text = ""
        for i in range(1, limit + 1):
            filename = "page_" + str(i) + ".jpg"
            page = str(((pytesseract.image_to_string(Image.open(filename)))))
            page = page.replace("-\n", "")
            text += page
            os.remove(filename)
        return text
    else:
        
        text = ""
        try:
            with pdfplumber.open(BytesIO(pdf_file.read())) as pdf_document:
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
