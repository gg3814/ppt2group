import yake
import logging

log = logging.getLogger(__name__)

def extract_keywords(text: str, max_keywords: int = 10) -> list:

    kw_extractor = yake.KeywordExtractor(lan="ko", n=1, top=max_keywords)
    keywords = [kw for kw, score in (kw_extractor.extract_keywords(text))]

    log.info("Extracted keywords: %s", keywords)
    return keywords