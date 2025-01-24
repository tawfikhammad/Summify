from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from typing import Tuple
from .enums import ScanEnums
import pymupdf 


class ScanChecker:
    
    @staticmethod
    async def is_scan(file: UploadFile) -> Tuple[bool, str]:
        
        try:
            content = await file.read()
            await file.seek(0)  
            
            doc = pymupdf.open(stream=content, filetype="pdf")
            text_pages = 0
            
            for page in doc:
                if page.get_text().strip():  
                    text_pages += 1
            
            if text_pages == len(doc) :
                return (False, ScanEnums.NATIVE_PDF.value)  
            
            return (True, ScanEnums.SCANNED_PDF.value)

        except Exception as e:
            raise HTTPException(500, f"PDF analysis failed: {str(e)}")
