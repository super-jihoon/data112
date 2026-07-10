import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="도입 전·후 비교",
    page_icon="📉",
    layout="wide"
)

st.title("📉 프리카스 도입 전·후 비교")

st.markdown("""
2021년 프리카스(Pre-CAS) 도입을 기준으로
도입 전(2014~2020)과 도입 후(2021~2024)의
평균 범죄 발생 건수와 변화율을 비교합니다.
""")

st.divider()

# -----------------------------
# 데이터
# -----------------------------

data = {
    "연도": [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "재산범죄":[86352,90864,86010,82816,89826,96935,105666,91984,98889,107671,125962],
    "강력범죄(폭력)":[34797,38662,39830,38326,37682,38872,35021,30105,32222,30231,28224],
    "강력범죄(흉악)":[4674,5005,5013,5250,5249,5102,5289,5739,6750,6231,5860]
}

df = pd.DataFrame(data)

df["구분"] = df["연도"].apply(
    lambda x: "도입 전" if x <= 2020 else "도입 후"
)

# -----------------------------
# 평균 계산
# -----------------------------

comparison = (
    df.groupby("구분")
    [["재산범죄","강력범죄(폭력)","강력범죄(흉악)"]]
    .mean()
    .round(2)
)

before = comparison.loc["도입 전"]
after = comparison.loc["도입 후"]

change = ((after-before)/before*100).round(2)

st.subheader("📊 도입 전·후 평균 발생 건수")

st.dataframe(comparison,use_container_width=True)

st.divider()

# -----------------------------
# KPI
# -----------------------------

st.subheader("📌 변화율")

col1,col2,col3 = st.columns(3)

col1.metric(
    "재산범죄",
    f"{change['재산범죄']} %"
)

col2.metric(
    "강력범죄(폭력)",
    f"{change['강력범죄(폭력)']} %"
)

col3.metric(
    "강력범죄(흉악)",
    f"{change['강력범죄(흉악)']} %"
)

st.divider()

# -----------------------------
# 변화율 그래프
# -----------------------------

change_df = pd.DataFrame({
    "범죄유형":change.index,
    "변화율":change.values
})

fig = px.bar(
    change_df,
    x="범죄유형",
    y="변화율",
    color="변화율",
    text="변화율",
    title="프리카스 도입 전후 평균 변화율"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------
# 평균 비교 그래프
# -----------------------------

compare_df = comparison.T.reset_index()

compare_df.columns=["범죄유형","도입 전","도입 후"]

fig2 = px.bar(
    compare_df,
    x="범죄유형",
    y=["도입 전","도입 후"],
    barmode="group",
    title="도입 전·후 평균 발생 건수 비교"
)

st.plotly_chart(fig2,use_container_width=True)

st.divider()

# -----------------------------
# 자동 해석
# -----------------------------

st.subheader("📝 분석 결과")

for crime in change.index:

    if change[crime] < 0:
        st.success(
            f"✅ {crime} : {abs(change[crime])}% 감소"
        )

    elif change[crime] > 0:
        st.warning(
            f"⚠️ {crime} : {change[crime]}% 증가"
        )

    else:
        st.info(
            f"{crime} : 변화 없음"
        )

st.divider()

st.subheader("📖 종합 해석")

st.info("""
본 분석 결과,

프리카스 도입 이후 일부 범죄는 감소하였으나
재산범죄는 증가하는 경향을 보였다.

따라서 프리카스가 모든 범죄를 감소시켰다고 단정하기는 어렵다.

또한 범죄 발생은
코로나19,
사회·경제적 변화,
인구 변화,
경찰 인력 운영 등
다양한 요인의 영향을 받을 수 있으므로
AI 기반 예측치안만으로 결과를 설명하는 데에는 한계가 있다.
""")
