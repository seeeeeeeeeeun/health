
import streamlit as st
import joblib
import pandas as pd

model = joblib.load("rf_model.pkl")
encoder = joblib.load("encoder.pkl")

features = [
    "gender", "age", "hospital_name", "diagnosis_code",
    "treatment_name", "insurance_covered", "welfare_support"
]

st.title("🩺 의료비 예측 도우미")

user_input = {}

user_input["gender"] = st.selectbox("성별", ["F", "M"])
user_input["age"] = st.slider("나이", 20, 90, 50)
user_input["hospital_name"] = st.selectbox("병원명", [
    "서울삼성병원", "서울아산병원", "분당서울대병원", "세브란스병원"
])
user_input["diagnosis_code"] = st.selectbox("진단 코드", [
    "I10", "C34.1", "J01.0", "E11.9"
])
user_input["treatment_name"] = st.selectbox("치료명", [
    "고혈압 진료", "폐암 항암 치료", "부비동염 진료", "당뇨병 정기검사"
])
user_input["insurance_covered"] = st.radio("보험 적용 여부", ["Y", "N"])
user_input["welfare_support"] = st.selectbox("복지 지원 유형", [
    "기초생활수급자", "장애인 의료비 지원", "해당 없음"
])

if st.button("예상 진료비 예측하기"):
    input_df = pd.DataFrame([user_input])
    input_encoded = encoder.transform(input_df)
    prediction = model.predict(input_encoded)[0]

    st.success(f"💰 예상 진료비는 약 {int(prediction):,}원입니다.")

    if user_input["insurance_covered"] == "Y":
        환급가능 = True
        환급률 = 0.7
        환급액 = int(prediction * 환급률)
        자기부담 = int(prediction - 환급액)
    else:
        환급가능 = False
        환급액 = 0
        자기부담 = int(prediction)

    st.markdown(f"**💸 실손 보험 청구 가능 여부**: {'가능' if 환급가능 else '불가능'}")
    st.markdown(f"**💰 예상 환급액**: {환급액:,}원")
    st.markdown(f"**🧾 본인 부담 예상금액**: {자기부담:,}원")
