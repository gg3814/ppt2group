from flask import Blueprint, request, jsonify
import json
from ..services.gpt import call_chatgpt, first_text

mode_bp = Blueprint("mode", __name__)

# A모드: 레벨 직접 선택 → 바로 등급 확정
@mode_bp.route("/mode/select", methods=["POST"])
def mode_select():
    data = request.json or {}
    level = data.get("level")          # "하"|"중"|"상"
    subject = data.get("subject","")
    keywords = data.get("keywords",{}) # {"slide_1":[...], ...}
    if not level or not subject or not keywords:
        return jsonify({"error":"missing level/subject/keywords"}), 400
    return jsonify({"level": level, "subject": subject, "keywords": keywords})

# B모드 시작: 객관식 5문제 생성(보기 3개, 정답 1개) JSON 강제
@mode_bp.route("/mode/test/start", methods=["POST"])
def test_start():
    subject = (request.json or {}).get("subject", "")
    if not subject:
        return jsonify({"error":"missing subject"}), 400

    prompt = (
        f"당신은 {subject} 과목 교수입니다. 객관식 5문제를 JSON 배열로 만드세요. "
        "각 문제는 {'question': '...', 'options': ['A','B','C'], 'answer': '정답'} 형태. "
        "오직 JSON만 출력."
    )
    resp = call_chatgpt([{"role":"user","content":prompt}])
    text = first_text(resp)

    # GPT가 JSON 말고 설명을 섞어서 주는 경우 대비
    import re, json
    match = re.search(r"\[.*\]", text, re.S)
    questions = []
    if match:
        try:
            questions = json.loads(match.group())
        except:
            questions = []
    return jsonify({"questions": questions})


# B모드 제출: 채점 → 점수/등급 JSON
@mode_bp.route("/mode/test/submit", methods=["POST"])
def test_submit():
    data = request.json or {}
    subject = data.get("subject","")
    questions = data.get("questions",[])
    answers = data.get("answers",[])  # 사용자가 고른 보기 문자열 배열
    if not subject or not questions or not answers:
        return jsonify({"error":"missing subject/questions/answers"}), 400
    prompt = (
        f"과목: {subject}\n문제: {questions}\n사용자답: {answers}\n\n"
        "각 문항 정답과 비교해 100점 만점 점수를 계산. "
        "점수→등급 규칙: 0-59 하, 60-84 중, 85-100 상. "
        "JSON만 출력: {'score': 0-100, 'level': '하|중|상'}"
    )
    resp = call_chatgpt([{"role":"user","content":prompt}])
    text = first_text(resp)
    try:
        result = json.loads(text)
    except:
        result = {"score": 0, "level": "하"}
    return jsonify(result)
