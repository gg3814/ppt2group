from flask import Blueprint, request, jsonify
from ..services.gpt_service import call_chatgpt, get_first_content
from ..services.prompt_service import createExplainKeywordPrompt
from http import HTTPStatus
import logging

explain_bp = Blueprint("explain_keyword", __name__)
log = logging.getLogger(__name__)

@explain_bp.route("/explain_keyword", methods=["POST"])
def explain():
    log.info("[START] /explain_keyword [POST]")

    subject = request.json.get("subject", "")
    level = request.json.get("level", "")
    keywords = request.json.get("keywords", "")
    
    if not subject or not level:
        log.warning("[ERROR] /explain_keyword [POST] : There is no subject or level");
        return jsonify({"error": "need subject or level"}), HTTPStatus.BAD_REQUEST
    
    prompt = createExplainKeywordPrompt(level, subject, keywords)

    resp = call_chatgpt([{"role": "user", "content": prompt}])

    log.info("[END] /explain_keyword [POST]")
    return jsonify({"explanation": get_first_content(resp)})