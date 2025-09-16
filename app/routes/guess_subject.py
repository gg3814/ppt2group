from flask import Blueprint, request, jsonify
from ..services.gpt_service import call_chatgpt, get_first_content
from ..services.prompt_service import createGuessSubjectPrompt
from http import HTTPStatus
import logging

guess_bp = Blueprint("guess_subject", __name__)
log = logging.getLogger(__name__)

@guess_bp.route("/guess_subject", methods=["POST"])
def subject():
    log.info("[START] /guess_subject [POST]")

    keywords: list[str] = request.json.get("keywords", [])
    if not keywords:
        log.warning("[ERROR] /guess_subject [POST] : There is no keywords");
        return jsonify({"error": "no keywords"}), HTTPStatus.BAD_REQUEST

    prompt = createGuessSubjectPrompt(keywords)

    resp = call_chatgpt([{"role": "user", "content": prompt}])

    log.info("[END] /guess_subject [POST]")
    return jsonify({"subject": get_first_content(resp)})