from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from ..services.ppt_parser import parse_ppt
from ..services.keywords import extract_keywords
from ..services.gpt import call_chatgpt, first_text

analyze_bp = Blueprint("analyze", __name__)
UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    fname = secure_filename(f.filename) or "upload.pptx"
    fpath = UPLOAD_DIR / fname
    f.save(fpath)

    # 1) 슬라이드 파싱
    slides = parse_ppt(str(fpath))  # {"slide_1": "text...", ...}

    # 2) 슬라이드별 키워드
    keywords = {sid: extract_keywords(txt) for sid, txt in slides.items()}

    # 3) 과목 유추
    flat = []
    for sid in keywords:
        flat += keywords[sid]
    prompt = (
        "다음 핵심 단어들이 포함된 PPT는 어떤 전공 과목일 가능성이 높습니까? "
        "가능한 한 구체적인 과목명을 1개만 출력하세요.\n\n"
        f"단어들: {', '.join(flat[:200])}"
    )
    subj_resp = call_chatgpt([{"role": "user", "content": prompt}])
    subject = first_text(subj_resp).strip()

    return jsonify({
        "slides": slides,
        "keywords": keywords,
        "subject": subject
    })
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from ..services.ppt_parser import parse_ppt
from ..services.keywords import extract_keywords
from ..services.gpt import call_chatgpt, first_text

analyze_bp = Blueprint("analyze", __name__)
UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    fname = secure_filename(f.filename) or "upload.pptx"
    fpath = UPLOAD_DIR / fname
    f.save(fpath)

    # 1) 슬라이드 파싱
    slides = parse_ppt(str(fpath))  # {"slide_1": "text...", ...}

    # 2) 슬라이드별 키워드
    keywords = {sid: extract_keywords(txt) for sid, txt in slides.items()}

    # 3) 과목 유추
    flat = []
    for sid in keywords:
        flat += keywords[sid]
    prompt = (
        "다음 핵심 단어들이 포함된 PPT는 어떤 전공 과목일 가능성이 높습니까? "
        "가능한 한 구체적인 과목명을 1개만 출력하세요.\n\n"
        f"단어들: {', '.join(flat[:200])}"
    )
    subj_resp = call_chatgpt([{"role": "user", "content": prompt}])
    subject = first_text(subj_resp).strip()

    return jsonify({
        "slides": slides,
        "keywords": keywords,
        "subject": subject
    })
