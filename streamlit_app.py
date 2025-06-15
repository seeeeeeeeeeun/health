
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder

st.title("🩺 의료비 예측 도우미 (GitHub CSV 연결형)")

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

encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_encoded, y)

user_input = {}
for col in features:
    if df[col].dtype == "object":
        user_input[col] = st.selectbox(col, df[col].unique())
    elif df[col].dtype in ["int64", "float64"]:
        user_input[col] = st.slider(col, int(df[col].min()), int(df[col].max()), int(df[col].mean()))

if st.button("예상 진료비 예측하기"):
    input_df = pd.DataFrame([user_input])
    input_encoded = encoder.transform(input_df)
    prediction = model.predict(input_encoded)[0]
    st.success(f"💰 예상 진료비는 약 {int(prediction):,}원입니다.")

    if user_input["insurance_covered"] == "Y":
        환급액 = int(prediction * 0.7)
        본인부담 = int(prediction - 환급액)
        st.markdown(f"💸 환급 예상 금액: **{환급액:,}원**")
        st.markdown(f"🧾 본인 부담 금액: **{본인부담:,}원**")
    else:
        st.markdown("❌ 보험 미적용. 전액 본인 부담입니다.")
