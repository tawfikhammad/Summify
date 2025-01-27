from fastapi import status
from fastapi.responses import JSONResponse
from helpers import LangDetector
from helpers.enums import SummaryEnums
from config import settings
from helpers import TextProcessor

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self, text:str):

        if not text or len(text.strip()) < 150:              # Minimum 150 chars
            raise ValueError(SummaryEnums.INVALID_TEXT.value)
        self.text = text

        response = LangDetector.detect(text)
        if response['status_code'] == status.HTTP_200_OK:
            self.lang = response['content']["lang"]
        else:
            logger.error(response['content']['message'])
            raise ValueError(SummaryEnums.UNSUPPORTED_LANGUAGE.value)
        
    async def abstractive_summarize(self, max_length: int = 300)-> JSONResponse:

        try:
            if self.lang == 'en':
                summarizer = pipeline("summarization", model=settings.ENG_MODEL)
                summary = summarizer(self.text, max_length=max_length, min_length=30, do_sample=False)[0]["summary_text"]
                
            elif self.lang == 'ar':
                tokenizer = AutoTokenizer.from_pretrained(settings.ARA_TOKENIZER, use_fast=False)
                model = AutoModelForSeq2SeqLM.from_pretrained(settings.ARA_MODEL)
                summarizer = pipeline("text2text-generation",model=model,tokenizer=tokenizer)
                summary = summarizer(self.text, max_length=max_length, repetition_penalty=3.0)[0]["generated_text"]

        except Exception as e:
            logger.error(f"Abstractive summarization failed: {str(e)}")
            raise
            
        if not summary or summary == "":
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": SummaryEnums.EMPTY_SUMMARY.value})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": SummaryEnums.SUCCESS.value, 
                                                                    "summary": summary})
        
        
    async def extractive_summarize(self, sentences_count: int = 3) -> str:

        processor = TextProcessor(self.text, self.lang)
        sentences = await processor.get_sentences()
            
        parser = PlaintextParser.from_string(" ".join(sentences), Tokenizer(self.lang))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, sentences_count)
        text = " ".join([str(sentence) for sentence in summary])
        
        if not text or text == "":
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": SummaryEnums.EMPTY_SUMMARY.value })
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": SummaryEnums.SUCCESS.value,
                                                                         "summary": text})
