from pydantic import BaseModel
from pydantic import Field, PositiveInt
from helpers.enums import SummApproach
from typing import Optional


class UploadRequest(BaseModel):

    summ_approach: SummApproach = Field(default= SummApproach.ABSTRACTIVE)
    num_sentences: Optional[PositiveInt] = Field(default=1)
    max_length: Optional[PositiveInt] = Field(default=100)