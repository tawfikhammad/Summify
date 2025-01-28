from enum import Enum

class SummaryEnums(str, Enum):
    SUCCESS = "Summary generated successfully"
    EMPTY_SUMMARY = "Empty generated summary"
    LENGTH_MISMATCH = "Summary length exceeds original text"
    UNSUPPORTED_LANGUAGE = "Unsupported language"
    INVALID_EXTRACTED_TEXT = "No extracted text found or it's too short"

class SummApproach(str, Enum):

    EXTRACTIVE = "extractive"
    ABSTRACTIVE = "abstractive"
