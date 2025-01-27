import langdetect 
from fastapi import status
from fastapi.responses import JSONResponse
from .enums import SummaryEnums

class LangDetector:

    @staticmethod
    def detect(text) -> dict:

        lang = langdetect.detect(text)

        if lang not in ["en", "ar"]:
            return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "content": {"message": SummaryEnums.UNSUPPORTED_LANGUAGE.value}}
        else:
            return {"status_code": status.HTTP_200_OK, "content": {"lang": lang}}