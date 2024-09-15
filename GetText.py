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
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_file):
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


'''def extractOCR(file, language):
    pages = convert_from_path(file, 500)

    text = ''
    image_counter = 1

    for page in pages:
        page = str(((pytesseract.image_to_string(page, lang=f'{language[:3]}'))))
        page = page.replace("-\n", "")
        text += page
        image_counter = image_counter + 1

    with open('snd_project/text summarizer/output_text.txt', 'w', encoding='utf-8') as file:
            file.write(text)
    
    return text'''


def extractOCR(file, language):
    doc = fitz.open(file)
    text = ''
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # Get the page as a pixmap (image)
        pix = page.get_pixmap()
        
        # Convert pixmap to bytes and then to an image
        img_bytes = pix.tobytes("png")
        img = Image.open(BytesIO(img_bytes))
        
        ocr_text = pytesseract.image_to_string(img, lang=language[:3])
        ocr_text = ocr_text.replace("-\n", "")
        
        text += ocr_text
    
    return text


