import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="데이터 탐색",
    page_icon="📊",
    layout="wide"
)

st.title("📊 데이터 탐색")

st.markdown("""
수원시 2014~2024년 범죄 데이터를 확인하고,
분석에 사용할 범죄 유형을 탐색합니다.
""")

st.divider()

# -----------------------------
# 데이터 불러오기
# -----------------------------

data = {
    "연도": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "재산범죄": [86352, 90864, 86010, 82816, 89826, 96935, 105666, 91984, 98889, 107671, 125962],
    "강력범죄(폭력)": [34797, 38662, 39830, 38326, 37682, 38872, 35021, 30105, 32222, 30231, 28224],
    "강력범죄(흉악)": [4674, 5005, 5013, 5250, 5249, 5102, 5289, 5739, 6750, 6231, 5860]
}

df = pd.DataFrame(data)

# -----------------------------
# 데이터 개요
# -----------------------------

st.header("📌 데이터 개요")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("분석 지역", "수원시")

with col2:
    st.metric("분석 기간", "2014~2024")

with col3:
    st.metric("범죄 유형", "3종")

st.divider()

# -----------------------------
# 연도 선택
# -----------------------------

st.header("📅 연도 선택")

year_range = st.slider(
    "분석할 연도 범위를 선택하세요.",
    min_value=2014,
    max_value=2024,
    value=(2014, 2024)
)

df = df[
    (df["연도"] >= year_range[0]) &
    (df["연도"] <= year_range[1])
]

# -----------------------------
# 범죄 선택
# -----------------------------

st.header("🚓 범죄 유형 선택")

selected = st.multiselect(
    "비교할 범죄를 선택하세요.",
    ["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"],
    default=["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"]
)

# -----------------------------
# 데이터 보기
# -----------------------------

st.header("📋 원본 데이터")

show_df = df[["연도"] + selected]

st.dataframe(
    show_df,
    use_container_width=True
)

# -----------------------------
# 기초 통계
# -----------------------------

st.header("📈 기초 통계")

st.dataframe(
    show_df.describe().round(2),
    use_container_width=True
)

# -----------------------------
# 데이터 다운로드
# -----------------------------

st.header("💾 데이터 다운로드")

csv = show_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 CSV 다운로드",
    data=csv,
    file_name="suwon_crime_data.csv",
    mime="text/csv"
)

st.divider()

st.info("""
다음 페이지에서는 선택한 데이터를 바탕으로
연도별 범죄 발생 추이를 그래프로 분석합니다.
""")
