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
    slides = data.get("slides",{})     # {"slide_1":"...", ...} 
    keywords = data.get("keywords",{}) # {"slide_1":[...], ...}

    if not subject or not level or not slides or not keywords:
        log.warning("[ERROR] /explain/slides [POST] : Missing request");
        return jsonify({"error":"missing subject/level/slides/keywords"}), HTTPStatus.BAD_REQUEST
    
    per_slide = {}
    for sid, text in slides.items():
        kw = keywords.get(sid, [])[:10]
        prompt = createExplainKeywordPrompt(level=level, subject=subject, keywords=kw)

        resp = ask_gpt([{"role":"user","content":prompt}])
        per_slide[sid] = get_first_content(resp)

    log.info("[END] /explain/slides [POST]")
    return jsonify({"explanations": per_slide})
