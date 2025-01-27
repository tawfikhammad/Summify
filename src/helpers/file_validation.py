from config import get_settings, Settings
from fastapi import UploadFile
from .enums import ValidationEnums
from typing import Tuple

settings = get_settings()

class FileValidator:

    @staticmethod   
    async def isvalid(file: UploadFile) -> Tuple[bool, str]:
        
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            return False, ValidationEnums.NOT_ALLOWED_FILE_TYPE.value
        
        if file.size > settings.MAX_FILE_SIZE:
            return False, ValidationEnums.INVALID_FILE_SIZE.value
        
        return True , ValidationEnums.VALID_FILE.value