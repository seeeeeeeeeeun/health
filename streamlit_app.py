
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 기반 의료비 예측 도우미", layout="wide")

# 사이드바: 앱 설명 + 챗봇
with st.sidebar:
    st.title("📌 사용 안내")
    st.markdown("""
    이 앱은 AI를 활용하여 예상 진료비를 예측하고,  
    보험 적용 여부에 따라 환급 금액과 본인 부담금을 계산합니다.

    사용 방법:
    1. 아래에서 정보를 입력하세요.
    2. '예상 진료비 예측하기' 버튼을 누르세요.
    3. 결과와 함께 시각화를 확인하세요.

    👉 하단에 챗봇 질문 입력도 가능해요!
    """)

    st.subheader("💬 챗봇 질문 시뮬레이션")
    question = st.text_input("궁금한 점을 입력해보세요")

    if question:
        if "환급" in question:
            st.info("실손보험이 적용되면 최대 70%까지 환급 가능합니다.")
        elif "병원비" in question or "진료비" in question:
            st.info("입력된 정보를 바탕으로 병원비를 예측합니다. 보험과 복지 지원에 따라 달라집니다.")
        elif "공제" in question or "연말정산" in question:
            st.info("연말정산 공제 예측 기능은 추후 업데이트될 예정입니다.")
        else:
            st.info("죄송해요! 아직 이 질문은 준비 중이에요.")

# 제목
st.title("💡 AI 기반 의료비 예측 도우미")

# 데이터 불러오기
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/seeeeeeeeeeun/health/main/%E1%84%8B%E1%85%B4%E1%84%85%E1%85%AD%E1%84%87%E1%85%B5%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%E1%84%89%E1%85%A6%E1%86%BA.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

features = ["gender", "age", "hospital_name", "diagnosis_code",
            "treatment_name", "insurance_covered", "welfare_support"]
target = "treatment_cost"

X = df[features]
y = df[target]

# 모델 학습
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_encoded, y)

# 사용자 입력
st.header("📥 사용자 정보 입력")
user_input = {}
cols = st.columns(2)
for i, col in enumerate(features):
    with cols[i % 2]:
        if df[col].dtype == "object":
            user_input[col] = st.selectbox(col, df[col].unique(), key=col)
        elif df[col].dtype in ["int64", "float64"]:
            user_input[col] = st.slider(col, int(df[col].min()), int(df[col].max()), int(df[col].mean()), key=col)

# 예측 결과
st.markdown("---")
if st.button("📊 예상 진료비 예측하기"):
    input_df = pd.DataFrame([user_input])
    input_encoded = encoder.transform(input_df)
    prediction = model.predict(input_encoded)[0]

    st.success(f"💰 예상 진료비는 약 {int(prediction):,}원입니다.")

    환급액 = 본인부담 = 0
    if user_input["insurance_covered"] == "Y":
        환급액 = int(prediction * 0.7)
        본인부담 = int(prediction - 환급액)
        st.markdown(f"💸 환급 예상 금액: **{환급액:,}원**")
        st.markdown(f"🧾 본인 부담 금액: **{본인부담:,}원**")
    else:
        본인부담 = int(prediction)
        st.markdown("❌ 보험 미적용. 전액 본인 부담입니다.")

    # 그래프 시각화
    st.markdown("### 📈 예측 결과 시각화")
    fig, ax = plt.subplots()
    bars = ax.bar(["예상 진료비", "환급액", "본인 부담금"],
                  [prediction, 환급액, 본인부담],
                  color=["#4CAF50", "#2196F3", "#FFC107"])
    ax.set_ylabel("금액 (원)")
    ax.set_ylim(0, max(prediction, 환급액 + 본인부담) * 1.2)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 10000, f"{int(yval):,}", ha='center', va='bottom')
    st.pyplot(fig)
