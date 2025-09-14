import yake

def extract_keywords(text: str, max_keywords: int = 10) -> list:
    kw_extractor = yake.KeywordExtractor(lan="ko", n=1, top=max_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]