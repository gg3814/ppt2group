from flask import Blueprint, jsonify
from services import gpt
import json, os

bp = Blueprint("explain", __name__, url_prefix="/api")

@bp.route("/explain/<aid>")
def explain(aid):
    jpath = f"storage/{aid}.json"
    if not os.path.exists(jpath): return {"error":"not found"},404
    data = json.load(open(jpath, encoding="utf-8"))

    for s in data["slides"]:
        for k in s["keywords"]:
            if not s["explanations"].get(k):
                msg = [{"role":"user","content":f"'{k}' 용어를 비전공자용으로 2~3문장으로 설명해줘."}]
                s["explanations"][k] = gpt.ask_gpt(msg)

    json.dump(data, open(jpath,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return jsonify({"ok":True})
