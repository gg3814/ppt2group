from flask import Blueprint, request, jsonify
from ..services.gpt import call_chatgpt, first_text

explain_bp = Blueprint("explain", __name__)

@explain_bp.route("/explain", methods=["POST"])
def explain():
    subject = request.json.get("subject", "")
    level = request.json.get("level", "")
    if not subject or not level:
        return jsonify({"error": "need subject and level"}), 400

    prompt = (
        f"학생의 수준은 {level}이다. "
        f"'{subject}' 과목을 이해할 수 있도록 수준에 맞게 설명해줘. "
        f"상은 심화된 개념을, 중은 보통 수준의 설명을, 하는 기초부터 쉽게 설명해."
    )

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    return jsonify({"explanation": first_text(resp)})