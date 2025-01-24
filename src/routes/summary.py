from fastapi import APIRouter, File, UploadFile
from controllers import SummaryController

summ_router = APIRouter()

@summ_router.post('/data/summary')
async def upload_file(file: UploadFile):
    
    summary_controller = SummaryController(file)
    summary = await summary_controller.get_summary()
    
    return summary

@summ_router.post('data/summary/text')
async def get_text():
    pass