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
수원시(2014~2024) 주요 범죄의 연도별 발생 추이를 시각화하여
**2021년 AI 기반 예측치안(Pre-CAS) 도입 전후 변화**를 분석합니다.
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

# -----------------------------
# 옵션
# -----------------------------

st.header("🎛 분석 옵션")

crime = st.selectbox(
    "분석할 범죄를 선택하세요.",
    ["재산범죄","강력범죄(폭력)","강력범죄(흉악)"]
)

st.divider()

# -----------------------------
# KPI
# -----------------------------

st.header("📊 데이터 요약")

col1,col2,col3=st.columns(3)

col1.metric(
    "최대 발생",
    f"{df[crime].max():,}건"
)

col2.metric(
    "최소 발생",
    f"{df[crime].min():,}건"
)

col3.metric(
    "평균 발생",
    f"{int(df[crime].mean()):,}건"
)

st.divider()

# -----------------------------
# 선그래프
# -----------------------------

st.header("📈 연도별 발생 추이")

fig = px.line(
    df,
    x="연도",
    y=crime,
    markers=True,
    text=crime,
    title=f"{crime} 발생 추이"
)

fig.update_traces(
    textposition="top center",
    line=dict(width=4)
)

fig.add_vline(
    x=2021,
    line_dash="dash",
    line_color="red",
    annotation_text="Pre-CAS 도입",
    annotation_position="top"
)

fig.update_layout(
    hovermode="x unified"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# -----------------------------
# 증감률
# -----------------------------

st.header("📉 전년 대비 증감률")

growth=df.copy()

growth["증감률"]=growth[crime].pct_change()*100

fig2=px.bar(
    growth,
    x="연도",
    y="증감률",
    text="증감률",
    title="전년 대비 증감률(%)"
)

fig2.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

st.plotly_chart(fig2,use_container_width=True)

st.divider()

# -----------------------------
# 누적 변화율
# -----------------------------

st.header("📊 2014년 대비 변화율")

base=df.loc[df["연도"]==2014,crime].values[0]

temp=df.copy()

temp["변화율"]=(temp[crime]-base)/base*100

fig3=px.area(
    temp,
    x="연도",
    y="변화율",
    title="2014년 대비 누적 변화율"
)

st.plotly_chart(fig3,use_container_width=True)

st.divider()

# -----------------------------
# 데이터 표
# -----------------------------

st.header("📋 연도별 데이터")

show=df[["연도",crime]]

st.dataframe(
    show,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# 자동 분석
# -----------------------------

st.header("🤖 자동 분석")

increase=df.iloc[-1][crime]-df.iloc[0][crime]

rate=increase/df.iloc[0][crime]*100

if rate>0:

    st.warning(f"""
### 분석 결과

- 2014년 대비 **{rate:.2f}% 증가**하였습니다.
- 증가 추세가 지속되는 경향을 보입니다.
- 2021년 Pre-CAS 도입 이후에도 증가 여부를 추가적으로 살펴볼 필요가 있습니다.
""")

else:

    st.success(f"""
### 분석 결과

- 2014년 대비 **{abs(rate):.2f}% 감소**하였습니다.
- 장기적으로 감소 추세를 보입니다.
- Pre-CAS 도입 이후 예방 효과가 나타났을 가능성을 확인할 수 있습니다.
""")

st.divider()

st.info("""
📌 다음 페이지에서는 **Pre-CAS 도입 전(2014~2020)** 과 **도입 후(2021~2024)**의 평균 발생 건수와 변화율을 직접 비교합니다.
""")
