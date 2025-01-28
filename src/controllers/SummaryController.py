from fastapi import UploadFile, File, status
from fastapi.responses import JSONResponse
from .BaseController import BaseController
from core import FileParser, TextSummarizer
from routes.schemas import UploadRequest
from helpers.enums import ExtractionEnums, SummApproach
from helpers import FileValidator, ScanChecker


class SummaryController(BaseController):
    def __init__(self, file: UploadFile, upload_request: UploadRequest):
        super().__init__()
        self.file = file
        self.summ_approach = upload_request.summ_approach
        self.max_length = upload_request.max_length
        self.num_sentences = upload_request.num_sentences
    
    async def get_summary(self):

        is_valid, message = await FileValidator.isvalid(self.file)

        if not is_valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"message": message})
        
        if self.file.content_type == self.settings.ALLOWED_FILE_TYPES[0]:       # pdf file
            Scanned, message = await ScanChecker.is_scan(self.file)
            if Scanned:
                response = await FileParser.get_scannedpdf_text(self.file) 
                if response['status_code'] == status.HTTP_200_OK:
                    text = response['content']['text']
                else: 
                    return JSONResponse(status_code=response['status_code'],
                                        content={response['content']})
            else:
                response= await FileParser.get_nativepdf_text(self.file)
                if response['status_code'] == status.HTTP_200_OK:
                    text = response['content']['text']
                else:
                    return JSONResponse(status_code=response['status_code'],
                                        content={response['content']})
        
        elif self.file.content_type == self.settings.ALLOWED_FILE_TYPES[1]:     # text file
            response = await FileParser.get_txtfile_text(self.file)
            if response['status_code'] == status.HTTP_200_OK:
                text = response['content']['text']
            else:
                return JSONResponse(status_code=response['status_code'], 
                                    content={response['content']})
        
            
        summarizer = TextSummarizer(text)

        if self.summ_approach == SummApproach.EXTRACTIVE:
            return await summarizer.extractive_summarize(num_sentences=self.num_sentences)
        
        elif self.summ_approach == SummApproach.ABSTRACTIVE:
            return await summarizer.abstractive_summarize(max_length=self.max_length)

            

        

        