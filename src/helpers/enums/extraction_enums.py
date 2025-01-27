from enum import Enum

class ExtractionEnums(Enum):

    SUCCESSFUL_EXTRACTION = "Text extraction successful"
    UNSUCCESSFUL_EXTRACTION = "Text extraction unsuccessful"
    NO_TEXT_FOUND = "No text found in file"
    INVALID_ENCODING = "File contains invalid UTF-8 encoding"
