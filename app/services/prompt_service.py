import logging

log = logging.getLogger(__name__)

def createGuessSubjectPrompt(keywords: list[str]):
    prompt = (
        f"다음 핵심 단어들이 포함된 PPT는 어떤 전공 과목에 해당할 가능성이 높습니까? "
        f"가능한 한 구체적인 과목명을, 설명말고 과목명만 응답하라.\n\n"
        f"키워드 목록: [{', '.join(keywords)}]"
    )
    logPrompt(prompt)
    return prompt

def createGenerateQuestionPrompt(subject: str):
    prompt = (
        f"'{subject}' 과목을 학습한 학생 수준을 평가하기 위한 3지선다 문제 5개를 만들어라.\n"
        f"각 문제는 JSON 배열 형태로 제공하라. 각 항목은"
        f"{{'question': '문제', 'options': [{{'A': '선택지1', 'B': '선택지2', 'C': '선택지3'}}, 'answer': '정답'}} "
        f"형태의 JSON이어야 한다. 오직 JSON만 출력하라. 코드블록(```)은 출력하지 마라."
    )
    logPrompt(prompt)
    return prompt

def createEvaluateLevelPrompt(subject: str, questions, answers: list[str]):
    prompt = (
        f"과목: {subject}\n문제: {questions}\n사용자 답변: {answers}\n\n"
        "각 문항 정답과 비교해 100점 만점 점수를 계산하라. "
        "점수→등급 규칙: 0-59 하, 60-84 중, 85-100 상. "
        "JSON만 출력: {'score': 0-100, 'level': '하|중|상'}. 코드블록(```)은 미출력"
    )
    logPrompt(prompt)
    return prompt

def createExplainKeywordPrompt(level: str, subject: str, keywords: list[str]):
    prompt = (
        f"과목: {subject}\n학습 수준: {level}\n"
        f"슬라이드 핵심 단어: {', '.join(keywords)}\n\n"
        "위 핵심 단어들만을 대상으로, 해당 단어들의 개념을 "
        "수준에 맞춰 3~5줄로 간결히 설명하라. 목록 형태로 출력."
    )
    logPrompt(prompt)
    return prompt

def logPrompt(prompt: str):
    log.info(prompt)