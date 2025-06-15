import streamlit as st
from predict import predict_medical_cost
from chatbot import respond_to_question

st.set_page_config(page_title="슬기로운 의료생활", page_icon="🏥")

col1, col2, col3 = st.columns([1, 2, 1])  # 좌우 여백 확보

with col2:
    st.title("슬기로운 의료생활")
    st.subheader("정보를 입력해주세요")

    gender = st.selectbox("성별", ["F", "M"], help="성별을 선택하세요")
    age = st.slider("나이", 0, 100, 30, help="예: 62")
    hospital = st.text_input("병원명", value="서울삼성병원", help="예: 서울삼성병원")
    diagnosis = st.text_input("진단코드", value="K35.2", help="예: K35.2")
    treatment = st.text_input("치료명", value="관절경 수술", help="예: 관절경 수술")

    if st.button("예측하기"):
        cost, covered, deductible = predict_medical_cost(gender, age, hospital, diagnosis, treatment)
        st.success(f"예상 진료비: {cost:,}원")
        st.info(f"보험 적용 여부: {covered}, 본인부담금: {deductible:,}원")

    st.markdown("---")
    st.subheader("궁금한 점을 입력해보세요")
    st.markdown("""_예시: 보험 환급 되나요? / 이 진료는 청구 가능해요?_""")

    user_question = st.text_input("질문을 입력하세요")
    if user_question:
        response = respond_to_question(user_question)
        st.markdown(f"💬 **{response}**")

    st.markdown("---")
    st.caption("© 2025 슬기로운 의료생활")
