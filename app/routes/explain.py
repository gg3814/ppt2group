from flask import Blueprint, request, jsonify
from ..services.gpt import call_chatgpt, first_text

explain_bp = Blueprint("explain", __name__)

# 슬라이드별 핵심 단어를 등급에 맞춰 설명. 하이라이트는 프론트에서 span 처리.
@explain_bp.route("/explain/slides", methods=["POST"])
def explain_slides():
    data = request.json or {}
    subject = data.get("subject","")
    level = data.get("level","")
    slides = data.get("slides",{})     # {"slide_1":"...", ...}
    keywords = data.get("keywords",{}) # {"slide_1":[...], ...}

    if not subject or not level or not slides or not keywords:
        return jsonify({"error":"missing subject/level/slides/keywords"}), 400

    per_slide = {}
    for sid, text in slides.items():
        kw = keywords.get(sid, [])[:10]
        prompt = (
            f"과목: {subject}\n학습 수준: {level}\n"
            f"슬라이드 핵심 단어: {', '.join(kw)}\n\n"
            "위 핵심 단어들만을 대상으로, 해당 단어들의 개념을 "
            "수준에 맞춰 3~5줄로 간결히 설명하라. 목록 형태로 출력."
        )
        resp = call_chatgpt([{"role":"user","content":prompt}])
        per_slide[sid] = first_text(resp).strip()

    return jsonify({"explanations": per_slide})
