from yake import KeywordExtractor
import re
STOP = {"그리고","그러나","입니다","등","및","것","수"}
ke = KeywordExtractor(lan="ko", n=3, top=10, dedupLim=0.9)

def get_keywords(text:str):
    if not text.strip(): return []
    cand = [k for k,_ in ke.extract_keywords(text)]
    out = []
    for c in cand:
        c = c.strip()
        if len(c)<2: continue
        if c in STOP: continue
        if re.fullmatch(r"[0-9\W_]+", c): continue
        if c not in out: out.append(c)
    return out[:10]
