from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go
import re

# 1. MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["Final_Project"]
collection = db["All_Leagues_Data"]

# 2. 데이터 로드
df = pd.DataFrame(list(collection.find()))
df = df[["League", "Market Value"]]

# 3. League 정제
df["League"] = df["League"].astype(str).str.strip().str.lower()
df["League"] = df["League"].apply(lambda x: re.sub(r'[^a-z\s]', '', x))
df["League"] = df["League"].str.title()

# 4. Market Value 변환
def convert_market_value(value):
    if pd.isna(value):
        return None
    try:
        val = str(value).strip().lower().replace("€", "").replace("¢æ", "")
        if val.endswith("k"):
            return int(float(val[:-1]) * 1000)
        elif val.endswith("m"):
            return int(float(val[:-1]) * 1000000)
        return int(float(val))
    except:
        return None

df["Market Value"] = df["Market Value"].apply(convert_market_value)
df.dropna(subset=["League", "Market Value"], inplace=True)

# 5. League 목록별 go.Box() trace 생성
box_traces = []
for league in sorted(df["League"].unique()):
    league_data = df[df["League"] == league]["Market Value"]
    trace = go.Box(
        y=league_data,
        name=league,
        boxpoints='outliers',
        marker=dict(color='royalblue'),
        line=dict(color='royalblue'),
        boxmean='sd'  # 평균 점과 표준편차 표시
    )
    box_traces.append(trace)

# 6. 그래프 생성
fig = go.Figure(data=box_traces)
fig.update_layout(
    title="각 리그별 선수 몸값 분포",
    yaxis_title="Market Value (€)",
    xaxis_title="League",
    xaxis_tickangle=-45,
    showlegend=False
)
fig.show()
