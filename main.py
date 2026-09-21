# 영화 데이터 그래프 도감 1 - 시간
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", page_icon="🎬", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data(ttl=3600)
def load_data():
    """1년치 일별 박스오피스 10위권 데이터를 불러와 날짜 열을 진짜 날짜로 바꾼다."""
    df = pd.read_csv(DATA_URL, dtype={"날짜": str})
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("KOBIS 일별 박스오피스 데이터로 그리는 그래프 모음")

df = load_data()

# ============================================================
# 그래프 1. 영화별 날짜별 일관객 변화
# ============================================================
st.header("📈 그래프 1. 영화별 일별 관객수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="graph1_movie")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객수"},
    title=f"{selected_movie} — 날짜별 일일 관객수",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)
st.plotly_chart(fig1, width="stretch")

# '이 그래프로 알 수 있는 것' — 그래프마다 한 문장 문구를 넣는 자리
GRAPH1_INSIGHT = "여기에 이 그래프로 알 수 있는 것을 한 문장으로 적어주세요."
st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH1_INSIGHT}")

# ============================================================
# 그래프 2. 일관객 합계 상위 5편 비교
# ============================================================
st.header("📈 그래프 2. 일관객 합계 상위 5편의 날짜별 관객수")

top5_names = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_names)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객수", "영화명": "영화명"},
    title="기간 내 일관객 합계 상위 5편 — 날짜별 일일 관객수",
)
fig2.update_traces(
    hovertemplate="영화명: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)
# 범례를 눌러 영화를 켜고 끌 수 있게 (plotly 기본 동작, 명시적으로 켜둔다)
fig2.update_layout(legend=dict(itemclick="toggle", itemdoubleclick="toggleothers"))
st.plotly_chart(fig2, width="stretch")

GRAPH2_INSIGHT = "여기에 이 그래프로 알 수 있는 것을 한 문장으로 적어주세요."
st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH2_INSIGHT}")

# ============================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ============================================================
st.header("📈 그래프 3. 날짜별 10위권 일관객 합계")

daily_total = df.groupby("날짜", as_index=False)["일관객"].sum()
daily_total = daily_total.sort_values("날짜")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={"날짜": "날짜", "일관객": "10위권 일관객 합계"},
    title="날짜별 10위권 전체 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>"
)

# 합계가 가장 컸던 날 3일을 찾아 그래프 위에 표시한다
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(size=10, color="crimson"),
    name="합계 상위 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>",
)
st.plotly_chart(fig3, width="stretch")

GRAPH3_INSIGHT = "여기에 이 그래프로 알 수 있는 것을 한 문장으로 적어주세요."
st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH3_INSIGHT}")

# ============================================================
# 그래프 4. 일관객 합계 TOP 10 영화
# ============================================================
st.header("📈 그래프 4. 일관객 합계 TOP 10 영화")

movie_stats = (
    df.groupby("영화명")
    .agg(합계일관객=("일관객", "sum"), 순위권일수=("영화명", "count"))
    .reset_index()
)
top10_stats = movie_stats.sort_values("합계일관객", ascending=True).tail(10)

fig4 = px.bar(
    top10_stats,
    x="합계일관객",
    y="영화명",
    orientation="h",
    labels={"합계일관객": "기간 내 일관객 합계", "영화명": "영화명"},
    title="기간 내 일관객 합계 TOP 10",
    custom_data=["순위권일수"],
)
fig4.update_traces(
    hovertemplate=(
        "영화명: %{y}<br>일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일<extra></extra>"
    )
)
st.plotly_chart(fig4, width="stretch")

GRAPH4_INSIGHT = "여기에 이 그래프로 알 수 있는 것을 한 문장으로 적어주세요."
st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH4_INSIGHT}")

# ============================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# ============================================================
st.header("📈 그래프 5. 월 × 요일별 일관객 합계")

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
df["월"] = df["날짜"].dt.month
df["요일"] = df["날짜"].dt.dayofweek.map(lambda i: weekday_names[i])

heatmap_data = (
    df.groupby(["요일", "월"])["일관객"].sum().reset_index()
)
pivot = heatmap_data.pivot(index="요일", columns="월", values="일관객")
pivot = pivot.reindex(weekday_names)  # 월요일부터 일요일 순서로
pivot = pivot.reindex(columns=sorted(pivot.columns))  # 월은 1월~12월 순서로

fig5 = px.imshow(
    pivot,
    labels=dict(x="월", y="요일", color="일관객 합계"),
    x=[f"{m}월" for m in pivot.columns],
    y=pivot.index,
    color_continuous_scale="Reds",  # 색이 진할수록 관객이 많음
    aspect="auto",
    title="월 × 요일별 일관객 합계",
)
fig5.update_traces(
    hovertemplate="월: %{x}<br>요일: %{y}<br>합계: %{z:,}명<extra></extra>"
)
st.plotly_chart(fig5, width="stretch")

GRAPH5_INSIGHT = "여기에 이 그래프로 알 수 있는 것을 한 문장으로 적어주세요."
st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH5_INSIGHT}")

# ============================================================
# 그래프 6. (다음 그래프를 위한 자리)
# ============================================================
st.header("📈 그래프 6.")
st.caption("다음 그래프가 여기에 추가될 예정입니다.")

# GRAPH6_INSIGHT = "..."
# st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH6_INSIGHT}")
