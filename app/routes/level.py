from flask import Blueprint, request, jsonify
from ..services.gpt import call_chatgpt, first_text
import json

level_bp = Blueprint("level", __name__)

# 1) 질문 생성
@level_bp.route("/level/questions", methods=["POST"])
def generate_questions():
    subject = request.json.get("subject", "")
    if not subject:
        return jsonify({"error": "no subject"}), 400

    prompt = (
        f"'{subject}' 과목을 학습한 학생 수준을 평가하기 위한 OX 문제 5개를 만들어라.\n"
        f"각 문제는 JSON 배열 형태로 제공하라. 각 항목은 {{'question': '...', 'answer': 'O'}} "
        f"형태여야 한다. 오직 JSON만 출력하라."
    )

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    text = first_text(resp)

    try:
        questions = json.loads(text)
    except Exception:
        # GPT가 JSON 형식을 안 지킨 경우 대비
        questions = [{"question": text, "answer": "O"}]

    return jsonify({"questions": questions})


# 2) 답안 제출 → 수준 평가
@level_bp.route("/level/evaluate", methods=["POST"])
def evaluate():
    subject = request.json.get("subject", "")
    answers = request.json.get("answers", [])
    questions = request.json.get("questions", [])

    if not subject or not answers or not questions:
        return jsonify({"error": "need subject, questions and answers"}), 400

    prompt = (
        f"'{subject}' 과목에 대한 OX 문제와 학생 답안이 있다.\n\n"
        f"문제와 정답: {questions}\n"
        f"학생의 답변: {answers}\n\n"
        f"정답과 비교해 점수를 매기고, 학생 수준을 '상/중/하' 중 하나로 평가하라. "
        f"그리고 간단한 이유를 한 문장으로 설명하라.\n"
        f"출력은 JSON 형식으로 {{'level': '상', 'reason': '...'}} 형태만 제공하라."
    )

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    text = first_text(resp)

    try:
        result = json.loads(text)
    except Exception:
        result = {"level": "중", "reason": text}

    return jsonify(result)
