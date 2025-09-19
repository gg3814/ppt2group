import yake
import logging

log = logging.getLogger(__name__)

# 텍스트에서 키워드 찾아 리스트 반환
def extract_keywords(texts: str, max_keywords: int = 10) -> list[str]:

    kw_extractor = yake.KeywordExtractor(lan="ko", n=1, top=max_keywords)
    keywords = [kw for kw, score in (kw_extractor.extract_keywords(texts))]

    log.info("Extracted keywords: %s", keywords)
    return keywords