from enum import Enum

class ValidationEnums(Enum):

    NOT_ALLOWED_FILE_TYPE = "Unsupported File Type"
    INVALID_FILE_SIZE = "File Size Exceeds Allowed Limit"
    VALID_FILE = "File Validation Successful"
    INVALID_FILE = "File Validation Unsuccessful"