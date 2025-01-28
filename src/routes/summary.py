from fastapi import APIRouter, UploadFile, Depends, Form
from controllers import SummaryController
from .schemas import UploadRequest
from helpers.enums import SummApproach


summ_router = APIRouter()

def get_upload_request(summ_approach: SummApproach = Form(SummApproach.EXTRACTIVE), 
                       max_length: int = Form(100),
                       num_sentences: int = Form(1)) -> UploadRequest:

    return UploadRequest(summ_approach = summ_approach, max_length = max_length, num_sentences = num_sentences)

@summ_router.post('/data/summary/file')
async def upload_file(file: UploadFile, upload_request: UploadRequest = Depends(get_upload_request)):
    
    summary_controller = SummaryController(file= file, upload_request= upload_request)
    summary = await summary_controller.get_summary()
    
    return summary

@summ_router.post('data/summary/text')
async def get_text():
    pass