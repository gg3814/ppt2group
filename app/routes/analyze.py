from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from ..services.ppt_parser import parse_ppt
from ..services.keywords import extract_keywords

analyze_bp = Blueprint("analyze", __name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files["file"]
    fname = secure_filename(f.filename) or "upload.pptx"
    fpath = UPLOAD_DIR / fname
    f.save(fpath)

    slides_text = parse_ppt(str(fpath))
    keywords_result = {sid: extract_keywords(text) for sid, text in slides_text.items()}
    return jsonify({"slides": slides_text, "keywords": keywords_result})
