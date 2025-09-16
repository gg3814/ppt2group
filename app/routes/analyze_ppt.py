from flask import Blueprint, request, jsonify
from ..services.ppt_service import parse_ppt
from ..services.keyword_service import extract_keywords
from ..services.file_service import save_file
from http import HTTPStatus
import logging

analyze_bp = Blueprint("analyze_ppt", __name__)
log = logging.getLogger(__name__)

# 프론트에서 파일을 받는 <input type="file"> 의 name 속성과 같아야 함
input_name = "file"

@analyze_bp.route("/analyze_ppt", methods=["POST"])
def analyze():
    log.info("[START] /analyze_ppt [POST]")
    
    if input_name not in request.files:
        log.warning("[ERROR] /analyze_ppt [POST] : There is no file");
        return jsonify({"error": "No file uploaded"}), HTTPStatus.BAD_REQUEST
    
    filepath = save_file(request.files[input_name])

    slides_text = parse_ppt(filepath)

    keywords = {sid: extract_keywords(text) for sid, text in slides_text.items()}

    log.info("[END] /analyze_ppt [POST]")
    return jsonify({"keywords": keywords})