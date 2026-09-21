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
# 그래프 2. (다음 그래프를 위한 자리)
# ============================================================
st.header("📈 그래프 2.")
st.caption("다음 그래프가 여기에 추가될 예정입니다.")

# GRAPH2_INSIGHT = "..."
# st.info(f"💡 이 그래프로 알 수 있는 것: {GRAPH2_INSIGHT}")
