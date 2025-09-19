import os, requests
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import logging

log = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")  # 환경변수에서 API 키 읽기
BASE_URL = "https://ai.tigrison.com/gateway/api-legacy" # AI Chat API 기본 URL

# API Key 설정 안됨: RuntimeError 던짐
def ask_gpt(messages, model="gpt-4o"):
    """
    AI Chat API (ChatGPT) 호출
    :param messages: [{"role": "user", "content": "..."}] 형식
    :param model: 사용할 모델명 (기본값 gpt-4o)
    :return: API 응답 JSON
    """
    if not API_KEY:
        log.error("Not found API_KEY")
        raise RuntimeError("API_KEY not found. 환경변수에 API_KEY를 설정하세요.")
      
    url = f"{BASE_URL}/ai/chatgpt/completions"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    try:
        resp.raise_for_status()
    except Exception as e:
        log.error("GTP ERROR: %s", e)
        log.error("Response: %s", resp.json())
        raise e

    data = resp.json()
    return data 

def ask_gpt_raw(messages: List[Dict[str, Any]], model: str = "gpt-4o") -> Dict[str, Any]:
    if not API_KEY:
        log.error("Not found API_KEY")
        raise RuntimeError("API_KEY not found. 환경변수에 API_KEY를 설정하세요.")
    
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    body = {"model": model, "messages": messages}
    r = requests.post(BASE_URL, headers=headers, json=body, timeout=30)

    # 400, 500대 응답시 예외 발생
    r.raise_for_status()
    data = r.json()

    # 게이트웨이 에러 포맷이 따로 있을 수도 있으니 가드
    if isinstance(data, dict) and data.get("error"):
        log.error(str(data["error"]))
        raise RuntimeError(str(data["error"]))
    
    log.info(data)
    return data

def get_first_content(resp: Dict[str, Any]) -> str:
    """
    GPT 응답 JSON에서 첫 번째 메시지(content)만 추출
    :param resp_json: call_chatgpt() 반환값
    :return: 문자열 응답
    """
    try:
        # 응답 구조에 따라 content 위치를 정확히 지정
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(e)
        raise RuntimeError("응답 파싱 실패")

# 사용 예
# resp = ask_gpt_raw([{"role":"user","content":"안녕"}])
# text = get_first_content(resp)