from flask import Blueprint, request, send_file, jsonify, render_template_string
from zipfile import ZipFile
from io import BytesIO

download_bp = Blueprint("download", __name__)

TEMPLATE = """<!doctype html><html lang="ko"><meta charset="utf-8">
<style>
body{font-family:sans-serif} .wrap{display:flex;gap:24px}
.left,.right{width:50%} .kw{background:yellow}
pre{white-space:pre-wrap}
</style>
<h1>결과 보고서</h1>
<p>과목: {{subject}} / 등급: {{level}}</p>
{% for sid in order %}
<div class="wrap">
  <div class="left"><h3>{{sid}}</h3><pre>{{slides.get(sid, "")}}</pre></div>
  <div class="right">
    <h3>핵심 단어</h3>
    <p>{{ (keywords.get(sid) or []) | join(", ") }}</p>
    <h3>설명</h3>
    <pre>{{ explanations.get(sid, "설명 없음") }}</pre>
  </div>
</div><hr>
{% endfor %}
"""


@download_bp.route("/download", methods=["POST"])
def download():
    try:
        data = request.json or {}
        required = ["subject","level","slides","keywords","explanations"]
        for k in required:
            if k not in data:
                return jsonify({"error": f"missing field {k}"}), 400

        slides = data.get("slides", {})
        keywords = data.get("keywords", {})
        explanations = data.get("explanations", {})

        import re
        def extract_num(sid: str) -> int:
            m = re.search(r'\d+', sid)
            return int(m.group()) if m else 0

        order = sorted(slides.keys(), key=extract_num)

        html = render_template_string(
            TEMPLATE,
            subject=data["subject"],
            level=data["level"],
            slides=slides,
            keywords=keywords,
            explanations=explanations,
            order=order
        )

        mem = BytesIO()
        with ZipFile(mem, "w") as zf:
            zf.writestr("result.html", html)
        mem.seek(0)
        return send_file(mem, as_attachment=True, download_name="result.zip",
                         mimetype="application/zip")

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500
