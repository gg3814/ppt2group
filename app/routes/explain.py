from flask import Blueprint, request, jsonify
from ..services.gpt_service import ask_gpt, get_first_content
from ..services.prompt_service import createExplainKeywordPrompt
from http import HTTPStatus
import logging

explain_bp = Blueprint("explain", __name__)
log = logging.getLogger(__name__)

@explain_bp.route("/explain/slides", methods=["POST"])
def explain():
    log.info("[START] /explain/slides [POST]")

    data = request.json or {}
    subject = request.json.get("subject", "")
    level = request.json.get("level", "")
    slides = data.get("slides",{})     # {1:"...", ...} 
    keywords = data.get("keywords",{}) # {1:[...], ...}

    if not subject or not level or not slides or not keywords:
        log.warning("[ERROR] /explain/slides [POST] : Missing request");
        return jsonify({"error":"missing subject/level/slides/keywords"}), HTTPStatus.BAD_REQUEST
    
    per_slide = {}
    for sid, text in slides.items():
        kw = keywords.get(sid, [])[:10]
        prompt = createExplainKeywordPrompt(level=level, subject=subject, keywords=kw)

        try:
            resp = ask_gpt([{"role":"user","content":prompt}])
        except RuntimeError:
            return jsonify({"error": "예외 발생. 다시 시도해주세요."}), HTTPStatus.INTERNAL_SERVER_ERROR
        
        per_slide[sid] = get_first_content(resp)

    log.info("[END] /explain/slides [POST]")
    return jsonify({"explanations": per_slide})
