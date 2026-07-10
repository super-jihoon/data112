import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI 예측치안 효과 평가",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI 기반 예측치안 효과 평가")

st.markdown("""
2021년 프리카스(Pre-CAS) 도입 이후
수원시 범죄 데이터를 바탕으로 AI 기반 예측치안의 효과를 종합적으로 평가합니다.
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

st.header("📊 변화율 요약")

result = pd.DataFrame({
    "범죄 유형":change.index,
    "변화율(%)":change.values
})

st.dataframe(result,use_container_width=True)

st.divider()

# -----------------------------
# AI 분석 버튼
# -----------------------------

if st.button("🤖 AI 분석 시작"):

    st.header("📑 AI 분석 결과")

    for crime in change.index:

        value = change[crime]

        if value < 0:

            st.success(
                f"""
### ✅ {crime}

평균 발생 건수가 **{abs(value):.2f}% 감소**했습니다.

프리카스 도입 이후 해당 범죄는 감소하는 경향을 보였습니다.
"""
            )

        elif value > 0:

            st.warning(
                f"""
### ⚠️ {crime}

평균 발생 건수가 **{value:.2f}% 증가**했습니다.

프리카스만으로 감소 효과를 설명하기는 어렵습니다.
"""
            )

        else:

            st.info(f"{crime} : 변화 없음")

    st.divider()

    st.header("💡 종합 평가")

    decrease = sum(change < 0)
    increase = sum(change > 0)

    if decrease > increase:

        st.success("""
### AI 종합 평가

분석한 범죄 가운데 감소한 범죄가 더 많았습니다.

이는 AI 기반 예측치안이
일부 범죄 예방에 긍정적인 영향을 주었을 가능성을 보여줍니다.

다만 범죄 감소의 원인을
프리카스만으로 단정하기는 어렵습니다.
""")

    else:

        st.warning("""
### AI 종합 평가

분석 결과 증가한 범죄도 확인되었습니다.

따라서 프리카스가
모든 범죄를 감소시켰다고 보기 어렵습니다.

범죄 발생에는
사회·경제적 변화,
인구 변화,
경찰력 운영,
코로나19 등의 영향도 함께 고려해야 합니다.
""")

    st.divider()

    st.header("📌 정책적 시사점")

    st.write("""
- AI 기반 예측치안은 경찰 순찰 우선순위를 결정하는 데 도움을 줄 수 있다.

- 특정 범죄 유형에서는 예방 효과를 기대할 수 있다.

- 그러나 모든 범죄를 감소시키는 것은 아니므로
  기존 경찰 활동과 함께 활용하는 것이 바람직하다.
""")

    st.divider()

    st.header("⚠️ 연구의 한계")

    st.write("""
1. 수원시 자료만 활용하였다.

2. 범죄 발생은 다양한 사회적 요인의 영향을 받는다.

3. 프리카스 효과만을 독립적으로 측정하기 어렵다.

4. AI 도입 이후 기간이 비교적 짧다.
""")

    st.divider()

    st.header("🏁 최종 결론")

    st.success("""
본 연구에서는
2021년 프리카스 도입 전후 수원시 주요 범죄를 비교하였다.

분석 결과 범죄 유형별로 서로 다른 변화가 나타났으며,
AI 기반 예측치안은 일부 범죄 예방에는 도움이 될 가능성이 있으나,
모든 범죄 감소 효과를 보인 것은 아니었다.

따라서 AI 기반 예측치안은
기존 경찰 활동을 보완하는 선제적 치안 수단으로 활용하는 것이 적절하다고 판단된다.
""")
