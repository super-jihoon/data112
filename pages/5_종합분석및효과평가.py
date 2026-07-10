import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="종합 분석 및 효과 평가",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 종합 분석 및 효과 평가")

st.markdown("""
2021년 **Pre-CAS(예측치안 시스템)** 도입 이후
수원시 범죄 데이터를 종합적으로 분석하여
AI 기반 예측치안의 효과와 한계를 평가합니다.
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

comparison = (
    df.groupby("구분")
    [["재산범죄","강력범죄(폭력)","강력범죄(흉악)"]]
    .mean()
)

before = comparison.loc["도입 전"]
after = comparison.loc["도입 후"]

change = ((after-before)/before*100).round(2)

# -----------------------------
# KPI
# -----------------------------

st.header("📊 핵심 결과")

col1, col2, col3 = st.columns(3)

for col, crime in zip(
    [col1, col2, col3],
    ["재산범죄","강력범죄(폭력)","강력범죄(흉악)"]
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
# 변화율 시각화
# -----------------------------

st.header("📈 범죄 유형별 변화율")

change_df = pd.DataFrame({
    "범죄유형": change.index,
    "변화율": change.values
})

fig = px.bar(
    change_df,
    x="범죄유형",
    y="변화율",
    color="변화율",
    text="변화율",
    title="도입 전·후 평균 변화율"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# 범죄별 평가
# -----------------------------

st.header("📋 범죄 유형별 평가")

for crime in change.index:

    value = change[crime]

    if value < 0:

        st.success(f"""
### ✅ {crime}

- 평균 발생 건수 **{abs(value):.2f}% 감소**
- AI 기반 예측치안의 예방 효과가 일부 나타났을 가능성이 있습니다.
""")

    else:

        st.warning(f"""
### ⚠️ {crime}

- 평균 발생 건수 **{value:.2f}% 증가**
- Pre-CAS만으로 감소 효과를 설명하기 어렵습니다.
- 사회적·경제적 요인도 함께 고려해야 합니다.
""")

st.divider()

# -----------------------------
# 종합 평가
# -----------------------------

st.header("📝 종합 평가")

st.info("""
### 연구 결과

- 강력범죄(폭력)는 도입 이후 감소하는 경향을 보였습니다.
- 재산범죄와 강력범죄(흉악)는 증가하는 경향을 보였습니다.
- 따라서 AI 기반 예측치안이 모든 범죄 감소에 직접적인 영향을 미쳤다고 보기는 어렵습니다.
- 다만 일부 범죄에서는 선제적 치안 활동의 효과가 나타났을 가능성이 있습니다.
""")

st.divider()

# -----------------------------
# 정책적 시사점
# -----------------------------

st.header("💡 정책적 시사점")

st.write("""
✅ AI 기반 예측치안은 경찰 순찰 우선지역을 설정하는 데 활용될 수 있습니다.

✅ 범죄 발생 위험지역을 사전에 예측하여 선제적으로 대응할 수 있습니다.

✅ 기존 경찰 순찰과 함께 활용할 때 더욱 효과적인 치안 체계를 구축할 수 있습니다.
""")

st.divider()

# -----------------------------
# 연구의 한계
# -----------------------------

st.header("⚠️ 연구의 한계")

st.warning("""
1. 수원시 자료만 분석하였습니다.

2. AI 도입 이후 기간이 4년으로 비교적 짧습니다.

3. 코로나19, 인구 변화, 사회·경제적 요인 등을 통제하지 못했습니다.

4. AI 예측치안의 효과만을 독립적으로 측정하기 어렵습니다.
""")

st.divider()

# -----------------------------
# 향후 연구
# -----------------------------

st.header("🚀 향후 연구 방향")

st.write("""
- 경기도 다른 시·군과의 비교 분석

- 장기적인 범죄 변화 분석

- 실제 경찰 순찰 데이터와의 비교

- AI 예측 정확도 분석
""")

st.success("➡ 마지막 페이지에서는 전체 연구를 요약하고 최종 결론을 제시합니다.")
