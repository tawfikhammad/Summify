from enum import Enum

class SummaryEnums(str, Enum):
    SUCCESS = "Summary generated successfully"
    EMPTY_SUMMARY = "Empty generated summary"
    LENGTH_MISMATCH = "Summary length exceeds original text"
    UNSUPPORTED_LANGUAGE = "Unsupported language"
    INVALID_TEXT = "No text found or text is too short"
