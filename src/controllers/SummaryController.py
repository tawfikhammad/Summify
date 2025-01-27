from fastapi import UploadFile, File, status
from fastapi.responses import JSONResponse
from .BaseController import BaseController
from helpers import FileValidator, ScanChecker
from core import FileParser, TextSummarizer
import json


class SummaryController(BaseController):
    def __init__(self, file: UploadFile):
        super().__init__()
        self.file = file
    
    async def get_summary(self):

        is_valid, message = await FileValidator.isvalid(self.file)

        if not is_valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
        
        if self.file.content_type == self.settings.ALLOWED_FILE_TYPES[0]:       # pdf file
            Scanned, message = await ScanChecker.is_scan(self.file)
            if Scanned:
                response = await FileParser.get_scannedpdf_text(self.file) 
                if response['status_code'] == 200:
                    text = response['content']['text']
                else: 
                    return JSONResponse(status_code=response['status_code'], content={response['content']})
            else:
                response= await FileParser.get_nativepdf_text(self.file)
                if response['status_code'] == 200:
                    text = response['content']['text']
                else:
                    return JSONResponse(status_code=response['status_code'], content={response['content']})
        
        elif self.file.content_type == self.settings.ALLOWED_FILE_TYPES[1]:     # text file
            response = await FileParser.get_txtfile_text(self.file)
            if response['status_code'] == 200:
                text = response['content']['text']
            else:
                return JSONResponse(status_code=response['status_code'], content={response['content']})
            
        summarizer = TextSummarizer(text)
        return await summarizer.abstractive_summarize()

            

        

        