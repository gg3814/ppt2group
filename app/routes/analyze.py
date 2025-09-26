from flask import Blueprint, request, jsonify
from ..services.ppt_service import parse_ppt
from ..services.keyword_service import extract_keywords
from ..services.file_service import save_file
from ..services.gpt_service import ask_gpt, get_first_content
from ..services.prompt_service import createGuessSubjectPrompt
from http import HTTPStatus
import logging

analyze_bp = Blueprint("analyze", __name__)
log = logging.getLogger(__name__)

# 프론트에서 파일을 받는 <input type="file"> 의 name 속성과 같아야 함
INPUT_NAME = "file"

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    log.info("[START] /analyze [POST]")
    
    # 파일이 없을 시 400 BAD REQUEST 응답
    if INPUT_NAME not in request.files:
        log.warning("[ERROR] /analyze [POST] : There is no file")
        return jsonify({"error": "파일이 없습니다."}), HTTPStatus.BAD_REQUEST
    # 1. PPT에서 텍스트 파싱    
    # 파일 저장 중 예외시 500 INTERNAL SERVER ERROR 응답
    filepath = ""
    try:
        filepath = save_file(request.files[INPUT_NAME])
    except RuntimeError:
        return jsonify({"error": "예외 발생. 다시 시도해주세요."}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    slides_text = parse_ppt(filepath)

    # 2. 텍스트에서 키워드 추출
    keywords = {}
    for idx, texts in slides_text.items():
        keywords[idx] = extract_keywords(texts);

    # 3. 과목 추측
    keyword_list = []
    for keyword in keywords.values():
        keyword_list += keyword

    try:
        prompt = createGuessSubjectPrompt(keyword_list[:200])
        resp = ask_gpt([{"role":"user","content":prompt}])
    except RuntimeError:
        return jsonify({"error": "예외 발생. 다시 시도해주세요."}), HTTPStatus.INTERNAL_SERVER_ERROR

    subject = get_first_content(resp)

    log.info("[END] /analyze [POST]")
    return jsonify({
        "slides": slides_text,
        "keywords": keywords,
        "subject": subject
    })
