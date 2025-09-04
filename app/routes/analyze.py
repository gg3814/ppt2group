from flask import Blueprint, request, jsonify
from services import ppt_parser, keywords
import os, uuid, json

bp = Blueprint("analyze", __name__, url_prefix="/api")

@bp.route("/analyze", methods=["POST"])
def analyze():
    f = request.files["file"]
    aid = uuid.uuid4().hex[:12]
    path = f"storage/{aid}.pptx"
    f.save(path)

    slides = ppt_parser.extract_text(path)
    for s in slides:
        s["keywords"] = keywords.get_keywords(s["text"])
        s["explanations"] = {}

    result = {"analysisId": aid, "slides": slides, "subject":None, "level":None, "feedback":None}
    os.makedirs("storage", exist_ok=True)
    with open(f"storage/{aid}.json","w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    return jsonify(result)
