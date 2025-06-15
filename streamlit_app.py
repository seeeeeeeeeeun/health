
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
    "서울삼성병원", "서울아산병원", "분당서울대병원", "세브란스병원", "서울의료원",
    "강남성심병원", "서울백병원", "한양대병원", "고대안암병원", "보라매병원",
    "부산대병원", "전남대병원", "제주대병원", "인하대병원", "강북삼성병원",
    "동국대일산병원", "화순전남대병원", "중앙보훈병원", "영남대병원", "국립암센터",
    "인제대일산백병원", "서울성모병원"
])
user_input["diagnosis_code"] = st.selectbox("진단 코드", [
    "K35.2", "I10", "C34.1", "J01.0", "E11.9", "N92.5", "K80.2", "I25.1", "F32.0", "N18.3",
    "S06.0", "D64.9", "K40.9", "M54.5", "R10.9", "G43.9", "C61", "J45.0", "I21.9", "O80",
    "L03.0", "C50.9", "R51", "H25.1"
])
user_input["treatment_name"] = st.selectbox("치료명", [
    "관절경 수술", "고혈압 진료", "폐암 항암 치료", "부비동염 진료", "당뇨병 정기검사",
    "월경과다 진료", "담낭절제술", "허혈성 심질환 검사", "우울증 치료", "만성 신부전 투석",
    "두부 외상 치료", "빈혈 치료", "탈장 수술", "요통 물리치료", "복통 진단 및 검사",
    "편두통 치료", "전립선암 방사선치료", "천식 약물치료", "심근경색 응급치료", "자연분만",
    "피부염 치료", "유방암 수술", "두통 진료", "백내장 수술"
])
user_input["insurance_covered"] = st.radio("보험 적용 여부", ["Y", "N"])
user_input["welfare_support"] = st.selectbox("복지 지원 유형", [
    "기초생활수급자", "의료급여 수급자", "장애인 의료비 지원", "출산 의료비 지원",
    "산재 보장 대상자", "응급지원 대상자", "해당 없음"
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
