def evaluate(correct: list[str], answers: list[str]):
    score = 0

    for i in range(len(correct)):
        if (correct[i] == answers[i]):
            score += 20

    level = "" 
    if score >= 80:
        level = "상"
    elif score >= 40:
        level = "중"
    else:
        level = "하"

    return {"level": level, "score": score}