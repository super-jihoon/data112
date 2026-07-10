import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="도입 전·후 비교",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Pre-CAS 도입 전·후 비교")

st.markdown("""
2021년 **AI 기반 예측치안(Pre-CAS)** 도입을 기준으로

- **도입 전 : 2014~2020**
- **도입 후 : 2021~2024**

평균 범죄 발생 건수와 변화율을 비교합니다.
""")

st.divider()

# -----------------------------
# 데이터
# -----------------------------

data = {
    "연도":[2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
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

st.header("📊 평균 발생 건수")

st.dataframe(comparison, use_container_width=True)

st.divider()

# -----------------------------
# KPI
# -----------------------------

st.header("📌 변화율")

col1, col2, col3 = st.columns(3)

for col, crime in zip(
    [col1, col2, col3],
    ["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"]
):
    value = change[crime]
    delta_color = "inverse" if value < 0 else "normal"

    col.metric(
        crime,
        f"{value:.2f}%",
        delta=f"{value:.2f}%",
        delta_color=delta_color
    )

st.divider()

# -----------------------------
# 변화율 그래프
# -----------------------------

st.header("📈 변화율 비교")

change_df = pd.DataFrame({
    "범죄유형": change.index,
    "변화율": change.values
})

fig = px.bar(
    change_df,
    x="범죄유형",
    y="변화율",
    text="변화율",
    color="변화율",
    title="Pre-CAS 도입 전·후 평균 변화율"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# 평균 비교 그래프
# -----------------------------

st.header("📊 평균 발생 건수 비교")

compare_df = comparison.T.reset_index()

compare_df.columns = ["범죄유형", "도입 전", "도입 후"]

fig2 = px.bar(
    compare_df,
    x="범죄유형",
    y=["도입 전", "도입 후"],
    barmode="group",
    text_auto=".0f",
    title="도입 전·후 평균 발생 건수"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------
# 결과 요약
# -----------------------------

st.header("📋 결과 요약")

summary = pd.DataFrame({
    "범죄 유형": change.index,
    "도입 전 평균": before.values.round(1),
    "도입 후 평균": after.values.round(1),
    "변화율(%)": change.values
})

st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()

# -----------------------------
# 자동 해석
# -----------------------------

st.header("🤖 분석 결과")

for crime in change.index:

    value = change[crime]

    if value < 0:

        st.success(f"""
### ✅ {crime}

- 평균 발생 건수 **{abs(value):.2f}% 감소**
- 도입 후 감소 경향이 나타남
- 선제적 치안 활동의 긍정적 효과 가능성
""")

    else:

        st.warning(f"""
### ⚠️ {crime}

- 평균 발생 건수 **{value:.2f}% 증가**
- Pre-CAS만으로 감소 효과를 설명하기 어려움
- 사회·경제적 요인도 함께 고려해야 함
""")

st.divider()

# -----------------------------
# 종합 평가
# -----------------------------

st.header("📝 종합 평가")

st.info("""
이번 분석에서는 **Pre-CAS 도입 이후 범죄 유형별 변화가 서로 다르게 나타났습니다.**

- 재산범죄는 증가하는 경향을 보였습니다.
- 강력범죄(폭력)는 감소하는 경향을 보였습니다.
- 강력범죄(흉악)는 증가하는 경향을 보였습니다.

따라서 AI 기반 예측치안이 모든 범죄를 감소시켰다고 단정하기는 어렵습니다.

다만 특정 범죄에서는 예방 효과가 나타났을 가능성이 있으며,
향후 더 장기간의 데이터와 다른 지역 사례를 함께 분석할 필요가 있습니다.
""")

st.success("➡ 다음 페이지에서는 분석 결과를 종합하여 AI 기반 예측치안의 효과와 한계를 평가합니다.")
