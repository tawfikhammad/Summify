import re
import spacy

class TextProcessor:
    def __init__(self, text:str, lang:str):
        self.text = text
        self.lang = lang
        self.nlp_models = {
            "ar": spacy.blank('ar'),
            "en": spacy.blank('en')
        }


    async def clean_ar(self) -> str:

        text = re.sub( 
            r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0020\u0640\u0621-ئء]', ' ', self.text)

        return text
    
    async def get_sentences(self) -> list:

        nlp = self.nlp_models[self.lang]
        nlp.add_pipe('sentencizer')
        doc = nlp(self.text)
        sentences = [sent.text for sent in doc.sents]

        return sentences