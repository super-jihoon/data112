import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="범죄 추세 분석",
    page_icon="📈",
    layout="wide"
)

st.title("📈 범죄 추세 분석")

st.markdown("""
2014~2024년 수원시 주요 범죄의 연도별 변화를 확인합니다.
2021년 프리카스(Pre-CAS) 도입 시점을 기준으로 범죄 발생 추이를 살펴봅니다.
""")

st.divider()

# -----------------------------
# 데이터
# -----------------------------

data = {
    "연도": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "재산범죄": [86352, 90864, 86010, 82816, 89826, 96935, 105666, 91984, 98889, 107671, 125962],
    "강력범죄(폭력)": [34797, 38662, 39830, 38326, 37682, 38872, 35021, 30105, 32222, 30231, 28224],
    "강력범죄(흉악)": [4674, 5005, 5013, 5250, 5249, 5102, 5289, 5739, 6750, 6231, 5860]
}

df = pd.DataFrame(data)

# -----------------------------
# 사이드바
# -----------------------------

st.sidebar.header("📌 그래프 옵션")

selected = st.sidebar.multiselect(
    "범죄 유형 선택",
    ["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"],
    default=["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"]
)

year = st.sidebar.slider(
    "분석 기간",
    2014,
    2024,
    (2014, 2024)
)

df = df[
    (df["연도"] >= year[0]) &
    (df["연도"] <= year[1])
]

# -----------------------------
# 선그래프
# -----------------------------

st.subheader("📈 연도별 범죄 발생 추이")

fig = px.line(
    df,
    x="연도",
    y=selected,
    markers=True,
    title="수원시 주요 범죄 발생 추이"
)

fig.add_vline(
    x=2021,
    line_dash="dash",
    line_color="red",
    annotation_text="Pre-CAS 도입"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 연도별 증감률
# -----------------------------

st.subheader("📊 전년 대비 증감률 (%)")

change = df.copy()

for crime in ["재산범죄", "강력범죄(폭력)", "강력범죄(흉악)"]:
    change[crime] = change[crime].pct_change() * 100

st.dataframe(change.round(2), use_container_width=True)

# -----------------------------
# 가장 많이 증가/감소한 연도
# -----------------------------

st.subheader("📌 범죄 유형별 특징")

for crime in selected:

    increase = df.loc[df[crime].idxmax()]

    decrease = df.loc[df[crime].idxmin()]

    st.write(f"### {crime}")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"가장 많이 발생한 연도 : {int(increase['연도'])}년 ({int(increase[crime]):,}건)"
        )

    with col2:
        st.info(
            f"가장 적게 발생한 연도 : {int(decrease['연도'])}년 ({int(decrease[crime]):,}건)"
        )

# -----------------------------
# 해석
# -----------------------------

st.divider()

st.subheader("📝 추세 해석")

st.info("""
• 그래프를 통해 프리카스 도입 전후 범죄 발생 추이를 시각적으로 비교할 수 있습니다.

• 2021년을 기준으로 일부 범죄는 감소하고, 일부 범죄는 증가하는 양상이 나타납니다.

• 이러한 변화는 프리카스뿐 아니라 코로나19, 사회·경제적 변화, 경찰력 운영 등 다양한 요인의 영향을 받을 수 있습니다.

• 따라서 다음 페이지에서는 도입 전후 평균과 변화율을 비교하여 프리카스 도입 효과를 보다 구체적으로 분석합니다.
""")
