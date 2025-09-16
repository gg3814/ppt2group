from flask import Blueprint, request, jsonify
from ..services.gpt_service import call_chatgpt, get_first_content
from ..services.prompt_service import createEvaluateLevelPrompt
import json
from http import HTTPStatus
import logging

evaluate_bp = Blueprint("evaluate_level", __name__)
log = logging.getLogger(__name__)

# 답안 제출 → 수준 평가
@evaluate_bp.route("/evaluate_level", methods=["POST"])
def evaluate():
    log.info("[START] /evaluate_level [POST]")

    subject: str = request.json.get("subject", "")
    questions: list[dict[str, str]] = request.json.get("questions", [])
    answers: list[str] = request.json.get("answers", [])

    if not subject or not answers or not questions:
        log.warning("[ERROR] /evaluate_level [POST] : There is no subject, level or answers");
        return jsonify({"error": "need subject, questions or answers"}), HTTPStatus.BAD_REQUEST
    
    prompt = createEvaluateLevelPrompt(subject, questions, answers)

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    text = get_first_content(resp)

    try:
        result = json.loads(text)
    except Exception:
        result = {"level": "중", "reason": text}

    log.info("[END] /evaluate_level [POST]")
    return jsonify(result)
