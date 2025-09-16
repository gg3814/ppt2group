from flask import Blueprint, request, jsonify
from ..services.gpt_service import call_chatgpt, get_first_content
from ..services.prompt_service import createGenerateQuestionPrompt
import json
from http import HTTPStatus
import logging

generate_bp = Blueprint("generate_question", __name__)
log = logging.getLogger(__name__)

# 1) 질문 생성
@generate_bp.route("/generate_question", methods=["POST"])
def generate():
    log.info("[START] /generate_question [POST]")

    subject: str = request.json.get("subject", "")
    if not subject:
        log.warning("[ERROR] /generate_question [POST] : There is no subject");
        return jsonify({"error": "no subject"}), HTTPStatus.BAD_REQUEST
    
    prompt = createGenerateQuestionPrompt(subject);

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    text = get_first_content(resp)

    questions = json.loads(text)

    log.info("[END] /generate_question [POST]")
    return jsonify(questions)