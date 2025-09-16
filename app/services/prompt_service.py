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
        f"'{subject}' 과목을 학습한 학생 수준을 평가하기 위한 O/X 문제 5개를 만들어라.\n"
        f"각 문제는 JSON 배열 형태로 제공하라. 각 항목은 {{'question': '문제', 'answer': 'O 또는 X'}} "
        f"형태의 JSON이어야 한다. 오직 JSON만 출력하라. 코드블록(```)은 출력하지 마라."
    )
    logPrompt(prompt)
    return prompt

def createEvaluateLevelPrompt(subject: str, questions: list[dict[str, str]], answers: list[str]):
    prompt = (
        f"'{subject}' 과목에 대한 O/X 문제와 학생 답안이 있다.\n\n"
        f"문제와 정답: {questions}\n"
        f"학생의 답변: {answers}\n\n"
        f"정답과 비교해 점수를 매기고, 학생 수준을 '상, 중, 하' 중 하나로 평가하라. "
        f"미응답은 틀린 것으로 간주하라."
        f"그리고 간단한 이유를 한 문장으로 설명하라.\n"
        f"출력은 JSON 형식으로 {{'level': '상', 'reason': '...'}} 형태만 제공하라. 코드블록(```)은 출력하지 마라."
    )
    logPrompt(prompt)
    return prompt

def createExplainKeywordPrompt(level: str, subject: str, keywords: list[str]):
    prompt = (
        f"학생의 수준은 '{level}'이다. "
        f"아래의 키워드들 중 '{subject}' 과목과 어느정도 관련이 있는 키워드를 사용자가 이해할 수 있도록 수준에 맞게 설명해줘. "
        f"키워드: [{', '.join(keywords)}]"
        f"'상'은 심화된 개념을, '중'은 보통 수준의 설명을, '하'는 기초부터 쉽게 설명해."
        f"각 설명은 50자 이내로 설명해."
    )
    logPrompt(prompt)
    return prompt


def logPrompt(prompt: str):
    log.info(prompt)