from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go
import re

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["Final_Project"]
collection = db["All_Leagues_Data"]

# 2. 데이터 로드 및 필요한 열 추출
df = pd.DataFrame(list(collection.find()))
df = df[["Position", "Age", "Market Value"]]

# 3. 포지션 필터링: 정확히 FW, MF, DF, GK만
valid_positions = ["FW", "MF", "DF", "GK"]
df = df[df["Position"].isin(valid_positions)]

# 4. Age 전처리
df["Age"] = df["Age"].astype(str).str.split("-").str[0]
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# 5. Market Value 전처리
def convert_market_value(val):
    if pd.isna(val):
        return None
    val = str(val).lower().replace("€", "").replace("¢æ", "").strip()
    if val.endswith("k"):
        return float(val[:-1]) * 1_000
    elif val.endswith("m"):
        return float(val[:-1]) * 1_000_000
    try:
        return float(val)
    except:
        return None

df["Market Value"] = df["Market Value"].apply(convert_market_value)
df.dropna(subset=["Age", "Market Value", "Position"], inplace=True)

# 6. 단위 변환: 천만 파운드
df["Market Value (천만 파운드)"] = df["Market Value"] / 10_000_000

# 7. 포지션별 색상 설정
color_map = {
    "FW": "#A2D2FF",   # 연파랑
    "MF": "#B5EAD7",   # 민트
    "DF": "#FFD6A5",   # 살구색
    "GK": "#D0A2F7"    # 연보라
}

# 8. 그래프 생성
fig = go.Figure()

# ▸ Histogram2dContour 
for pos in valid_positions:
    pos_data = df[df["Position"] == pos]
    fig.add_trace(go.Histogram2dContour(
        x=pos_data["Age"],
        y=pos_data["Market Value (천만 파운드)"],
        colorscale=[[0, color_map[pos]], [1, color_map[pos]]],
        contours_coloring="lines",       
        line=dict(width=1.5),
        opacity=0.9,
        name=pos,
        showlegend=False,                
        showscale=False                
    ))

# ▸ 범례용 색상 박스 추가 (Scatter 활용)
for pos in valid_positions:
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=12, color=color_map[pos]),
        name=pos,
        showlegend=True
    ))

# 9. 레이아웃 설정
fig.update_layout(
    title="나이와 시장 가치의 밀도 분포",
    xaxis_title="Age (나이)",
    yaxis_title="Market Value (천만 파운드)",
    font=dict(family="Arial", size=14),
    legend_title="Pos(포지션)",
    legend=dict(x=1.02, y=1, bgcolor="rgba(255,255,255,0.8)"),
    margin=dict(r=160),
    plot_bgcolor='white'
)

fig.show()
