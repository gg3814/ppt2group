from flask import Blueprint, request, jsonify
import json
from ..services.gpt_service import ask_gpt, get_first_content
from ..services.prompt_service import createGenerateQuestionPrompt, createEvaluateLevelPrompt
from ..services.evaluation_service import evaluate
from http import HTTPStatus
import logging

log = logging.getLogger(__name__)

mode_bp = Blueprint("mode", __name__)

# A모드: 레벨 직접 선택 → 바로 등급 확정
# @mode_bp.route("/mode/select", methods=["POST"])
# def mode_select():
#     log.info("[START] /mode/select [POST]")

#     data = request.json or {}
#     level = data.get("level")          # "하"|"중"|"상"
#     subject = data.get("subject","")
#     keywords = data.get("keywords",{}) # {"slide_1":[...], ...}

#     if not level or not subject or not keywords:
#         log.warning("[ERROR] /mode/select [POST] : Missing request")
#         return jsonify({"error":"missing level/subject/keywords"}), HTTPStatus.BAD_REQUEST
    
#     log.info("[END] /mode/select [POST]")
#     return jsonify({"level": level})

# B모드 시작: 객관식 5문제 생성(보기 3개, 정답 1개) JSON 강제
@mode_bp.route("/mode/test/start", methods=["POST"])
def test_start():
    log.info("[START] /mode/test/start [POST]")

    subject = (request.json or {}).get("subject", "")

    if not subject:
        log.warning("[ERROR] /mode/test/start [POST] : Missing subject")
        return jsonify({"error":"missing subject"}), HTTPStatus.BAD_REQUEST
    
    prompt = createGenerateQuestionPrompt(subject)
    try:
        resp = ask_gpt([{"role":"user","content":prompt}])
    except RuntimeError:
        return jsonify({"error": "예외 발생. 다시 시도해주세요."}), HTTPStatus.INTERNAL_SERVER_ERROR
    text = get_first_content(resp)

    # GPT가 JSON 말고 설명을 섞어서 주는 경우 대비
    import re, json
    match = re.search(r"\[.*\]", text, re.S)
    questions = []
    if match:
        try:
            questions = json.loads(match.group())
        except:
            questions = []
  
    log.info("[END] /mode/test/start [POST]")
    return jsonify({"questions": questions})


# B모드 제출: 채점 → 점수/등급 JSON
@mode_bp.route("/mode/test/submit", methods=["POST"])
def test_submit():
    log.info("[START] /mode/test/submit [POST]")

    data = request.json or {}
    subject = data.get("subject","")
    questions = data.get("questions",[])
    answers = data.get("answers",[])  # 사용자가 고른 보기 문자열 배열

    if not subject or not questions or not answers:
        log.warning("[ERROR] /mode/test/submit [POST] : Missing request")
        return jsonify({"error":"missing subject/questions/answers"}), HTTPStatus.BAD_REQUEST
    
    correct = [question['answer'] for question in questions]
    result = evaluate(correct, answers)

    log.info("[END] /mode/test/submit [POST]")    
    return jsonify(result)
