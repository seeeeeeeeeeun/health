def respond_to_question(question):
    q = question.lower()
    if "환급" in q or "보험" in q:
        return "이번 치료는 실손 보험으로 청구 가능하며, 예상 환급액은 약 10만원입니다."
    elif "진료비" in q:
        return "진료비는 평균 15만원 내외입니다."
    else:
        return "질문을 다시 입력해 주세요."
