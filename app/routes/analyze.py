from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from ..services.ppt_parser import parse_ppt
from ..services.keywords_extractor import extract_keywords

analyze_bp = Blueprint("analyze", __name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 프론트에서 파일을 받는 <input type="file"> 의 name 속성과 같아야 함
input_name = "file";

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    # 요청 바디에 파일이 없으면 400 Bad Request 응답
    if input_name not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    f = request.files["file"]
    fname = secure_filename(f.filename) or "upload.pptx"
    fpath = UPLOAD_DIR / fname
    f.save(fpath)

    slides_text = parse_ppt(str(fpath))

    keywords = {sid: extract_keywords(text) for sid, text in slides_text.items()}

    return jsonify({"slides": slides_text, "keywords": keywords})
