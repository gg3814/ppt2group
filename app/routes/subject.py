from flask import Blueprint, request, jsonify
from ..services.chat_gpt import call_chatgpt, get_first_content

subject_bp = Blueprint("subject", __name__)

@subject_bp.route("/subject", methods=["POST"])
def subject():
    keywords = request.json.get("keywords", [])
    if not keywords:
        return jsonify({"error": "no keywords"}), 400

    prompt = (
        f"다음 핵심 단어들이 포함된 PPT는 어떤 전공 과목에 해당할 가능성이 높습니까? "
        f"가능한 한 구체적인 과목명을 알려주세요.\n\n"
        f"키워드 목록: {', '.join(keywords)}"
    )

    resp = call_chatgpt([{"role": "user", "content": prompt}])
    print("GPT 원본 응답:", resp)   # 서버 로그 확인용
    return jsonify({"answer": get_first_content(resp), "raw": resp})

