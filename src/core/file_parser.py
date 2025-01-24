from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
import pymupdf
from helpers.enums import ExtractionEnums
from helpers import CleanText
from config import get_settings
from pdf2image import convert_from_bytes
import pytesseract
pytesseract.pytesseract.tesseract_cmd =  get_settings().TESSERACT_CMD


class FileParser:
    
    @staticmethod
    async def get_nativepdf_text(file: UploadFile) -> JSONResponse:

        try:
            content = await file.read()
            await file.seek(0)

            doc = pymupdf.open(stream=content, filetype="pdf")
            text = "".join(page.get_text() for page in doc)

            if not text or text == " ":
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ExtractionEnums.NO_TEXT_FOUND.value})
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": ExtractionEnums.SUCCESSFUL_EXTRACTION.value,
                    "text": "\n\n".join(text)
                })
        
        except Exception as e:
            print(f"Error text extracting from PDF: {e}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": ExtractionEnums.UNSUCCESSFUL_EXTRACTION.value}) 


    @staticmethod
    async def get_scannedpdf_text(file: UploadFile) -> JSONResponse:
        try:
            pdf_content = await file.read()
            await file.seek(0)  

            images = convert_from_bytes(
                pdf_content,
                dpi=300,          # Higher DPI improves accuracy
                fmt="jpeg",       # Output format
                thread_count=4,   # Parallel processing
                grayscale=True 
            )

            text = []
            for img in images:
                page_text  = pytesseract.image_to_string(img, lang="eng+ara")
                if page_text.strip():
                    text.append(page_text.strip())

            text = "\n\n".join(text)

            if not text or text == " ":
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ExtractionEnums.NO_TEXT_FOUND.value})
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": ExtractionEnums.SUCCESSFUL_EXTRACTION.value,
                    "text": text
                })
                
        except Exception as e:
            print(f"OCR extraction failed: {str(e)}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": ExtractionEnums.UNSUCCESSFUL_EXTRACTION.value})


    @staticmethod
    async def get_txtfile_text(file: UploadFile) -> JSONResponse:

        try:
            content = await file.read()
            await file.seek(0) 

            try:
                text = content.decode('utf-8').replace('\r\n', '\n').strip()
            except UnicodeDecodeError:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "File contains invalid UTF-8 encoding"})

            if not text:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": ExtractionEnums.NO_TEXT_FOUND.value}
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": ExtractionEnums.SUCCESSFUL_EXTRACTION.value,
                    "text": text
                })

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Text file processing failed: {str(e)}"})

    